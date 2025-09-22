# Engine/runtime.py
# Runtime control and module execution orchestration

import time
import subprocess
import sys
import os
import threading
import select
from Engine.logger import info, success, warning, error, target_info
from Engine.input_utils import get_input, clear_input_buffer

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
    print(f"Failed to import modules: {e}")

def dummy_run(*args, **kwargs):
    error("Module not available")
    return False

# Fallback to dummy functions if imports failed
whois_run = whois_run if 'whois_run' in locals() else dummy_run
subfinder_run = subfinder_run if 'subfinder_run' in locals() else dummy_run
amass_run = amass_run if 'amass_run' in locals() else dummy_run
httpx_run = httpx_run if 'httpx_run' in locals() else dummy_run
nmap_run = nmap_run if 'nmap_run' in locals() else dummy_run
screenshot_run = screenshot_run if 'screenshot_run' in locals() else dummy_run

# Global variables
runtime_control_flag = threading.Event()
control_action = None
current_module = ""
is_paused = False
listener_active = True  # flag to suspend listener while prompting

def runtime_control_listener():
    """Listen for runtime control commands in a separate thread"""
    global control_action, listener_active
    while not runtime_control_flag.is_set():
        try:
            if not listener_active:
                time.sleep(0.1)
                continue

            if sys.stdin in select.select([sys.stdin], [], [], 0.1)[0]:
                user_input = sys.stdin.readline().strip()
                if user_input == '00' and control_action is None:
                    control_action = 'menu'
                elif user_input == 'p' and control_action is None:
                    control_action = 'pause'
                elif user_input == 'r' and control_action is None:
                    control_action = 'resume'
                elif user_input == 's' and control_action is None:
                    control_action = 'skip'
                elif user_input == 'q' and control_action is None:
                    control_action = 'quit'
                while sys.stdin in select.select([sys.stdin], [], [], 0.01)[0]:
                    sys.stdin.readline()

        except:
            break

def pause_listener():
    """Suspend the runtime control listener"""
    global listener_active
    listener_active = False

def resume_listener():
    """Resume the runtime control listener"""
    global listener_active
    listener_active = True

def safe_input(prompt, default=None):
    """
    Wrapper for input/get_input that suspends the runtime listener.
    If default is provided, return default when user presses Enter.
    """
    pause_listener()
    try:
        if default is None:
            return get_input(prompt)
        else:
            val = get_input(prompt)
            if val is None:
                return default
            val = val.strip()
            return val if val else default
    finally:
        resume_listener()

def show_runtime_menu():
    """Display the runtime control menu."""
    menu = """
    +----------------------------+
    |      Runtime Control       |
    +----------------------------+
    | [p] Pause current module   |
    | [r] Resume paused module   |
    | [s] Skip current module    |
    | [q] Quit VAJRA entirely    |
    | [any] Return to execution  |
    +----------------------------+
    """
    print(menu)

    try:
        clear_input_buffer()
        print("Select action > ", end="", flush=True)

        pause_listener()
        start_time = time.time()
        input_line = ""
        while True:
            if sys.stdin in select.select([sys.stdin], [], [], 0.1)[0]:
                char = sys.stdin.read(1)
                if char == '\n':
                    break
                input_line += char
                if len(input_line) == 1:
                    print(f"{input_line}", end="", flush=True)
                elif len(input_line) > 1:
                    input_line = input_line[0]
                    print(f"{input_line}", end="", flush=True)

            if time.time() - start_time > 5:
                print("\r" + " " * 30 + "\r", end="", flush=True)
                info("Auto-returning to execution...")
                resume_listener()
                return None

        choice = input_line.strip().lower() if input_line else None
        print()
        return choice

    except (KeyboardInterrupt, EOFError):
        print("\r" + " " * 30 + "\r", end="", flush=True)
        return None
    finally:
        resume_listener()

def handle_paused_state(process, module_name):
    """Handle the paused state until user explicitly resumes."""
    global control_action, is_paused

    is_paused = True
    info(f"Module {module_name} is paused. Press 'r' to resume or 's' to skip.")

    while is_paused:
        try:
            if control_action == 'menu':
                choice = show_runtime_menu()
                control_action = None
                if choice == 'r':
                    info(f"Resuming {module_name}...")
                    is_paused = False
                    return True
                elif choice == 's':
                    info(f"Skipping {module_name}...")
                    process.terminate()
                    is_paused = False
                    return False
                elif choice == 'q':
                    info("Quitting VAJRA...")
                    process.terminate()
                    sys.exit(0)

            elif control_action == 'resume':
                info(f"Resuming {module_name}...")
                is_paused = False
                control_action = None
                return True

            elif control_action == 'skip':
                info(f"Skipping {module_name}...")
                process.terminate()
                is_paused = False
                control_action = None
                return False

            elif control_action == 'quit':
                info("Quitting VAJRA...")
                process.terminate()
                sys.exit(0)

            time.sleep(0.3)

        except KeyboardInterrupt:
            info("Interrupted. Returning to execution.")
            is_paused = False
            return True

