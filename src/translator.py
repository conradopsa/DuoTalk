from deep_translator import GoogleTranslator
from backoff import on_exception, expo

@on_exception(expo, Exception, max_tries=5, base=1, max_value=60)
def translate(text, src='en', dest='pt'):
    return GoogleTranslator(source=src, target=dest).translate(text)
    