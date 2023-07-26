import random
import edge_tts

from . import utils
from elevenlabs import set_api_key, generate as el_generate, save


async def get_voice(lang = "en-US"):
    voices = [voice for voice in await edge_tts.list_voices() if lang in voice["Locale"] and voice["Gender"] == "Male"]
    return random.choice(voices)["ShortName"]

async def generate(text, name, voice, concat=True):
    path = f"output/{name}.mp3"
    communicate = edge_tts.Communicate(text=text, voice=voice)
    await communicate.save(path)
    return path



def req_el(sentence, lang, path, rep=0):
    '''
    Try to create infinite free eleven labs requests.
    Use api key with a premium account to get faster result
    '''
    audio = el_generate(
        text=sentence,
        voice="Josh",
        model='eleven_monolingual_v1' if lang == "en" else 'eleven_multilingual_v1',
    )
    save(audio, path)



def generate_el(text, name, lang, concat=True):
    # Uncomment the line below to use eleven labs pro with api key
    set_api_key(utils.config['eleven_labs_api_key'])
    path = f"output/{name}.mp3"
    req_el(text, lang, path)
    return path