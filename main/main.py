import praw
import pyttsx3
from utils import utils
import os
import shutil
from main import account_info as ai

#init reddit instance
reddit = praw.Reddit(client_id=ai.client_id, 
                     client_secret=ai.client_secret, 
                     user_agent=ai.user_agent, 
                     username=ai.username,
                    password =ai.password)

url = 'https://www.reddit.com/r/AskReddit/comments/i1sh57/what_is_the_greatest_comeback_to_a_insult_youve/'

top_comments, top_links = utils.scrape_subreddit(reddit, url, 5000)

print(str(len(top_comments)) + " comments to be processed")


#global text-to-speech declaration using Mac OS speech driver 'nsss'
engine = pyttsx3.init(driverName='nsss')

#slow down rate of speech to 185 words per minute
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-25)
engine.startLoop(False)

output_dir = 'output'
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
os.makedirs(output_dir)
os.makedirs(output_dir + "/mp3")
counter = 0
for comment in top_comments:
  #utils.text_to_audio(engine, comment[0], counter, output_dir)
  utils.screenshot(comment[1], counter, output_dir)

  filename = str(counter) + "-full.png"
  filepath = "output/" + filename

  im_crop = utils.crop_to_bottom(filepath)
  os.remove(filepath)
  bottom = utils.find_bottom_of_comment(im_crop)
  final_crop = utils.crop_to_comment(im_crop, bottom)
  final_black = utils.change_background(final_crop)
  final = utils.normalize(final_black)
  final.save(filepath)
  counter += 1
