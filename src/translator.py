from deep_translator import GoogleTranslator
from backoff import on_exception, expo

@on_exception(expo, Exception, max_tries=5, base=1, max_value=60)
def translate(text, src='en', dest='pt'):
    startsWithLower = text[0].islower()
    
    translated = GoogleTranslator(source=src, target=dest).translate(text)
    
    if startsWithLower:
        translated[0] = translated[0].lower()
        
    return 
    