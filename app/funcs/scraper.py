import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from . import utils, translator

def scrape(post_url, lang = "en", limit_comments=5):
    print("Scrapping...")
    bot = utils.create_bot(headless=True)
    data = {}
    
    try:
        print("Connecting to Reddit...")
        # Load cookies to prevent cookie overlay & other issues
        bot.get('https://www.reddit.com')
        for cookie in utils.config['reddit_cookies'].split('; '):
            cookie_data = cookie.split('=')
            bot.add_cookie({'name':cookie_data[0],'value':cookie_data[1],'domain':'reddit.com'})
        bot.get(post_url)

        # Fetching the post itself, text & screenshot
        print("Accessing post...")
        post = WebDriverWait(bot, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.Post')))
        post_text = post.find_element(By.CSS_SELECTOR, 'h1')
        translated_text = translator.translate_text_deepl(post_text.text, lang)
        bot.execute_script("arguments[0].innerHTML = arguments[1];", post_text, translated_text.capitalize())
        data['post'] = translated_text


        # Translate original post content
        print("Translating post...")
        content_paragraphs = bot.find_elements(By.CSS_SELECTOR, '.Post .RichTextJSON-root p')
        if content_paragraphs:
            content_translated = []
            for paragraph in content_paragraphs:
                original_text = paragraph.text
                translated_text = translator.translate_text_deepl(original_text, lang)  # Assuming translate_text function is already defined
                bot.execute_script("arguments[0].innerHTML = arguments[1];", paragraph, translated_text.capitalize())
                content_translated.append(translated_text)
            data['post_content'] = "\n".join(content_translated)


        # Create call to action
        cta = "Please don't forget to subscribe !"
        data['cta'] = cta if lang == "en" else translator.translate_text_deepl(cta, lang)

        # Removing reddit interest popup
        print("Removing reddit interest popup...")
        try :
            time.sleep(3)
            interest_popup_close_button = bot.find_element(By.XPATH, '//*[@id="SHORTCUT_FOCUSABLE_DIV"]/div[4]/div/div/div/header/div/div[2]/button')
            if interest_popup_close_button:
                interest_popup_close_button.click()
                time.sleep(1)
        except:
            print("Interest popup removal error !")

        # Screenshot post
        post.screenshot('app/output/post.png')

        # Screenshot post for CTA
        post.screenshot('app/output/cta.png')

        # Screenshot post content if exists
        if content_paragraphs:
            post.screenshot('app/output/post_content.png')

        # Let comments load
        print("Loading comments...")
        bot.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        # Fetching comments & top level comment determinator
        print("Fetching top comments...")
        comments = bot.find_elements(By.CSS_SELECTOR, 'div[id^=t1_][tabindex]')
        allowed_style = comments[0].get_attribute("style")

        print("Filtering comments...")
        # Filter for top only comments
        comments = [comment for comment in comments if comment.get_attribute("style") == allowed_style][:limit_comments]

        print('💬 Scraping comments...',end="",flush=True)
        # Save time & resources by only fetching X content
        for i in range(len(comments)):
            try:
                print('.',end="",flush=True)
                # Filter out locked comments (AutoMod) 
                try:
                    comments[i].find_element(By.CSS_SELECTOR, 'icon.icon-lock_fill')
                    continue
                except:
                    pass

                # Scrolling to the comment ensures that the profile picture loads
                desired_y = (comments[i].size['height'] / 2) + comments[i].location['y']
                window_h = bot.execute_script('return window.innerHeight')
                window_y = bot.execute_script('return window.pageYOffset')
                current_y = (window_h / 2) + window_y
                scroll_y_by = desired_y - current_y

                bot.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
                time.sleep(0.2)

                # Getting comment into string
                elements = comments[i].find_elements(By.CSS_SELECTOR, '.RichTextJSON-root')
                translated_elements = []
                for element in elements:
                    translated_text = translator.translate_text_deepl(element.text, lang)
                    bot.execute_script("arguments[0].innerHTML = arguments[1];", element, translated_text.capitalize())
                    translated_elements.append(translated_text)
                text = "\n".join(translated_elements)

                if "I am a bot" not in text and text:
                    # Screenshot & save text
                    image_path = f'app/output/{i}.png'
                    comments[i].screenshot(image_path)
                    data[str(i)] = text
            except Exception as e:
                if utils.config['debug']:
                    raise e
                pass
        if bot.session_id:
            bot.quit()
        return data
    except Exception as e:
        if bot.session_id:
            bot.quit()
        if utils.config['debug']:
            raise e
        return False
