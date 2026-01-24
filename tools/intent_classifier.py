"""
Intent Classifier Tool - Classify user intent from text using AI Pipe.

Powered by AI Pipe for accurate, context-aware intent classification.
"""

from .ai_tool import BaseAITool


class IntentClassifierTool(BaseAITool):
    """Classify the intent of user text using AI Pipe."""
    
    def __init__(self):
        super().__init__()
        self.name = "intent_classifier"
        self.description = "Classify user text into intent categories like question, command, greeting, complaint, feedback, etc. Uses AI Pipe for accurate semantic understanding."
        
        self.parameters = {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Text to classify"
                },
                "custom_intents": {
                    "type": "string",
                    "description": "Comma-separated custom intent categories (optional)"
                }
            },
            "required": ["text"]
        }
    
    def system_prompt(self) -> str:
        """System prompt for intent classification."""
        return (
            "You are an expert at understanding user intent and intent classification. "
            "Analyze the provided text and determine the user's primary intent.\n\n"
            "Default intent categories:\n"
            "- question: User is asking something\n"
            "- command: User is asking to perform an action\n"
            "- greeting: User is greeting or saying hello\n"
            "- farewell: User is saying goodbye\n"
            "- gratitude: User is thanking or expressing appreciation\n"
            "- complaint: User is expressing a problem or dissatisfaction\n"
            "- feedback: User is providing feedback or suggestions\n"
            "- confirmation: User is confirming something\n"
            "- denial: User is refusing or disagreeing\n"
            "- information: User is providing or requesting information\n"
            "- request: User is making a request\n"
            "- apology: User is apologizing\n\n"
            "Respond in this exact JSON format:\n"
            "{\n"
            '  "primary_intent": "intent_name",\n'
            '  "confidence": 85,\n'
            '  "alternative_intents": ["intent1", "intent2"],\n'
            '  "reasoning": "why this intent",\n'
            '  "keywords": ["word1", "word2"]\n'
            "}\n"
            "Only respond with valid JSON, no other text."
        )
    
    def build_prompt(self, text: str, custom_intents: str = None, **kwargs) -> str:
        """Build prompt for intent classification."""
        prompt = f"Classify the intent of this text: \"{text}\""
        
        if custom_intents:
            intents = [i.strip() for i in custom_intents.split(",")]
            custom_list = ", ".join(intents)
            prompt += f"\n\nAlso consider these custom intents: {custom_list}"
        
        return prompt
    
    def parse_response(self, response: str) -> str:
        """Parse AI response into formatted output."""
        import json
        
        try:
            # Extract JSON from response
            json_str = response.strip()
            if json_str.startswith("```"):
                json_str = json_str.split("```")[1]
                if json_str.startswith("json"):
                    json_str = json_str[4:]
            
            data = json.loads(json_str)
            
            primary = data.get("primary_intent", "unknown").upper()
            confidence = data.get("confidence", 0)
            reasoning = data.get("reasoning", "")
            keywords = data.get("alternative_intents", [])
            found_keywords = data.get("keywords", [])
            
            # Confidence emoji
            if confidence >= 80:
                conf_emoji = "🟢"
            elif confidence >= 60:
                conf_emoji = "🟡"
            else:
                conf_emoji = "🔴"
            
            # Format output
            alt_intents = "\n".join([f"  - {k}" for k in keywords]) if keywords else "  None"
            keywords_str = ", ".join(found_keywords) if found_keywords else "None"
            
            return f"""🎯 **Intent Classification**

**Primary Intent:** **{primary}**
**Confidence:** {conf_emoji} {confidence}%

**Reasoning:** {reasoning}

**Alternative Intents:**
{alt_intents}

**Key Words:** {keywords_str}"""
            
        except json.JSONDecodeError:
            # If JSON parsing fails, return raw response
            return f"🎯 **Intent Classification Result:**\n\n{response}"