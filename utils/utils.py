import praw
import pyttsx3
import os
from moviepy.editor import *
from PIL import Image
import PIL.ImageOps

def scrape_subreddit(reddit, url, comment_threshold):
  remove_chars = ['\n', '\t', '.', '!', '-', '?', ';', ':', '[', ']', '(', ')', '*']
  submission = reddit.submission(url=url)
  top_comments = []
  top_links = []
  #top_comments.append((submission.selftext ,submission.permalink))
  #top_comments.append((submission.title, submission.permalink))
  submission.comments.replace_more(limit=0)
  for top_level_comment in submission.comments:
    if top_level_comment.score > comment_threshold:
        top_comment = top_level_comment.body
        for char in remove_chars:
          top_comment = top_comment.replace(char, ' ')
        top_comments.append((top_comment, "https://www.reddit.com" + top_level_comment.permalink))
        top_links.append("https://www.reddit.com" + top_level_comment.permalink)
  

  return top_comments, top_links

def text_to_audio(engine, text, author, output_dir):
  filename = str(author) + ".wav"
  filepath = output_dir + "/mp3/" + filename
  engine.connect('starting', save_audio(engine, text, filepath))


def save_audio(engine, text, filepath):
  engine.save_to_file(text, filepath)
  engine.iterate()

def screenshot(url_to_comment, counter, output_dir):
  command = "webkit2png -F  -o " + output_dir + "/" + str(counter) + " " + url_to_comment
  os.system(command)

def crop_to_bottom(filepath):
  im = Image.open(filepath)
  im_crop = im.crop((122, 440, 676, 955)) #magic numbers for bottom of comment, needs to be found manually
  return im_crop

def find_bottom_of_comment(im_crop):
  pixels = im_crop.load()
  bottom = 0                    # y-cord of bottom of comment
  for j in range(im_crop.size[1]):
    pixel = pixels[1, j]
    #if pixels[1, j] != (245, 245, 246, 255) or pixels[1, j] != (245, 245, 245, 255):
    if pixel[0] != 245:
      bottom = j
      return bottom

def crop_to_comment(im_crop, bottom):
  if bottom % 2 == 1:                           # Make dimensions even
    bottom += 1
  final_crop = im_crop.crop((0, 0, im_crop.size[0], bottom))
  return final_crop


def change_background(final_crop):
  r,g,b,a = final_crop.split()
  rgb_image = Image.merge('RGB', (r,g,b))
  inverted_image = PIL.ImageOps.invert(rgb_image)
  r2,g2,b2 = inverted_image.split()
  final_transparent_image = Image.merge('RGBA', (r2,g2,b2,a))
  return final_transparent_image

def normalize(final_black):
  old_size = final_black.size
  new_size = (1280, 720)        #720p in YouTube standards
  normal_im = Image.new("RGB", new_size) 
  new_x = int((new_size[0]-old_size[0])/2)
  new_y = int((new_size[1]-old_size[1])/2)
  normal_im.paste(final_black, (new_x, new_y))

  return normal_im
