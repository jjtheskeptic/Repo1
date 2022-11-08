# import the required packages
from types import GeneratorType
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2

#contstruct the argument parser and parse arguments
ap=argparse.ArgumentParser()
ap.add_argument("-v","--video",help="path to the video file")
ap.add_argument("-a","--min-area",type=int,default=500,help="minimum area size in px")
args=vars(ap.parse_args())

#if the video argument is none, then we are reading from the webcam
if args.get("video",None) is None:
    vs=VideoStream(src=0).start()
    time.sleep(2.0)
#otherwise we are reading from a file
else:
    vs=cv2.VideoCapture(args["video"])

#initialize the first frame in the video stream
firstFrame=None
###################################################
# loop over the frames in the video
while True:
    #grab current frame & initialize occupied/unoccupied 
    #text
    frame=vs.read()
    frame=frame if args.get("video",None) is None else frame[1]
    text="unoccupied"

# if the frame couldnot be grabbed, we have reached end
# of the video
if frame is None:
    break

# resize the frame, convert to grayscalse, and blur
frame=imutils.resize(frame,width=500)
gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
gray=cv2.GaussianBlur(gray,(21,21),0)

#i first frame is none, intitialize it
if firstFrame is None:
    firstFrame = gray 
    continue