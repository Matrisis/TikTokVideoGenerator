import asyncio
import os
import argparse

from funcs.reddit import reddit
from funcs.remaker import remaker
from funcs.randomgen import randomgen

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Tiktok video generator",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--func", type=str, default="reddit", help="Function to use. (default: reddit)")
    parser.add_argument("-l", "--lang", type=str, default="fr-FR", help="Destination language. (default : fr-FR)")
    parser.add_argument("-fl", "--fromlang", type=str, default="en-EN", help="Original language. (default : en-EN)")
    parser.add_argument("--subreddit", type=str, default="AskReddit", help="if used with reddit function : Subreddit. (default : AskReddit)")
    parser.add_argument("--lp", type=int, default=5, help="if used with reddit function : Posts limit. (default : 5)")
    parser.add_argument("--lc", type=int, default=5, help="if used with reddit function : Comments limit. (default : 5)")
    parser.add_argument("--file", type=str, default="output/")
    parser.add_argument("--elevenlabs", type=bool, default=False)
    parser.add_argument("--option", default=None)
    parser.add_argument("--facts", type=int, default=7)
    args = parser.parse_args()

    if args.func in locals():
        print(f"Starting {args.func}.")
        [os.mkdir(dir) for dir in [
            'output', 'render', 'render/reddit', 'render/remaker', 'render/randomgen', 'backgrounds'
        ] if not os.path.exists(dir)]
        asyncio.run(locals()[args.func](args))
    else:
        print("Unknown function !")