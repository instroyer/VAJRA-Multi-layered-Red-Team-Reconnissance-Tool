#VAJRA/Engine/runtime.py

import importlib
import multiprocessing
import threading
import time
import select
import sys
import os
import signal
from .logger import info, error, success, warning
#
#
class RuntimeControl:
    """Background listener that watches stdin for the '00' trigger and exposes
    flags plus helper functions to pause/resume/skip/quit the currently running
    module process (by PID)."""
    def __init__(self):
        self.stop_thread = threading.Event()
        self.listener_paused = threading.Event()
        self.listener_paused.set() # start active
        self.thread = None
        self.runtime_menu_active = False
        # runtime state
        self.module_paused = False
        self.skip_current = False
        self.quit_program = False
        self.current_module = None
        # process control
        self.current_pid = None
        # last trigger time to debounce
        self.last_trigger_time = 0.0
    def start(self):
        self.thread = threading.Thread(target=self._listener, daemon=True)
        self.thread.start()
        info("Runtime control activated. Type '00' then ENTER during execution for control menu.")
    def stop(self):
        self.stop_thread.set()
        if self.thread:
            self.thread.join(timeout=1)
        info("Runtime control deactivated.")
    def pause_listener(self):
        """Pause the listener (avoid catching keys while user types other prompts)."""
        self.listener_paused.clear()
    def resume_listener(self):
        self.listener_paused.set()
    def set_current_module(self, module_name):
        self.current_module = module_name
    def set_current_pid(self, pid):
        """Set the PID of the currently running module process (or None)."""
        self.current_pid = pid
    #----- high level commands
    def pause_module(self):
        if self.current_module:
            self.module_paused = True
            info(f"Module '{self.current_module}' PAUSED (will suspend process).")
            if self.current_pid:
                try:
                    os.kill(self.current_pid, signal.SIGSTOP)
                except Exception as e:
                    warning(f"Could not SIGSTOP pid {self.current_pid}: {e}")

    def resume_module(self):
        if self.current_module and self.module_paused:
            self.module_paused = False
            info(f"Module '{self.current_module}' RESUMED (will continue process).")
            if self.current_pid:
                try:
                    os.kill(self.current_pid, signal.SIGCONT)
                    # This new line gives you the feedback you wanted
                    info(f"Process (PID: {self.current_pid}) is running. Type '00' for menu.")
                except Exception as e:
                    warning(f"Could not SIGCONT pid {self.current_pid}: {e}")

    def skip_module(self):
        if self.current_module:
            self.skip_current = True
            info(f"Skip requested for module '{self.current_module}'.")
            if self.current_pid:
                try:
                    os.kill(self.current_pid, signal.SIGTERM)
                except Exception as e:
                    warning(f"Could not SIGTERM pid {self.current_pid}: {e}")
    def quit_execution(self):
        self.quit_program = True
        info("Quit requested. Terminating VAJRA run.")
        if self.current_pid:
            try:
                os.kill(self.current_pid, signal.SIGTERM)
            except Exception as e:
                warning(f"Could not SIGTERM pid {self.current_pid}: {e}")
    #----- helpers
    def _get_char(self, timeout=0.1):
        """Non-blocking single char read (works when user presses ENTER)."""
        try:
            if select.select([sys.stdin], [], [], timeout)[0]:
                return sys.stdin.read(1)
        except Exception:
            pass
        return None
    def _clear_input_buffer(self):
        """Clear pending stdin (helpful after menu input)."""
        try:
            while select.select([sys.stdin], [], [], 0.0)[0]:
                sys.stdin.readline()
        except Exception:
            pass
    def _display_runtime_menu(self):
        current_module_display = f" ({self.current_module})" if self.current_module else ""
        menu_text = f"""
{'='*40}
[*] RUNTIME CONTROL MENU{current_module_display}
{'='*40}
[p] Pause current module
[r] Resume paused module
[s] Skip current module
[q] Quit VAJRA entirely
Any other key → Exit Runtime Menu
{'='*40}
Enter choice: """
        print(menu_text, end="", flush=True)
    def _process_runtime_command(self, command):
        command = command.lower().strip()
        if command == 'p':
            self.pause_module()
        elif command == 'r':
            self.resume_module()
        elif command == 's':
            self.skip_module()
        elif command == 'q':
            self.quit_execution()
        else:
            info("Exiting runtime control menu.")
        self.runtime_menu_active = False
        self._clear_input_buffer()
    def _listener(self):
        """Thread: detect '00' + ENTER trigger and run menu."""
        buffer = ""
        while not self.stop_thread.is_set():
            if not self.listener_paused.is_set():
                time.sleep(0.1)
                continue
            if self.runtime_menu_active:
                time.sleep(0.1)
                continue
            ch = self._get_char(timeout=0.05)
            if ch:
                buffer += ch
                if len(buffer) > 8:
                    buffer = buffer[-8:]
                if buffer.endswith("00\n") or buffer.endswith("00\r\n"):
                    now = time.time()
                    if now - self.last_trigger_time > 1.0:
                        self.last_trigger_time = now
                        self._clear_input_buffer()
                        self.runtime_menu_active = True
                        buffer = ""
                        self._display_runtime_menu()
                        try:
                            self.pause_listener()
                            command = input().strip()
                            self._process_runtime_command(command)
                        except (KeyboardInterrupt, EOFError):
                            self.runtime_menu_active = False
                            info("Runtime menu cancelled.")
                        finally:
                            self.resume_listener()
                elif ch == '\n':
                    buffer = ""
            time.sleep(0.05)

    def wait_if_paused(self):
        while self.module_paused and not self.quit_program and not self.skip_current:
            time.sleep(0.3)
            if self.quit_program or self.skip_current:
                break

    def should_skip_current(self):
        return self.skip_current
    def should_quit(self):
        return self.quit_program
    def reset_module_state(self):
        self.module_paused = False
        self.skip_current = False
        self.current_pid = None
        self.current_module = None
