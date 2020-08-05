# Automated video production
The goal of this project is to automate the labor-intensive process of video production. There are [YouTube channels](https://www.youtube.com/c/الغازمعالحل123/feature)] that only produce one kind of video: a screenshot of a 'funny' subreddit comment, and a robotic voice reading the comment. There are some [wildly successful videos](https://www.youtube.com/watch?v=aTHHvcdQ6to) that are just 20-30 minutes of comment reading.

These videos are hard to produce by hand: one must go on a subreddit and find acceptable comments, screenshot them, turn the text into speech, then put it all into a video editor. I wanted to leverage the power of python (and its many packages) to automate this process. The final goal is to have a program in which you input a link to a subreddit, and the program spits out a video. Below is a version log that will track my development of this project.

## Version 1.0.0, August 4th, 2020
Our first version lacks many of the bells and whistles promised above, and there is still much manual work to be done.

What it can do: 
Produce screenshots of reddit comments (the screenshots have a white background and are not cropped)
Produce .mp3 files with audio from a speech engine reading each comment

What it can't do (future versions will have these as features):
Crop the screenshot of the comment so that only the comment is visible
Turn the background of the comment to dark gray to make the video look better
Output a video


