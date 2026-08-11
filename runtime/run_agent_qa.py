import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.qa import QAAgent
from runtime.runner import run_agent

run_agent(QAAgent(), "QA Engineer", "qa_report")
