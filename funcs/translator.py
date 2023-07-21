from deep_translator import GoogleTranslator, DeeplTranslator
from . import utils


def translate_text(text, lang):
    return GoogleTranslator(source='auto', target=lang.split("-")[0]).translate(text)

def translate_text_deepl(text, lang, original_lang="en"):
    return DeeplTranslator(api_key=utils.config['deepl_api_key'],
                           source=original_lang.split("-")[0],
                           target=lang.split("-")[0], use_free_api=True).translate(text)