# this is from here: https://pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/
# Very simple motion detection
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
    vs=VideoStream(src=1).start()  #src=0 does not give an image.
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
    ######################### section 3 ###################
    #compute absolute difference between current frame and
    #first frame
    frameDelta=cv2.absdiff(firstFrame,gray)
    thresh=cv2.threshold(frameDelta,25,255,cv2.THRESH_BINARY)[1]

    #dilate the threshoded image to fill in holes, then find contours
    # on the thresholded image
    thresh=cv2.dilate(thresh,None,iterations=2)
    cnts=cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts=imutils.grab_contours(cnts)

    #loop over the contorus
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < args["min_area"]:
            continue

        #compute bounding box for the contour and ddraw it on the frame,
        # update the text
        (x,y,w,h)=cv2.boundingRect(c)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        text="occupied"

    ######### section 4 #######
    # draw the text and timestamp on the frame
    cv2.putText(frame, "Room Status: {}".format(text), (10, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    #
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
	#
    # show the frame and record if the user presses a key
    cv2.imshow("Security Feed", frame)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frameDelta)
    key = cv2.waitKey(1) & 0xFF
	# if the `q` key is pressed, break from the lop
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()