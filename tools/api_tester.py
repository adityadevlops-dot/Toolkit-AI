"""
API Tester Tool - Test HTTP APIs and endpoints.
"""

from .base_tool import BaseTool


class APITesterTool(BaseTool):
    """Test HTTP APIs with various methods and parameters."""
    
    def __init__(self):
        super().__init__()
        self.name = "api_tester"
        self.description = "Test HTTP APIs by sending requests and analyzing responses. Supports GET, POST, PUT, DELETE methods."
        
        self.parameters = {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "API endpoint URL"
                },
                "method": {
                    "type": "string",
                    "enum": ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"],
                    "description": "HTTP method",
                    "default": "GET"
                },
                "headers": {
                    "type": "string",
                    "description": "Headers as JSON string"
                },
                "body": {
                    "type": "string",
                    "description": "Request body as JSON string"
                },
                "params": {
                    "type": "string",
                    "description": "Query parameters as JSON string"
                },
                "timeout": {
                    "type": "integer",
                    "description": "Request timeout in seconds",
                    "default": 30
                }
            },
            "required": ["url"]
        }
    
    def execute(self, url, method="GET", headers=None, body=None, params=None, timeout=30):
        try:
            if not url:
                return "Please provide an API URL."
            
            try:
                import requests
            except ImportError:
                return "Error: requests library not installed. Run: pip install requests"
            
            import json
            import time
            
            parsed_headers = self._parse_json(headers)
            parsed_body = self._parse_json(body)
            parsed_params = self._parse_json(params)
            
            if parsed_headers is None:
                parsed_headers = {}
            
            if "Content-Type" not in parsed_headers and "content-type" not in parsed_headers:
                parsed_headers["Content-Type"] = "application/json"
            
            if "User-Agent" not in parsed_headers and "user-agent" not in parsed_headers:
                parsed_headers["User-Agent"] = "MultiTool-API-Tester/1.0"
            
            start_time = time.time()
            
            try:
                if method.upper() == "GET":
                    response = requests.get(url, headers=parsed_headers, params=parsed_params, timeout=timeout)
                elif method.upper() == "POST":
                    response = requests.post(url, headers=parsed_headers, json=parsed_body, params=parsed_params, timeout=timeout)
                elif method.upper() == "PUT":
                    response = requests.put(url, headers=parsed_headers, json=parsed_body, params=parsed_params, timeout=timeout)
                elif method.upper() == "DELETE":
                    response = requests.delete(url, headers=parsed_headers, params=parsed_params, timeout=timeout)
                elif method.upper() == "PATCH":
                    response = requests.patch(url, headers=parsed_headers, json=parsed_body, params=parsed_params, timeout=timeout)
                elif method.upper() == "HEAD":
                    response = requests.head(url, headers=parsed_headers, params=parsed_params, timeout=timeout)
                else:
                    response = requests.request(method.upper(), url, headers=parsed_headers, json=parsed_body, params=parsed_params, timeout=timeout)
                
                end_time = time.time()
                elapsed = round((end_time - start_time) * 1000, 2)
                
                return self._format_response(url, method, response, elapsed, parsed_headers, parsed_body)
                
            except requests.exceptions.Timeout:
                return self._format_error(url, method, "Request timed out after " + str(timeout) + " seconds")
            except requests.exceptions.ConnectionError:
                return self._format_error(url, method, "Connection failed. Check URL and network.")
            except requests.exceptions.RequestException as e:
                return self._format_error(url, method, str(e))
            
        except Exception as e:
            return "API test error: " + str(e)
    
    def _parse_json(self, json_string):
        if not json_string:
            return None
        
        import json
        
        try:
            return json.loads(json_string)
        except json.JSONDecodeError:
            return None
    
    def _format_response(self, url, method, response, elapsed, sent_headers, sent_body):
        import json
        
        result = "API TEST RESULT\n"
        result += "=" * 50 + "\n\n"
        
        result += "REQUEST\n"
        result += "-" * 30 + "\n"
        result += "Method: " + method.upper() + "\n"
        result += "URL: " + url + "\n"
        
        if sent_headers:
            result += "Headers sent:\n"
            for key, value in sent_headers.items():
                result += "  " + key + ": " + str(value) + "\n"
        
        if sent_body:
            result += "Body sent:\n"
            try:
                body_str = json.dumps(sent_body, indent=2)
                if len(body_str) > 200:
                    body_str = body_str[:200] + "..."
                result += "  " + body_str + "\n"
            except Exception:
                result += "  " + str(sent_body)[:200] + "\n"
        
        result += "\n"
        result += "RESPONSE\n"
        result += "-" * 30 + "\n"
        
        status = response.status_code
        if status >= 200 and status < 300:
            status_emoji = "[SUCCESS]"
        elif status >= 400 and status < 500:
            status_emoji = "[CLIENT ERROR]"
        elif status >= 500:
            status_emoji = "[SERVER ERROR]"
        else:
            status_emoji = "[INFO]"
        
        result += "Status: " + str(status) + " " + status_emoji + "\n"
        result += "Time: " + str(elapsed) + " ms\n"
        
        content_type = response.headers.get("Content-Type", "unknown")
        content_length = response.headers.get("Content-Length", "unknown")
        result += "Content-Type: " + content_type + "\n"
        result += "Content-Length: " + str(content_length) + "\n"
        
        result += "\nResponse Headers:\n"
        header_count = 0
        for key, value in response.headers.items():
            if header_count < 10:
                result += "  " + key + ": " + value[:50] + "\n"
                header_count += 1
        if len(response.headers) > 10:
            result += "  ... and " + str(len(response.headers) - 10) + " more headers\n"
        
        result += "\nResponse Body:\n"
        try:
            json_response = response.json()
            body_str = json.dumps(json_response, indent=2)
            if len(body_str) > 1000:
                result += body_str[:1000] + "\n... (truncated)\n"
            else:
                result += body_str + "\n"
        except Exception:
            text = response.text
            if len(text) > 1000:
                result += text[:1000] + "\n... (truncated)\n"
            else:
                result += text + "\n"
        
        result += "\n"
        result += "ANALYSIS\n"
        result += "-" * 30 + "\n"
        result += self._analyze_response(response)
        
        return result
    
    def _format_error(self, url, method, error_message):
        result = "API TEST FAILED\n"
        result += "=" * 50 + "\n\n"
        result += "Method: " + method.upper() + "\n"
        result += "URL: " + url + "\n\n"
        result += "Error: " + error_message + "\n\n"
        result += "Troubleshooting:\n"
        result += "- Check if the URL is correct\n"
        result += "- Verify your internet connection\n"
        result += "- Check if the server is running\n"
        result += "- Try increasing the timeout\n"
        return result
    
    def _analyze_response(self, response):
        analysis = []
        
        status = response.status_code
        if status == 200:
            analysis.append("Status 200: Request successful")
        elif status == 201:
            analysis.append("Status 201: Resource created successfully")
        elif status == 204:
            analysis.append("Status 204: Success with no content")
        elif status == 400:
            analysis.append("Status 400: Bad request - check your request format")
        elif status == 401:
            analysis.append("Status 401: Unauthorized - authentication required")
        elif status == 403:
            analysis.append("Status 403: Forbidden - insufficient permissions")
        elif status == 404:
            analysis.append("Status 404: Not found - check the endpoint URL")
        elif status == 405:
            analysis.append("Status 405: Method not allowed - try different HTTP method")
        elif status == 429:
            analysis.append("Status 429: Rate limited - too many requests")
        elif status == 500:
            analysis.append("Status 500: Internal server error")
        elif status == 502:
            analysis.append("Status 502: Bad gateway")
        elif status == 503:
            analysis.append("Status 503: Service unavailable")
        
        content_type = response.headers.get("Content-Type", "")
        if "application/json" in content_type:
            analysis.append("Response is JSON format")
        elif "text/html" in content_type:
            analysis.append("Response is HTML - may not be an API endpoint")
        elif "text/plain" in content_type:
            analysis.append("Response is plain text")
        elif "application/xml" in content_type:
            analysis.append("Response is XML format")
        
        cache_control = response.headers.get("Cache-Control", "")
        if cache_control:
            analysis.append("Cache-Control: " + cache_control)
        
        if "X-RateLimit-Remaining" in response.headers:
            remaining = response.headers.get("X-RateLimit-Remaining")
            analysis.append("Rate limit remaining: " + remaining)
        
        if not analysis:
            analysis.append("No specific issues detected")
        
        return "\n".join(analysis)