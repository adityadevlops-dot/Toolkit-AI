"""
Regex Tool - Test and build regular expressions.
"""

from .base_tool import BaseTool
import re


class RegexTool(BaseTool):
    """Test, build, and explain regular expressions."""
    
    def __init__(self):
        super().__init__()
        self.name = "regex_tool"
        self.description = "Test regular expressions against text, find matches, and get explanations of regex patterns."
        
        self.parameters = {
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "Regular expression pattern"
                },
                "text": {
                    "type": "string",
                    "description": "Text to search in"
                },
                "operation": {
                    "type": "string",
                    "enum": ["match", "findall", "replace", "split", "explain", "build"],
                    "description": "Operation to perform",
                    "default": "findall"
                },
                "replacement": {
                    "type": "string",
                    "description": "Replacement string for replace operation"
                },
                "flags": {
                    "type": "string",
                    "description": "Regex flags: i (ignore case), m (multiline), s (dotall)",
                    "default": ""
                }
            },
            "required": ["pattern"]
        }
        
        self._common_patterns = {
            "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            "phone": r"\+?[\d\s\-\(\)]{10,}",
            "url": r"https?://[^\s<>\"]+",
            "ip": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
            "date": r"\d{4}[-/]\d{2}[-/]\d{2}",
            "time": r"\d{1,2}:\d{2}(?::\d{2})?(?:\s*[AP]M)?",
            "hexcolor": r"#[0-9A-Fa-f]{6}\b",
            "zipcode": r"\b\d{5}(?:-\d{4})?\b",
            "creditcard": r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",
            "ssn": r"\b\d{3}-\d{2}-\d{4}\b"
        }
        
        self._token_explanations = {
            ".": "Matches any single character except newline",
            "*": "Matches 0 or more of the preceding element",
            "+": "Matches 1 or more of the preceding element",
            "?": "Matches 0 or 1 of the preceding element (optional)",
            "^": "Matches the start of the string",
            "$": "Matches the end of the string",
            "\\d": "Matches any digit (0-9)",
            "\\D": "Matches any non-digit",
            "\\w": "Matches any word character (a-z, A-Z, 0-9, _)",
            "\\W": "Matches any non-word character",
            "\\s": "Matches any whitespace character",
            "\\S": "Matches any non-whitespace character",
            "\\b": "Matches a word boundary",
            "\\B": "Matches a non-word boundary",
            "[]": "Character class - matches any character inside",
            "[^]": "Negated character class - matches any character NOT inside",
            "()": "Capturing group - groups and captures",
            "(?:)": "Non-capturing group - groups without capturing",
            "|": "Alternation - matches either left or right",
            "{n}": "Matches exactly n occurrences",
            "{n,}": "Matches n or more occurrences",
            "{n,m}": "Matches between n and m occurrences"
        }
    
    def execute(self, pattern, text=None, operation="findall", replacement=None, flags=""):
        try:
            if not pattern:
                return "Please provide a regex pattern."
            
            if operation == "explain":
                return self._explain_pattern(pattern)
            
            if operation == "build":
                return self._build_pattern(pattern)
            
            if not text:
                return "Please provide text to search in."
            
            regex_flags = self._parse_flags(flags)
            
            try:
                compiled = re.compile(pattern, regex_flags)
            except re.error as e:
                return "Invalid regex pattern: " + str(e)
            
            if operation == "match":
                return self._do_match(compiled, text, pattern)
            elif operation == "findall":
                return self._do_findall(compiled, text, pattern)
            elif operation == "replace":
                return self._do_replace(compiled, text, pattern, replacement)
            elif operation == "split":
                return self._do_split(compiled, text, pattern)
            else:
                return self._do_findall(compiled, text, pattern)
            
        except Exception as e:
            return "Regex error: " + str(e)
    
    def _parse_flags(self, flags):
        regex_flags = 0
        if "i" in flags.lower():
            regex_flags |= re.IGNORECASE
        if "m" in flags.lower():
            regex_flags |= re.MULTILINE
        if "s" in flags.lower():
            regex_flags |= re.DOTALL
        return regex_flags
    
    def _do_match(self, compiled, text, pattern):
        match = compiled.match(text)
        
        result = "REGEX MATCH\n"
        result += "=" * 40 + "\n\n"
        result += "Pattern: " + pattern + "\n"
        result += "Text: " + text[:100]
        if len(text) > 100:
            result += "..."
        result += "\n\n"
        
        if match:
            result += "STATUS: Match found at start\n\n"
            result += "Matched: " + match.group() + "\n"
            result += "Position: 0 to " + str(match.end()) + "\n"
            
            if match.groups():
                result += "\nCapture Groups:\n"
                for i, group in enumerate(match.groups()):
                    result += "  Group " + str(i + 1) + ": " + str(group) + "\n"
        else:
            result += "STATUS: No match at start of string\n"
        
        return result
    
    def _do_findall(self, compiled, text, pattern):
        matches = list(compiled.finditer(text))
        
        result = "REGEX FIND ALL\n"
        result += "=" * 40 + "\n\n"
        result += "Pattern: " + pattern + "\n"
        result += "Text length: " + str(len(text)) + " characters\n\n"
        
        if matches:
            result += "STATUS: " + str(len(matches)) + " match(es) found\n\n"
            result += "Matches:\n"
            result += "-" * 30 + "\n"
            
            for i, match in enumerate(matches[:20]):
                pos = str(match.start()) + "-" + str(match.end())
                result += str(i + 1) + ". \"" + match.group() + "\" at position " + pos + "\n"
                
                if match.groups():
                    for j, group in enumerate(match.groups()):
                        result += "   Group " + str(j + 1) + ": " + str(group) + "\n"
            
            if len(matches) > 20:
                result += "\n... and " + str(len(matches) - 20) + " more matches\n"
        else:
            result += "STATUS: No matches found\n"
        
        return result
    
    def _do_replace(self, compiled, text, pattern, replacement):
        if replacement is None:
            replacement = ""
        
        new_text = compiled.sub(replacement, text)
        count = len(compiled.findall(text))
        
        result = "REGEX REPLACE\n"
        result += "=" * 40 + "\n\n"
        result += "Pattern: " + pattern + "\n"
        result += "Replacement: " + replacement + "\n"
        result += "Replacements made: " + str(count) + "\n\n"
        
        result += "Original:\n"
        result += "-" * 30 + "\n"
        if len(text) > 200:
            result += text[:200] + "...\n"
        else:
            result += text + "\n"
        
        result += "\nResult:\n"
        result += "-" * 30 + "\n"
        if len(new_text) > 200:
            result += new_text[:200] + "...\n"
        else:
            result += new_text + "\n"
        
        return result
    
    def _do_split(self, compiled, text, pattern):
        parts = compiled.split(text)
        
        result = "REGEX SPLIT\n"
        result += "=" * 40 + "\n\n"
        result += "Pattern: " + pattern + "\n"
        result += "Parts created: " + str(len(parts)) + "\n\n"
        
        result += "Parts:\n"
        result += "-" * 30 + "\n"
        
        for i, part in enumerate(parts[:20]):
            display = part[:50]
            if len(part) > 50:
                display += "..."
            result += str(i + 1) + ". \"" + display + "\"\n"
        
        if len(parts) > 20:
            result += "\n... and " + str(len(parts) - 20) + " more parts\n"
        
        return result
    
    def _explain_pattern(self, pattern):
        result = "REGEX EXPLANATION\n"
        result += "=" * 40 + "\n\n"
        result += "Pattern: " + pattern + "\n\n"
        
        result += "Token Analysis:\n"
        result += "-" * 30 + "\n"
        
        explanations = []
        i = 0
        while i < len(pattern):
            char = pattern[i]
            
            if char == "\\" and i + 1 < len(pattern):
                token = pattern[i:i+2]
                if token in self._token_explanations:
                    explanations.append((token, self._token_explanations[token]))
                else:
                    explanations.append((token, "Escaped character: " + pattern[i+1]))
                i += 2
            
            elif char == "[":
                end = pattern.find("]", i)
                if end != -1:
                    token = pattern[i:end+1]
                    if token.startswith("[^"):
                        explanations.append((token, "Negated character class - matches any char NOT in: " + token[2:-1]))
                    else:
                        explanations.append((token, "Character class - matches any char in: " + token[1:-1]))
                    i = end + 1
                else:
                    explanations.append((char, "Opening bracket (unclosed)"))
                    i += 1
            
            elif char == "(":
                if i + 2 < len(pattern) and pattern[i:i+3] == "(?:":
                    explanations.append(("(?:", "Start non-capturing group"))
                    i += 3
                elif i + 2 < len(pattern) and pattern[i:i+3] == "(?=":
                    explanations.append(("(?=", "Positive lookahead"))
                    i += 3
                elif i + 2 < len(pattern) and pattern[i:i+3] == "(?!":
                    explanations.append(("(?!", "Negative lookahead"))
                    i += 3
                else:
                    explanations.append(("(", "Start capturing group"))
                    i += 1
            
            elif char == ")":
                explanations.append((")", "End group"))
                i += 1
            
            elif char == "{":
                end = pattern.find("}", i)
                if end != -1:
                    token = pattern[i:end+1]
                    explanations.append((token, "Quantifier: " + token))
                    i = end + 1
                else:
                    explanations.append((char, "Opening brace"))
                    i += 1
            
            elif char in self._token_explanations:
                explanations.append((char, self._token_explanations[char]))
                i += 1
            
            else:
                explanations.append((char, "Literal character: " + char))
                i += 1
        
        for token, explanation in explanations:
            result += "  " + token + " : " + explanation + "\n"
        
        result += "\n"
        result += "Common Pattern Templates:\n"
        result += "-" * 30 + "\n"
        for name, pat in list(self._common_patterns.items())[:5]:
            result += "  " + name + ": " + pat + "\n"
        
        return result
    
    def _build_pattern(self, description):
        desc_lower = description.lower()
        
        result = "REGEX BUILDER\n"
        result += "=" * 40 + "\n\n"
        result += "Request: " + description + "\n\n"
        
        suggested_pattern = None
        pattern_name = None
        
        for name, pattern in self._common_patterns.items():
            if name in desc_lower:
                suggested_pattern = pattern
                pattern_name = name
                break
        
        if "email" in desc_lower:
            suggested_pattern = self._common_patterns["email"]
            pattern_name = "email"
        elif "phone" in desc_lower or "number" in desc_lower:
            suggested_pattern = self._common_patterns["phone"]
            pattern_name = "phone"
        elif "url" in desc_lower or "link" in desc_lower or "http" in desc_lower:
            suggested_pattern = self._common_patterns["url"]
            pattern_name = "url"
        elif "ip" in desc_lower or "address" in desc_lower:
            suggested_pattern = self._common_patterns["ip"]
            pattern_name = "ip address"
        elif "date" in desc_lower:
            suggested_pattern = self._common_patterns["date"]
            pattern_name = "date"
        elif "time" in desc_lower:
            suggested_pattern = self._common_patterns["time"]
            pattern_name = "time"
        elif "color" in desc_lower or "hex" in desc_lower:
            suggested_pattern = self._common_patterns["hexcolor"]
            pattern_name = "hex color"
        elif "zip" in desc_lower or "postal" in desc_lower:
            suggested_pattern = self._common_patterns["zipcode"]
            pattern_name = "zip code"
        elif "word" in desc_lower:
            suggested_pattern = r"\b\w+\b"
            pattern_name = "word"
        elif "digit" in desc_lower or "number" in desc_lower:
            suggested_pattern = r"\d+"
            pattern_name = "digits"
        elif "whitespace" in desc_lower or "space" in desc_lower:
            suggested_pattern = r"\s+"
            pattern_name = "whitespace"
        
        if suggested_pattern:
            result += "Suggested Pattern for " + pattern_name + ":\n"
            result += "-" * 30 + "\n"
            result += suggested_pattern + "\n\n"
            result += "Usage Example:\n"
            result += "  import re\n"
            result += "  pattern = r\"" + suggested_pattern + "\"\n"
            result += "  matches = re.findall(pattern, text)\n"
        else:
            result += "Could not auto-generate pattern.\n\n"
            result += "Available Templates:\n"
            result += "-" * 30 + "\n"
            for name, pat in self._common_patterns.items():
                result += "  " + name + ":\n"
                result += "    " + pat + "\n\n"
        
        return result