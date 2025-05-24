from deep_translator import GoogleTranslator

def translate(text, src='en', dest='pt'):
    try:
        return GoogleTranslator(source=src, target=dest).translate(text)
    except Exception as e:
        print(f"[translation error] {e}")
        return "[translation error]"