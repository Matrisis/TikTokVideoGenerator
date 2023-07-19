import random
import edge_tts
from edge_tts import VoicesManager

async def get_voice(lang = "en-US"):
    voices = [voice for voice in await edge_tts.list_voices() if lang in voice["Locale"] and voice["Gender"] == "Male"]
    return random.choice(voices)["ShortName"]

async def generate(text, name, voice):
    communicate = edge_tts.Communicate(text=text, voice=voice)
    await communicate.save("output/" + name + ".mp3")
