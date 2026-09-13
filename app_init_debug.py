#!/usr/bin/env python
"""
Patch to add ultra-verbose debugging to initialization
Insert this before initialize_system() is called
"""

import sys
import os

# Monkey patch logger to add debug info
original_logger_info = None
original_logger_error = None

def create_debug_wrapper():
    """Create wrapper for logger.info to log every call"""
    def debug_wrapper(msg):
        sys.stdout.write(f"[LOG] {msg}\n")
        sys.stdout.flush()
        sys.stderr.write(f"[LOG] {msg}\n")
        sys.stderr.flush()
        try:
            with open('/tmp/init_debug.log', 'a') as f:
                f.write(f"{msg}\n")
                f.flush()
        except:
            pass
        if original_logger_info:
            original_logger_info(msg)
    
    return debug_wrapper

# Create checkpoint markers
checkpoint_file = '/tmp/checkpoint.log'

def checkpoint(name):
    """Write a checkpoint marker"""
    with open(checkpoint_file, 'a') as f:
        f.write(f"{name}\n")
        f.flush()
    sys.stdout.write(f"[CHECKPOINT] {name}\n")
    sys.stdout.flush()

# Module for detailed model loader debug
class ModelLoaderDebug:
    @staticmethod
    def wrap_model_load(model_type, model_path, idx=None):
        """Wrap model loading with checkpoints"""
        checkpoint(f"START_LOAD_{model_type}_{idx}")
        sys.stdout.write(f"[MODEL {idx}] Loading {model_type} from {model_path}\n")
        sys.stdout.flush()
        
        try:
            # Actual loading happens here
            yield
            checkpoint(f"SUCCESS_LOAD_{model_type}_{idx}")
            sys.stdout.write(f"[MODEL {idx}] ✅ {model_type} loaded\n")
            sys.stdout.flush()
        except Exception as e:
            checkpoint(f"FAILED_LOAD_{model_type}_{idx}_{str(e)}")
            sys.stdout.write(f"[MODEL {idx}] ❌ {model_type} failed: {e}\n")
            sys.stdout.flush()
            raise

# Inject into app.py before model loading happens
def inject_debug():
    """Inject debug checkpoints"""
    checkpoint("INIT_START")
    
    # Import app
    checkpoint("IMPORTING_APP")
    try:
        from app import app, initialize_system, logger
        checkpoint("APP_IMPORTED")
    except Exception as e:
        checkpoint(f"IMPORT_FAILED_{e}")
        raise
    
    # Call initialize_system
    checkpoint("CALLING_INITIALIZE_SYSTEM")
    try:
        with app.app_context():
            result = initialize_system()
        checkpoint("INITIALIZE_SYSTEM_SUCCESS")
        return result
    except Exception as e:
        checkpoint(f"INITIALIZE_SYSTEM_FAILED_{e}")
        import traceback
        traceback.print_exc(file=sys.stderr)
        raise

if __name__ == '__main__':
    try:
        inject_debug()
        print("✅ Initialization complete")
        with open(checkpoint_file, 'r') as f:
            print("\nCheckpoints reached:")
            for line in f:
                print(f"  {line.rstrip()}")
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        if os.path.exists(checkpoint_file):
            with open(checkpoint_file, 'r') as f:
                print("\nCheckpoints reached before crash:")
                for line in f:
                    print(f"  {line.rstrip()}")
        sys.exit(1)

