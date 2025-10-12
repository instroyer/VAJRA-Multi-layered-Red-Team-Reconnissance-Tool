# VAJRA/Engine/runtime.py
# Description: Runtime control and module execution orchestration.

import time
import subprocess
import sys
import os
import threading
import select

from .logger import info, success, warning, error, target_info
from .input_utils import get_input, clear_input_buffer
from .finaljson import FinalJsonGenerator
from .report import generate_report

# Add the parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import modules directly
try:
    from Modules.whois import run as whois_run
    from Modules.subfinder import run as subfinder_run
    from Modules.amass import run as amass_run
    from Modules.httpx import run as httpx_run
    from Modules.nmap import run as nmap_run
    from Modules.screenshot import run as screenshot_run
except ImportError as e:
    error(f"Failed to import modules: {e}")
    # Define dummy functions if imports fail
    def dummy_run(*args, **kwargs):
        error("Module not available or import failed.")
        return False
    whois_run, subfinder_run, amass_run, httpx_run, nmap_run, screenshot_run = (dummy_run,) * 6

# Global variables for runtime control
runtime_control_flag = threading.Event()
control_action = None
current_module = ""
is_paused = False
listener_active = True

def nmap_run_all(target, output_dir):
    """Wrapper for Nmap in Run All mode with default quick scan."""
    return nmap_run(target, output_dir, False, 'quick')

def runtime_control_listener():
    """Listen for runtime control commands in a separate thread."""
    global control_action, listener_active
    while not runtime_control_flag.is_set():
        try:
            if not listener_active or not sys.stdin.isatty():
                time.sleep(0.1)
                continue
            
            if select.select([sys.stdin], [], [], 0.1)[0]:
                user_input = sys.stdin.readline().strip()
                if control_action is None:
                    if user_input == '00': control_action = 'menu'
                    elif user_input == 'p': control_action = 'pause'
                    elif user_input == 'r': control_action = 'resume'
                    elif user_input == 's': control_action = 'skip'
                    elif user_input == 'q': control_action = 'quit'
        except (IOError, ValueError): # Catches errors when stdin is not available
            break
        except Exception as e:
            error(f"Runtime listener error: {e}")
            break

def pause_listener():
    global listener_active
    listener_active = False

def resume_listener():
    global listener_active
    listener_active = True

def safe_input(prompt, default=None):
    """Wrapper for input that suspends the runtime listener."""
    pause_listener()
    try:
        val = get_input(prompt)
        return val.strip() if val else default
    finally:
        resume_listener()

def show_runtime_menu():
    """Display the runtime control menu."""
    global current_module
    menu = f"""
    +----------------------------+
    |     Runtime Control        |
    | Current: {current_module:<15} |
    +----------------------------+
    | [p] Pause   [s] Skip       |
    | [r] Resume  [q] Quit       |
    | [any] Return to execution  |
    +----------------------------+
    """
    print(menu)
    pause_listener()
    try:
        choice = get_input("Select action > ", clear_buffer=True)
        return choice.strip().lower() if choice else None
    finally:
        resume_listener()

def handle_paused_state(process, module_name):
    """Handle the paused state until user explicitly resumes."""
    global control_action, is_paused
    is_paused = True
    info(f"Module {module_name} is paused. Press 'r' to resume or 's' to skip.")
    while is_paused:
        time.sleep(0.3)
        if control_action in ['resume', 'r']:
            info(f"Resuming {module_name}...")
            is_paused = False
            control_action = None
            return True
        elif control_action in ['skip', 's']:
            info(f"Skipping {module_name}...")
            process.terminate()
            is_paused = False
            control_action = None
            return False
        elif control_action in ['quit', 'q']:
            info("Quitting VAJRA...")
            process.terminate()
            sys.exit(0)
        elif control_action == 'menu':
            choice = show_runtime_menu()
            control_action = None # Reset after menu
            if choice == 'r': control_action = 'resume'
            elif choice == 's': control_action = 'skip'
            elif choice == 'q': control_action = 'quit'

def execute_command_with_control(command, module_name):
    """Execute a command with runtime control support."""
    global control_action, current_module
    current_module = module_name
    info(f"Running: {command}")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    try:
        while process.poll() is None:
            time.sleep(0.1) # Prevent CPU spinning
            if control_action in ['pause', 'p']:
                info(f"Pausing {module_name}...")
                control_action = None
                if not handle_paused_state(process, module_name): return False
            elif control_action in ['skip', 's']:
                info(f"Skipping {module_name}...")
                process.terminate()
                control_action = None
                return False
            elif control_action in ['quit', 'q']:
                info("Quitting VAJRA...")
                process.terminate()
                sys.exit(0)
            elif control_action == 'menu':
                choice = show_runtime_menu()
                control_action = None # Reset after menu
                if choice == 'p': control_action = 'pause'
                elif choice == 's': control_action = 'skip'
                elif choice == 'q': control_action = 'quit'

        stdout, stderr = process.communicate()
        if process.returncode == 0:
            success(f"Completed module: {module_name}")
            return True
        else:
            error(f"{module_name} failed: {stderr.strip()}")
            return False
    except KeyboardInterrupt:
        warning(f"{module_name} interrupted.")
        process.terminate()
        return False
    except Exception as e:
        error(f"Error in execute_command_with_control for {module_name}: {e}")
        process.terminate()
        return False

