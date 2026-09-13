# Advanced debug patch for SIGSEGV tracking
import sys
import os
import signal
import traceback
import faulthandler

# Enable fault handler to catch segfaults
faulthandler.enable(file=sys.stderr)

def debug_signal_handler(signum, frame):
    """Catch segfault and log stack trace"""
    import logging
    logger = logging.getLogger(__name__)
    logger.critical(f"🔴 SIGSEGV CAUGHT at signal {signum}")
    logger.critical(f"Stack trace:\n{traceback.format_stack(frame)}")
    traceback.print_exc(file=sys.stderr)
    sys.stderr.flush()
    sys.stdout.flush()
    os._exit(1)

signal.signal(signal.SIGSEGV, debug_signal_handler)

def log_flush(logger, msg, level='info'):
    """Log with forced flush to ensure output appears before crash"""
    getattr(logger, level)(msg)
    sys.stdout.flush()
    sys.stderr.flush()
    
    # Also write to a debug file
    try:
        with open('/tmp/sigsegv_debug.log', 'a') as f:
            f.write(f"[{level.upper()}] {msg}\n")
            f.flush()
    except:
        pass

