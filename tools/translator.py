"""
Translator Tool - Translate text between languages.
"""

from .base_tool import BaseTool


class TranslatorTool(BaseTool):
    """Translate text between different languages."""
    
    def __init__(self):
        super().__init__()
        self.name = "translator"
        self.description = "Translate text between languages. Supports detection, translation, and common phrases."
        
        self.parameters = {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Text to translate"
                },
                "source_lang": {
                    "type": "string",
                    "description": "Source language code (e.g., en, es, fr, de, hi, ja)",
                    "default": "auto"
                },
                "target_lang": {
                    "type": "string",
                    "description": "Target language code",
                    "default": "en"
                },
                "operation": {
                    "type": "string",
                    "enum": ["translate", "detect", "languages", "phrases"],
                    "description": "Operation to perform",
                    "default": "translate"
                }
            },
            "required": ["text"]
        }
        
        self._languages = {
            "en": "English",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "it": "Italian",
            "pt": "Portuguese",
            "ru": "Russian",
            "ja": "Japanese",
            "ko": "Korean",
            "zh": "Chinese",
            "ar": "Arabic",
            "hi": "Hindi",
            "bn": "Bengali",
            "pa": "Punjabi",
            "ta": "Tamil",
            "te": "Telugu",
            "mr": "Marathi",
            "gu": "Gujarati",
            "kn": "Kannada",
            "ml": "Malayalam",
            "th": "Thai",
            "vi": "Vietnamese",
            "id": "Indonesian",
            "ms": "Malay",
            "tr": "Turkish",
            "pl": "Polish",
            "uk": "Ukrainian",
            "nl": "Dutch",
            "sv": "Swedish",
            "da": "Danish",
            "no": "Norwegian",
            "fi": "Finnish",
            "el": "Greek",
            "he": "Hebrew",
            "cs": "Czech",
            "ro": "Romanian",
            "hu": "Hungarian",
            "sk": "Slovak",
            "bg": "Bulgarian",
            "hr": "Croatian",
            "sr": "Serbian",
            "sl": "Slovenian",
            "et": "Estonian",
            "lv": "Latvian",
            "lt": "Lithuanian",
            "fa": "Persian",
            "ur": "Urdu",
            "sw": "Swahili"
        }
        
        self._common_phrases = {
            "hello": {
                "es": "hola",
                "fr": "bonjour",
                "de": "hallo",
                "it": "ciao",
                "pt": "olá",
                "ru": "привет",
                "ja": "こんにちは",
                "ko": "안녕하세요",
                "zh": "你好",
                "ar": "مرحبا",
                "hi": "नमस्ते"
            },
            "goodbye": {
                "es": "adiós",
                "fr": "au revoir",
                "de": "auf wiedersehen",
                "it": "arrivederci",
                "pt": "adeus",
                "ru": "до свидания",
                "ja": "さようなら",
                "ko": "안녕히 가세요",
                "zh": "再见",
                "ar": "وداعا",
                "hi": "अलविदा"
            },
            "thank you": {
                "es": "gracias",
                "fr": "merci",
                "de": "danke",
                "it": "grazie",
                "pt": "obrigado",
                "ru": "спасибо",
                "ja": "ありがとう",
                "ko": "감사합니다",
                "zh": "谢谢",
                "ar": "شكرا",
                "hi": "धन्यवाद"
            },
            "yes": {
                "es": "sí",
                "fr": "oui",
                "de": "ja",
                "it": "sì",
                "pt": "sim",
                "ru": "да",
                "ja": "はい",
                "ko": "네",
                "zh": "是",
                "ar": "نعم",
                "hi": "हाँ"
            },
            "no": {
                "es": "no",
                "fr": "non",
                "de": "nein",
                "it": "no",
                "pt": "não",
                "ru": "нет",
                "ja": "いいえ",
                "ko": "아니요",
                "zh": "不",
                "ar": "لا",
                "hi": "नहीं"
            },
            "please": {
                "es": "por favor",
                "fr": "s'il vous plaît",
                "de": "bitte",
                "it": "per favore",
                "pt": "por favor",
                "ru": "пожалуйста",
                "ja": "お願いします",
                "ko": "제발",
                "zh": "请",
                "ar": "من فضلك",
                "hi": "कृपया"
            },
            "sorry": {
                "es": "lo siento",
                "fr": "désolé",
                "de": "entschuldigung",
                "it": "scusa",
                "pt": "desculpe",
                "ru": "извините",
                "ja": "ごめんなさい",
                "ko": "미안합니다",
                "zh": "对不起",
                "ar": "آسف",
                "hi": "माफ़ कीजिए"
            },
            "how are you": {
                "es": "¿cómo estás?",
                "fr": "comment allez-vous?",
                "de": "wie geht es dir?",
                "it": "come stai?",
                "pt": "como você está?",
                "ru": "как дела?",
                "ja": "お元気ですか？",
                "ko": "어떻게 지내세요?",
                "zh": "你好吗？",
                "ar": "كيف حالك؟",
                "hi": "आप कैसे हैं?"
            },
            "good morning": {
                "es": "buenos días",
                "fr": "bonjour",
                "de": "guten morgen",
                "it": "buongiorno",
                "pt": "bom dia",
                "ru": "доброе утро",
                "ja": "おはようございます",
                "ko": "좋은 아침",
                "zh": "早上好",
                "ar": "صباح الخير",
                "hi": "सुप्रभात"
            },
            "good night": {
                "es": "buenas noches",
                "fr": "bonne nuit",
                "de": "gute nacht",
                "it": "buonanotte",
                "pt": "boa noite",
                "ru": "спокойной ночи",
                "ja": "おやすみなさい",
                "ko": "안녕히 주무세요",
                "zh": "晚安",
                "ar": "تصبح على خير",
                "hi": "शुभ रात्रि"
            }
        }
        
        self._char_patterns = {
            "ja": r"[\u3040-\u30ff\u4e00-\u9fff]",
            "ko": r"[\uac00-\ud7af\u1100-\u11ff]",
            "zh": r"[\u4e00-\u9fff]",
            "ar": r"[\u0600-\u06ff]",
            "he": r"[\u0590-\u05ff]",
            "hi": r"[\u0900-\u097f]",
            "th": r"[\u0e00-\u0e7f]",
            "ru": r"[\u0400-\u04ff]",
            "el": r"[\u0370-\u03ff]"
        }
    
    def execute(self, text, source_lang="auto", target_lang="en", operation="translate"):
        try:
            if not text or not text.strip():
                return "Please provide text to translate."
            
            text = text.strip()
            
            if operation == "translate":
                return self._translate(text, source_lang, target_lang)
            elif operation == "detect":
                return self._detect_language(text)
            elif operation == "languages":
                return self._list_languages()
            elif operation == "phrases":
                return self._common_phrases_list(target_lang)
            else:
                return self._translate(text, source_lang, target_lang)
                
        except Exception as e:
            return "Translation error: " + str(e)
    
    def _translate(self, text, source_lang, target_lang):
        if source_lang == "auto":
            source_lang = self._detect_language_code(text)
        
        source_name = self._languages.get(source_lang, source_lang)
        target_name = self._languages.get(target_lang, target_lang)
        
        text_lower = text.lower().strip()
        
        if text_lower in self._common_phrases:
            if target_lang in self._common_phrases[text_lower]:
                translated = self._common_phrases[text_lower][target_lang]
                
                result = "TRANSLATION\n"
                result += "=" * 50 + "\n\n"
                result += "Source (" + source_name + "):\n"
                result += text + "\n\n"
                result += "Target (" + target_name + "):\n"
                result += translated + "\n\n"
                result += "Method: Phrase dictionary\n"
                return result
        
        try:
            import requests
            
            url = "https://api.mymemory.translated.net/get"
            params = {
                "q": text,
                "langpair": source_lang + "|" + target_lang
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("responseStatus") == 200:
                    translated = data["responseData"]["translatedText"]
                    
                    result = "TRANSLATION\n"
                    result += "=" * 50 + "\n\n"
                    result += "Source (" + source_name + "):\n"
                    result += text + "\n\n"
                    result += "Target (" + target_name + "):\n"
                    result += translated + "\n\n"
                    result += "Method: MyMemory API\n"
                    return result
        except Exception:
            pass
        
        result = "TRANSLATION REQUEST\n"
        result += "=" * 50 + "\n\n"
        result += "Source language: " + source_name + " (" + source_lang + ")\n"
        result += "Target language: " + target_name + " (" + target_lang + ")\n\n"
        result += "Original text:\n"
        result += text + "\n\n"
        result += "Note: Online translation unavailable.\n"
        result += "Please use an online translator for accurate results.\n\n"
        result += "Suggested services:\n"
        result += "- Google Translate: translate.google.com\n"
        result += "- DeepL: deepl.com\n"
        result += "- Microsoft Translator: translator.microsoft.com\n"
        
        return result
    
    def _detect_language(self, text):
        import re
        
        detected = self._detect_language_code(text)
        lang_name = self._languages.get(detected, "Unknown")
        
        scores = {}
        
        for lang, pattern in self._char_patterns.items():
            matches = len(re.findall(pattern, text))
            if matches > 0:
                scores[lang] = matches
        
        result = "LANGUAGE DETECTION\n"
        result += "=" * 50 + "\n\n"
        
        result += "Text sample:\n"
        if len(text) > 100:
            result += text[:100] + "...\n\n"
        else:
            result += text + "\n\n"
        
        result += "Detected language: " + lang_name + " (" + detected + ")\n\n"
        
        if scores:
            result += "Character analysis:\n"
            result += "-" * 30 + "\n"
            
            sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            for lang, score in sorted_scores[:5]:
                lang_name_score = self._languages.get(lang, lang)
                result += lang_name_score + ": " + str(score) + " matching characters\n"
        
        result += "\n"
        result += "Text statistics:\n"
        result += "-" * 30 + "\n"
        result += "Characters: " + str(len(text)) + "\n"
        result += "Words: " + str(len(text.split())) + "\n"
        
        return result
    
    def _detect_language_code(self, text):
        import re
        
        for lang, pattern in self._char_patterns.items():
            if re.search(pattern, text):
                return lang
        
        text_lower = text.lower()
        
        spanish_words = ["el", "la", "los", "las", "un", "una", "que", "de", "en", "es", "por", "con"]
        french_words = ["le", "la", "les", "un", "une", "de", "et", "est", "que", "dans", "pour"]
        german_words = ["der", "die", "das", "und", "ist", "ein", "eine", "nicht", "mit", "auf"]
        italian_words = ["il", "la", "che", "di", "un", "una", "non", "per", "sono", "come"]
        portuguese_words = ["o", "a", "os", "as", "um", "uma", "que", "de", "em", "para"]
        
        words = text_lower.split()
        
        lang_scores = {
            "es": sum(1 for w in words if w in spanish_words),
            "fr": sum(1 for w in words if w in french_words),
            "de": sum(1 for w in words if w in german_words),
            "it": sum(1 for w in words if w in italian_words),
            "pt": sum(1 for w in words if w in portuguese_words)
        }
        
        max_lang = max(lang_scores, key=lang_scores.get)
        if lang_scores[max_lang] > 0:
            return max_lang
        
        return "en"
    
    def _list_languages(self):
        result = "SUPPORTED LANGUAGES\n"
        result += "=" * 50 + "\n\n"
        
        result += "Total languages: " + str(len(self._languages)) + "\n\n"
        
        result += "CODE  | LANGUAGE\n"
        result += "-" * 30 + "\n"
        
        sorted_langs = sorted(self._languages.items(), key=lambda x: x[1])
        
        for code, name in sorted_langs:
            result += code.ljust(6) + "| " + name + "\n"
        
        result += "\n"
        result += "Usage example:\n"
        result += "  Translate from English to Spanish:\n"
        result += "  source_lang='en', target_lang='es'\n"
        
        return result
    
    def _common_phrases_list(self, target_lang):
        target_name = self._languages.get(target_lang, target_lang)
        
        result = "COMMON PHRASES\n"
        result += "=" * 50 + "\n\n"
        
        result += "Target language: " + target_name + " (" + target_lang + ")\n\n"
        
        result += "PHRASE".ljust(20) + "| TRANSLATION\n"
        result += "-" * 50 + "\n"
        
        for phrase, translations in self._common_phrases.items():
            translation = translations.get(target_lang, "N/A")
            result += phrase.ljust(20) + "| " + translation + "\n"
        
        result += "\n"
        result += "These are basic phrases. For complex translations,\n"
        result += "use the translate operation.\n"
        
        return result