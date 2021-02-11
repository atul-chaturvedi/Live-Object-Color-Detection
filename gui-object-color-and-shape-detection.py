import threading
from functools import partial
import cv2
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.togglebutton import  ToggleButton 
from kivy.uix.widget import  Widget
from kivy.properties import ObjectProperty

import numpy as np
import imutils

# Glonbal Variables
color = 0
# do_vid = True

class MainScreen(Screen):
    pass



# class Controls(Widget):
#     pass


class Manager(ScreenManager):
    pass

# Builder.load_string('''
# <Controls>:    
#     GridLayout  
#         cols:6
#         Label:
#             text:red
#             font_size:30
#             color:0,1,1,1

#         ToggleButton:

# ''')

Builder.load_string('''
<MainScreen>:
    name: "Test"       
    FloatLayout:
        Label:
            text: "Object Color And Shape Detection"
            pos_hint: {"x":0.0, "y":0.85}
            size_hint: 1.0, 0.2  

        Image:
            # this is where the video will show
            # the id allows easy access
            id: vid
            size_hint: 1, 0.6
            allow_stretch: True  # allow the video image to be scaled
            keep_ratio: True  # keep the aspect ratio so people don't look squashed
            pos_hint: {'center_x':0.5, 'top':0.9}              

        ToggleButton:
            text:"Red"
            id:pow
            pos_hint: {"x":0.2, "y":0.15}
            size_hint:0.2,0.1
            group:"color"
            on_press:app.red()

        ToggleButton:
            text:"Green"
            pos_hint: {"x":0.4, "y":0.15}
            size_hint:0.2,0.1
            group:"color"
            on_press:app.green()

        ToggleButton:
            text:"Blue"
            pos_hint: {"x":0.6, "y":0.15}
            size_hint:0.2,0.1
            group:"color"
            on_press:app.blue()

        Button:
            text: 'Stop Video'
            pos_hint: {"x":0.01, "y":0.04}
            size_hint: 0.98, 0.1
            font_size: 30
            on_release:app.stop_vid()

''')


class Main(App):
    def build(self):

        # start the camera access code on a separate thread
        # if this was done on the main thread, GUI would stop
        # daemon=True means kill this thread when app stops
        threading.Thread(target=self.doit, daemon=True).start()

        sm = ScreenManager()
        self.main_screen = MainScreen()
        sm.add_widget(self.main_screen)
        return sm

    def doit(self):
        # this code is run in a separate thread
        self.do_vid = True  # flag to stop loop

        # make a window for use by cv2
        # flags allow resizing without regard to aspect ratio
        cv2.namedWindow('Hidden', cv2.WINDOW_NORMAL | cv2.WINDOW_FREERATIO)

        # resize the window to (0,0) to make it invisible
        cv2.resizeWindow('Hidden', 0, 0)
        cam = cv2.VideoCapture(0)

        # start processing loop
        while (self.do_vid):
            _, frame = cam.read()
            hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

            lower_green = np.array([40,70,80])
            upper_green = np.array([70,255,255])

            lower_red = np.array([0,50,120])
            upper_red = np.array([10,255,255])

            lower_blue = np.array([90,60,0])
            upper_blue = np.array([121,255,255])

            mask1 = cv2.inRange(hsv,lower_green,upper_green)
            mask2 = cv2.inRange(hsv,lower_red,upper_red)
            mask3 = cv2.inRange(hsv,lower_blue,upper_blue)
            

            cnts1 = cv2.findContours(mask1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            cnts1 = imutils.grab_contours(cnts1)

            cnts2 = cv2.findContours(mask2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            cnts2 = imutils.grab_contours(cnts2)

            cnts3 = cv2.findContours(mask3,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            cnts3 = imutils.grab_contours(cnts3)    
            
            if(color==2):
                for c in cnts1:
                    area1 = cv2.contourArea(c)
                    if area1>5000:
                        cv2.drawContours(frame,[c],-1,(0,255,0),3)
                        M = cv2.moments(c)
                        cx = int(M["m10"]/M["m00"])
                        cy = int(M["m01"]/M["m00"])
                        
                        # cv2.circle(frame,(cx,cy),7,(255,255,255),-1)
                        cv2.putText(frame,"Green",(cx-20,cy-20),cv2.FONT_HERSHEY_SIMPLEX,2.5,(255,255,255),3)
                        # cv2.putText(frame,"Green")
            if(color==1):
                for c in cnts2:
                    area1 = cv2.contourArea(c)
                    if area1>5000:
                        cv2.drawContours(frame,[c],-1,(0,255,0),3)
                        M = cv2.moments(c)
                        cx = int(M["m10"]/M["m00"])
                        cy = int(M["m01"]/M["m00"])
                        
                        # cv2.circle(frame,(cx,cy),7,(255,255,255),-1)
                        cv2.putText(frame,"Red",(cx-20,cy-20),cv2.FONT_HERSHEY_SIMPLEX,2.5,(255,255,255),3)
                        # cv2.putText(frame,"Green")
            if(color==3):
                for c in cnts3:
                    area1 = cv2.contourArea(c)
                    if area1>5000:
                        cv2.drawContours(frame,[c],-1,(0,255,0),3)
                        M = cv2.moments(c)
                        cx = int(M["m10"]/M["m00"])
                        cy = int(M["m01"]/M["m00"])
                        
                        # cv2.circle(frame,(cx,cy),7,(255,255,255),-1)
                        cv2.putText(frame,"Blue",(cx-20,cy-20),cv2.FONT_HERSHEY_SIMPLEX,2.5,(255,255,255),3)
                        # cv2.putText(frame,"Green")

            # ...
            # more code
            # ...

            # send this frame to the kivy Image Widget
            # Must use Clock.schedule_once to get this bit of code
            # to run back on the main thread (required for GUI operations)
            # the partial function just says to call the specified method with the provided argument (Clock adds a time argument)
            Clock.schedule_once(partial(self.display_frame, frame))

            cv2.imshow('Hidden', frame)
            cv2.waitKey(1)
        cam.release()
        cv2.destroyAllWindows()

    def stop_vid(self):
        # stop the video capture loop
        self.do_vid = False
        
    def red(self):
        global color
        color = 1
        
    def green(self):
       global color
       color = 2

    def blue(self):
        global color
        color = 3


    def display_frame(self, frame, dt):
        # display the current video frame in the kivy Image widget

        # create a Texture the correct size and format for the frame
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')

        # copy the frame data into the texture
        texture.blit_buffer(frame.tobytes(order=None), colorfmt='bgr', bufferfmt='ubyte')

        # flip the texture (otherwise the video is upside down
        texture.flip_vertical()

        # actually put the texture in the kivy Image widget
        self.main_screen.ids.vid.texture = texture


if __name__ == '__main__':
    Main().run()