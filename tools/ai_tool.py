"""
Base AI Tool class - Foundation for all AI-powered tools using AI Pipe.

This module provides BaseAITool, an abstract base class that integrates AI Pipe
for tools requiring language model capabilities. It handles:
- API client management and lifecycle
- Prompt templating and formatting
- Response parsing and validation
- Error handling and retries
- Token usage tracking
"""

from abc import abstractmethod
from typing import Dict, Optional, List, Any
from agent.aipipe_client import AIPipeClient
from config import Config
from .base_tool import BaseTool


class BaseAITool(BaseTool):
    """Abstract base class for AI-powered tools using AI Pipe.
    
    Extends BaseTool to provide AI Pipe integration for tools that need
    language model capabilities. Subclasses should:
    
    1. Set name, description, and parameters in __init__
    2. Optionally customize system_prompt()
    3. Implement build_prompt() to format user input into a prompt
    4. Implement parse_response() to process AI output (optional, defaults to raw response)
    5. Optionally override execute() if complex orchestration is needed
    
    Example:
        class MyAITool(BaseAITool):
            def __init__(self):
                super().__init__()
                self.name = "my_tool"
                self.description = "Does something with AI"
                self.parameters = {...}
            
            def system_prompt(self) -> str:
                return "You are an expert at..."
            
            def build_prompt(self, **kwargs) -> str:
                return f"User wants: {kwargs.get('input', '')}"
            
            def parse_response(self, response: str) -> str:
                return response.strip()  # Optional post-processing
    """
    
    def __init__(self, model: Optional[str] = None):
        """Initialize the AI tool.
        
        Args:
            model: Optional model override. If not provided, uses Config.DEFAULT_MODEL
        """
        super().__init__()
        self.model = model or Config.DEFAULT_MODEL
        self._aipipe_client = None
        self._total_tokens_used = 0
    
    @property
    def aipipe_client(self) -> AIPipeClient:
        """Lazy-load and cache AI Pipe client.
        
        Initializes the client on first access. API key is loaded from
        AIPIPE_API_KEY environment variable (no hardcoding).
        
        Returns:
            AIPipeClient: Initialized AI Pipe client
            
        Raises:
            ValueError: If AIPIPE_API_KEY environment variable is not set
        """
        if self._aipipe_client is None:
            self._aipipe_client = AIPipeClient(model=self.model)
        return self._aipipe_client
    
    def system_prompt(self) -> str:
        """Get the system prompt for this tool.
        
        Override this method to customize the AI's behavior and instructions.
        
        Returns:
            str: System prompt that provides context and instructions
        """
        return (
            "You are a helpful AI assistant. Provide clear, concise, and accurate responses. "
            "Format your output for clarity and usability."
        )
    
    @abstractmethod
    def build_prompt(self, **kwargs) -> str:
        """Build the user prompt from tool parameters.
        
        This method must be implemented by subclasses to format user input
        into a prompt suitable for the AI model.
        
        Args:
            **kwargs: Tool-specific parameters from execute()
            
        Returns:
            str: Formatted prompt for the AI model
        """
        pass
    
    def parse_response(self, response: str) -> str:
        """Parse and format the AI response (optional).
        
        Override this method to process AI output before returning.
        Default implementation returns response as-is.
        
        Args:
            response: Raw response from AI Pipe API
            
        Returns:
            str: Processed response ready for user/tool output
        """
        return response
    
    def execute(self, **kwargs) -> str:
        """Execute the AI tool.
        
        This method orchestrates the tool:
        1. Validates parameters
        2. Builds a prompt from parameters
        3. Sends to AI Pipe API with system prompt
        4. Parses the response
        5. Handles errors gracefully with detailed messages
        
        Args:
            **kwargs: Tool-specific parameters defined in self.parameters
            
        Returns:
            str: Tool result or detailed error message
        """
        try:
            # Validate parameters
            self._validate_parameters(**kwargs)
            
            # Build the prompt
            user_prompt = self.build_prompt(**kwargs)
            
            # Get system prompt
            sys_prompt = self.system_prompt()
            
            # Call AI Pipe via production client
            result = self._call_ai_pipe(user_prompt, sys_prompt)
            
            # Parse response
            parsed_response = self.parse_response(result)
            
            return parsed_response
            
        except ValueError as e:
            # Parameter validation failed
            return f"❌ Invalid input: {str(e)}"
        except Exception as e:
            # API or processing error
            error_msg = str(e)
            if "Token Required" in error_msg or "Token" in error_msg:
                return "❌ AI Pipe API key not configured. Set AIPIPE_API_KEY environment variable. See SETUP_GUIDE.md"
            return f"❌ Error: {error_msg}"
    
    def _call_ai_pipe(self, user_prompt: str, system_prompt: str) -> str:
        """Call AI Pipe API with error handling and token tracking.
        
        Args:
            user_prompt: The user message/prompt
            system_prompt: The system instruction
            
        Returns:
            str: AI response
            
        Raises:
            Exception: On API errors
        """
        try:
            response = self.aipipe_client.call(
                system_prompt=system_prompt,
                user_message=user_prompt
            )
            
            # Track token usage
            tokens_used = response.get("tokens_used", 0)
            self._total_tokens_used += tokens_used
            
            if Config.VERBOSE:
                print(f"  ✓ {self.name}: {tokens_used} tokens used (total: {self._total_tokens_used})")
            
            return response.get("content", "")
            
        except Exception as e:
            raise Exception(f"AI Pipe API error: {str(e)}")
    
    def _validate_parameters(self, **kwargs) -> None:
        """Validate that required parameters are provided.
        
        Checks that all required parameters from self.parameters are present in kwargs.
        
        Args:
            **kwargs: Parameters to validate
            
        Raises:
            ValueError: If required parameters are missing
        """
        required = self.parameters.get("required", [])
        for param in required:
            if param not in kwargs or kwargs[param] is None:
                raise ValueError(f"Missing required parameter: {param}")
            # Check for empty strings where that's not allowed
            if isinstance(kwargs[param], str) and not kwargs[param].strip():
                raise ValueError(f"Parameter '{param}' cannot be empty")
    
    def get_token_usage(self) -> int:
        """Get total tokens used by this tool.
        
        Returns:
            int: Total tokens sent to and received from AI Pipe API
        """
        return self._total_tokens_used
    
    def reset_token_usage(self):
        """Reset token usage counter."""
        self._total_tokens_used = 0
    
    def set_model(self, model: str):
        """Change the model for this tool.
        
        Args:
            model: Model identifier (e.g., 'gpt-4o-mini', 'gpt-4o')
        """
        self.model = model
        if self._aipipe_client:
            self._aipipe_client.set_model(model)
    
    def set_temperature(self, temperature: float):
        """Set temperature for this tool's API calls.
        
        Higher values (0.0-2.0) make output more creative/random.
        Lower values make output more deterministic.
        
        Args:
            temperature: Temperature value between 0.0 and 2.0
        """
        if self._aipipe_client:
            self._aipipe_client.set_temperature(temperature)
