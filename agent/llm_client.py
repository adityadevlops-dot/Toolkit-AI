"""
LLM Client for AI Pipe (aipipe.org)
"""

import json
import time
from typing import Dict, List, Optional
from openai import OpenAI
from config import Config


class LLMClient:
    """Client for AI Pipe API."""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """Initialize the AI Pipe client."""
        self.api_key = api_key or Config.AIPIPE_API_KEY
        self.base_url = base_url or Config.AIPIPE_BASE_URL
        self.model = Config.DEFAULT_MODEL
        self.max_tokens = Config.MAX_TOKENS
        self.temperature = Config.TEMPERATURE
        
        # Validate API key
        if not self.api_key:
            raise ValueError(
                "❌ AI Pipe Token Required!\n\n"
                "Get your token from: https://aipipe.org/login\n"
                "Then add to .env: AIPIPE_API_KEY=your_token"
            )
        
        # Initialize OpenAI-compatible client
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=60.0
        )
        
        # Detect if using OpenRouter
        self.is_openrouter = "openrouter" in self.base_url.lower()
        
        if Config.VERBOSE:
            print(f"✅ AI Pipe Client Initialized")
            print(f"   🌐 Endpoint: {self.base_url}")
            print(f"   🤖 Model: {self.model}")
            print(f"   📡 Provider: {'OpenRouter' if self.is_openrouter else 'OpenAI'}")
    
    def chat(
        self,
        messages: List[Dict],
        tools: Optional[List[Dict]] = None,
        tool_choice: str = "auto",
        retry_count: int = 3
    ) -> Dict:
        """Send chat request to AI Pipe."""
        
        last_error = None
        
        for attempt in range(retry_count):
            try:
                # Build request parameters
                params = {
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": self.max_tokens,
                    "temperature": self.temperature,
                }
                
                # Add tools if provided
                if tools:
                    params["tools"] = tools
                    params["tool_choice"] = tool_choice
                
                # Make API call
                response = self.client.chat.completions.create(**params)
                
                # Parse response
                choice = response.choices[0]
                message = choice.message
                
                result = {
                    "content": message.content,
                    "tool_calls": None,
                    "finish_reason": choice.finish_reason,
                    "usage": None
                }
                
                # Get usage info if available
                if hasattr(response, 'usage') and response.usage:
                    result["usage"] = {
                        "prompt_tokens": response.usage.prompt_tokens,
                        "completion_tokens": response.usage.completion_tokens,
                        "total_tokens": response.usage.total_tokens,
                    }
                
                # Handle tool calls
                if hasattr(message, 'tool_calls') and message.tool_calls:
                    result["tool_calls"] = []
                    for tool_call in message.tool_calls:
                        result["tool_calls"].append({
                            "id": tool_call.id,
                            "name": tool_call.function.name,
                            "arguments": json.loads(tool_call.function.arguments)
                        })
                
                return result
                
            except Exception as e:
                last_error = e
                error_str = str(e).lower()
                
                # Handle specific errors
                if "rate" in error_str or "limit" in error_str:
                    wait_time = 2 ** attempt
                    print(f"⚠️ Rate limited. Waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                    
                elif "connection" in error_str:
                    if attempt < retry_count - 1:
                        print(f"⚠️ Connection error. Retrying ({attempt + 1}/{retry_count})...")
                        time.sleep(2)
                        continue
                    else:
                        raise Exception(
                            f"❌ Cannot connect to AI Pipe!\n\n"
                            f"Please check:\n"
                            f"1. Your internet connection\n"
                            f"2. AI Pipe service status at https://aipipe.org/playground\n\n"
                            f"Error: {e}"
                        )
                
                elif "unauthorized" in error_str or "invalid" in error_str:
                    raise Exception(
                        f"❌ Invalid AI Pipe Token!\n\n"
                        f"Please get a new token from:\n"
                        f"https://aipipe.org/login\n\n"
                        f"Error: {e}"
                    )
                
                elif "model" in error_str:
                    raise Exception(
                        f"❌ Model '{self.model}' not available!\n\n"
                        f"Try changing DEFAULT_MODEL in .env to:\n"
                        f"- gpt-4o-mini\n"
                        f"- gpt-3.5-turbo\n"
                        f"- gpt-4o\n\n"
                        f"Error: {e}"
                    )
                
                elif "budget" in error_str or "quota" in error_str:
                    raise Exception(
                        f"❌ AI Pipe budget exceeded!\n\n"
                        f"Check your usage at: https://aipipe.org/login\n\n"
                        f"Error: {e}"
                    )
                
                # Unknown error - raise immediately
                raise Exception(f"❌ AI Pipe Error: {e}")
        
        # All retries failed
        raise Exception(f"❌ Failed after {retry_count} attempts.\nLast error: {last_error}")
    
    def simple_chat(self, prompt: str, system_message: str = None) -> str:
        """Simple chat without tools."""
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})
        
        response = self.chat(messages)
        return response["content"]
    
    def test_connection(self) -> bool:
        """Test the API connection."""
        try:
            response = self.simple_chat("Say 'OK'")
            return True
        except:
            return False
    
    def set_model(self, model: str):
        """Change the model."""
        self.model = model
    
    def set_temperature(self, temperature: float):
        """Set temperature (0.0 - 2.0)."""
        self.temperature = max(0.0, min(2.0, temperature))