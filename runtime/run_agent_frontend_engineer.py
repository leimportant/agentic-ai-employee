import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.frontend_engineer import FrontendEngineerAgent
from runtime.runner import run_agent

run_agent(FrontendEngineerAgent(), "Frontend Engineer", "frontend")
