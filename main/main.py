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

url = 'https://www.reddit.com/r/AskReddit/comments/h9gc8e/anyone_who_has_taken_part_in_judge_judy_either_as'

top_comments, top_links = utils.scrape_subreddit(reddit, url, 1000)

print(len(top_comments))
print(top_links)


#global text-to-speech declaration
engine = pyttsx3.init(driverName='nsss')
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