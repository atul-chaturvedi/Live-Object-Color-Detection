import threading
from functools import partial
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
import cv2
import pickle
import win32com.client as winclc



########### PARAMETERS ##############
width = 640
height = 480
threshold = 0.65 # MINIMUM PROBABILITY TO CLASSIFY
cameraNo = 0
#####################################

#### LOAD THE TRAINNED MODEL 
pickle_in = open("model_trained.p","rb")
model = pickle.load(pickle_in)

#### PREPORCESSING FUNCTION
def preProcessing(img):
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img = cv2.equalizeHist(img)
    img = img/255
    return img

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
        cap = cv2.VideoCapture(0)

        # start processing loop
        while (self.do_vid):
            success, imgOriginal = cap.read()
            # img = np.asarray(imgOriginal)
            # img = cv2.resize(img,(32,32))
            # img = preProcessing(img)
            # cv2.imshow("Processsed Image",img)
            # img = img.reshape(1,32,32,1)
            # #### PREDICT
            # classIndex = int(model.predict_classes(img))
            # #print(classIndex)
            # predictions = model.predict(img)
            # #print(predictions)
            # probVal= np.amax(predictions)
            # print(classIndex,probVal)

            # if probVal> threshold:
            #     cv2.putText(imgOriginal,str(classIndex) + "   "+str(probVal),
            #                 (50,50),cv2.FONT_HERSHEY_COMPLEX,
            #                 1,(0,0,255),1)
            #     if(probVal>0.95):
            #         mytext = str(classIndex)
            #         language = 'en'
            #         speak = winclc.Dispatch("SAPI.SpVoice")
            #         speak.Speak(mytext)

            # cv2.imshow("Original Image",imgOriginal)
            Clock.schedule_once(partial(self.display_frame, imgOriginal))

            cv2.imshow('Hidden', imgOriginal)
            cv2.waitKey(1)
        cap.release()
        cv2.destroyAllWindows()

    def stop_vid(self):
        # stop the video capture loop
        self.do_vid = False
        
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