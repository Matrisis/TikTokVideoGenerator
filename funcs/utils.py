import yaml
import undetected_chromedriver as uc

# Load and validate config
config = yaml.safe_load(open('config.yaml').read())

if not config['tiktok_cookies']:
    raise Exception('Missing TikTok Cookies')

if not config['reddit_cookies']:
    raise Exception('Missing Reddit Cookies')

def cleanup(text):
    result_text = []
    for sentence in text.split("."):
        if "emoji" in sentence:
            sentence = ": Comment your birthdate to see your birthday twins"
        if "type" in sentence:
            sentence = "Can you type your name with your phone upside down ? Show me in the comments"
        if "music" in sentence:
            sentence = "The music you listen to, affects your mood and the way you see the world"
        elif "follow" in sentence or "subscribe" in sentence:
            sentence =  "Don't forget to subscribe to learn more"
        elif "share" in sentence or "three dots" in sentence or "icon" in sentence:
            sentence = "Your best friends are probably the persons you see first when clicking share. Share them this video to tell them"
        result_text.append(sentence)
        result_text = [i for i in result_text if i]
    return (".").join(result_text)

def filter_sentences(sentences):
    updated_sentences = []
    for sentence in sentences.split("."):
        print(f'Current sentence: {sentence}')
        action = input('Do you want to keep this sentence? (yes/no): ')
        if action.lower() == 'yes' or action.lower() == 'y':
            updated_sentences.append(sentence)
        else:
            new_sentence = input('Please enter a new sentence to replace the current one: ')
            updated_sentences.append(new_sentence)
    return (".").join(updated_sentences)


def create_bot(headless=False):
    options = uc.ChromeOptions()
    options.add_argument("--log-level=3")
    options.add_argument('disable-infobars')
    if headless:
        options.headless = True

    bot = uc.Chrome(options=options)

    bot.set_page_load_timeout(25)
    bot.set_window_size(1920, 1080)
    return bot