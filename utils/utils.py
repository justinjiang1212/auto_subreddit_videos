import praw
import pyttsx3
import pyautogui
import time as time
import os



def scrape_subreddit(reddit, url, comment_threshold):
  submission = reddit.submission(url=url)
  submission.comments.replace_more(limit=0)
  top_comments = []
  top_links = []
  for top_level_comment in submission.comments:
    if top_level_comment.score > comment_threshold:
        top_comment = top_level_comment.body.replace('\n', ' ')
        top_comment = top_comment.replace('\t', ' ')
        top_comments.append((top_comment, "https://www.reddit.com" + top_level_comment.permalink))
        top_links.append("https://www.reddit.com" + top_level_comment.permalink)
  

  return top_comments, top_links

def text_to_audio(engine, text, author, output_dir):
  filename = str(author) + ".mp3"
  filepath = output_dir + "/" + filename
  engine.connect('starting', save_audio(engine, text, filepath))


def save_audio(engine, text, filepath):
  engine.save_to_file(text, filepath)
  engine.iterate()

def screenshot(url_to_comment, counter, output_dir):
  command = "webkit2png -F  -o " + output_dir + "/" + str(counter) + ".png " + url_to_comment
  os.system(command)
 