#
#
def execute_modules(module_choices, target, target_dir, report_enabled):
    module_map = {
        '1': {'file': 'whois', 'handler': 'run', 'name': 'Whois'},
        '2': {'file': 'subfinder', 'handler': 'run', 'name': 'Subfinder'},
        '3': {'file': 'amass', 'handler': 'run', 'name': 'Amass'},
        '4': {'file': 'httpx', 'handler': 'run', 'name': 'HTTPX'},
        '5': {'file': 'nmap', 'handler': 'run', 'name': 'Nmap'},
        '6': {'file': 'screenshot', 'handler': 'run', 'name': 'Screenshot'}
    }
    if '0' in module_choices:
        choices = sorted(module_map.keys())
    else:
        choices = module_choices.split()
    runtime_controller = RuntimeControl()
    runtime_controller.start()
    info(f"Starting {len(choices)} module(s)...")
    def _module_runner(choice, target, target_dir, is_auto_mode=False):
        try:
            # Re-open stdin in the child process if it's interactive Nmap
            if choice == '5' and not is_auto_mode:
                sys.stdin = open(0)
            
            module_info = module_map.get(choice)
            if not module_info:
                print(f"[!] Unknown module '{choice}'")
                return
            module_name = module_info['name']
            module_package_name = f"Modules.{module_info['file']}"
            module = importlib.import_module(module_package_name)
            handler_name = module_info['handler']
            handler = getattr(module, handler_name)
            if isinstance(handler, type):
                if choice == '5' and is_auto_mode:
                    instance = handler(target, target_dir, runtime_control=None, is_auto_mode=True)
                else:
                    instance = handler(target, target_dir, runtime_control=None)
                instance.run()
            else:
                if choice == '5' and is_auto_mode:
                    handler(target, target_dir, is_auto_mode=True)
                else:
                    handler(target, target_dir)
        except Exception as e:
            print(f"[module runner] error: {e}")
    for choice in choices:
        runtime_controller.reset_module_state()
        if runtime_controller.should_quit():
            info("Quitting as requested...")
            break
        module_info = module_map.get(choice)
        if not module_info:
            warning(f"Unknown module choice '{choice}'. Skipping.")
            continue
        module_name = module_info['name']
        runtime_controller.set_current_module(module_name)
        if runtime_controller.should_skip_current():
            warning(f"Module '{module_name}' SKIPPED.")
            runtime_controller.reset_module_state()
            continue
        try:
            # First, check if this is an interactive Nmap run
            is_auto = ('0' in module_choices) and choice == '5'
            
            runtime_controller.pause_listener()
            
            # Only resume the listener if the module is NOT interactive
            if module_name != 'Nmap' or is_auto:
                runtime_controller.resume_listener()

            info(f"--- Executing module: {module_name} ---")
            proc = multiprocessing.Process(target=_module_runner, args=(choice,
                target, target_dir, is_auto))
            proc.start()
            runtime_controller.set_current_pid(proc.pid)
            while proc.is_alive():
                if runtime_controller.module_paused:
                    pass
                if runtime_controller.should_skip_current():
                    try:
                        os.kill(proc.pid, signal.SIGTERM)
                    except Exception:
                        pass
                    break
                if runtime_controller.should_quit():
                    try:
                        os.kill(proc.pid, signal.SIGTERM)
                    except Exception:
                        pass
                    break
                time.sleep(0.2)
            if proc.is_alive():
                try:
                    proc.join(timeout=1)
                except Exception:
                    pass
            runtime_controller.set_current_pid(None)

            # Always resume the listener after a module process finishes
            runtime_controller.resume_listener()

            if runtime_controller.should_quit():
                info("Quitting as requested...")
                break
            if runtime_controller.should_skip_current():
                warning(f"Module '{module_name}' SKIPPED.")
                runtime_controller.reset_module_state()
                continue
        except ImportError as e:
            error(f"Could not import module: {module_info['file']}. Details: {e}")
        except AttributeError:
            error(f"Module {module_info['file']} is missing the required handler.")
        except Exception as e:
            error(f"An error occurred while running module {module_info['file']}: {e}")
    time.sleep(1)
    runtime_controller.stop()
    if runtime_controller.should_quit():
        info("VAJRA terminated by user.")
        return False
    else:
        #
        success("--- Module execution completed ---")
        # Conditional Report Generation (your logic)
        #
        if report_enabled and not runtime_controller.should_quit():
            # Generate report for Run-All (0) or any custom subset
            # Skip only if the user selected *only* Eyewitness (6)
            if ('0' in module_choices) or (sorted(choices) != ['6']):
                try:
                    from .report import generate_report
                    info("Generating final HTML report...")
                    if generate_report(target, target_dir, module_choices):
                        success("HTML report generation successful.")
                    else:
                        error("Failed to generate final HTML report.")
                except Exception as e:
                    error(f"Report generation failed: {e}")
            else:
                info("Eyewitness (6) only run detected, skipping report generation.")
    return True
