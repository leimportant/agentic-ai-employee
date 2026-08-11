import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.product_manager import ProductManagerAgent
from runtime.runner import run_agent

run_agent(ProductManagerAgent(), "Product Manager", "prd")
