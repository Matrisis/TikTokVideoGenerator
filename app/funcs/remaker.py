from app.funcs import whisper, utils, tts, translator, video_maker
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
    text = utils.cleanup(text)
    text = utils.filter_sentences(text)

    print("⏱ Translating text...")
    text = translator.translate_text_deepl(text, lang, original_lang)
    #text = translator.translate_text(text, lang)
    text = " ".join([num2words(word, lang=lang.split("-")[0]) if word.isdigit() else word for word in text.split()])

    print("📢 Generating voice clips...", end="", flush=True)
    text_split = text.split(".")
    text_split = [i for i in text_split if i]
    audio_clips = []
    for index, sentence in enumerate(text_split):
        if elabs:
            audio_clips.append(await tts.generate_el(sentence, f"remaker_voice-{index}", lang, concat=False))
        else:
            voice = await tts.get_voice(lang)
            print('.', end="", flush=True)
            audio_clips.append(await tts.generate(text=sentence, name=f"remaker_voice-{index}", voice=voice, concat=False))
    print("🎥 Rendering video...")
    if video_maker.render_remaker(audio_clips, lang=lang):
        print("Video Rendered !")


