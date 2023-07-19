from deep_translator import GoogleTranslator, DeeplTranslator
from utils import config


def translate_text(text, lang):
    return GoogleTranslator(source='auto', target=lang.split("-")[0]).translate(text)

def translate_text_deepl(text, lang):
    return DeeplTranslator(api_key=config['deepl_api_key'], source="en", target=lang.split("-")[0], use_free_api=True).translate(text)