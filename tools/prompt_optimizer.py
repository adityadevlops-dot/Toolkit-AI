"""
Prompt Optimizer Tool - Optimize and improve prompts for LLMs.
"""

from .base_tool import BaseTool


class PromptOptimizerTool(BaseTool):
    """Optimize prompts for better LLM responses."""
    
    def __init__(self):
        super().__init__()
        self.name = "prompt_optimizer"
        self.description = "Analyze and optimize prompts for better LLM responses. Provides suggestions, rewrites, and scoring."
        
        self.parameters = {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "The prompt to optimize"
                },
                "task_type": {
                    "type": "string",
                    "enum": ["general", "coding", "creative", "analysis", "conversation", "instruction"],
                    "description": "Type of task",
                    "default": "general"
                },
                "operation": {
                    "type": "string",
                    "enum": ["analyze", "optimize", "rewrite", "score"],
                    "description": "Operation to perform",
                    "default": "optimize"
                }
            },
            "required": ["prompt"]
        }
        
        self._weak_patterns = [
            ("please", "Direct instructions work better"),
            ("i think", "Be more assertive"),
            ("maybe", "Be specific about requirements"),
            ("something like", "Provide exact examples"),
            ("etc", "List all items explicitly"),
            ("stuff", "Use specific terminology"),
            ("things", "Be more specific"),
            ("good", "Define what good means"),
            ("nice", "Specify exact criteria"),
            ("asap", "Specify exact timeframe or length")
        ]
        
        self._strong_patterns = [
            ("step by step", 1.5),
            ("for example", 1.3),
            ("specifically", 1.2),
            ("must include", 1.4),
            ("format:", 1.5),
            ("requirements:", 1.4),
            ("constraints:", 1.3),
            ("output should", 1.4),
            ("do not", 1.2),
            ("avoid", 1.1),
            ("ensure", 1.2),
            ("exactly", 1.3)
        ]
    
    def execute(self, prompt, task_type="general", operation="optimize"):
        try:
            if not prompt or not prompt.strip():
                return "Please provide a prompt to optimize."
            
            prompt = prompt.strip()
            
            if operation == "analyze":
                return self._analyze_prompt(prompt, task_type)
            elif operation == "optimize":
                return self._optimize_prompt(prompt, task_type)
            elif operation == "rewrite":
                return self._rewrite_prompt(prompt, task_type)
            elif operation == "score":
                return self._score_prompt(prompt)
            else:
                return self._optimize_prompt(prompt, task_type)
                
        except Exception as e:
            return "Optimization error: " + str(e)
    
    def _analyze_prompt(self, prompt, task_type):
        prompt_lower = prompt.lower()
        words = prompt_lower.split()
        
        weaknesses = []
        for pattern, suggestion in self._weak_patterns:
            if pattern in prompt_lower:
                weaknesses.append("- '" + pattern + "': " + suggestion)
        
        strengths = []
        for pattern, score in self._strong_patterns:
            if pattern in prompt_lower:
                strengths.append("- Contains '" + pattern + "'")
        
        structure_notes = []
        if len(prompt) < 20:
            structure_notes.append("- Very short prompt - add more detail")
        if len(prompt) > 2000:
            structure_notes.append("- Very long prompt - consider condensing")
        if "?" in prompt:
            structure_notes.append("- Contains question format")
        if ":" in prompt:
            structure_notes.append("- Uses structured formatting")
        if "\n" in prompt:
            structure_notes.append("- Multi-line structure")
        
        task_notes = self._check_task_specific(prompt_lower, task_type)
        
        weaknesses_str = "\n".join(weaknesses) if weaknesses else "None found"
        strengths_str = "\n".join(strengths) if strengths else "None detected"
        structure_str = "\n".join(structure_notes) if structure_notes else "Basic structure"
        
        result = "PROMPT ANALYSIS\n\n"
        result += "Original Prompt:\n"
        if len(prompt) > 200:
            result += '"' + prompt[:200] + '..."\n\n'
        else:
            result += '"' + prompt + '"\n\n'
        result += "Statistics:\n"
        result += "- Length: " + str(len(prompt)) + " characters\n"
        result += "- Words: " + str(len(words)) + "\n"
        result += "- Sentences: " + str(prompt.count('.') + prompt.count('!') + prompt.count('?')) + "\n\n"
        result += "Strengths:\n" + strengths_str + "\n\n"
        result += "Weaknesses:\n" + weaknesses_str + "\n\n"
        result += "Structure:\n" + structure_str + "\n\n"
        result += "Task-Specific (" + task_type + "):\n" + task_notes
        
        return result
    
    def _optimize_prompt(self, prompt, task_type):
        analysis = self._analyze_prompt(prompt, task_type)
        suggestions = self._generate_suggestions(prompt, task_type)
        score = self._calculate_score(prompt)
        optimized = self._build_optimized_prompt(prompt, task_type)
        
        result = analysis + "\n\n"
        result += "---\n\n"
        result += "Optimization Suggestions:\n" + suggestions + "\n\n"
        result += "Current Score: " + str(score) + "/100\n\n"
        result += "Optimized Version:\n" + optimized
        
        return result
    
    def _rewrite_prompt(self, prompt, task_type):
        optimized = self._build_optimized_prompt(prompt, task_type)
        original_score = self._calculate_score(prompt)
        new_score = self._calculate_score(optimized)
        improvement = new_score - original_score
        
        result = "PROMPT REWRITE\n\n"
        result += "Original:\n" + prompt + "\n\n"
        result += "Rewritten:\n" + optimized + "\n\n"
        result += "Score Comparison:\n"
        result += "- Original: " + str(original_score) + "/100\n"
        result += "- Rewritten: " + str(new_score) + "/100\n"
        result += "- Improvement: +" + str(improvement) + " points"
        
        return result
    
    def _score_prompt(self, prompt):
        score = self._calculate_score(prompt)
        
        if score >= 90:
            grade = "A+"
        elif score >= 80:
            grade = "A"
        elif score >= 70:
            grade = "B"
        elif score >= 60:
            grade = "C"
        elif score >= 50:
            grade = "D"
        else:
            grade = "F"
        
        clarity = self._score_category(prompt, "clarity")
        context = self._score_category(prompt, "context")
        specificity = self._score_category(prompt, "specificity")
        structure = self._score_category(prompt, "structure")
        actionable = self._score_category(prompt, "actionable")
        
        result = "PROMPT SCORE\n\n"
        result += "Overall: " + str(score) + "/100 (Grade: " + grade + ")\n\n"
        result += "Category Breakdown:\n"
        result += "- Clarity: " + str(clarity) + "/100\n"
        result += "- Context: " + str(context) + "/100\n"
        result += "- Specificity: " + str(specificity) + "/100\n"
        result += "- Structure: " + str(structure) + "/100\n"
        result += "- Actionable: " + str(actionable) + "/100\n\n"
        result += "Prompt:\n"
        if len(prompt) > 150:
            result += '"' + prompt[:150] + '..."'
        else:
            result += '"' + prompt + '"'
        
        return result
    
    def _calculate_score(self, prompt):
        prompt_lower = prompt.lower()
        score = 50
        
        length = len(prompt)
        if 50 <= length <= 500:
            score += 10
        elif 500 < length <= 1500:
            score += 15
        elif length < 20:
            score -= 20
        
        for pattern, bonus in self._strong_patterns:
            if pattern in prompt_lower:
                score += bonus * 3
        
        for pattern, suggestion in self._weak_patterns:
            if pattern in prompt_lower:
                score -= 3
        
        if ":" in prompt:
            score += 5
        if "\n" in prompt:
            score += 5
        
        start_patterns = ["You are", "Act as", "I want you"]
        for p in start_patterns:
            if prompt.strip().startswith(p):
                score += 8
                break
        
        if score < 0:
            score = 0
        if score > 100:
            score = 100
        
        return int(score)
    
    def _score_category(self, prompt, category):
        prompt_lower = prompt.lower()
        score = 40
        
        if category == "clarity":
            if len(prompt) >= 30:
                score += 20
            if "?" not in prompt or prompt.count("?") <= 2:
                score += 10
            if "specifically" in prompt_lower or "exactly" in prompt_lower:
                score += 20
        
        elif category == "context":
            if "you are" in prompt_lower or "act as" in prompt_lower:
                score += 25
            if "background" in prompt_lower or "context" in prompt_lower:
                score += 20
        
        elif category == "specificity":
            if "example" in prompt_lower:
                score += 20
            if "format" in prompt_lower:
                score += 20
            has_digit = False
            for char in prompt:
                if char.isdigit():
                    has_digit = True
                    break
            if has_digit:
                score += 15
        
        elif category == "structure":
            if "\n" in prompt:
                score += 20
            if ":" in prompt:
                score += 15
            if "-" in prompt or "*" in prompt:
                score += 15
        
        elif category == "actionable":
            action_words = ["create", "generate", "write", "explain", "analyze", "list", "provide", "describe"]
            for word in action_words:
                if word in prompt_lower:
                    score += 25
                    break
            if "output" in prompt_lower or "result" in prompt_lower:
                score += 15
        
        if score < 0:
            score = 0
        if score > 100:
            score = 100
        
        return score
    
    def _generate_suggestions(self, prompt, task_type):
        prompt_lower = prompt.lower()
        suggestions = []
        
        if "you are" not in prompt_lower and "act as" not in prompt_lower:
            suggestions.append("1. Add a role: Start with 'You are an expert...'")
        
        if "example" not in prompt_lower:
            suggestions.append("2. Add examples: Include 'For example:...'")
        
        if "format" not in prompt_lower and "output" not in prompt_lower:
            suggestions.append("3. Specify format: Add 'Format the output as...'")
        
        if len(prompt) < 50:
            suggestions.append("4. Add more detail and context")
        
        if "step" not in prompt_lower:
            suggestions.append("5. Request step-by-step reasoning")
        
        if not suggestions:
            suggestions.append("Your prompt follows most best practices!")
        
        return "\n".join(suggestions)
    
    def _check_task_specific(self, prompt_lower, task_type):
        notes = []
        
        if task_type == "coding":
            if "language" not in prompt_lower:
                notes.append("- Specify programming language")
            if "error" not in prompt_lower and "handle" not in prompt_lower:
                notes.append("- Consider error handling requirements")
        
        elif task_type == "creative":
            if "tone" not in prompt_lower and "style" not in prompt_lower:
                notes.append("- Specify tone or style")
            if "length" not in prompt_lower and "word" not in prompt_lower:
                notes.append("- Specify desired length")
        
        elif task_type == "analysis":
            if "data" not in prompt_lower and "source" not in prompt_lower:
                notes.append("- Specify data source")
            if "metric" not in prompt_lower:
                notes.append("- Define metrics or criteria")
        
        elif task_type == "instruction":
            if "step" not in prompt_lower:
                notes.append("- Request step-by-step format")
            if "warning" not in prompt_lower and "caution" not in prompt_lower:
                notes.append("- Consider adding safety notes")
        
        if notes:
            return "\n".join(notes)
        else:
            return "Meets basic task requirements"
    
    def _build_optimized_prompt(self, prompt, task_type):
        prompt_lower = prompt.lower()
        parts = []
        
        if "you are" not in prompt_lower and "act as" not in prompt_lower:
            if task_type == "coding":
                parts.append("You are an expert software developer.")
            elif task_type == "creative":
                parts.append("You are a creative writer.")
            elif task_type == "analysis":
                parts.append("You are a data analyst.")
            else:
                parts.append("You are a helpful assistant.")
        
        parts.append("")
        parts.append(prompt)
        
        if "format" not in prompt_lower and "output" not in prompt_lower:
            parts.append("")
            parts.append("Please provide a clear, well-structured response.")
        
        if "step" not in prompt_lower and task_type in ["coding", "analysis", "instruction"]:
            parts.append("Think through this step by step.")
        
        return "\n".join(parts)