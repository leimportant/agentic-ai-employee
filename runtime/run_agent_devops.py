import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.devops import DevOpsAgent
from runtime.runner import run_agent

run_agent(DevOpsAgent(), "DevOps Engineer", "devops")
