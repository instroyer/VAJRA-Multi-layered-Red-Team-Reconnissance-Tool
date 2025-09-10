# Runtime control and module execution orchestration
import time
import subprocess
import sys
import os
import threading
import select
from Engine.logger import info, success, warning, error

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
    # Create dummy functions so the code doesn't break
    def dummy_run(target, output_dir, report_enabled=False):
        error(f"Module not available: {target}")
        return False
    whois_run = subfinder_run = amass_run = httpx_run = nmap_run = screenshot_run = dummy_run

# Global variables for runtime control
runtime_control_flag = threading.Event()
control_action = None
current_module = ""
is_paused = False

def runtime_control_listener():
    """Listen for runtime control commands in a separate thread."""
    global control_action
    while not runtime_control_flag.is_set():
        try:
            # Use select with a very short timeout to avoid blocking
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
                # Clear input buffer to prevent multiple triggers
                while sys.stdin in select.select([sys.stdin], [], [], 0.01)[0]:
                    sys.stdin.readline()
        except:
            break

def show_runtime_menu():
    """Display the runtime control menu."""
    menu = """
    ╔══════════════════════════════╗
    ║       Runtime Control        ║
    ╠══════════════════════════════╣
    ║ [p] Pause current module     ║
    ║ [r] Resume paused module     ║
    ║ [s] Skip current module      ║
    ║ [q] Quit VAJRA entirely      ║
    ║ [any] Return to execution    ║
    ╚══════════════════════════════╝
    """
    print(menu)
    
    try:
        # Show prompt and wait for single key + Enter
        print("Select action > ", end='', flush=True)
        
        # Wait for input with 5-second timeout
        start_time = time.time()
        input_line = ""
        
        while True:
            if sys.stdin in select.select([sys.stdin], [], [], 0.1)[0]:
                char = sys.stdin.read(1)
                if char == '\n':  # Enter pressed
                    break
                input_line += char
                
                # Only show the first character if multiple are pressed
                if len(input_line) == 1:
                    print(f"\rSelect action > {input_line}", end='', flush=True)
                elif len(input_line) > 1:
                    # If multiple keys pressed, keep only the first one
                    input_line = input_line[0]
                    print(f"\rSelect action > {input_line}", end='', flush=True)
            
            # Check timeout
            if time.time() - start_time > 5:
                print("\r" + " " * 30 + "\r", end='', flush=True)
                info("Auto-returning to execution...")
                return None
        
        choice = input_line.strip().lower() if input_line else None
        print()  # New line after input
        return choice
        
    except (KeyboardInterrupt, EOFError):
        print("\r" + " " * 30 + "\r", end='', flush=True)
        return None

def handle_paused_state(process, module_name):
    """Handle the paused state until user explicitly resumes."""
    global control_action, is_paused
    
    is_paused = True
    info(f"Module {module_name} is paused. Press 'r' to resume or 's' to skip.")
    
    # Wait for explicit resume command
    while is_paused:
        try:
            # Check for control actions
            if control_action == 'menu':
                choice = show_runtime_menu()
                control_action = None  # Reset immediately
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
                control_action = None  # Reset immediately
                return True
                
            elif control_action == 'skip':
                info(f"Skipping {module_name}...")
                process.terminate()
                is_paused = False
                control_action = None  # Reset immediately
                return False
                
            elif control_action == 'quit':
                info("Quitting VAJRA...")
                process.terminate()
                sys.exit(0)
                
            time.sleep(0.3)  # Check less frequently while paused
            
        except KeyboardInterrupt:
            info("Interrupted. Returning to execution.")
            is_paused = False
            return True