def execute_command_with_control(command, module_name):
    """Execute a command with runtime control support."""
    global control_action, current_module, is_paused

    current_module = module_name
    info(f"Running: {command}")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    try:
        while process.poll() is None:
            if control_action == 'menu':
                choice = show_runtime_menu()
                control_action = None
                if choice == 'p':
                    info(f"Pausing {module_name}...")
                    return handle_paused_state(process, module_name)
                elif choice == 'r':
                    info(f"Resuming {module_name}...")
                elif choice == 's':
                    info(f"Skipping {module_name}...")
                    process.terminate()
                    return False
                elif choice == 'q':
                    info("Quitting VAJRA...")
                    process.terminate()
                    sys.exit(0)

            elif control_action == 'pause':
                info(f"Pausing {module_name}...")
                control_action = None
                return handle_paused_state(process, module_name)

            elif control_action == 'quit':
                info("Quitting VAJRA...")
                process.terminate()
                sys.exit(0)

            elif control_action == 'skip':
                info(f"Skipping {module_name}...")
                process.terminate()
                control_action = None
                return False

            elif control_action == 'resume':
                info(f"Resuming {module_name}...")
                control_action = None

            time.sleep(0.1)

        stdout, stderr = process.communicate()

        if process.returncode == 0:
            success(f"Completed module: {module_name}")
            return True
        else:
            error(f"{module_name} failed: {stderr}")
            return False

    except KeyboardInterrupt:
        warning(f"{module_name} interrupted.")
        process.terminate()
        return False

def merge_subdomain_files(target_dir):
    """Merge subfinder and amass results into a single file."""
    subfinder_file = f"{target_dir}/Logs/subfinder.txt"
    amass_file = f"{target_dir}/Logs/amass.txt"
    merged_file = f"{target_dir}/Logs/merged_subs.txt"

    all_subs = set()

    # Read from Subfinder
    if os.path.exists(subfinder_file) and os.path.getsize(subfinder_file) > 0:
        try:
            with open(subfinder_file, 'r') as f:
                for line in f:
                    sub = line.strip()
                    if sub:
                        all_subs.add(sub)
            info(f"Loaded {len(all_subs)} subdomains from Subfinder")
        except Exception as e:
            error(f"Error reading Subfinder file: {e}")

    # Read from Amass
    if os.path.exists(amass_file) and os.path.getsize(amass_file) > 0:
        try:
            with open(amass_file, 'r') as f:
                for line in f:
                    sub = line.strip()
                    if sub:
                        all_subs.add(sub)
            info(f"Loaded {len(all_subs)} total subdomains after Amass")
        except Exception as e:
            error(f"Error reading Amass file: {e}")

    # Write merged results
    if all_subs:
        try:
            with open(merged_file, 'w') as f:
                for sub in sorted(all_subs):
                    f.write(f"{sub}\n")
            success(f"Merged {len(all_subs)} unique subdomains into: {merged_file}")
            return True
        except Exception as e:
            error(f"Error writing merged file: {e}")
            return False
    else:
        error("No subdomains found to merge. Both Subfinder and Amass returned empty results.")
        return False

