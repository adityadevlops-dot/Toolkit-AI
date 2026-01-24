"""
Code Generator Tool - Generate code from natural language descriptions using AI Pipe.

Powered by AI Pipe for intelligent, context-aware code generation.
"""

from .ai_tool import BaseAITool


class CodeGeneratorTool(BaseAITool):
    """Generate code from natural language descriptions using AI Pipe."""
    
    def __init__(self):
        super().__init__()
        self.name = "code_generator"
        self.description = "Generate code snippets from natural language descriptions using AI Pipe. Supports Python, JavaScript, HTML, CSS, SQL, Java, C++, and more."
        
        self.parameters = {
            "type": "object",
            "properties": {
                "description": {
                    "type": "string",
                    "description": "Natural language description of what the code should do"
                },
                "language": {
                    "type": "string",
                    "enum": ["python", "javascript", "html", "css", "sql", "bash", "java", "cpp", "go", "rust"],
                    "description": "Programming language",
                    "default": "python"
                },
                "style": {
                    "type": "string",
                    "enum": ["simple", "documented", "production"],
                    "description": "Code style (simple, documented, or production-ready)",
                    "default": "documented"
                }
            },
            "required": ["description"]
        }
    
    def system_prompt(self) -> str:
        """System prompt for code generation."""
        return (
            "You are an expert programmer with deep knowledge of all major programming languages. "
            "Generate clean, efficient, and well-structured code based on the user's description. "
            "Follow best practices for the target language. "
            "Only output the code block, wrapped in ```language``` markers. "
            "Include error handling and comments where appropriate."
        )
    
    def build_prompt(self, description: str, language: str = "python", style: str = "documented", **kwargs) -> str:
        """Build prompt for code generation."""
        style_guide = {
            "simple": "Write simple, minimal code that works correctly.",
            "documented": "Write well-commented code with docstrings.",
            "production": "Write production-ready code with comprehensive error handling, logging, and best practices."
        }
        
        style_desc = style_guide.get(style, style_guide["documented"])
        
        prompt = f"""Generate {language.upper()} code that: {description}

Style: {style_desc}

Wrap the code in ```{language}``` markers."""
        
        return prompt
    
    def parse_response(self, response: str) -> str:
        """Extract and format the code from response."""
        # Extract code from markdown blocks if present
        code_block = response
        
        if "```" in response:
            parts = response.split("```")
            if len(parts) >= 2:
                code_block = parts[1]
                if code_block.startswith(("python", "javascript", "html", "css", "sql", "bash", "java", "cpp", "go", "rust")):
                    code_block = code_block.split("\n", 1)[1] if "\n" in code_block else code_block
        
        return f"""💻 **Generated Code**

```
{code_block.strip()}
```

---
Generated using AI Pipe API"""