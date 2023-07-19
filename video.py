from moviepy.editor import *
import random,os
from utils import config

resolution = (1080,1920)

def render(name, lang, limit_comments, post_content):
    # Create clip 'flow'
    flow = ['post', 'cta']
    if post_content:
        flow.append('post_content')
    for i in range(limit_comments):
        if os.path.exists(f'output/{i}.mp3'):
            flow.append(str(i))

    # Load all the clips
    clips = []
    duration = 0
    for part in flow:
        audio = AudioFileClip(f"output/{part}.mp3")
        clip = ImageClip(f"output/{part}.png").set_duration(audio.duration).fx(vfx.resize,width=resolution[0]*0.9).set_position(("center","center"))
        clip = clip.set_audio(audio)
        clips.append(clip)
        if duration > 90:
            break

    # Combine all the clips into one
    image_clips = concatenate_videoclips(clips).set_position(("center","center"))

    #Loading background
    background_clip = "backgrounds/" + random.choice(os.listdir("backgrounds"))
    background = VideoFileClip(background_clip, audio=False).fx(vfx.resize, height=resolution[1]).fx(vfx.loop, duration=image_clips.duration).set_position(("center","center"))

    # Composite all the components
    composite = CompositeVideoClip([background,image_clips], resolution)
    # Render
    composite.write_videofile(f'render/{lang}/{name}.mp4',threads=config['render_threads'],fps=60)
    return True
