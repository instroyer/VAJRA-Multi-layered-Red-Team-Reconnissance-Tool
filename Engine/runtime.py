# VAJRA/Engine/runtime.py
# Description: Handles the dynamic execution of modules and the runtime control thread.

import importlib
import threading
import time
from .logger import info, error, success, warning

class RuntimeControl:
    """
    Manages a background thread to listen for runtime commands (e.g., '00').
    """
    def __init__(self):
        self.stop_thread = threading.Event()
        self.listener_paused = threading.Event()
        self.listener_paused.set()
        self.thread = None

    def start(self):
        self.thread = threading.Thread(target=self.listener, daemon=True)
        self.thread.start()

    def stop(self):
        self.stop_thread.set()
        if self.thread:
            self.thread.join(timeout=1)
        info("Runtime control deactivated.")

    def pause_listener(self):
        self.listener_paused.clear()
        info("Runtime listener paused for user input.")
        time.sleep(0.1)

    def resume_listener(self):
        self.listener_paused.set()
        info("Runtime listener resumed.")

    def listener(self):
        try:
            from .utils import get_char 
        except ImportError:
            return
        buffer = ""
        while not self.stop_thread.is_set():
            self.listener_paused.wait()
            char = get_char(timeout=0.1)
            if char:
                buffer += char
                if "00" in buffer:
                    print("\n[!] Runtime Menu Activated (Feature Placeholder)")
                    buffer = "" 
            if len(buffer) > 2:
                buffer = buffer[-2:]

def execute_modules(module_choices, target, target_dir, report_enabled):
    """
    Orchestrates the execution of selected modules.
    """
    module_map = {
        '1': {'file': 'whois', 'handler': 'run'},
        '2': {'file': 'subfinder', 'handler': 'run'},
        '3': {'file': 'amass', 'handler': 'run'},
        '4': {'file': 'httpx', 'handler': 'run'},
        '5': {'file': 'nmap', 'handler': 'run'},
        '6': {'file': 'screenshot', 'handler': 'run'}
    }

    if '0' in module_choices:
        choices = sorted(module_map.keys())
    else:
        choices = module_choices.split()

    runtime_controller = RuntimeControl()
    runtime_controller.start()

    info(f"Starting {len(choices)} module(s)...")

    for choice in choices:
        module_info = module_map.get(choice)
        if not module_info:
            warning(f"Unknown module choice '{choice}'. Skipping.")
            continue

        try:
            module_name = f"Modules.{module_info['file']}"
            module = importlib.import_module(module_name)
            handler_name = module_info['handler']
            handler = getattr(module, handler_name)

            if isinstance(handler, type):
                # This handles class-based modules like the refactored Nmap scanner
                if choice == '5':
                    instance = handler(target, target_dir, runtime_control=runtime_controller)
                else:
                    instance = handler(target, target_dir)
                instance.run()
            else:
                # This handles simple function-based modules
                handler(target, target_dir)

        except ImportError as e:
            error(f"Could not import module: {module_info['file']}. Details: {e}")
        except AttributeError:
            error(f"Module {module_info['file']} is missing the required '{handler_name}' handler.")
        except Exception as e:
            error(f"An error occurred while running module {module_info['file']}: {e}")

    runtime_controller.stop()
    success("--- Module execution completed ---")

    if report_enabled and '5' not in choices:
        from .report import generate_report
        info("Generating final HTML report...")
        if generate_report(target, target_dir, module_choices):
            success("HTML report generation successful.")
        else:
            error("Failed to generate final HTML report.")
