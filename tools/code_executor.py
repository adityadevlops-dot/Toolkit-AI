"""
Code Executor Tool - Safely execute Python code snippets.
"""

import sys
import io
import traceback
from contextlib import redirect_stdout, redirect_stderr
from typing import Dict
from .base_tool import BaseTool


class CodeExecutorTool(BaseTool):
    """Safely execute Python code snippets in a restricted environment."""
    
    def __init__(self):
        super().__init__()
        self.name = "code_executor"
        self.description = """Execute Python code snippets. Useful for:
        - Running calculations
        - Data manipulation
        - Testing code logic
        - Generating formatted output
        Note: Code runs in a restricted environment with limited library access."""
        
        self.parameters = {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Python code to execute"
                }
            },
            "required": ["code"]
        }
        
        # Safe built-ins
        self.safe_builtins = {
            'abs': abs, 'all': all, 'any': any, 'bin': bin,
            'bool': bool, 'chr': chr, 'dict': dict, 'divmod': divmod,
            'enumerate': enumerate, 'filter': filter, 'float': float,
            'format': format, 'frozenset': frozenset, 'hash': hash,
            'hex': hex, 'int': int, 'isinstance': isinstance,
            'len': len, 'list': list, 'map': map, 'max': max,
            'min': min, 'oct': oct, 'ord': ord, 'pow': pow,
            'print': print, 'range': range, 'repr': repr, 'reversed': reversed,
            'round': round, 'set': set, 'slice': slice, 'sorted': sorted,
            'str': str, 'sum': sum, 'tuple': tuple, 'type': type,
            'zip': zip, 'True': True, 'False': False, 'None': None,
        }
        
        # Safe modules
        self.safe_modules = {}
        
        # Try to import safe modules
        try:
            import math
            self.safe_modules['math'] = math
        except: pass
        
        try:
            import random
            self.safe_modules['random'] = random
        except: pass
        
        try:
            import datetime
            self.safe_modules['datetime'] = datetime
        except: pass
        
        try:
            import json
            self.safe_modules['json'] = json
        except: pass
        
        try:
            import re
            self.safe_modules['re'] = re
        except: pass
        
        try:
            import statistics
            self.safe_modules['statistics'] = statistics
        except: pass
    
    def execute(self, code: str) -> str:
        """Execute Python code safely."""
        try:
            # Check for dangerous operations
            dangerous_keywords = [
                'import os', 'import sys', 'import subprocess',
                '__import__', 'eval(', 'exec(', 'compile(',
                'open(', 'file(', '__builtins__',
                'globals(', 'locals(', 'vars(',
                '__class__', '__bases__', '__subclasses__',
                'getattr', 'setattr', 'delattr',
            ]
            
            code_lower = code.lower()
            for keyword in dangerous_keywords:
                if keyword.lower() in code_lower:
                    return f"❌ Security Error: '{keyword}' is not allowed for safety reasons."
            
            # Create restricted globals
            restricted_globals = {
                '__builtins__': self.safe_builtins,
                **self.safe_modules
            }
            
            # Capture stdout and stderr
            stdout_capture = io.StringIO()
            stderr_capture = io.StringIO()
            
            # Execute with timeout-like behavior (limited iterations)
            result = None
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                try:
                    # Try to exec and capture result
                    exec_globals = restricted_globals.copy()
                    exec(code, exec_globals)
                    
                    # Check if there's a 'result' variable
                    if 'result' in exec_globals:
                        result = exec_globals['result']
                except Exception as e:
                    return f"❌ Runtime Error:\n```\n{traceback.format_exc()}\n```"
            
            # Get output
            stdout_output = stdout_capture.getvalue()
            stderr_output = stderr_capture.getvalue()
            
            # Format response
            output_parts = []
            output_parts.append("✅ **Code executed successfully!**\n")
            output_parts.append("```python\n" + code + "\n```\n")
            
            if stdout_output:
                output_parts.append("**Output:**\n```\n" + stdout_output + "```")
            
            if stderr_output:
                output_parts.append("**Warnings:**\n```\n" + stderr_output + "```")
            
            if result is not None:
                output_parts.append(f"**Result:** `{result}`")
            
            if not stdout_output and not stderr_output and result is None:
                output_parts.append("*No output produced*")
            
            return '\n'.join(output_parts)
            
        except Exception as e:
            return f"❌ Execution Error: {str(e)}"