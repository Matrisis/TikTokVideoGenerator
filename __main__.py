import asyncio,tts,os,video,requests
import imp
import sys
import edge_tts
from scraper import scrape
from upload import upload_to_tiktok
from utils import config

async def main():

    args = sys.argv
    lang = args[1] if args[1] else config['lang'] if config['lang'] else None
    sub =  args[2] if args[2] else config['sub'] if config['sub'] else "AskReddit"
    limit_posts =  args[3] if args[3] else config['limit_posts'] if config['limit_posts'] else 5
    limit_comments =  int(args[4] if args[4] else config['limit_comments'] if config['limit_comments'] else 5)

    # Fetching posts from r/AskReddit
    headers = { 'user-agent':'py-reddit-scraping:0:1.0 (by u/ur_name)' }
    url = f"https://www.reddit.com/r/{sub}/top.json?t=day&limit={limit_posts}"
    posts = requests.get(url, headers=headers).json()['data']['children']
    print("Scraping from : " + url)

    for post in posts:
        try:
            # Avoid getting banned, no NSFW posts
            if post['data']['over_18']:
                continue

            url = post['data']['url']
            name = url.split('/')[-2]
            print(f"⏱ Processing post: {name}")

            # Make sure we have not already rendered/uploaded post
            dir = f"render/{lang}"
            if not os.path.exists(dir):
                os.mkdir(dir)
            if name in [entry.split('.')[0] for entry in os.listdir(dir)]:
                print("❌ Post already processed!")
                continue

            # Clean 'temporary' files from last video
            for file in os.listdir('output'):
                os.remove(f'output/{file}')

            # Scraping the post, screenshotting, etc
            print("Url : " + url)
            print("📸 Screenshotting post...")
            data = scrape(url, lang, limit_comments)
            if not data:
                print("❌ Failed to screenshot post!")
                continue

            # Generate TTS clips for each comment
            print("\n📢 Generating voice clips...", end="", flush=True)
            voice = await tts.get_voice(lang)
            for key in data.keys():
                print('.',end="",flush=True)
                await tts.generate(text=data[key], name=key, voice=voice)

            # Render & Upload
            print("\n🎥 Rendering video...")
            if video.render(name, lang, limit_comments, "post_content" in data.keys()):
                # Upload video if rendered
                print("Video Rendered !")
                '''
                print("🌟 Uploading to TikTok...")
                if upload_to_tiktok(name, data["post"]):
                    print("✅ Uploaded successfully!")
                else:
                    print("❌ Failed to upload!")
                '''
        except Exception as e:
            if config['debug']:
                raise e
            pass

if __name__ == '__main__':
    [os.mkdir(dir) for dir in ['output','render','backgrounds'] if not os.path.exists(dir)]
    asyncio.run(main())

