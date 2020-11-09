#!/usr/bin/env python3

import cv2
import os
import time
import threading
import queue

maxbuffer = 10

def extract(clipFileName, coloredframes):

    # initialize frame count
    count = 0
    
    # open the video clip
    vidcap = cv2.VideoCapture(clipFileName)

    # read one frame
    success,image = vidcap.read()

    print(f'Reading frame {count} {success}')

    while success:

            semaphore.acquire()
            
            success, jpgImage = cv2.imencode('.jpg', image)

            # add the frame to queue 1
            coloredframes.put(image)

            success,image = vidcap.read()
            print(f'Reading frame {count} {success}')
            count += 1

            semaphore.release()

    print("Extraction Complete")
    
def convert(coloredframes, greyframes):

    # initialize frame count
    count = 0
   
    while coloredframes is not None:

        semaphore.acquire()
        print(f'Converting frame {count}')
        
        # convert the image to grayscale
        grayscaleFrame = cv2.cvtColor(coloredframes.get(), cv2.COLOR_BGR2GRAY)
        # Get next frame
        count += 1
    
        # grey frames Queue 2 is written to
        greyframes.put(grayscaleFrame)
        semaphore.release()
        
    print("Conversion Complete")
    
def display(greyframes):

    # initialize frame count
    count = 0

    while greyframes is not None:
        semaphore.acquire()
        # get the next frame
        frame = greyframes.get()

        print(f'Displaying frame {count}')        

        # display the image in a window called "video" and wait 42ms
        # before displaying the next frame
        cv2.imshow('Video', frame)
        if (cv2.waitKey(42) and 0xFF == ord("q")) or greyframes.empty() is True:
            break
        
        semaphore.release()
    
        count += 1

    # make sure we cleanup the windows, otherwise we might end up with a mess
    cv2.destroyAllWindows()
        
    print("Display Complete")

# Bounded Semaphore ensures that there is a limit on the amount of stuff placed inside the queue
# and that an empty queue is never read from   
semaphore = threading.BoundedSemaphore(3)
fileName = 'clip.mp4'


coloredframes = queue.Queue()
greyframes = queue.Queue()


# start threads
thread1 = threading.Thread(target = extract, args = (fileName, coloredframes))
thread2 = threading.Thread(target = convert, args = (coloredframes, greyframes))
thread3 = threading.Thread(target = display, args = (greyframes,))

thread1.start()
thread2.start()
thread3.start()
