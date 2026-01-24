"""
Dependency Analyzer Tool - Analyze project dependencies and imports.
"""

from .base_tool import BaseTool
import re


class DependencyAnalyzerTool(BaseTool):
    """Analyze code dependencies, imports, and package requirements."""
    
    def __init__(self):
        super().__init__()
        self.name = "dependency_analyzer"
        self.description = "Analyze code to find dependencies, imports, and generate requirements. Supports Python and JavaScript."
        
        self.parameters = {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Code to analyze for dependencies"
                },
                "language": {
                    "type": "string",
                    "enum": ["python", "javascript", "auto"],
                    "description": "Programming language",
                    "default": "auto"
                },
                "operation": {
                    "type": "string",
                    "enum": ["analyze", "requirements", "tree", "security"],
                    "description": "Operation to perform",
                    "default": "analyze"
                }
            },
            "required": ["code"]
        }
        
        self._python_stdlib = {
            "os", "sys", "re", "json", "math", "time", "datetime", "random",
            "collections", "itertools", "functools", "operator", "string",
            "io", "pathlib", "glob", "shutil", "tempfile", "csv", "pickle",
            "sqlite3", "socket", "http", "urllib", "email", "html", "xml",
            "logging", "unittest", "doctest", "typing", "abc", "copy",
            "hashlib", "hmac", "secrets", "base64", "binascii", "struct",
            "codecs", "unicodedata", "locale", "gettext", "argparse",
            "configparser", "fileinput", "stat", "filecmp", "subprocess",
            "threading", "multiprocessing", "concurrent", "queue", "asyncio",
            "contextvars", "select", "selectors", "signal", "mmap", "ctypes",
            "platform", "errno", "warnings", "dataclasses", "contextlib",
            "decimal", "fractions", "statistics", "cmath", "array", "weakref",
            "types", "traceback", "gc", "inspect", "dis", "pickletools",
            "pprint", "reprlib", "enum", "graphlib", "heapq", "bisect",
            "calendar", "zoneinfo", "pdb", "profile", "timeit", "trace",
            "zipfile", "tarfile", "gzip", "bz2", "lzma", "zlib"
        }
        
        self._common_packages = {
            "requests": {"version": ">=2.28.0", "description": "HTTP library"},
            "numpy": {"version": ">=1.21.0", "description": "Numerical computing"},
            "pandas": {"version": ">=1.3.0", "description": "Data analysis"},
            "flask": {"version": ">=2.0.0", "description": "Web framework"},
            "django": {"version": ">=4.0.0", "description": "Web framework"},
            "fastapi": {"version": ">=0.85.0", "description": "API framework"},
            "sqlalchemy": {"version": ">=1.4.0", "description": "Database ORM"},
            "pytest": {"version": ">=7.0.0", "description": "Testing framework"},
            "beautifulsoup4": {"version": ">=4.11.0", "description": "HTML parsing"},
            "selenium": {"version": ">=4.0.0", "description": "Browser automation"},
            "pillow": {"version": ">=9.0.0", "description": "Image processing"},
            "matplotlib": {"version": ">=3.5.0", "description": "Plotting"},
            "scikit-learn": {"version": ">=1.0.0", "description": "Machine learning"},
            "tensorflow": {"version": ">=2.10.0", "description": "Deep learning"},
            "torch": {"version": ">=1.12.0", "description": "Deep learning"},
            "opencv-python": {"version": ">=4.6.0", "description": "Computer vision"},
            "streamlit": {"version": ">=1.15.0", "description": "Data apps"},
            "openai": {"version": ">=0.27.0", "description": "OpenAI API"},
            "langchain": {"version": ">=0.0.200", "description": "LLM framework"},
            "transformers": {"version": ">=4.25.0", "description": "NLP models"},
            "boto3": {"version": ">=1.26.0", "description": "AWS SDK"},
            "redis": {"version": ">=4.0.0", "description": "Redis client"},
            "celery": {"version": ">=5.2.0", "description": "Task queue"},
            "pydantic": {"version": ">=1.10.0", "description": "Data validation"},
            "httpx": {"version": ">=0.23.0", "description": "HTTP client"},
            "aiohttp": {"version": ">=3.8.0", "description": "Async HTTP"},
            "pymongo": {"version": ">=4.0.0", "description": "MongoDB driver"},
            "psycopg2": {"version": ">=2.9.0", "description": "PostgreSQL driver"},
            "cryptography": {"version": ">=38.0.0", "description": "Cryptography"},
            "pyjwt": {"version": ">=2.6.0", "description": "JWT handling"},
            "python-dotenv": {"version": ">=0.21.0", "description": "Env variables"},
            "click": {"version": ">=8.0.0", "description": "CLI creation"},
            "typer": {"version": ">=0.7.0", "description": "CLI creation"},
            "rich": {"version": ">=12.0.0", "description": "Rich text"},
            "tqdm": {"version": ">=4.64.0", "description": "Progress bars"},
            "pytest-cov": {"version": ">=4.0.0", "description": "Test coverage"},
            "black": {"version": ">=22.0.0", "description": "Code formatter"},
            "flake8": {"version": ">=5.0.0", "description": "Linter"},
            "mypy": {"version": ">=0.990", "description": "Type checker"},
            "scipy": {"version": ">=1.9.0", "description": "Scientific computing"},
            "sympy": {"version": ">=1.11.0", "description": "Symbolic math"},
            "networkx": {"version": ">=2.8.0", "description": "Graph analysis"},
            "seaborn": {"version": ">=0.12.0", "description": "Statistical plots"},
            "plotly": {"version": ">=5.11.0", "description": "Interactive plots"},
            "dash": {"version": ">=2.7.0", "description": "Dashboards"},
            "gunicorn": {"version": ">=20.1.0", "description": "WSGI server"},
            "uvicorn": {"version": ">=0.20.0", "description": "ASGI server"},
            "sentence-transformers": {"version": ">=2.2.0", "description": "Embeddings"},
            "faiss-cpu": {"version": ">=1.7.0", "description": "Vector search"},
            "chromadb": {"version": ">=0.3.0", "description": "Vector database"}
        }
        
        self._security_concerns = {
            "pickle": "pickle can execute arbitrary code during deserialization",
            "eval": "eval can execute arbitrary code",
            "exec": "exec can execute arbitrary code",
            "subprocess": "subprocess can run system commands",
            "os.system": "os.system can run system commands",
            "yaml": "yaml.load without Loader can be unsafe",
            "marshal": "marshal can execute arbitrary code",
            "shelve": "shelve uses pickle internally"
        }
    
    def execute(self, code, language="auto", operation="analyze"):
        try:
            if not code or not code.strip():
                return "Please provide code to analyze."
            
            code = code.strip()
            
            if language == "auto":
                language = self._detect_language(code)
            
            if operation == "analyze":
                return self._analyze_dependencies(code, language)
            elif operation == "requirements":
                return self._generate_requirements(code, language)
            elif operation == "tree":
                return self._generate_tree(code, language)
            elif operation == "security":
                return self._security_analysis(code, language)
            else:
                return self._analyze_dependencies(code, language)
                
        except Exception as e:
            return "Dependency analysis error: " + str(e)
    
    def _detect_language(self, code):
        if "import " in code or "from " in code and "def " in code:
            return "python"
        if "require(" in code or "import " in code and "from " in code:
            if "const " in code or "let " in code or "var " in code:
                return "javascript"
        if "function " in code or "=>" in code:
            return "javascript"
        return "python"
    
    def _analyze_dependencies(self, code, language):
        if language == "python":
            return self._analyze_python(code)
        elif language == "javascript":
            return self._analyze_javascript(code)
        else:
            return self._analyze_python(code)
    
    def _analyze_python(self, code):
        imports = []
        from_imports = []
        
        import_pattern = r'^import\s+([\w\.,\s]+)'
        from_pattern = r'^from\s+([\w\.]+)\s+import\s+([\w\.,\s\*]+)'
        
        lines = code.split("\n")
        for line in lines:
            line = line.strip()
            
            match = re.match(from_pattern, line)
            if match:
                module = match.group(1)
                names = match.group(2)
                from_imports.append({"module": module, "names": names})
                continue
            
            match = re.match(import_pattern, line)
            if match:
                modules = match.group(1)
                for mod in modules.split(","):
                    mod = mod.strip()
                    if " as " in mod:
                        mod = mod.split(" as ")[0].strip()
                    imports.append(mod)
        
        all_modules = set()
        for imp in imports:
            base = imp.split(".")[0]
            all_modules.add(base)
        for imp in from_imports:
            base = imp["module"].split(".")[0]
            all_modules.add(base)
        
        stdlib = []
        third_party = []
        unknown = []
        
        for mod in all_modules:
            if mod in self._python_stdlib:
                stdlib.append(mod)
            elif mod in self._common_packages:
                third_party.append(mod)
            else:
                lower_mod = mod.lower()
                found = False
                for pkg in self._common_packages:
                    if lower_mod in pkg.lower() or pkg.lower() in lower_mod:
                        third_party.append(mod)
                        found = True
                        break
                if not found:
                    if mod.startswith("_") or mod[0].isupper():
                        unknown.append(mod)
                    else:
                        third_party.append(mod)
        
        result = "DEPENDENCY ANALYSIS\n"
        result += "=" * 50 + "\n\n"
        result += "Language: Python\n"
        result += "Total imports found: " + str(len(all_modules)) + "\n\n"
        
        result += "STANDARD LIBRARY (" + str(len(stdlib)) + ")\n"
        result += "-" * 30 + "\n"
        if stdlib:
            for mod in sorted(stdlib):
                result += "  - " + mod + "\n"
        else:
            result += "  None\n"
        
        result += "\n"
        result += "THIRD-PARTY PACKAGES (" + str(len(third_party)) + ")\n"
        result += "-" * 30 + "\n"
        if third_party:
            for mod in sorted(third_party):
                info = self._common_packages.get(mod, {})
                desc = info.get("description", "")
                if desc:
                    result += "  - " + mod + " : " + desc + "\n"
                else:
                    result += "  - " + mod + "\n"
        else:
            result += "  None\n"
        
        if unknown:
            result += "\n"
            result += "LOCAL/UNKNOWN (" + str(len(unknown)) + ")\n"
            result += "-" * 30 + "\n"
            for mod in sorted(unknown):
                result += "  - " + mod + "\n"
        
        result += "\n"
        result += "IMPORT STATEMENTS\n"
        result += "-" * 30 + "\n"
        
        if imports:
            result += "Direct imports:\n"
            for imp in imports[:10]:
                result += "  import " + imp + "\n"
            if len(imports) > 10:
                result += "  ... and " + str(len(imports) - 10) + " more\n"
        
        if from_imports:
            result += "\nFrom imports:\n"
            for imp in from_imports[:10]:
                result += "  from " + imp["module"] + " import " + imp["names"] + "\n"
            if len(from_imports) > 10:
                result += "  ... and " + str(len(from_imports) - 10) + " more\n"
        
        return result
    
    def _analyze_javascript(self, code):
        imports = []
        requires = []
        
        import_pattern = r'import\s+.*?\s+from\s+[\'"]([^\'"]+)[\'"]'
        require_pattern = r'require\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)'
        
        import_matches = re.findall(import_pattern, code)
        require_matches = re.findall(require_pattern, code)
        
        imports.extend(import_matches)
        requires.extend(require_matches)
        
        all_modules = set(imports + requires)
        
        node_builtin = {"fs", "path", "http", "https", "url", "crypto", "os", "util", "events", "stream", "buffer", "child_process", "cluster", "net", "dns", "tls", "readline", "zlib", "assert", "querystring"}
        
        builtin = []
        third_party = []
        local = []
        
        for mod in all_modules:
            if mod.startswith("./") or mod.startswith("../") or mod.startswith("/"):
                local.append(mod)
            elif mod in node_builtin:
                builtin.append(mod)
            else:
                third_party.append(mod)
        
        result = "DEPENDENCY ANALYSIS\n"
        result += "=" * 50 + "\n\n"
        result += "Language: JavaScript\n"
        result += "Total imports found: " + str(len(all_modules)) + "\n\n"
        
        result += "NODE.JS BUILT-IN (" + str(len(builtin)) + ")\n"
        result += "-" * 30 + "\n"
        if builtin:
            for mod in sorted(builtin):
                result += "  - " + mod + "\n"
        else:
            result += "  None\n"
        
        result += "\n"
        result += "NPM PACKAGES (" + str(len(third_party)) + ")\n"
        result += "-" * 30 + "\n"
        if third_party:
            for mod in sorted(third_party):
                result += "  - " + mod + "\n"
        else:
            result += "  None\n"
        
        result += "\n"
        result += "LOCAL MODULES (" + str(len(local)) + ")\n"
        result += "-" * 30 + "\n"
        if local:
            for mod in sorted(local):
                result += "  - " + mod + "\n"
        else:
            result += "  None\n"
        
        return result
    
    def _generate_requirements(self, code, language):
        if language != "python":
            return "Requirements generation only supported for Python."
        
        from_pattern = r'^from\s+([\w\.]+)\s+import'
        import_pattern = r'^import\s+([\w]+)'
        
        modules = set()
        lines = code.split("\n")
        
        for line in lines:
            line = line.strip()
            
            match = re.match(from_pattern, line)
            if match:
                mod = match.group(1).split(".")[0]
                modules.add(mod)
                continue
            
            match = re.match(import_pattern, line)
            if match:
                mod = match.group(1)
                modules.add(mod)
        
        third_party = []
        for mod in modules:
            if mod not in self._python_stdlib:
                third_party.append(mod)
        
        result = "REQUIREMENTS.TXT GENERATOR\n"
        result += "=" * 50 + "\n\n"
        
        if not third_party:
            result += "No third-party packages detected.\n"
            result += "Only standard library modules are used.\n"
            return result
        
        result += "Detected " + str(len(third_party)) + " third-party package(s)\n\n"
        result += "Generated requirements.txt:\n"
        result += "-" * 30 + "\n"
        
        req_lines = []
        for mod in sorted(third_party):
            if mod in self._common_packages:
                version = self._common_packages[mod]["version"]
                req_lines.append(mod + version)
            else:
                req_lines.append(mod)
        
        for line in req_lines:
            result += line + "\n"
        
        result += "\n"
        result += "Copy the above lines to your requirements.txt file.\n"
        result += "Install with: pip install -r requirements.txt\n"
        
        return result
    
    def _generate_tree(self, code, language):
        if language != "python":
            return "Dependency tree only supported for Python."
        
        from_pattern = r'^from\s+([\w\.]+)\s+import\s+([\w\.,\s\*]+)'
        import_pattern = r'^import\s+([\w\.]+)'
        
        tree = {}
        lines = code.split("\n")
        
        for line in lines:
            line = line.strip()
            
            match = re.match(from_pattern, line)
            if match:
                mod = match.group(1)
                names = match.group(2)
                base = mod.split(".")[0]
                
                if base not in tree:
                    tree[base] = {"submodules": set(), "names": set()}
                
                if "." in mod:
                    tree[base]["submodules"].add(mod)
                
                for name in names.split(","):
                    name = name.strip()
                    if name:
                        tree[base]["names"].add(name)
                continue
            
            match = re.match(import_pattern, line)
            if match:
                mod = match.group(1)
                base = mod.split(".")[0]
                
                if base not in tree:
                    tree[base] = {"submodules": set(), "names": set()}
                
                if "." in mod:
                    tree[base]["submodules"].add(mod)
        
        result = "DEPENDENCY TREE\n"
        result += "=" * 50 + "\n\n"
        
        if not tree:
            result += "No imports found.\n"
            return result
        
        for base in sorted(tree.keys()):
            pkg_type = "[stdlib]" if base in self._python_stdlib else "[third-party]"
            result += base + " " + pkg_type + "\n"
            
            info = tree[base]
            
            if info["submodules"]:
                for submod in sorted(info["submodules"]):
                    result += "  +-- " + submod + "\n"
            
            if info["names"]:
                names_list = sorted(info["names"])
                if len(names_list) <= 5:
                    for name in names_list:
                        result += "      - " + name + "\n"
                else:
                    for name in names_list[:5]:
                        result += "      - " + name + "\n"
                    result += "      ... and " + str(len(names_list) - 5) + " more\n"
            
            result += "\n"
        
        return result
    
    def _security_analysis(self, code, language):
        result = "SECURITY ANALYSIS\n"
        result += "=" * 50 + "\n\n"
        
        issues = []
        
        for concern, description in self._security_concerns.items():
            if concern in code:
                issues.append({"item": concern, "description": description})
        
        if "password" in code.lower() and ("=" in code):
            issues.append({"item": "hardcoded password", "description": "Possible hardcoded password detected"})
        
        if "api_key" in code.lower() or "apikey" in code.lower():
            if "=" in code and ("\"" in code or "'" in code):
                issues.append({"item": "hardcoded API key", "description": "Possible hardcoded API key detected"})
        
        if "secret" in code.lower():
            if "=" in code and ("\"" in code or "'" in code):
                issues.append({"item": "hardcoded secret", "description": "Possible hardcoded secret detected"})
        
        if "sql" in code.lower() or "query" in code.lower():
            if "%" in code or ".format(" in code or "f\"" in code or "f'" in code:
                issues.append({"item": "SQL injection", "description": "Possible SQL injection vulnerability - use parameterized queries"})
        
        if not issues:
            result += "STATUS: No obvious security issues detected\n\n"
            result += "Note: This is a basic static analysis.\n"
            result += "Consider using dedicated security tools for thorough analysis.\n"
        else:
            result += "STATUS: " + str(len(issues)) + " potential issue(s) found\n\n"
            result += "ISSUES:\n"
            result += "-" * 30 + "\n"
            
            for i, issue in enumerate(issues):
                result += str(i + 1) + ". " + issue["item"].upper() + "\n"
                result += "   " + issue["description"] + "\n\n"
            
            result += "RECOMMENDATIONS:\n"
            result += "-" * 30 + "\n"
            result += "- Use environment variables for secrets\n"
            result += "- Avoid eval/exec when possible\n"
            result += "- Use parameterized queries for SQL\n"
            result += "- Validate and sanitize all inputs\n"
            result += "- Use safe deserialization methods\n"
        
        return result