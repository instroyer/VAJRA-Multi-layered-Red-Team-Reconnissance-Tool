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
            if sys.stdin in select.select([sys.stdin], [], [], 0.1)[0]:
                user_input = sys.stdin.readline().strip()
                if user_input == '00':
                    control_action = 'menu'
                elif user_input == 'p':
                    control_action = 'pause'
                elif user_input == 'r':
                    control_action = 'resume'
                elif user_input == 's':
                    control_action = 'skip'
                elif user_input == 'q':
                    control_action = 'quit'
        except:
            break

def show_runtime_menu():
    """Display the runtime control menu with proper pause handling."""
    menu = """
    ╔══════════════════════════════╗
    ║       Runtime Control        ║
    ╠══════════════════════════════╣
    ║ [p] Pause current module     ║
    ║ [r] Resume paused module     ║
    ║ [s] Skip to next target      ║
    ║ [q] Quit VAJRA entirely      ║
    ║ [any] Return to execution    ║
    ╚══════════════════════════════╝
    """
    print(menu)
    
    try:
        # Show prompt and wait for input without auto-return
        print("Select action > ", end='', flush=True)
        choice = input().strip().lower()
        return choice
        
    except (KeyboardInterrupt, EOFError):
        return None

def handle_paused_state(process, module_name):
    """Handle the paused state until user explicitly resumes."""
    global control_action, is_paused
    
    is_paused = True
    info(f"Module {module_name} is paused. Press 'r' to resume.")
    
    # Wait for explicit resume command
    while is_paused:
        try:
            # Check for control actions
            if control_action == 'menu':
                choice = show_runtime_menu()
                if choice == 'r':
                    info(f"Resuming {module_name}...")
                    is_paused = False
                    control_action = None
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
                else:
                    info("Module is still paused. Press 'r' to resume.")
            
            elif control_action == 'resume':
                info(f"Resuming {module_name}...")
                is_paused = False
                control_action = None
                return True
                
            elif control_action == 'skip':
                info(f"Skipping {module_name}...")
                process.terminate()
                is_paused = False
                return False
                
            elif control_action == 'quit':
                info("Quitting VAJRA...")
                process.terminate()
                sys.exit(0)
                
            time.sleep(0.5)  # Check less frequently while paused
            
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
                if choice == 'p':
                    info(f"Pausing {module_name}...")
                    return handle_paused_state(process, module_name)
                elif choice == 'r':
                    info(f"Resuming {module_name}...")
                    control_action = None
                elif choice == 's':
                    info(f"Skipping {module_name}...")
                    process.terminate()
                    return False
                elif choice == 'q':
                    info("Quitting VAJRA...")
                    process.terminate()
                    sys.exit(0)
                else:
                    control_action = None
                    info(f"Resuming {module_name}...")
                    
            elif control_action == 'pause':
                info(f"Pausing {module_name}...")
                return handle_paused_state(process, module_name)
                
            elif control_action == 'quit':
                process.terminate()
                sys.exit(0)
                
            elif control_action == 'skip':
                process.terminate()
                return False
                
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

def check_file_exists_and_not_empty(file_path, description):
    """Check if a file exists and is not empty."""
    if not os.path.exists(file_path):
        error(f"{description} not found: {file_path}")
        return False
    if os.path.getsize(file_path) == 0:
        error(f"{description} is empty: {file_path}")
        return False
    return True

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
        if control_action == 'quit':
            info("Quitting VAJRA.")
            sys.exit(0)
        if control_action == 'skip':
            info(f"Skipping {module_name}.")
            control_action = None
            
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
                        control_action = None
                except KeyboardInterrupt:
                    info("Continuing with HTTPX execution.")
                    control_action = None
            
            continue
            
        info(f"Starting module: {module_name}")
        
        try:
            # Special pre-processing for HTTPX
            if module_name == "HTTPX":
                # Check if we have merged subdomains file
                merged_file = f"{target_dir}/Logs/merged_subs.txt"
                if not os.path.exists(merged_file):
                    # Try to create merged file from available results
                    if not merge_subdomain_files(target_dir):
                        error("Cannot run HTTPX without subdomain data. Skipping HTTPX and subsequent modules.")
                        skip_httpx = True
                        continue
            
            # Special handling for modules that need previous results
            if module_name in ["Nmap", "Screenshot"] and skip_httpx:
                info(f"Skipping {module_name} because HTTPX was skipped/failed.")
                continue
                
            if module_name in ["Nmap", "Screenshot"]:
                # Check if alive.txt exists and has content
                alive_file = f"{target_dir}/Logs/alive.txt"
                if not check_file_exists_and_not_empty(alive_file, "Alive hosts file"):
                    info(f"Skipping {module_name} because no alive hosts were found.")
                    continue
            
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
                    command = f"httpx -l {target_dir}/Logs/merged_subs.txt -silent -o {target_dir}/Logs/alive.txt"
                elif module_name == "Screenshot":
                    command = f"eyewitness --web -f {target_dir}/Logs/alive.txt -d {target_dir}/Screenshots/ --no-prompt"
                
                success_flag = execute_command_with_control(command, module_name)
                
                # Post-processing after Subfinder or Amass
                if module_name in ["Subfinder", "Amass"] and success_flag:
                    # Try to merge results after each subdomain discovery tool
                    merge_subdomain_files(target_dir)
                
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
                
                # Special handling for HTTPX skip
                if module_name == "HTTPX":
                    skip_httpx = True
                
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
