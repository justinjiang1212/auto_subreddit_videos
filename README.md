# Automated video production
The goal of this project is to automate the labor-intensive process of video production. There are [YouTube channels](https://www.youtube.com/c/الغازمعالحل123/feature) that only produce one kind of video: a screenshot of a 'funny' subreddit comment, and a robotic voice reading the comment. Yet some of these channels boast hundreds of thousands of subscribers. There are some [wildly successful videos](https://www.youtube.com/watch?v=aTHHvcdQ6to) with a few million views that are just 20-30 minutes of comment reading.

These videos are hard to produce by hand: one must go on a subreddit and find acceptable comments, screenshot them, turn the text into speech, then put it all into a video editor. I wanted to leverage the power of python (and its many packages) to automate this process. The final goal is to have a program in which you input a link to a subreddit, and the program spits out a video. Below is a version log that will track my development of this project.



## Version 2.5.0, August 9th, 2020
Added clip of the channel logo along with static audio, which emuluates other popular channels who have done the same thing.

## Version 2.1.0, August 9th, 2020
Increased bitrate of videos to be 720p-quality on YouTube.

## Version 2.0.0, August 8th, 2020
Video production is fully automated. Here is the [first video](https://www.youtube.com/watch?v=9PalHFOIp-U&feature=youtu.be) produced using this version of the code.

## Version 1.5.0, August 7th, 2020
Screenshots are now cropped with colors inverted. Before this feature was implemented, we had to crop each screenshot by hand, which was extremely time-consuming and honestly a complete waste of time. Below is an example of before and after. <br/>
**New** <br/>
![new](https://github.com/justinjiang1212/auto_subreddit_videos/blob/master/samples/new.png)
**Old** <br/>
![old](https://github.com/justinjiang1212/auto_subreddit_videos/blob/master/samples/old.png)

## Version 1.0.0, August 4th, 2020
Our first version lacks many of the bells and whistles promised above, and there is still much manual work to be done. This is the first [video](https://youtu.be/ZdxreABoeK4) produced with this program.

**What it can do:**  
Produce screenshots of reddit comments (the screenshots have a white background and are not cropped)<br/>
Produce .mp3 files with audio from a speech engine reading each comment<br/>

**What it _can't_ do** (future versions will have these as features):  
Crop the screenshot of the comment so that only the comment is visible<br/>
Turn the background of the comment to dark gray to make the video look better<br/>
Output a video<br/>


## Authors
Justin Jiang, Harvey Mudd College 2023
