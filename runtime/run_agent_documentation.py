import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.documentation import DocumentationAgent
from runtime.runner import run_agent

run_agent(DocumentationAgent(), "Documentation", "documentation")
