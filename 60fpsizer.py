
# before running, run
# pip install ffmpy easygui

import easygui
from ffmpy import FFmpeg
import sys
from os.path import splitext

interlaced = easygui.ynbox("Is your video interlaced? " +
    "If your video has tiny horiziontal lines across "
    "each frame when there's motion, then it's probably interlaced.",
    "Interlaced", ("Yes it's interlaced", "No it's not"))

if interlaced is None: 
    sys.exit(-1)

video = easygui.fileopenbox("Please select your " + 
    f"480{'i' if interlaced else 'p'} video...")

if video is None: 
    sys.exit(-1)

output = splitext(video)[0]+"_60fpsizer.mp4"

filters = '-vf ' + ('"yadif=1,' if interlaced else '"') +\
    'scale=1280:720:force_original_aspect_ratio=decrease,' +\
    'pad=1280:720:(ow-iw)/2:(oh-ih)/2" ' + \
    "-b:v 3500k -c:v libx264 -preset medium " + \
    "-r 60 -level 4.2 -c:a aac -b:a 192k "

ff = FFmpeg(
    inputs={video: None},
    outputs={output: filters}
)

print(ff.cmd)
ff.run()
