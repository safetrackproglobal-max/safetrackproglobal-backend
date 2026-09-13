#!/usr/bin/env python
import sys, os, logging
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

checkpoint_file = '/tmp/checkpoint.log'

def checkpoint(name):
    with open(checkpoint_file, 'a') as f:
        f.write(f"{name}\n")
        f.flush()
    sys.stdout.write(f"[CHECKPOINT] {name}\n")
    sys.stdout.flush()

def inject_debug():
    checkpoint("INIT_START")
    checkpoint("IMPORTING_APP")
    try:
        from app import app, initialize_system, logger
        checkpoint("APP_IMPORTED")
    except Exception as e:
        checkpoint(f"IMPORT_FAILED_{e}")
        raise
    
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
            print("\nCheckpoints:")
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
