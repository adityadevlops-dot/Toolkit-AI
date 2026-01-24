"""
AIPipeClient - Production-ready wrapper for AI Pipe API integration.

Handles:
- Environment variable management (AIPIPE_API_KEY from environment)
- Prompt structuring and formatting
- Response parsing and validation
- Error handling and retries with exponential backoff
- Token tracking per call
- Seamless integration with LLMClient
"""

import os
import time
from typing import Dict, Optional, List
from config import Config
from agent.llm_client import LLMClient


class AIPipeClient:
    """Production-ready AI Pipe API client wrapper.
    
    This client provides a clean interface for tools to call AI Pipe without
    worrying about API key management, error handling, or retry logic.
    
    Key features:
    - Environment variable loading (AIPIPE_API_KEY - NO HARDCODING)
    - Automatic retry with exponential backoff
    - Token usage tracking
    - Structured error messages
    - Simple call interface
    """
    
    def __init__(self, model: Optional[str] = None, api_key: Optional[str] = None):
        """Initialize the AI Pipe client.
        
        Args:
            model: Optional model override. If not provided, uses Config.DEFAULT_MODEL
            api_key: Optional API key override. If not provided, reads from AIPIPE_API_KEY
                    environment variable via Config
                    
        Raises:
            ValueError: If AIPIPE_API_KEY environment variable is not set
        """
        # Load API key from environment variable (via Config)
        self.api_key = api_key or Config.AIPIPE_API_KEY
        if not self.api_key:
            raise ValueError(
                "❌ AI Pipe API Key Required!\n\n"
                "Set environment variable: AIPIPE_API_KEY=your_token\n"
                "Or add to .env file: AIPIPE_API_KEY=your_token\n"
                "Get token from: https://aipipe.org/login"
            )
        
        self.model = model or Config.DEFAULT_MODEL
        self.base_url = Config.AIPIPE_BASE_URL
        self.max_tokens = Config.MAX_TOKENS
        self.temperature = Config.TEMPERATURE
        
        # Initialize underlying LLM client
        self._llm_client = LLMClient(
            api_key=self.api_key,
            base_url=self.base_url
        )
        self._llm_client.set_model(self.model)
        
        # Usage tracking
        self._usage_stats = {
            "total_calls": 0,
            "total_tokens": 0,
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "last_usage": None
        }
    
    def call(
        self,
        system_prompt: str,
        user_message: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        retry_count: int = 3
    ) -> Dict[str, any]:
        """Call AI Pipe with structured prompt.
        
        This is the main method for tools to use AI Pipe. It handles:
        - Message formatting (system + user)
        - Temperature/token customization
        - Automatic retries on failure
        - Token usage tracking
        
        Args:
            system_prompt: System instruction for the AI
            user_message: User query/prompt
            temperature: Optional temperature override (0.0-2.0)
            max_tokens: Optional max tokens override
            retry_count: Number of retries on failure (default: 3)
            
        Returns:
            Dict with keys:
                - "content": str - The AI's response
                - "tokens_used": int - Tokens in this call
                - "total_tokens": int - Total tokens so far
                - "finish_reason": str - Why generation stopped
                - "model": str - Model used
                
        Raises:
            ValueError: If API key is missing
            Exception: If all retries fail
        """
        # Set temperature if provided
        if temperature is not None:
            self._llm_client.set_temperature(temperature)
        else:
            self._llm_client.set_temperature(self.temperature)
        
        # Set max tokens if provided
        if max_tokens is not None:
            self._llm_client.max_tokens = max_tokens
        else:
            self._llm_client.max_tokens = self.max_tokens
        
        # Format messages
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        # Call with retries
        last_error = None
        for attempt in range(retry_count):
            try:
                response = self._llm_client.chat(messages, retry_count=1)
                
                # Track usage
                self._usage_stats["total_calls"] += 1
                if response.get("usage"):
                    usage = response["usage"]
                    self._usage_stats["total_tokens"] += usage.get("total_tokens", 0)
                    self._usage_stats["total_input_tokens"] += usage.get("prompt_tokens", 0)
                    self._usage_stats["total_output_tokens"] += usage.get("completion_tokens", 0)
                    self._usage_stats["last_usage"] = usage
                
                return {
                    "content": response.get("content", ""),
                    "tokens_used": response.get("usage", {}).get("total_tokens", 0),
                    "total_tokens": self._usage_stats["total_tokens"],
                    "finish_reason": response.get("finish_reason", "stop"),
                    "model": self.model
                }
                
            except Exception as e:
                last_error = e
                error_str = str(e).lower()
                
                # Retry on rate limit
                if "rate" in error_str or "limit" in error_str:
                    if attempt < retry_count - 1:
                        wait_time = 2 ** attempt
                        if Config.VERBOSE:
                            print(f"⚠️  Rate limited. Retrying in {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                
                # Retry on connection error
                elif "connection" in error_str:
                    if attempt < retry_count - 1:
                        if Config.VERBOSE:
                            print(f"⚠️  Connection error. Retrying ({attempt + 1}/{retry_count})...")
                        time.sleep(1)
                        continue
                
                # Don't retry on auth/model errors
                elif "unauthorized" in error_str or "invalid" in error_str or "model" in error_str:
                    raise
                
                # Retry on other errors
                if attempt < retry_count - 1:
                    time.sleep(1)
                    continue
        
        # All retries exhausted
        raise Exception(
            f"❌ AI Pipe call failed after {retry_count} attempts.\n"
            f"Last error: {last_error}"
        )
    
    def get_usage_stats(self) -> Dict:
        """Get token usage statistics.
        
        Returns:
            Dict with:
                - total_calls: Number of API calls made
                - total_tokens: Total tokens used (input + output)
                - total_input_tokens: Input tokens
                - total_output_tokens: Output tokens
                - last_usage: Last call's usage info
        """
        return self._usage_stats.copy()
    
    def reset_usage_stats(self):
        """Reset usage statistics."""
        self._usage_stats = {
            "total_calls": 0,
            "total_tokens": 0,
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "last_usage": None
        }
    
    def set_model(self, model: str):
        """Change the model.
        
        Args:
            model: Model identifier (e.g., 'gpt-4o-mini', 'gpt-4o')
        """
        self.model = model
        self._llm_client.set_model(model)
    
    def set_temperature(self, temperature: float):
        """Set default temperature (0.0-2.0).
        
        Args:
            temperature: Temperature value
        """
        self.temperature = max(0.0, min(2.0, temperature))
        self._llm_client.set_temperature(self.temperature)
    
    def test_connection(self) -> bool:
        """Test if the API connection works.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            result = self.call(
                system_prompt="Say 'OK' and nothing else.",
                user_message="Test"
            )
            return result["content"].strip().upper() == "OK"
        except Exception as e:
            if Config.VERBOSE:
                print(f"Connection test failed: {e}")
            return False