def merge_subdomain_files(target_dir):
    """Merge subfinder and amass results into a single file."""
    subfinder_file = os.path.join(target_dir, "Logs", "subfinder.txt")
    amass_file = os.path.join(target_dir, "Logs", "amass.txt")
    merged_file = os.path.join(target_dir, "Logs", "merged_subs.txt")
    all_subs = set()

    for file_path in [subfinder_file, amass_file]:
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            try:
                with open(file_path, 'r') as f:
                    all_subs.update(line.strip() for line in f if line.strip())
            except Exception as e:
                error(f"Error reading {os.path.basename(file_path)} file: {e}")
    
    if all_subs:
        try:
            with open(merged_file, 'w') as f:
                for sub in sorted(all_subs):
                    f.write(f"{sub}\n")
            success(f"Merged {len(all_subs)} unique subdomains into: {os.path.basename(merged_file)}")
            return True
        except Exception as e:
            error(f"Error writing merged file: {e}")
            return False
    else:
        warning("No subdomains found to merge. Subfinder and Amass returned empty results.")
        return False

def execute_modules(module_choices, target, target_dir, report_enabled):
    """Execute the selected modules in the appropriate order."""
    global control_action, runtime_control_flag, current_module
    
    # Reset control action and start listener
    control_action = None
    runtime_control_flag.clear()
    listener_thread = threading.Thread(target=runtime_control_listener, daemon=True)
    listener_thread.start()
    info("Runtime control activated. Press '00' during execution for controls.")

    module_map = {
        '1': ("Whois", whois_run), '2': ("Subfinder", subfinder_run),
        '3': ("Amass", amass_run),   '4': ("HTTPX", httpx_run),
        '5': ("Nmap", nmap_run),     '6': ("Screenshot", screenshot_run)
    }

    execution_plan = []
    if module_choices == '0':
        info("Running all modules with default settings...")
        execution_plan = [("Whois", whois_run), ("Subfinder", subfinder_run), ("Amass", amass_run),
                          ("HTTPX", httpx_run), ("Nmap", nmap_run_all), ("Screenshot", screenshot_run)]
    else:
        for choice in sorted(module_choices.split()):
            if choice in module_map:
                execution_plan.append(module_map[choice])

    if not execution_plan:
        error("No valid modules selected.")
        return

    info(f"Starting {len(execution_plan)} module(s)...")
    time.sleep(1)

    # --- MAIN EXECUTION LOOP ---
    for module_name, module_func in execution_plan:
        current_module = module_name
        success_flag = False

        if control_action in ['skip', 's']:
            info(f"Skipping {module_name}.")
            control_action = None
            continue
        if control_action in ['quit', 'q']:
            break

        info(f"--- Starting module: {module_name} ---")
        try:
            # --- CHANGE START: Conditional logic for HTTPX and dependent modules ---
            if module_name == "HTTPX":
                if module_choices == '0': # Run All mode
                    if not merge_subdomain_files(target_dir):
                        error("HTTPX depends on subdomain data. Aborting 'Run All' pipeline for this target.")
                        break # Stop further execution for this target
                    httpx_input_target = f"@{os.path.join(target_dir, 'Logs', 'merged_subs.txt')}"
                    success_flag = module_func(httpx_input_target, target_dir)
                else: # Custom module selection mode
                    success_flag = module_func(target, target_dir)
            
            elif module_name in ["Nmap", "Screenshot"]:
                if module_choices == '0': # Run All mode
                    alive_file = os.path.join(target_dir, "Logs", "alive.txt")
                    if os.path.exists(alive_file) and os.path.getsize(alive_file) > 0:
                        input_target = f"@{alive_file}"
                        info(f"{module_name} will use alive hosts from HTTPX.")
                    else:
                        warning(f"HTTPX output 'alive.txt' not found. {module_name} will use original target.")
                        input_target = target
                    success_flag = module_func(input_target, target_dir)
                else: # Custom module selection mode
                    success_flag = module_func(target, target_dir, report_enabled)
            
            else: # For Whois, Subfinder, Amass
                success_flag = module_func(target, target_dir)
            # --- CHANGE END ---

            if success_flag:
                success(f"Module {module_name} completed successfully.")
            else:
                error(f"Module {module_name} failed or was skipped.")
        
        except KeyboardInterrupt:
            warning(f"Module {module_name} interrupted by user.")
            control_action = 'menu'
        except Exception as e:
            error(f"An unexpected error occurred in {module_name}: {e}")

    # Stop the listener thread
    runtime_control_flag.set()
    if listener_thread.is_alive():
        listener_thread.join(timeout=1.0)
    success("--- Module execution completed ---")
