"""
URL Reader Tool - Read and extract content from web pages.
"""

import requests
from typing import Dict
from bs4 import BeautifulSoup
from .base_tool import BaseTool


class URLReaderTool(BaseTool):
    """Read and extract content from web pages."""
    
    def __init__(self):
        super().__init__()
        self.name = "url_reader"
        self.description = "Read and extract content from any web page URL. Returns the main text content of the page."
        
        self.parameters = {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL of the web page to read"
                },
                "max_length": {
                    "type": "integer",
                    "description": "Maximum characters to return (default: 5000)",
                    "default": 5000
                }
            },
            "required": ["url"]
        }
    
    def execute(self, url: str, max_length: int = 5000) -> str:
        """Read content from URL."""
        try:
            # Validate URL
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'form']):
                element.decompose()
            
            # Get page title
            title = soup.title.string if soup.title else "No title"
            
            # Extract main content
            # Try to find main content area
            main_content = None
            for selector in ['article', 'main', '.content', '#content', '.post', '.article']:
                main_content = soup.select_one(selector)
                if main_content:
                    break
            
            if main_content:
                text = main_content.get_text(separator='\n', strip=True)
            else:
                # Fallback to body
                body = soup.find('body')
                if body:
                    text = body.get_text(separator='\n', strip=True)
                else:
                    text = soup.get_text(separator='\n', strip=True)
            
            # Clean up text
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            text = '\n'.join(lines)
            
            # Truncate if necessary
            if len(text) > max_length:
                text = text[:max_length] + "\n\n... [Content truncated]"
            
            return f"""🌐 **Content from:** {url}
📰 **Title:** {title}

---

{text}"""
            
        except requests.exceptions.RequestException as e:
            return f"❌ Could not fetch URL: {str(e)}"
        except Exception as e:
            return f"❌ Error processing URL: {str(e)}"