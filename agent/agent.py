"""
Multi-Tool LLM Agent - Core agent logic.
"""

import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime

from .llm_client import LLMClient
from tools import get_all_tools, get_tool_by_name, BaseTool
from config import Config


class MultiToolAgent:
    """
    An intelligent agent that can use multiple tools to answer questions.
    
    The agent follows a ReAct-style approach:
    1. Reason about the query
    2. Choose appropriate tools
    3. Execute tools
    4. Synthesize final response
    """
    
    SYSTEM_PROMPT = """You are a helpful AI assistant with access to various tools. 
Your goal is to help users by using the most appropriate tools when needed.

Guidelines:
1. Use tools when you need current information, calculations, or specific data
2. You can use multiple tools in sequence to answer complex questions
3. Always provide clear, well-formatted responses
4. If a tool fails, explain what happened and try an alternative approach
5. Be conversational and helpful

Current date: {current_date}

Available tools:
{tool_descriptions}
"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the multi-tool agent.
        
        Args:
            api_key: Optional API key for the LLM. If not provided, uses Config.AIPIPE_API_KEY
            
        Raises:
            ValueError: If API key is not available or invalid
        """
        self.llm = LLMClient(api_key=api_key)
        self.tools: Dict[str, BaseTool] = {}
        self.tool_schemas: List[Dict] = []
        self.conversation_history: List[Dict] = []
        self.max_iterations = Config.MAX_ITERATIONS
        self.verbose = Config.VERBOSE
        
        # Load all tools
        self._load_tools()
        
        # Initialize system prompt
        self._init_system_prompt()
    
    def _load_tools(self):
        """Load all available tools from the tools package.
        
        Initializes tool registry and generates OpenAI-compatible tool schemas.
        """
        for tool in get_all_tools():
            self.tools[tool.name] = tool
            self.tool_schemas.append(tool.get_schema())
        
        if self.verbose:
            print(f"✅ Loaded {len(self.tools)} tools: {list(self.tools.keys())}")
    
    def _init_system_prompt(self):
        """Initialize the system prompt with tool descriptions.
        
        Creates a context-aware system prompt that includes information about
        available tools and the current date.
        """
        tool_descriptions = "\n".join([
            f"- **{tool.name}**: {tool.description}"
            for tool in self.tools.values()
        ])
        
        self.system_prompt = self.SYSTEM_PROMPT.format(
            current_date=datetime.now().strftime("%Y-%m-%d"),
            tool_descriptions=tool_descriptions
        )
        
        # Add system message to history
        self.conversation_history = [
            {"role": "system", "content": self.system_prompt}
        ]
    
    def _execute_tool(self, tool_name: str, arguments: Dict) -> str:
        """Execute a tool with given arguments and return result.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Dictionary of arguments to pass to the tool
            
        Returns:
            str: Tool execution result or error message
        """
        if tool_name not in self.tools:
            return f"❌ Unknown tool: {tool_name}"
        
        tool = self.tools[tool_name]
        
        if self.verbose:
            print(f"🔧 Executing tool: {tool_name}")
            print(f"   Arguments: {arguments}")
        
        try:
            result = tool.execute(**arguments)
            if self.verbose:
                print(f"   Result: {result[:200]}..." if len(result) > 200 else f"   Result: {result}")
            return result
        except Exception as e:
            error_msg = f"❌ Tool error ({tool_name}): {str(e)}"
            if self.verbose:
                print(f"   Error: {e}")
            return error_msg
    
    def process_query(self, query: str) -> Tuple[str, List[Dict]]:
        """Process a user query using tools and return the response.
        
        Implements a ReAct-style loop:
        1. Send query to LLM with available tools
        2. If LLM suggests tools, execute them
        3. Add results to conversation history
        4. Repeat until LLM provides final response or max iterations reached
        
        Args:
            query: User's question or request
            
        Returns:
            Tuple of (response_text, list_of_tool_calls_made)
        """
        tool_calls_made = []
        
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": query
        })
        
        # Iterative tool use loop
        for iteration in range(self.max_iterations):
            if self.verbose:
                print(f"\n--- Iteration {iteration + 1} ---")
            
            # Get LLM response
            try:
                response = self.llm.chat(
                    messages=self.conversation_history,
                    tools=self.tool_schemas if self.tool_schemas else None,
                    tool_choice="auto"
                )
            except Exception as e:
                error_response = f"I apologize, but I encountered an error: {str(e)}"
                return error_response, tool_calls_made
            
            # Check if we have tool calls
            if response["tool_calls"]:
                # Process each tool call
                assistant_message = {
                    "role": "assistant",
                    "content": response["content"],
                    "tool_calls": []
                }
                
                for tool_call in response["tool_calls"]:
                    tool_name = tool_call["name"]
                    arguments = tool_call["arguments"]
                    tool_id = tool_call["id"]
                    
                    # Execute the tool
                    result = self._execute_tool(tool_name, arguments)
                    
                    # Record the tool call
                    tool_calls_made.append({
                        "tool": tool_name,
                        "arguments": arguments,
                        "result": result
                    })
                    
                    # Add tool call to assistant message
                    assistant_message["tool_calls"].append({
                        "id": tool_id,
                        "type": "function",
                        "function": {
                            "name": tool_name,
                            "arguments": json.dumps(arguments)
                        }
                    })
                    
                    # Add tool result to history
                    self.conversation_history.append(assistant_message)
                    self.conversation_history.append({
                        "role": "tool",
                        "tool_call_id": tool_id,
                        "content": result
                    })
                
            else:
                # No tool calls, we have our final response
                final_response = response["content"] or "I'm not sure how to help with that."
                
                # Add assistant response to history
                self.conversation_history.append({
                    "role": "assistant",
                    "content": final_response
                })
                
                return final_response, tool_calls_made
        
        # Max iterations reached
        return "I've made several attempts but couldn't complete the task. Please try rephrasing your question.", tool_calls_made
    
    def chat(self, query: str) -> str:
        """Simple chat interface - returns just the response text.
        
        Args:
            query: User's question or request
            
        Returns:
            Response text from the agent
        """
        response, _ = self.process_query(query)
        return response
    
    def clear_history(self):
        """Clear conversation history (keeps system prompt).
        
        Useful for starting fresh conversations while maintaining the agent's context.
        """
        self._init_system_prompt()
    
    def get_conversation_history(self) -> List[Dict]:
        """Get the conversation history (excluding system prompt).
        
        Returns:
            List of messages in the conversation
        """
        return self.conversation_history[1:]  # Exclude system prompt
    
    def add_tool(self, tool: BaseTool):
        """Add a new tool to the agent dynamically.
        
        Args:
            tool: BaseTool instance to add
        """
        self.tools[tool.name] = tool
        self.tool_schemas.append(tool.get_schema())
        self._init_system_prompt()  # Update system prompt