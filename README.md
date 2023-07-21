# TikTok Video Maker
Automatic content bot using Selenium to scrape Reddit and render videos with MoviePY.

# Requirements
You need to have the latest version of google chrome installed on your PC.

# Usage
Requires some manual setup, 
1. Install pip packages from `requirements.txt`. `pip install -r requirements.txt`
2. Run `cp config.yaml.example config.yaml`
3Get cookies for TikTok & Reddit
   1. Sign into TikTok in your browser by choice
   2. Open DevTools and go to the network tab
   3. Reload the page and find the sent cookie header
   4. Copy the header and save to `tiktok_cookies` in `config.yaml`
   5. Repeat for Reddit, however there is no need to sign in, only accept cookies to get rid of notice (`reddit_cookies` this time)
4. Add background video files to `backgrounds` folder, find some [here](https://www.pexels.com/videos/)
5. Put config data in config.yaml
6. Run the code using `python  __main__.py`
7. You can run `python  __main__.py {subreddit} {posts_numbers} {comments_numbers}` to specify data directly.
4. Enjoy!
