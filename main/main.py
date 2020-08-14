import praw
import pyttsx3
from utils import utils
import os
import shutil
from main import account_info as ai
from params import *
import sys
from optparse import OptionParser

def main(url: str, comment_threshold: int = 100, max_comment_length: int = 30000, output: str = 'output'):
    '''Wrapper function to create video from subreddit comments
    :param url: url to subreddit
    :param comment_threshold: number representing upvote cutoff, anything above will be returned
    :param max_comment_length: max length of comment in chars
    :param output: output directory
    '''
    # init reddit instance
    reddit = praw.Reddit(client_id=ai.client_id,
                         client_secret=ai.client_secret,
                         user_agent=ai.user_agent,
                         username=ai.username,
                         password=ai.password)

    top_comments, title = utils.scrape_subreddit(reddit, url, comment_threshold,
                                                 max_comment_length)

    print(str(len(top_comments)) + " comments to be processed")

    # Global text-to-speech declaration using Mac OS speech driver 'nsss'
    engine = pyttsx3.init(driverName='nsss')

    # Slow down rate of speech to 185 words per minute
    rate = engine.getProperty('rate')

    # Set to 0 for male voice, 1 for female voice
    voices = VOICES
    engine.setProperty('voice', voices[1])

    engine.setProperty('rate', rate-SLOWDOWN_RATE)
    engine.startLoop(False)

    output_dir = output
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    os.makedirs(output_dir + "/wav")

    utils.text_to_audio(engine=engine, text=title[0], name='title', output_dir=output_dir)
    utils.screenshot(title[1], 'title', output_dir)
    filename = 'title' + "-full.png"
    filepath = "output/" + filename
    title_crop = utils.crop_to_bottom(filepath, is_title=True)
    os.remove(filepath)
    title_black = utils.change_background(title_crop)
    final_title = utils.normalize(title_black)
    final_title.save(filepath)

    # Counter is just a filename counter
    counter = 0
    for comment in top_comments:
        utils.text_to_audio(engine=engine, text=comment[0], name=str(counter), output_dir=output_dir)
        utils.screenshot(comment[1], str(counter), output_dir)

        # Screenshot function adds -full.png to each screenshot, redundancy is unavoidable :(
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


url = sys.argv[1]
comment_threshold = int(sys.argv[2])
max_comment_length = int(sys.argv[3])
output = sys.argv[4]

main(url, comment_threshold, max_comment_length, output)
