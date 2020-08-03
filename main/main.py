import praw
import pyttsx3
from utils import utils
import os
import shutil



#init reddit instance
reddit = praw.Reddit(client_id='dwiIzGyzmAcWuQ', 
                     client_secret='QXTKGNfgbA0ytJEl_XTaGKMQGyk', 
                     user_agent='top_comments by /u/Able-Faithlessness44', 
                     username='Able-Faithlessness44',
                    password = '12Ctyisawesome!')

url = 'https://www.reddit.com/r/AskReddit/comments/i1sh57/what_is_the_greatest_comeback_to_a_insult_youve/'

top_comments, top_links = utils.scrape_subreddit(reddit, url, 5000)

print(str(len(top_comments)) + " comments to be processed")

#global text-to-speech declaration using Mac OS speech driver 'nsss'
engine = pyttsx3.init(driverName='nsss')

#slow down rate of speech to 185 words per minute
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-15)
engine.startLoop(False)

output_dir = 'output'
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
os.makedirs(output_dir)

counter = 0
for comment in top_comments:
  utils.text_to_audio(engine, comment[0], counter, output_dir)

  utils.screenshot(comment[1], counter, output_dir)
  counter += 1
