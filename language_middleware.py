import json
from deep_translator import GoogleTranslator
from functools import wraps

class LanguageMiddleware:
    """Middleware to handle language in AI requests"""
    
    def __init__(self, default_language='en'):
        self.default_language = default_language
        
    def extract_language(self, request_data):
        """Extract language from request"""
        language_keys = ['language', 'language_code', 'user_language', 'lang']
        
        for key in language_keys:
            if key in request_data:
                lang = request_data[key]
                if lang in ['en', 'hi', 'ja', 'ar', 'ru', 'fr', 'es', 'de', 'pt', 'zh']:
                    return lang
        
        return self.default_language
    
    def translate_ai_response(self, text, target_lang):
        """Translate AI response text"""
        if target_lang == 'en' or not text:
            return text
            
        try:
            translator = GoogleTranslator(source='auto', target=target_lang)
            return translator.translate(text)
        except Exception as e:
            print(f"Translation error: {e}")
            return text
    
    def translate_response_dict(self, data, target_lang):
        """Recursively translate response dictionary"""
        if isinstance(data, str):
            return self.translate_ai_response(data, target_lang)
        elif isinstance(data, dict):
            # Don't translate keys, only values
            translated = {}
            for key, value in data.items():
                # Skip translation for certain keys
                if key in ['id', 'code', 'status', 'score', 'accuracy', 'probability', 'timestamp']:
                    translated[key] = value
                else:
                    translated[key] = self.translate_response_dict(value, target_lang)
            return translated
        elif isinstance(data, list):
            return [self.translate_response_dict(item, target_lang) for item in data]
        else:
            return data
    
    def wrap_ai_endpoint(self, func):
        """Decorator for AI endpoints"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get request data
            request_data = kwargs.get('data', {}) or args[0] if args else {}
            
            # Extract language
            language = self.extract_language(request_data)
            
            # Call original AI function
            result = func(*args, **kwargs)
            
            # Translate if needed
            if language != 'en':
                result = self.translate_response_dict(result, language)
            
            # Add language info to response
            if isinstance(result, dict):
                result['response_language'] = language
                result['original_language'] = 'en'
            
            return result
        return wrapper

# Create instance
language_middleware = LanguageMiddleware()

# Usage example:
@language_middleware.wrap_ai_endpoint
def analyze_symptoms(data):
   
    result = ai_model.predict(data['symptoms'])
    return result