import asyncio
import os
import sys
import argparse
import logging
import threading
from typing import Optional
from src.config import settings
from src.security import load_credentials, clear_credentials
from src.agent import AgentWorker
from src.ui import ModernAgentUI

def setup_logging(debug: bool = False):
    level = logging.DEBUG if debug else logging.WARNING
    logging.basicConfig(level=level, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", handlers=[logging.StreamHandler(sys.stdout)])

def setup_sys_path():
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
        sys.path.insert(0, base_path)
                                                                                       
        sys.path.insert(0, os.path.join(base_path, 'src', 'backend'))
        sys.path.insert(0, os.path.join(base_path, 'backend'))
    else:
                          
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
                           
        sys.path.insert(0, os.path.join(current_dir))
                                       
        sys.path.insert(0, os.path.abspath(os.path.join(project_root, '..')))
        sys.path.insert(0, os.path.abspath(os.path.join(project_root, '..', 'backend')))

setup_sys_path()

try:
    from backend.operator_use.computer.windows.desktop.service import Desktop
    from backend.operator_use.computer.tools.windows import computer
except ImportError:
    from operator_use.computer.windows.desktop.service import Desktop
    from operator_use.computer.tools.windows import computer

def main():
    parser = argparse.ArgumentParser(description="Terminal Agent Worker")
    parser.add_argument("--clear", action="store_true", help="Clear saved credentials and exit")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()
    setup_logging(args.debug)
    if args.clear:
        clear_credentials()
        sys.exit(0)
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    desktop_instance = Desktop(use_vision=False, use_annotation=False, use_accessibility=True)
    agent = AgentWorker(desktop_instance, computer)
    app = ModernAgentUI(agent)
    app.mainloop()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
