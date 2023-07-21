from funcs import whisper, utils, translator, tts, video_maker
import re
from num2words import num2words


async def remaker(args):
    file = args.file
    lang = args.lang if args.lang else utils.config['lang'] if utils.config['lang'] else None
    original_lang = args.fromlang
    option = args.option
    elabs = args.elevenlabs

    print("Remaking video...")

    print("⏱ Extracting text...")
    text = whisper.video_to_text(file, option, original_lang)

    print("⏱ Translating text...")
    #text = translator.translate_text_deepl(text, lang, original_lang)
    text = translator.translate_text(text, lang)
    text = " ".join([num2words(word, lang=lang.split("-")[0]) if word.isdigit() else word for word in text.split()])


    print("📢 Generating voice clips...", end="", flush=True)
    text_split = text.split(".")
    sentences = []
    audio_clips = []
    for i in range(0, len(text_split), 3):
        sentences.append('.'.join(text_split[i:i + 3]))
    for index, sentence in enumerate(sentences):
        if elabs:
            audio_clips.append(await tts.generate_el(sentence, f"remaker_voice-{index}", lang, concat=False))
        else:
            voice = await tts.get_voice(lang)
            print('.', end="", flush=True)
            audio_clips.append(await tts.generate(text=sentence, name=f"remaker_voice-{index}", voice=voice, concat=False))

    print("🎥 Rendering video...")
    if video_maker.render_remaker(audio_clips, lang=lang):
        print("Video Rendered !")


