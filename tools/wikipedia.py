"""
Wikipedia Tool - Search and retrieve Wikipedia articles.
"""

import requests
from typing import Dict
from .base_tool import BaseTool


class WikipediaTool(BaseTool):
    """Search and retrieve information from Wikipedia."""
    
    def __init__(self):
        super().__init__()
        self.name = "wikipedia"
        self.description = "Search Wikipedia for detailed information about any topic. Returns article summary or full content."
        
        self.parameters = {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The topic to search for on Wikipedia"
                },
                "sentences": {
                    "type": "integer",
                    "description": "Number of sentences to return (default: 5, max: 20)",
                    "default": 5
                }
            },
            "required": ["query"]
        }
    
    def execute(self, query: str, sentences: int = 5) -> str:
        """Search Wikipedia and return results."""
        try:
            sentences = min(max(sentences, 1), 20)
            
            # Use Wikipedia API directly (no library needed)
            result = self._search_wikipedia(query, sentences)
            
            return result
            
        except Exception as e:
            return f"❌ Wikipedia error: {str(e)}"
    
    def _search_wikipedia(self, query: str, sentences: int) -> str:
        """Search Wikipedia using the MediaWiki API."""
        try:
            # First, search for the page
            search_url = "https://en.wikipedia.org/w/api.php"
            search_params = {
                'action': 'query',
                'list': 'search',
                'srsearch': query,
                'format': 'json',
                'srlimit': 1
            }
            
            response = requests.get(search_url, params=search_params, timeout=10)
            data = response.json()
            
            if not data['query']['search']:
                return f"❌ No Wikipedia article found for: '{query}'"
            
            # Get the page title
            page_title = data['query']['search'][0]['title']
            
            # Get the summary
            summary_url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + page_title.replace(' ', '_')
            
            response = requests.get(summary_url, timeout=10)
            summary_data = response.json()
            
            if 'extract' not in summary_data:
                return f"❌ Could not retrieve content for: '{query}'"
            
            # Get full extract and limit sentences
            full_extract = summary_data.get('extract', '')
            
            # Split into sentences and limit
            import re
            sentence_list = re.split(r'(?<=[.!?])\s+', full_extract)
            limited_extract = ' '.join(sentence_list[:sentences])
            
            # Format output
            output = f"""📚 **Wikipedia: {summary_data.get('title', page_title)}**

{limited_extract}

🔗 **Read more:** {summary_data.get('content_urls', {}).get('desktop', {}).get('page', f'https://en.wikipedia.org/wiki/{page_title.replace(" ", "_")}')}"""
            
            return output
            
        except Exception as e:
            # Try fallback with wikipedia library
            try:
                import wikipedia
                wikipedia.set_lang('en')
                
                page = wikipedia.page(query)
                summary = wikipedia.summary(query, sentences=sentences)
                
                return f"""📚 **Wikipedia: {page.title}**

{summary}

🔗 **Read more:** {page.url}"""
            except:
                return f"❌ Could not find Wikipedia article for: '{query}'"