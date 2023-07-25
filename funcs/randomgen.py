from num2words import num2words

from funcs import utils, script, translator, video_maker, tts


async def randomgen(args):
    print("Starting random facts generation...")
    lang = args.lang if args.lang else utils.config['lang'] if utils.config['lang'] else None
    elabs = args.elevenlabs
    facts_number = args.facts if args.facts else 7
    option = args.option

    print("Generating random facts...")
    facts = script.get_random_phrases("scripts/script.json", facts_number)
    ctas =  script.get_random_phrases("scripts/cta.json", round(facts_number / 2))
    final_facts = script.integrate_phrases(facts, ctas)
    text = (" ").join(["Random facts."] + final_facts + ["Don't forget to subscribe to learn more."])

    print("Translating random facts...")
    #text = translator.translate_text_deepl(text, lang)
    text = translator.translate_text(text, lang)
    text = " ".join([num2words(word, lang=lang.split("-")[0]) if word.isdigit() else word for word in text.split()])

    print("📢 Generating voice clips...", end="", flush=True)
    text_split = text.split(".")
    text_split = [i for i in text_split if i]
    audio_clips = []
    for index, sentence in enumerate(text_split):
        sentence = sentence.replace(".", "")
        sentence = sentence + "."
        if elabs:
            audio_clips.append(tts.generate_el(sentence, f"randomgen_voice-{index}", lang, concat=False))
        else:
            voice = await tts.get_voice(lang)
            print('.', end="", flush=True)
            audio_clips.append(
                await tts.generate(text=sentence, name=f"randomgen_voice-{index}", voice=voice, concat=False))
    print("🎥 Rendering video...")
    if video_maker.render_remaker(audio_clips, lang=lang, dir="randomgen"):
        print("Video Rendered !")