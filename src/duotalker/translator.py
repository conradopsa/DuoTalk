from deep_translator import GoogleTranslator
from backoff import on_exception, expo

@on_exception(expo, Exception, max_tries=5, base=1, max_value=60)
def translate(text, src='en', dest='pt'):
    if not text:
        return text  # evita erro com string vazia

    startsWithLower = text[0].islower()

    translated = GoogleTranslator(source=src, target=dest).translate(text)

    if startsWithLower and translated:
        translated = translated[0].lower() + translated[1:]

    return translated
    