#!/usr/bin/env python
"""
Advanced debug wrapper for model initialization
Logs every operation before it happens to catch SIGSEGV point
"""
import sys
import os
import signal
import traceback
import faulthandler
import logging

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.StreamHandler(sys.stderr),
        logging.FileHandler('/tmp/model_debug.log', mode='w')
    ]
)

logger = logging.getLogger(__name__)

# Enable fault handler to catch crashes
faulthandler.enable(file=sys.stderr)

def safe_log(msg, level='info'):
    """Log with forced flush"""
    getattr(logger, level)(msg)
    sys.stdout.flush()
    sys.stderr.flush()
    try:
        with open('/tmp/sigsegv_debug.log', 'a') as f:
            f.write(f"[{level.upper()}] {msg}\n")
            f.flush()
    except:
        pass

def signal_handler(signum, frame):
    """Catch SIGSEGV and log details"""
    safe_log("🔴 SIGSEGV CAUGHT!", 'critical')
    safe_log(f"Signal number: {signum}", 'critical')
    safe_log(f"Stack trace: {traceback.format_stack(frame)}", 'critical')
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)

signal.signal(signal.SIGSEGV, signal_handler)

safe_log("=" * 80)
safe_log("DEBUG: Model initialization wrapper loaded")
safe_log("=" * 80)

# Wrap imports
safe_log("DEBUG: About to import models.py")
try:
    import models
    safe_log("✅ models.py imported successfully")
except Exception as e:
    safe_log(f"❌ Failed to import models: {e}", 'critical')
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)

safe_log("DEBUG: About to import app")
try:
    from app import app, db
    safe_log("✅ app imported successfully")
except Exception as e:
    safe_log(f"❌ Failed to import app: {e}", 'critical')
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)

safe_log("DEBUG: About to call initialize_system()")
try:
    with app.app_context():
        safe_log("DEBUG: Inside app context, about to call initialize_system()")
        from app import initialize_system
        result = initialize_system()
        safe_log(f"✅ initialize_system completed: {result}")
except Exception as e:
    safe_log(f"❌ initialize_system failed: {e}", 'critical')
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)

safe_log("=" * 80)
safe_log("✅ All initialization complete!")
safe_log("=" * 80)

