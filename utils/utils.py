import praw
import pyttsx3
import os
from moviepy.editor import *
from PIL import Image
import PIL.ImageOps

def scrape_subreddit(reddit, url, comment_threshold, max_comment_length):
  remove_chars = ['\n', '\t', '.', '!', '-', '?', ';', ':', '[', ']', '(', ')', '*', '~', '#', '^']
  submission = reddit.submission(url=url)
  top_comments = []
  title = (submission.title + submission.selftext, 'https://www.reddit.com' + submission.permalink)
  submission.comments.replace_more(limit=0)
  for top_level_comment in submission.comments:
    if top_level_comment.score > comment_threshold:
        top_comment = top_level_comment.body
        for char in remove_chars:
          top_comment = top_comment.replace(char, ' ')
        if top_comment != ' deleted ':
          if len(top_comment) < max_comment_length:
            top_comments.append((top_comment, 'https://www.reddit.com' + top_level_comment.permalink))
  return top_comments, title

def text_to_audio(engine, text, author, output_dir):
  filename = str(author) + '.wav'
  filepath = output_dir + '/wav/' + filename
  engine.connect('starting', _save_audio(engine, text, filepath))


def _save_audio(engine, text, filepath):
  engine.save_to_file(text, filepath)
  engine.iterate()


def screenshot(url_to_comment, filename, output_dir):
  command = 'webkit2png -F  -o ' + output_dir + '/' + str(filename) + ' ' + url_to_comment
  os.system(command)


def crop_to_bottom(filepath, is_title = False):
  im = Image.open(filepath)
  if is_title:
    # Magic numbers for title crop
    im_crop = im.crop((111, 151, 740, 330))
  else:
    # Magic numbers for bottom of comment, needs to be found manually
    im_crop = im.crop((122, 440, 676, 955))
  return im_crop


def find_bottom_of_comment(im_crop):
  pixels = im_crop.load()
  # y-cord of bottom of comment
  bottom = 0
  # Magic number in range may need to be adjusted
  for j in range(30, im_crop.size[1]):
    pixel = pixels[1, j]

    # Uncomment to debug if screenshots are not being cropped correctly
    #print(pixel)
    #print(bottom)

    if pixel[0] != 245:       # This value is usually 245, but it is sometimes 253
      bottom = j
      return bottom


def crop_to_comment(im_crop, bottom):
  # Make dimensions even
  if bottom % 2 == 1:
    bottom += 1
  # Crop photo to bottom box of comment
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
  final_black = _resize(final_black, 1.5)
  old_size = final_black.size

  # 720p in YouTube standards
  new_size = (1280, 720)

  normal_im = Image.new('RGB', new_size) 
  new_x = int((new_size[0]-old_size[0])/2)
  new_y = int((new_size[1]-old_size[1])/2)
  normal_im.paste(final_black, (new_x, new_y))

  return normal_im

def _resize(im, factor):
  width = int(im.size[0] * factor)
  height = int(im.size[1] * factor)
  im = im.resize((width, height), Image.ANTIALIAS)
  return im

def make_video(counter):
  clips = []
  title_audio = AudioFileClip('output/wav/title.wav')
  duration = title_audio.duration
  title_image = ImageClip('output/title-full.png', duration = duration)
  title_image = title_image.set_fps(30)
  clip = title_image.set_audio(title_audio)
  clips.append(clip)

  static = _get_static()
  clips.append(static)

  for i in range(0, counter):
    audio_path = 'output/wav/' + str(i) + '.wav'
    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration

    try: 
      image_path = 'output/' + str(i) + '-full.png'
      image_clip = ImageClip(image_path, duration = duration)
      image_clip = image_clip.set_fps(30)

      clip = image_clip.set_audio(audio_clip)
      clips.append(clip)
      clips.append(static)
    except:
      print("image missing")

  final_clip = concatenate_videoclips(clips)
  final_clip.write_videofile("output/video.mp4", fps = 30, codec = "mpeg4", remove_temp = True, bitrate = '7000k')

def _get_static():
    static_audio = AudioFileClip('logo/static.wav')
    duration = static_audio.duration

    logo = ImageClip('logo/break.png', duration = duration)
    logo = logo.set_fps(30)
    
    logo_clip = logo.set_audio(static_audio)
    logo_clip = logo_clip.volumex(0.5)
    return logo_clip
  


def _print_all_voices():
  '''Prints all possible voices in the speech engine'''
  engine = pyttsx3.init()

  voices = engine.getProperty('voices')
  for voice in voices:
      print("Voice:")
      print(" - ID: %s" % voice.id)
      print(" - Name: %s" % voice.name)
      print(" - Languages: %s" % voice.languages)
      print(" - Gender: %s" % voice.gender)
      print(" - Age: %s" % voice.age)


