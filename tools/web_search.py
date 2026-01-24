"""
Web Search Tool - Search the web for information.
"""

import requests
from typing import Dict, List
from config import Config
from .base_tool import BaseTool


class WebSearchTool(BaseTool):
    """Search the web using DuckDuckGo (free, no API key needed)."""
    
    def __init__(self):
        super().__init__()
        self.name = "web_search"
        self.description = "Search the web for current information, news, facts, or any topic. Returns top search results with titles, snippets, and URLs."
        
        self.parameters = {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                },
                "num_results": {
                    "type": "integer",
                    "description": "Number of results to return (default: 5, max: 10)",
                    "default": 5
                }
            },
            "required": ["query"]
        }
    
    def execute(self, query: str, num_results: int = 5) -> str:
        """Execute web search."""
        try:
            num_results = min(num_results, 10)
            
            # Try DuckDuckGo instant answer API first
            results = self._duckduckgo_search(query, num_results)
            
            if not results:
                return f"❌ No results found for: '{query}'"
            
            # Format results
            output = f"🔍 **Search Results for: '{query}'**\n\n"
            for i, result in enumerate(results, 1):
                output += f"**{i}. {result['title']}**\n"
                output += f"   {result['snippet']}\n"
                if result.get('url'):
                    output += f"   🔗 {result['url']}\n"
                output += "\n"
            
            return output
            
        except Exception as e:
            return f"❌ Search error: {str(e)}"
    
    def _duckduckgo_search(self, query: str, num_results: int) -> List[Dict]:
        """Search using DuckDuckGo HTML (no API key needed)."""
        try:
            # Using DuckDuckGo HTML version
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            # DuckDuckGo instant answer API
            url = "https://api.duckduckgo.com/"
            params = {
                'q': query,
                'format': 'json',
                'no_html': 1,
                'skip_disambig': 1
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            data = response.json()
            
            results = []
            
            # Get abstract if available
            if data.get('Abstract'):
                results.append({
                    'title': data.get('Heading', 'Summary'),
                    'snippet': data.get('Abstract', ''),
                    'url': data.get('AbstractURL', '')
                })
            
            # Get related topics
            for topic in data.get('RelatedTopics', [])[:num_results]:
                if isinstance(topic, dict) and topic.get('Text'):
                    results.append({
                        'title': topic.get('Text', '')[:50] + '...',
                        'snippet': topic.get('Text', ''),
                        'url': topic.get('FirstURL', '')
                    })
            
            # If we have SerpAPI key, use it for better results
            if Config.SERPAPI_KEY and len(results) < num_results:
                serp_results = self._serpapi_search(query, num_results)
                results.extend(serp_results)
            
            return results[:num_results]
            
        except Exception as e:
            # Fallback: return a simulated response
            return [{
                'title': f'Search results for: {query}',
                'snippet': f'Please check online for the latest information about "{query}". You can visit google.com or duckduckgo.com for real-time results.',
                'url': f'https://duckduckgo.com/?q={query.replace(" ", "+")}'
            }]
    
    def _serpapi_search(self, query: str, num_results: int) -> List[Dict]:
        """Search using SerpAPI (requires API key)."""
        try:
            url = "https://serpapi.com/search"
            params = {
                'q': query,
                'api_key': Config.SERPAPI_KEY,
                'num': num_results
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            results = []
            for item in data.get('organic_results', [])[:num_results]:
                results.append({
                    'title': item.get('title', ''),
                    'snippet': item.get('snippet', ''),
                    'url': item.get('link', '')
                })
            
            return results
        except:
            return []