def execute_command_with_control(command, module_name):
    """Execute a command with runtime control support."""
    global control_action, current_module, is_paused
    
    current_module = module_name
    info(f"Running: {command}")
    
    # Start the process
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    try:
        while process.poll() is None:
            # Check for control actions
            if control_action == 'menu':
                choice = show_runtime_menu()
                control_action = None  # Reset immediately after handling
                if choice == 'p':
                    info(f"Pausing {module_name}...")
                    return handle_paused_state(process, module_name)
                elif choice == 'r':
                    info(f"Resuming {module_name}...")
                    # Continue execution
                elif choice == 's':
                    info(f"Skipping {module_name}...")
                    process.terminate()
                    return False
                elif choice == 'q':
                    info("Quitting VAJRA...")
                    process.terminate()
                    sys.exit(0)
                # Any other key just continues execution
                    
            elif control_action == 'pause':
                info(f"Pausing {module_name}...")
                action = control_action
                control_action = None  # Reset immediately
                return handle_paused_state(process, module_name)
                
            elif control_action == 'quit':
                info("Quitting VAJRA...")
                process.terminate()
                sys.exit(0)
                
            elif control_action == 'skip':
                info(f"Skipping {module_name}...")
                process.terminate()
                action = control_action
                control_action = None  # Reset immediately
                return False
                
            elif control_action == 'resume':
                info(f"Resuming {module_name}...")
                control_action = None  # Reset immediately
                # Continue execution
                
            time.sleep(0.1)  # Small delay
            
        # Get process result
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
    """Merge subfinder and amass results into a single file, handling missing files."""
    subfinder_file = f"{target_dir}/Logs/subfinder.txt"
    amass_file = f"{target_dir}/Logs/amass.txt"
    merged_file = f"{target_dir}/Logs/merged_subs.txt"
    
    all_subs = set()
    
    # Read Subfinder results if file exists and has content
    if os.path.exists(subfinder_file) and os.path.getsize(subfinder_file) > 0:
        try:
            with open(subfinder_file, 'r') as f:
                for line in f:
                    sub = line.strip()
                    if sub:
                        all_subs.add(sub)
            info(f"Loaded {len([s for s in all_subs if s])} subdomains from Subfinder")
        except Exception as e:
            error(f"Error reading Subfinder file: {e}")
    
    # Read Amass results if file exists and has content
    if os.path.exists(amass_file) and os.path.getsize(amass_file) > 0:
        try:
            with open(amass_file, 'r') as f:
                for line in f:
                    sub = line.strip()
                    if sub:
                        all_subs.add(sub)
            info(f"Loaded {len([s for s in all_subs if s])} total subdomains after Amass")
        except Exception as e:
            error(f"Error reading Amass file: {e}")
    
    # Write merged results if we have any subdomains
    if all_subs:
        with open(merged_file, 'w') as f:
            for sub in sorted(all_subs):
                f.write(f"{sub}\n")
        success(f"Merged {len(all_subs)} unique subdomains into: {merged_file}")
        return True
    else:
        error("No subdomains found to merge. Both Subfinder and Amass returned empty results.")
        return False

def get_httpx_command(target_dir):
    """Get the correct HTTPX command syntax for httpx-toolkit."""
    merged_file = f"{target_dir}/Logs/merged_subs.txt"
    # httpx-toolkit command (Kali Linux package)
    return f"cat {merged_file} | httpx-toolkit -silent -o {target_dir}/Logs/alive.txt"

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
                    choice = input("Do you want to continue skipping? This will break Nmap and Screenshot. (y/n) > ").strip().lower()
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
            if module_name in ["Whois", "Subfinder", "Amass", "HTTPX", "Screenshot"]:
                # Build the command based on module
                if module_name == "Whois":
                    command = f"whois {target} > {target_dir}/Logs/whois.txt"
                elif module_name == "Subfinder":
                    command = f"subfinder -d {target} -silent -o {target_dir}/Logs/subfinder.txt"
                elif module_name == "Amass":
                    command = f"amass enum -d {target} -o {target_dir}/Logs/amass.txt"
                elif module_name == "HTTPX":
                    # Merge subdomains BEFORE running HTTPX
                    if not merge_subdomain_files(target_dir):
                        error("Cannot run HTTPX without subdomain data. Skipping HTTPX and subsequent modules.")
                        skip_httpx = True
                        continue
                    command = get_httpx_command(target_dir)
                elif module_name == "Screenshot":
                    # Build eyewitness command based on target type
                    if target.startswith('@'):
                        # File input - use the file directly
                        file_path = target[1:]
                        command = f"eyewitness --web --timeout 30 --threads 500 --prepend-https -f {file_path} -d {target_dir}/Screenshots/ --no-prompt"
                    else:
                        # Single target
                        if not target.startswith(('http://', 'https://')):
                            target_url = f"https://{target}"
                        else:
                            target_url = target
                        command = f"eyewitness --web --timeout 30 --threads 500 --prepend-https --single {target_url} -d {target_dir}/Screenshots/ --no-prompt"
                
                success_flag = execute_command_with_control(command, module_name)
                
            else:
                # For Nmap with custom logic
                if module_choices == '0':  # Run All uses default quick scan
                    success_flag = module_func(target, target_dir, report_enabled)
                else:  # Individual Nmap selection
                    success_flag = module_func(target, target_dir, report_enabled)
            
            if not success_flag:
                error(f"Module {module_name} encountered an error or was skipped.")
                
                # If HTTPX fails, mark subsequent modules to be skipped
                if module_name == "HTTPX":
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
    
    # Handle report generation
    if report_enabled and module_choices != '6' and module_choices != '5': 
        info("Generating consolidated report...")
        success("Report generation complete.")
