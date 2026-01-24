"""
Code Debugger Tool - Analyze and debug code for errors and issues.
"""

from .base_tool import BaseTool


class CodeDebuggerTool(BaseTool):
    """Analyze and debug code for errors, issues, and improvements."""
    
    def __init__(self):
        super().__init__()
        self.name = "code_debugger"
        self.description = "Analyze code for bugs, syntax errors, logic issues, and suggest fixes. Supports Python, JavaScript, and more."
        
        self.parameters = {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Code to debug"
                },
                "language": {
                    "type": "string",
                    "enum": ["python", "javascript", "java", "cpp", "auto"],
                    "description": "Programming language",
                    "default": "auto"
                },
                "error_message": {
                    "type": "string",
                    "description": "Error message if available"
                }
            },
            "required": ["code"]
        }
        
        self._python_issues = {
            "indentation": {
                "patterns": ["IndentationError", "unexpected indent", "expected an indented block"],
                "description": "Indentation Error",
                "suggestion": "Check that all code blocks are properly indented with consistent spaces or tabs."
            },
            "syntax": {
                "patterns": ["SyntaxError", "invalid syntax", "EOL while scanning"],
                "description": "Syntax Error",
                "suggestion": "Check for missing colons, parentheses, quotes, or brackets."
            },
            "name_error": {
                "patterns": ["NameError", "is not defined"],
                "description": "Name Error",
                "suggestion": "Variable or function is used before being defined. Check spelling and scope."
            },
            "type_error": {
                "patterns": ["TypeError", "unsupported operand", "not callable", "argument"],
                "description": "Type Error",
                "suggestion": "Check data types. You may be mixing incompatible types or calling non-functions."
            },
            "index_error": {
                "patterns": ["IndexError", "list index out of range"],
                "description": "Index Error",
                "suggestion": "Array/list index is out of bounds. Check loop ranges and array lengths."
            },
            "key_error": {
                "patterns": ["KeyError"],
                "description": "Key Error",
                "suggestion": "Dictionary key does not exist. Use .get() method or check key existence first."
            },
            "attribute_error": {
                "patterns": ["AttributeError", "has no attribute"],
                "description": "Attribute Error",
                "suggestion": "Object does not have the specified attribute or method. Check object type and spelling."
            },
            "import_error": {
                "patterns": ["ImportError", "ModuleNotFoundError", "No module named"],
                "description": "Import Error",
                "suggestion": "Module not found. Install it with pip or check the module name spelling."
            },
            "value_error": {
                "patterns": ["ValueError", "invalid literal"],
                "description": "Value Error",
                "suggestion": "Invalid value passed to function. Check input data and conversion operations."
            },
            "zero_division": {
                "patterns": ["ZeroDivisionError", "division by zero"],
                "description": "Zero Division Error",
                "suggestion": "Cannot divide by zero. Add a check before division operations."
            }
        }
        
        self._common_bugs = [
            {
                "pattern": "= =",
                "issue": "Space in comparison operator",
                "fix": "Use == without space"
            },
            {
                "pattern": "if.*[^=!<>]=[^=]",
                "issue": "Assignment instead of comparison in condition",
                "fix": "Use == for comparison, not ="
            },
            {
                "pattern": "except:",
                "issue": "Bare except clause",
                "fix": "Specify exception type: except Exception as e:"
            },
            {
                "pattern": "while True:",
                "issue": "Infinite loop without break condition visible",
                "fix": "Ensure there is a break statement or termination condition"
            },
            {
                "pattern": "global ",
                "issue": "Global variable usage",
                "fix": "Consider passing variables as parameters instead"
            },
            {
                "pattern": "eval\\(",
                "issue": "Use of eval() is a security risk",
                "fix": "Avoid eval() or use ast.literal_eval() for safe evaluation"
            },
            {
                "pattern": "exec\\(",
                "issue": "Use of exec() is a security risk",
                "fix": "Avoid exec() - restructure code to avoid dynamic execution"
            },
            {
                "pattern": "import \\*",
                "issue": "Wildcard import pollutes namespace",
                "fix": "Import specific names: from module import name1, name2"
            },
            {
                "pattern": "\\.append\\(.*\\.append",
                "issue": "Chained append calls do not work as expected",
                "fix": "append() returns None, cannot chain. Use separate statements"
            },
            {
                "pattern": "is True|is False",
                "issue": "Using is for boolean comparison",
                "fix": "Use == True or just the boolean expression directly"
            }
        ]
    
    def execute(self, code, language="auto", error_message=None):
        try:
            if not code or not code.strip():
                return "Please provide code to debug."
            
            code = code.strip()
            
            if language == "auto":
                language = self._detect_language(code)
            
            issues = []
            suggestions = []
            
            if error_message:
                error_analysis = self._analyze_error(error_message, language)
                issues.extend(error_analysis["issues"])
                suggestions.extend(error_analysis["suggestions"])
            
            code_analysis = self._analyze_code(code, language)
            issues.extend(code_analysis["issues"])
            suggestions.extend(code_analysis["suggestions"])
            
            syntax_check = self._check_syntax(code, language)
            issues.extend(syntax_check["issues"])
            suggestions.extend(syntax_check["suggestions"])
            
            result = self._format_result(code, language, issues, suggestions)
            
            return result
            
        except Exception as e:
            return "Debug error: " + str(e)
    
    def _detect_language(self, code):
        code_lower = code.lower()
        
        if "def " in code and ":" in code:
            return "python"
        if "import " in code and "from " in code:
            return "python"
        if "print(" in code:
            return "python"
        
        if "function " in code or "const " in code or "let " in code or "var " in code:
            return "javascript"
        if "console.log" in code:
            return "javascript"
        if "=>" in code:
            return "javascript"
        
        if "public class" in code or "public static void main" in code:
            return "java"
        
        if "#include" in code or "std::" in code:
            return "cpp"
        
        return "python"
    
    def _analyze_error(self, error_message, language):
        issues = []
        suggestions = []
        
        if language == "python":
            for error_type, info in self._python_issues.items():
                for pattern in info["patterns"]:
                    if pattern.lower() in error_message.lower():
                        issues.append(info["description"] + " detected")
                        suggestions.append(info["suggestion"])
                        break
        
        if not issues:
            issues.append("Error detected: " + error_message[:100])
            suggestions.append("Review the error message and check the indicated line number")
        
        return {"issues": issues, "suggestions": suggestions}
    
    def _analyze_code(self, code, language):
        issues = []
        suggestions = []
        
        import re
        
        for bug in self._common_bugs:
            try:
                if re.search(bug["pattern"], code):
                    issues.append(bug["issue"])
                    suggestions.append(bug["fix"])
            except re.error:
                if bug["pattern"] in code:
                    issues.append(bug["issue"])
                    suggestions.append(bug["fix"])
        
        if language == "python":
            python_checks = self._python_specific_checks(code)
            issues.extend(python_checks["issues"])
            suggestions.extend(python_checks["suggestions"])
        
        elif language == "javascript":
            js_checks = self._javascript_specific_checks(code)
            issues.extend(js_checks["issues"])
            suggestions.extend(js_checks["suggestions"])
        
        return {"issues": issues, "suggestions": suggestions}
    
    def _python_specific_checks(self, code):
        issues = []
        suggestions = []
        lines = code.split("\n")
        
        open_parens = code.count("(") - code.count(")")
        open_brackets = code.count("[") - code.count("]")
        open_braces = code.count("{") - code.count("}")
        
        if open_parens != 0:
            issues.append("Unbalanced parentheses: " + str(abs(open_parens)) + " unclosed")
            suggestions.append("Check that all ( have matching )")
        
        if open_brackets != 0:
            issues.append("Unbalanced brackets: " + str(abs(open_brackets)) + " unclosed")
            suggestions.append("Check that all [ have matching ]")
        
        if open_braces != 0:
            issues.append("Unbalanced braces: " + str(abs(open_braces)) + " unclosed")
            suggestions.append("Check that all { have matching }")
        
        for i, line in enumerate(lines):
            stripped = line.rstrip()
            
            if stripped.endswith(("def ", "class ", "if ", "for ", "while ", "try", "except", "else", "elif", "finally")):
                issues.append("Line " + str(i + 1) + ": Missing colon after statement")
                suggestions.append("Add : at the end of the statement")
            
            has_def = "def " in stripped
            has_class = "class " in stripped
            ends_with_colon = stripped.endswith(":")
            if (has_def or has_class) and not ends_with_colon and stripped and not stripped.startswith("#"):
                if "(" in stripped and ")" in stripped:
                    issues.append("Line " + str(i + 1) + ": Possibly missing colon after function/class definition")
                    suggestions.append("Add : at the end of def/class statements")
        
        single_quotes = code.count("'") - code.count("\\'")
        double_quotes = code.count('"') - code.count('\\"')
        
        if single_quotes % 2 != 0:
            issues.append("Unbalanced single quotes")
            suggestions.append("Check that all ' have matching '")
        
        if double_quotes % 2 != 0:
            issues.append("Unbalanced double quotes")
            suggestions.append("Check that all \" have matching \"")
        
        return {"issues": issues, "suggestions": suggestions}
    
    def _javascript_specific_checks(self, code):
        issues = []
        suggestions = []
        lines = code.split("\n")
        
        open_parens = code.count("(") - code.count(")")
        open_brackets = code.count("[") - code.count("]")
        open_braces = code.count("{") - code.count("}")
        
        if open_parens != 0:
            issues.append("Unbalanced parentheses")
            suggestions.append("Check that all ( have matching )")
        
        if open_brackets != 0:
            issues.append("Unbalanced brackets")
            suggestions.append("Check that all [ have matching ]")
        
        if open_braces != 0:
            issues.append("Unbalanced braces")
            suggestions.append("Check that all { have matching }")
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            if "var " in stripped:
                issues.append("Line " + str(i + 1) + ": Using var instead of let/const")
                suggestions.append("Use let for variables that change, const for constants")
            
            if "== " in stripped and "===" not in stripped:
                issues.append("Line " + str(i + 1) + ": Using == instead of ===")
                suggestions.append("Use === for strict equality comparison")
        
        return {"issues": issues, "suggestions": suggestions}
    
    def _check_syntax(self, code, language):
        issues = []
        suggestions = []
        
        if language == "python":
            try:
                compile(code, "<string>", "exec")
            except SyntaxError as e:
                issues.append("Syntax Error at line " + str(e.lineno) + ": " + str(e.msg))
                suggestions.append("Fix the syntax error at the indicated line")
            except Exception as e:
                pass
        
        return {"issues": issues, "suggestions": suggestions}
    
    def _format_result(self, code, language, issues, suggestions):
        lines = code.split("\n")
        
        result = "CODE DEBUG REPORT\n"
        result += "=" * 40 + "\n\n"
        
        result += "Language: " + language.upper() + "\n"
        result += "Lines of code: " + str(len(lines)) + "\n\n"
        
        if not issues:
            result += "STATUS: No obvious issues found\n\n"
            result += "The code appears to be syntactically correct.\n"
            result += "However, runtime errors may still occur.\n\n"
            result += "Recommendations:\n"
            result += "- Test with various inputs\n"
            result += "- Add error handling\n"
            result += "- Consider edge cases\n"
        else:
            result += "STATUS: " + str(len(issues)) + " issue(s) found\n\n"
            
            result += "ISSUES:\n"
            result += "-" * 30 + "\n"
            for i, issue in enumerate(issues):
                result += str(i + 1) + ". " + issue + "\n"
            
            result += "\n"
            
            result += "SUGGESTIONS:\n"
            result += "-" * 30 + "\n"
            unique_suggestions = []
            for s in suggestions:
                if s not in unique_suggestions:
                    unique_suggestions.append(s)
            
            for i, suggestion in enumerate(unique_suggestions):
                result += str(i + 1) + ". " + suggestion + "\n"
        
        result += "\n"
        result += "CODE PREVIEW:\n"
        result += "-" * 30 + "\n"
        
        preview_lines = lines[:10]
        for i, line in enumerate(preview_lines):
            line_num = str(i + 1).rjust(3)
            if len(line) > 60:
                result += line_num + " | " + line[:60] + "...\n"
            else:
                result += line_num + " | " + line + "\n"
        
        if len(lines) > 10:
            result += "    ... (" + str(len(lines) - 10) + " more lines)\n"
        
        return result