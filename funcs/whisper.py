from moviepy.editor import VideoFileClip
import replicate
import os
from funcs import utils


def video_to_text(path, initial_prompt, lang="en"):
    video = VideoFileClip(path)
    transcribe_path = "output/transcribing.mp3"
    video.audio.write_audiofile(transcribe_path)
    os.environ["REPLICATE_API_TOKEN"] = utils.config['replicate_api_key']
    print("Reading text...")
    text = replicate.run(
        "openai/whisper:91ee9c0c3df30478510ff8c8a3a545add1ad0259ad3a9f78fba57fbc05ee64f7",
        input={
            "language": lang.split("-")[0],
            "audio": open(transcribe_path, "rb"),
            "initial_prompt" : initial_prompt if initial_prompt
            else "Random facts. I am a random fact. I am a second random fact, i am details about that fact."
        }
    )
    os.remove(transcribe_path)
    return initial_prompt + text['transcription']
