"""
Text Summarizer Tool - Summarize long text into concise summaries using AI Pipe.

Powered by AI Pipe for abstractive and extractive summarization.

This tool demonstrates best practices for AI Pipe integration:
- Environment variable loading (no hardcoded keys)
- Clean prompt structuring
- Modular and production-ready
"""

from .ai_tool import BaseAITool


class TextSummarizerTool(BaseAITool):
    """Summarize long text into concise key points or paragraphs using AI Pipe.
    
    Features:
    - Flexible summary lengths (short, medium, long)
    - Multiple output formats (paragraph, bullet points, keywords)
    - Clean formatting with compression stats
    - Token-efficient with AI Pipe integration
    """
    
    def __init__(self):
        super().__init__()
        self.name = "text_summarizer"
        self.description = (
            "Summarize long text into concise bullet points, paragraphs, or keywords "
            "using AI Pipe for better semantic understanding."
        )
        
        self.parameters = {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Text to summarize"
                },
                "max_length": {
                    "type": "string",
                    "enum": ["short", "medium", "long"],
                    "description": "Summary length (default: medium)",
                    "default": "medium"
                },
                "style": {
                    "type": "string",
                    "enum": ["paragraph", "bullets", "keywords"],
                    "description": "Output style (default: paragraph)",
                    "default": "paragraph"
                }
            },
            "required": ["text"]
        }
    
    def system_prompt(self) -> str:
        """System prompt for text summarization.
        
        Returns:
            str: System instruction that guides the AI's summarization approach
        """
        return (
            "You are an expert summarizer. Your role is to create clear, concise, "
            "and accurate summaries of text. Follow these principles:\n\n"
            "1. Capture the most important information\n"
            "2. Remove redundancy and unnecessary details\n"
            "3. Maintain key points and context from the original text\n"
            "4. Be precise and avoid adding information not in the original\n"
            "5. Use simple, clear language\n"
            "6. Format output for easy reading"
        )
    
    def build_prompt(self, text: str, max_length: str = "medium", style: str = "paragraph", **kwargs) -> str:
        """Build the summarization prompt.
        
        This method formats the user input into a structured prompt that guides
        the AI to produce the desired summary format and length.
        
        Args:
            text: The text to summarize
            max_length: Desired summary length ('short', 'medium', or 'long')
            style: Output format ('paragraph', 'bullets', or 'keywords')
            **kwargs: Additional parameters (ignored)
            
        Returns:
            str: Formatted prompt for AI Pipe
        """
        # Define length guidelines
        length_guide = {
            "short": "2-3 sentences or 3-4 bullet points",
            "medium": "3-5 sentences or 5-7 bullet points",
            "long": "5-8 sentences or 8-10 bullet points"
        }
        
        length_desc = length_guide.get(max_length, length_guide["medium"])
        
        # Build style-specific prompt
        if style == "bullets":
            prompt = (
                f"Summarize this text into {length_desc} in bullet point format. "
                f"Each point should be concise and stand-alone.\n\n"
                f"TEXT:\n{text}"
            )
        elif style == "keywords":
            count = length_desc.split()[0]
            prompt = (
                f"Extract the {count} most important keywords or key phrases from "
                f"this text. Format as a comma-separated list.\n\n"
                f"TEXT:\n{text}"
            )
        else:  # paragraph (default)
            prompt = (
                f"Summarize this text in {length_desc}. "
                f"Write a cohesive paragraph that captures the essence.\n\n"
                f"TEXT:\n{text}"
            )
        
        return prompt
    
    def parse_response(self, response: str) -> str:
        """Parse and format the AI response with metadata.
        
        Adds formatting and summary statistics to the AI's response.
        
        Args:
            response: Raw response from AI Pipe
            
        Returns:
            str: Formatted response with statistics
        """
        # Clean response
        summary = response.strip()
        
        # Calculate compression ratio (approximate)
        original_words = 500  # Approximate average
        summary_words = len(summary.split())
        compression_ratio = int((summary_words / original_words) * 100) if original_words > 0 else 100
        
        # Format output with metadata
        formatted_output = f"""📝 **Summary**

{summary}

---
📊 **Summary Stats:** ~{summary_words} words ({compression_ratio}% of typical original)"""
        
        return formatted_output