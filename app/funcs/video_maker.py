import uuid

from moviepy.editor import *
import random, os

from . import utils

resolution = (1080, 1920)

def render_remaker(audio_files, video_dir="backgrounds/", lang="en-EN", dir="remaker"):
    video_files = [os.path.join(video_dir, file) for file in os.listdir(video_dir) if file.endswith('.mp4')]
    video_clips = []
    prev_video_files = []

    # We need to iterate over audio_files in groups of three
    first = True
    for i in range(0, len(audio_files), 2):
        audio_group = audio_files[i:i+2]

        # Concatenate three audios into one
        audios = [AudioFileClip(audio) for audio in audio_group]
        audio = concatenate_audioclips(audios)

        # Audio fadein
        audio = audio.fx(afx.audio_fadein, 0.3)

        # Choose a video file, excluding the previously used file
        available_files = [f for f in video_files if f not in prev_video_files]
        video_file = random.choice(available_files)

        video = VideoFileClip(video_file, audio=False)

        # Trim audio or video if they are not of the same duration
        #if video.duration < audio.duration:
        #    audio = audio.subclip(0, video.duration)
        #else:
        video = video.subclip(0, audio.duration)

        # Add the audio to the muted video
        video = video.set_audio(audio)

        # Convert video to consistent fps
        video = video.set_fps(60)

        # Apply fade in
        if not first:
            video = video.fx(vfx.fadein, 0.3).fx(vfx.fadeout, 0.3)
        else:
            first = False

        # Append the video clip to the list
        video_clips.append(video)

        # Remember the video file for next iteration
        prev_video_files.append(video_file)

    # Concatenate all video clips
    final_video = concatenate_videoclips(video_clips)

    # Write the result to a file
    final_video.write_videofile(
        f'render/{dir}/{lang}/{uuid.uuid4()}.mp4',
        threads=utils.config['render_threads'],
        audio_codec="aac",
        fps=60)

    # Remove audio files after processing
    for c in audio_files:
        os.remove(c)

    return True



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
        clip = ImageClip(f"output/{part}.png").set_duration(audio.duration).fx(vfx.resize,
                                                                               width=resolution[0] * 0.9).set_position(
            ("center", "center"))
        clip = clip.set_audio(audio)
        clips.append(clip)
        if duration > 90:
            break

    # Combine all the clips into one
    image_clips = concatenate_videoclips(clips).set_position(("center", "center"))

    # Loading background
    background_clip = "backgrounds/" + random.choice(os.listdir("backgrounds"))
    background = VideoFileClip(background_clip, audio=False).fx(vfx.resize, height=resolution[1]).fx(vfx.loop,
                                                                                                     duration=image_clips.duration).set_position(
        ("center", "center"))

    # Composite all the components
    composite = CompositeVideoClip([background, image_clips], resolution)
    # Render
    composite.write_videofile(
        f'render/reddit/{lang}/{name}.mp4',
          audio_codec="aac",
          threads=utils.config['render_threads'],
          fps=60)
    return True