def execute_modules(module_choices, target, target_dir, report_enabled):
    """
    Execute the selected modules in the appropriate order.
    module_choices: string of user input (e.g., '0', '1 2 4')
    """
    global control_action, runtime_control_flag, current_module, is_paused

    # Reset control action and pause state
    control_action = None
    current_module = ""
    is_paused = False

    # Start runtime control listener thread
    listener_thread = threading.Thread(target=runtime_control_listener, daemon=True)
    listener_thread.start()

    # Map choices to modules and their execution order for '0'
    module_map = {
        '1': (whois_run, "Whois"),
        '2': (subfinder_run, "Subfinder"),
        '3': (amass_run, "Amass"),
        '4': (httpx_run, "HTTPX"),
        '5': (nmap_run, "Nmap"),
        '6': (screenshot_run, "Screenshot")
    }

    execution_plan = []
    skip_httpx = False

    # Determine execution plan based on user choice
    if module_choices == '0':
        # Run All sequence with default Nmap (quick scan)
        execution_plan = [
            (whois_run, "Whois"),
            (subfinder_run, "Subfinder"),
            (amass_run, "Amass"),
            (httpx_run, "HTTPX"),
            (lambda t, d, r: nmap_run(t, d, r, 'quick'), "Nmap"),
            (screenshot_run, "Screenshot")
        ]
    else:
        for choice in module_choices.split():
            if choice in module_map:
                execution_plan.append(module_map[choice])

    # Show target info before executing modules
    if execution_plan:
        target_info(f"Target set to: {target}")
        info(f"Output directory: {target_dir}")
        info(f"Starting {len(execution_plan)} module(s)...")
        time.sleep(1)  # Brief pause to let user see the info

    # Execute each module in the plan
    for i, (module_func, module_name) in enumerate(execution_plan):
        # Reset skip flag for each module
        skip_current_module = False

        if control_action == 'quit':
            info("Quitting VAJRA.")
            sys.exit(0)

        if control_action == 'skip':
            info(f"Skipping {module_name}.")
            control_action = None
            skip_current_module = True

        # Special handling for HTTPX skip
        if module_name == "HTTPX":
            warning("HTTPX is critical for the recon pipeline. Skipping it will break subsequent modules.")
            try:
                choice = safe_input("Do you want to continue skipping? This will skip Nmap and Screenshot. (y/n) > ", default="n").strip().lower()
                if choice == 'y':
                    skip_httpx = True
                    info("Skipping HTTPX. Nmap and Screenshot will be skipped automatically.")
                    continue
                else:
                    info("Continuing with HTTPX execution.")
                    skip_current_module = False
                    control_action = None
            except KeyboardInterrupt:
                info("Continuing with HTTPX execution.")
                skip_current_module = False
                control_action = None

        if skip_current_module:
            continue

        info(f"Starting module: {module_name}")

        try:
            # For modules that use subprocess directly
            if module_name in ["Whois", "Subfinder", "Amass", "HTTPX"]:
                # Build the command based on module
                if module_name == "Whois":
                    command = f"whois {target} > {target_dir}/Logs/whois.txt"
                    success_flag = execute_command_with_control(command, module_name)
                elif module_name == "Subfinder":
                    command = f"subfinder -d {target} -silent -o {target_dir}/Logs/subfinder.txt"
                    success_flag = execute_command_with_control(command, module_name)
                elif module_name == "Amass":
                    command = f"amass enum -d {target} -o {target_dir}/Logs/amass.txt"
                    success_flag = execute_command_with_control(command, module_name)
                elif module_name == "HTTPX":
                    # Merge subdomains BEFORE running HTTPX
                    if not merge_subdomain_files(target_dir):
                        error("Cannot run HTTPX without subdomain data. Skipping HTTPX and subsequent modules.")
                        skip_httpx = True
                        success_flag = False
                    else:
                        # HTTPX module now handles everything internally
                        success_flag = module_func(target, target_dir)
            else:
                # For Nmap with custom logic or Screenshot delegation
                # When running the full pipeline (module_choices == '0'), prefer alive.txt if it exists
                alive_file = f"{target_dir}/Logs/alive.txt"
                alive_exists = os.path.exists(alive_file) and os.path.getsize(alive_file) > 0
                
                if module_name == "Nmap":
                    # If run-all and httpx produced alive.txt, run nmap on that list
                    if module_choices == '0' and alive_exists:
                        nmap_target = f"@{alive_file}"
                        # module_func could be a lambda that already wraps scan type for run-all
                        success_flag = module_func(nmap_target, target_dir, report_enabled)
                    elif module_name == "Nmap" and module_choices != '0':
                        # interactive Nmap selection for single-module invocation
                        from Engine.menu import nmap_submenu
                        scan_type, nmap_report_enabled = nmap_submenu(safe_input)
                        success_flag = module_func(target, target_dir, nmap_report_enabled, scan_type)
                    else:
                        # fallback
                        success_flag = module_func(target, target_dir, report_enabled)

                elif module_name == "Screenshot":
                    # if run-all and httpx produced alive.txt, run screenshots on that list
                    if module_choices == '0' and alive_exists:
                        screenshot_target = f"@{alive_file}"
                        success_flag = module_func(screenshot_target, target_dir, report_enabled)
                    else:
                        success_flag = module_func(target, target_dir, report_enabled)
                else:
                    # Other modules (including when run-all wraps nmap as lambda)
                    success_flag = module_func(target, target_dir, report_enabled)

            if not success_flag:
                error(f"Module {module_name} encountered an error or was skipped.")

            # If HTTPX fails, mark subsequent modules to be skipped
            if module_name == "HTTPX" and not success_flag:
                skip_httpx = True

        except KeyboardInterrupt:
            warning(f"Module {module_name} interrupted by user.")
            choice = show_runtime_menu()
            if choice == 'q':
                info("Quitting VAJRA.")
                sys.exit(0)
            elif choice == 's':
                info(f"Skipping {module_name}.")
                continue
        except Exception as e:
            error(f"Unexpected error in {module_name}: {e}")
            # If HTTPX fails, mark subsequent modules to be skipped
            if module_name == "HTTPX":
                skip_httpx = True

    # Stop the listener thread
    runtime_control_flag.set()

    # After all modules are executed, create final.json
    if execution_plan:  # Only if modules were actually run
        try:
            from Engine.finaljson import create_final_json
            create_final_json(target_dir, module_choices)
        except ImportError:
            warning("finaljson module not available, skipping JSON creation")
        except Exception as e:
            error(f"Error creating final.json: {e}")

    # Handle report generation
    if report_enabled and module_choices not in ['6', '5']:
        info("Generating consolidated report...")
        success("Report generation complete.")
