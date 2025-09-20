# Input utility functions with buffer clearing
import sys
import select

def clear_input_buffer():
    """Clear any pending input from the buffer"""
    try:
        while select.select([sys.stdin], [], [], 0.0)[0]:
            sys.stdin.readline()
    except:
        pass

def get_input(prompt, clear_buffer=True):
    """Get input from user with optional buffer clearing"""
    if clear_buffer:
        clear_input_buffer()
    
    try:
        response = input(prompt).strip()
        # Clear any additional buffered input
        if clear_buffer:
            clear_input_buffer()
        return response
    except (KeyboardInterrupt, EOFError):
        clear_input_buffer()
        raise KeyboardInterrupt
