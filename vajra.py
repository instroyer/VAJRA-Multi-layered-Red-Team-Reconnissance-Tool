#!/usr/bin/env python3
""" 
VAJRA - Multi-layered Red Team Reconnaissance Framework Main Entry Point | Orchestrator
"""

import sys
import os
import time
import readline
import glob

# Get the absolute path to the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the current directory to Python path
sys.path.insert(0, current_dir)

# Configure readline for better input experience with file completion
readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.parse_and_bind("set editing-mode emacs")

# Custom completer for file paths
def path_completer(text, state):
    """Custom tab completer for file paths"""
    # Expand ~ to home directory
    if '~' in text:
        text = os.path.expanduser(text)

    # Handle @ prefix for file targets
    if text.startswith('@'):
        text = text[1:]
        prefix = '@'
    else:
        prefix = ''

    # Find matches
    matches = glob.glob(text + '*')

    # Add appropriate suffix based on whether it's a directory or file
    completed_matches = []
    for match in matches:
        if os.path.isdir(match):
            completed_matches.append(prefix + match + '/')
        else:
            completed_matches.append(prefix + match)

    # Return the match at the current state
    if state < len(completed_matches):
        return completed_matches[state]
    else:
        return None

# Set the completer
readline.set_completer(path_completer)

# Now import using absolute paths that work from this directory
try:
    from Engine.banner import display_banner
    from Engine.logger import info, success, warning, error, target_info
    from Engine.menu import main_menu, show_help
    from Engine.file_ops import create_target_dirs
    from Engine.runtime import execute_modules
    from Engine.dependencies import check_dependencies, install_dependencies
    from Engine.input_utils import get_input, clear_input_buffer  # ADDED
except ImportError as e:
    print(f"Import error: {e}")
    print("Current Python path:", sys.path)
    sys.exit(1)

# Global configuration
class Config:
    RESULTS_BASE_DIR = "Results"  # Base directory for all results

def get_targets_from_file(file_path):
    """Read targets from a file and return as list."""
    try:
        with open(file_path, 'r') as f:
            targets = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
        return targets
    except IOError as e:
        error(f"Error reading file {file_path}: {e}")
        return []

def get_target():
    """Get and validate target input from user."""
    while True:
        try:
            target = get_input("\nEnter your target > ").strip()
            if not target:
                error("Target cannot be empty. Please try again.")
                continue

            # Handle file input (@filename.txt)
            if target.startswith('@'):
                file_path = target[1:]  # Remove the @ symbol
                if not os.path.isfile(file_path):
                    error(f"File not found: {file_path}")
                    continue

                # Read targets from file
                targets = get_targets_from_file(file_path)

                if not targets:
                    error(f"No valid targets found in {file_path}")
                    continue

                # Get just the filename without path for folder naming
                file_name = os.path.splitext(os.path.basename(file_path))[0]

                info(f"Found {len(targets)} targets in file: {file_path}")
                return target, targets, True, file_name  # Return file specifier, target list, is_file flag, and file_name

            # Validate single target format
            if " " in target and not all(part.isdigit() or part == '.' for part in target.split()):
                error("Invalid target format. Use @file.txt for multiple targets.")
                continue

            return target, [target], False, None  # Return as single target in list, not file

        except KeyboardInterrupt:
            info("\nOperation cancelled by user.")
            sys.exit(0)

def process_targets(targets, module_choices, report_enabled, is_file_input=False, file_name=None):
    """Process multiple targets with the same module selection and report preference."""
    for target in targets:
        # Create target-specific directory structure
        clean_target = ''.join(c for c in target if c.isalnum() or c in ['.', '-', '_'])
        target_dir = create_target_dirs(Config.RESULTS_BASE_DIR, clean_target, is_file_input, file_name)

        if not target_dir:
            error(f"Failed to create output directories for {target}. Skipping.")
            continue

        # Use yellow color for target information
        target_info(f"Target set to: {target}")
        info(f"Output directory: {target_dir}")

        if is_file_input:
            info(f"Processing target {targets.index(target) + 1}/{len(targets)} from file")

        # Execute the selected modules for this target
        execute_modules(module_choices, target, target_dir, report_enabled)

        if is_file_input and targets.index(target) < len(targets) - 1:
            info("Moving to next target...")

def main():
    """Main orchestration function for VAJRA."""
    try:
        # Display the banner
        display_banner()

        # Check for module availability
        info("Checking system dependencies...")
        missing_tools = check_dependencies(silent=False)

        if missing_tools:
            if not install_dependencies(missing_tools):
                sys.exit(1)

        info("Verifying installation...")
        still_missing = check_dependencies(silent=True)

        if still_missing:
            error("Some tools are still missing. Exiting.")
            for tool in still_missing:
                error(f"- {tool} not found")
            sys.exit(1)
        else:
            success("All dependencies are now satisfied!")

        # Main program loop
        while True:
            # Get target from user (could be single target or file)
            target_input, targets, is_file_input, file_name = get_target()

            # Get module selection (only once for file inputs)
            if is_file_input:
                info("File input detected. Select modules once for all targets.")
                target_for_menu = targets[0] if targets else "file_targets"
            else:
                target_for_menu = target_input

            # MODULE SELECTION LOOP FOR THIS TARGET
            while True:
                # Display main menu and get user selection
                module_choices = main_menu(target_for_menu)

                # Handle special commands from main menu
                if module_choices == '000':  # Help Menu
                    show_help()
                    continue  # Stay in module selection loop
                elif module_choices == '00':  # Runtime Control Menu
                    warning("Runtime control is available during module execution.")
                    continue  # Stay in module selection loop

                # Get report preference (only once for file inputs)
                if module_choices == '6':  # Eyewitness only - skip report prompt
                    report_enabled = False
                elif module_choices == '5':  # Nmap handles its own report prompt internally
                    report_enabled = False
                else:
                    try:
                        generate_report = get_input("\nDo you want to generate a report for this? (y/n) > ").strip().lower()
                        report_enabled = (generate_report == 'y')
                    except KeyboardInterrupt:
                        info("\nOperation cancelled by user.")
                        break  # Break out of module selection loop

                # Process all targets with the same module selection and report preference
                process_targets(targets, module_choices, report_enabled, is_file_input, file_name)
                break  # Break out of module selection loop after processing

            # After finishing all targets, ask if user wants to scan NEW targets
            try:
                new_target = get_input("\nScan new targets? (y/n) > ").strip().lower()

                if new_target != 'y':
                    success("Thank you for using VAJRA. Exiting.")
                    break  # Break out of main program loop
            except KeyboardInterrupt:
                success("Thank you for using VAJRA. Exiting.")
                break  # Break out of main program loop

    except KeyboardInterrupt:
        info("\nOperation cancelled by user. Exiting.")
        sys.exit(0)
    except Exception as e:
        error(f"An unexpected error occurred in the main loop: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
