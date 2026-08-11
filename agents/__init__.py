"""
Agents package for AI Employee Platform
"""

from .product_manager import ProductManagerAgent
from .architect import ArchitectAgent
from .database_engineer import DatabaseEngineerAgent
from .backend_engineer import BackendEngineerAgent
from .frontend_engineer import FrontendEngineerAgent
from .documentation import DocumentationAgent
from .qa import QAAgent
from .devops import DevOpsAgent
from .marketing import MarketingAgent
from .ceo import CEOAgent
from .ui_ux import UIUXAgent

__all__ = [
    "CEOAgent",
    "ProductManagerAgent",
    "ArchitectAgent",
    "BackendEngineerAgent",
    "FrontendEngineerAgent",
    "DatabaseEngineerAgent",
    "DocumentationAgent",
    "QAAgent",
    "DevOpsAgent",
    "MarketingAgent",
    "UIUXAgent",
]
