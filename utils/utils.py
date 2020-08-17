'''
Util functions used by main script
Justin Jiang
'''

import praw
import pyttsx3
import os
from moviepy.editor import *
from PIL import Image
import PIL.ImageOps
from params import *


def scrape_subreddit(reddit: praw.Reddit, url: str, comment_threshold: int = 100,
                     max_comment_length: int = 30000):
    '''
    Scrapes given subreddit using Praw
    :param reddit:  praw object containing auth info
    :param url:  url to subreddit
    :param comment_threshold: number representing upvote cutoff, anything above will be returned
    :param max_comment_length: max length of comment in chars
    :return list of comments [(comment, url)] and title (title_text, url)
    '''
    submission = reddit.submission(url=url)
    # Only get root of comment tree
    submission.comments.replace_more(limit=0)

    # Get title info
    title = (submission.title + submission.selftext, 'https://www.reddit.com' + submission.permalink)

    top_comments = []

    for top_level_comment in submission.comments:
        # Only take comments above rating threshold
        if top_level_comment.score > comment_threshold:
            top_comment = top_level_comment.body
            # Remove unwanted chars
            for char in REMOVED_CHARS:
                top_comment = top_comment.replace(char, ' ')
            # Check if comment was deleted by user
            if top_comment != ' deleted ':
                # Only take comments below length cutoff
                if len(top_comment) < max_comment_length:
                    top_comments.append((top_comment, 'https://www.reddit.com' + top_level_comment.permalink))
    return top_comments, title


def text_to_audio(engine: pyttsx3.init, text: str, name: str, output_dir: str):
    '''
    Turns text to audio using pyttsx3
    :param engine: pyttsx3 engine instance
    :param text: text to be turned into audio
    :param name: name for output, in the case of comments, this is usually a number
    :param output_dir: output path
    '''
    filename = str(name) + '.wav'
    filepath = output_dir + '/wav/' + filename
    engine.connect('starting', _save_audio(engine, text, filepath))


def _save_audio(engine: pyttsx3.init, text: str, filepath: str):
    '''
    Add audio job to engine queue
    :param engine: pyttsx3 engine instance
    :param text: text to be turned into audio
    :param filepath: output dir
    '''
    engine.save_to_file(text, filepath)
    engine.iterate()


def screenshot(url_to_comment: str, filename: str, output_dir: str):
    '''
    Use webkit2png script to take screenshot of comment
    :param url_to_comment: url to comment, found in scrape_reddit
    :param filename: name to save png output
    :param output_dir: where to save output
    '''
    command = 'webkit2png -F  -o ' + output_dir + '/' + str(filename) + ' ' + url_to_comment
    os.system(command)


def crop_to_bottom(filepath: str, is_title: bool = False):
    '''
    Remove top half of screenshot
    param filepath: filepath to png to be cropped
    param is_title: True if filepath leads to a title screenshot, False otherwise
    return cropped image
    '''
    im = Image.open(filepath)
    # Uncomment to debug is image is not cropping correctly
    #im.show()
    if is_title:
        im_crop = im.crop(TITLE_CROP)
    else:
        im_crop = im.crop(COMMENT_CROP)
    return im_crop


def find_bottom_of_comment(im_crop: Image):
    '''
    Find the y-coord of the bottom of the comment box
    param: im_crop: cropped image with no top half and with comment box in different color than rest
    return bottom of comment
    '''
    pixels = im_crop.load()
    for j in range(X_GAP, im_crop.size[1]):
        pixel = pixels[0, j]

        # Uncomment to debug if screenshots are not being cropped correctly
        #print(pixel)
        #print(bottom)

        if pixel[0] != COMMENT_BOX_PIXEL:   
            return j


def crop_to_comment(im_crop: Image, bottom: int):
    '''
    Crops given image to the comment box
    param im_crop: image with top cropped and comment box a different color than rest
    param bottom: y-coord of bottom of comment box
    return cropped image
    '''
    # Make dimensions even
    if bottom % 2 == 1:
        bottom += 1
    # Crop photo to bottom box of comment
    final_crop = im_crop.crop((0, 0, im_crop.size[0], bottom))
    return final_crop


def change_background(final_crop: Image):
    '''
    Invert colors of image
    param final_crop: cropped image with just comment box, with white background
    return inverted color image
    '''
    r, g, b, a = final_crop.split()
    rgb_image = Image.merge('RGB', (r, g, b))
    inverted_image = PIL.ImageOps.invert(rgb_image)
    r2, g2, b2 = inverted_image.split()
    final_transparent_image = Image.merge('RGBA', (r2, g2, b2, a))
    return final_transparent_image


def normalize(final_black: Image):
    '''
    Set cropped comment to consistent background
    param final_black: cropped inverted comment
    return normalized image with comment in middle
    '''

    final_black = _resize(final_black, RESIZE)
    old_size = final_black.size
    new_size = VIDEO_QUALITY

    normal_im = Image.new('RGB', new_size)
    new_x = int((new_size[0]-old_size[0])/2)
    new_y = int((new_size[1]-old_size[1])/2)
    normal_im.paste(final_black, (new_x, new_y))

    return normal_im


def _resize(im: Image, factor: int):
    '''
    Resizes image to be larger or smaller, based on factor
    param im: image to be scaled
    param factor: how much image will be scaled
    return resized image
    '''
    width = int(im.size[0] * factor)
    height = int(im.size[1] * factor)
    im = im.resize((width, height), Image.ANTIALIAS)
    return im


def make_video(counter: int):
    '''
    Make video from given file counter
    param counter: how many images to make into video
    '''
    clips = []
    title_audio = AudioFileClip('output/wav/title.wav')
    duration = title_audio.duration
    title_image = ImageClip('output/title-full.png', duration=duration)
    title_image = title_image.set_fps(FPS)
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
            image_clip = ImageClip(image_path, duration=duration)
            image_clip = image_clip.set_fps(FPS)

            clip = image_clip.set_audio(audio_clip)
            clips.append(clip)
            clips.append(static)
        except:
            print('image missing')

    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile('output/video.mp4', fps=FPS, codec='mpeg4',
                               remove_temp=True, bitrate=BITRATE)
    final_clip.close()
    for clip in clips:
        clip.close()


def _get_static():
    '''
    Load in static and create cut clip of logo and static
    return ImageClip of logo and static
    '''
    static_audio = AudioFileClip('logo/static.wav')
    duration = static_audio.duration

    logo = ImageClip('logo/break.png', duration=duration)
    logo = logo.set_fps(FPS)

    logo_clip = logo.set_audio(static_audio)
    final = logo_clip.volumex(STATIC_SCALE)
    return final


def _print_all_voices():
    '''
    Prints all possible voices in the speech engine
    unused function, used in development to see all usable voices
    '''
    engine2 = pyttsx3.init()

    voices = engine2.getProperty('voices')
    for voice in voices:
        print('Voice:')
        print(' - ID: %s' % voice.id)
        print(' - Name: %s' % voice.name)
        print(' - Languages: %s' % voice.languages)
        print(' - Gender: %s' % voice.gender)
        print(' - Age: %s' % voice.age)
