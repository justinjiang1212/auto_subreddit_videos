
# chars to remove from comment text
REMOVED_CHARS = ['\n', '\t', '.', '!', '-', '?', ';', ':', '[', ']', '(', ')', '*', '~', '#', '^']

# crop to bottom params
# Magic numbers for title crop
TITLE_CROP = (111, 151, 740, 330)
# Magic numbers for bottom of comment, needs to be found manually
# Most of the time, it's the 2nd value that needs to be changed, usually 440
COMMENT_CROP = (122, 440, 676, 955)


# find botton of comment params
# Magic number in range may need to be adjusted, usually set to 30
# This is how far to the right the loop starts
X_GAP = 30
# This value is usually 245, but it is sometimes 253
COMMENT_BOX_PIXEL = 245

# normalize params
RESIZE = 1.5
# 720p in YouTube standards
VIDEO_QUALITY = (1280, 720)

# video params
FPS = 30
BITRATE = '7000k'
STATIC_SCALE = 0.2

VOICES = ['com.apple.speech.synthesis.voice.Alex',
          'com.apple.speech.synthesis.voice.samantha']
SLOWDOWN_RATE = 25
