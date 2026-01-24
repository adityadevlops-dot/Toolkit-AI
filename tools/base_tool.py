"""
Base Tool class - All tools must inherit from this.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel


class BaseTool(ABC):
    """Abstract base class for all tools.
    
    All tools must:
    1. Inherit from BaseTool
    2. Set self.name, self.description, and self.parameters in __init__
    3. Implement execute() method with proper error handling
    """
    
    def __init__(self):
        """Initialize the base tool. Subclasses should override and set: name, description, parameters."""
        self.name: str = "base_tool"
        self.description: str = "Base tool description"
        self.parameters: Dict = {
            "type": "object",
            "properties": {},
            "required": []
        }
    
    @abstractmethod
    def execute(self, **kwargs) -> str:
        """Execute the tool with given parameters. Must be implemented by subclasses.
        
        Args:
            **kwargs: Tool-specific parameters
            
        Returns:
            str: Result of the tool execution or error message
        """
        pass
    
    def get_schema(self) -> Dict:
        """Get OpenAI function schema for this tool.
        
        Returns:
            Dict: Tool schema compatible with OpenAI function calling API
        """
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }
    
    def __repr__(self) -> str:
        """String representation of the tool."""
        return f"<Tool: {self.name}>"