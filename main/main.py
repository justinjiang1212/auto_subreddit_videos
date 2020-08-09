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

url = 'https://www.reddit.com/r/AskReddit/comments/i6jf2s/redditors_who_have_been_in_such_severe_and/'

top_comments, title = utils.scrape_subreddit(reddit, url, comment_threshold=100,\
                                            max_comment_length=30000)

print(str(len(top_comments)) + " comments to be processed")


#global text-to-speech declaration using Mac OS speech driver 'nsss'
engine = pyttsx3.init(driverName='nsss')

#slow down rate of speech to 185 words per minute
rate = engine.getProperty('rate')

# set to Alex for male voice, Samantha for female voice
voices = ['com.apple.speech.synthesis.voice.Alex', 'com.apple.speech.synthesis.voice.samantha']
engine.setProperty('voice', voices[0])

engine.setProperty('rate', rate-25)
engine.startLoop(False)

output_dir = 'output'
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
os.makedirs(output_dir)
os.makedirs(output_dir + "/wav")

utils.text_to_audio(engine, title[0], 'title', output_dir)
utils.screenshot(title[1], 'title', output_dir)
filename = 'title' + "-full.png"
filepath = "output/" + filename
title_crop = utils.crop_to_bottom(filepath, is_title=True)
os.remove(filepath)
title_black = utils.change_background(title_crop)
final_title = utils.normalize(title_black)
final_title.save(filepath)

counter = 0             #counter is just a filename
for comment in top_comments:
  utils.text_to_audio(engine, comment[0], counter, output_dir)
  utils.screenshot(comment[1], counter, output_dir)

  #screenshot function adds -full.png to each screenshot, redundancy is unavoidable :( 
  filename = str(counter) + "-full.png"
  filepath = "output/" + filename

  im_crop = utils.crop_to_bottom(filepath)
  # Uncomment to debug if screenshots are not being cropped correctly
  #im_crop.show()
  os.remove(filepath)
  bottom = utils.find_bottom_of_comment(im_crop)
  final_crop = utils.crop_to_comment(im_crop, bottom)
  final_black = utils.change_background(final_crop)
  final = utils.normalize(final_black)
  final.save(filepath)
  counter += 1
  
  # Uncomment to debug if screenshots are not being cropped correctly
  #break

control = input("Ready to start video production? (y/n) ")

if control == 'y':
  utils.make_video(counter)
else:
  print("When you are ready, you can run make_videos with counter = " + str(counter))