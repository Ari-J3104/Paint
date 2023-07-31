import cv2
import numpy

#cProgramScreen should handle all the drawing, and event control
#You need to modify the cProgramScreen.
class cProgramScreen: 
    #ScreenParameters
    mcScreenWidth=600#WidthOfTheProgram
    mcScreenHeight=600#HeightOftheProgram
    mcTitle="DrawingProgram"#NameOftheScreenForDrawing
    mDisplayImage=None#WhereEverythingGetsDrawn
    mPressedKey=-1#TellsWhichKeyIsPressed
    mCurrentMode="None"#ControlsCurrentDrawingMode_StringIsInefficentForThisButItisModeReadable
    def __init__(self):
        cv2.namedWindow(self.mcTitle)
        self.fCreateRGBTrackBars()
        cv2.setMouseCallback(self.mcTitle,self.fMouseEvent)#CreatesaCallbackforMouseEvents
        self.fRefreshScreen()#Creates an Empty Screen To Draw On
    #UsedForDrawingTrackBarsToImage
    def fCreateRGBTrackBars(self):
        def fEmptyFunction(vInput):
            pass
        cv2.createTrackbar('R',self.mcTitle,0,255,fEmptyFunction)
        cv2.createTrackbar('G',self.mcTitle,0,255,fEmptyFunction)
        cv2.createTrackbar('B',self.mcTitle,0,255,fEmptyFunction)
    #UsedForGettingSelectedRGBColorFromTrackBars
    def fGetSelectedRGBColor(self):
        vRColor=cv2.getTrackbarPos('R',self.mcTitle)
        vGColor=cv2.getTrackbarPos('G',self.mcTitle)
        vBColor=cv2.getTrackbarPos('B',self.mcTitle)
        oSelectedRGBColor=(vRColor,vGColor,vBColor)
        return oSelectedRGBColor
    #HandlesAllMouseRelatedEvents
    #This Function is where majority of your code goes
    #And Majority Of Drawing
    #This function gets called evertime there is a mouse event, and the execution of this function starts from its beginning. That means there might be multiple of these running in parallel for each event(Mouse movement is event and mouse move gets called every time mouse moves a pixel). So our traditional loop and update structure wont work. You might need different variables to check or control different states of your program.
    #ImportantEventsYouNeedToHandleAre
    #cv2.EVENT_LBUTTONDOWN
    #cv2.EVENT_MOUSEMOVE
    #cv2.EVENT_LBUTTONUP
    #cv2.EVENT_RBUTTONDOWN
    def fMouseEvent(self,iEvent,iX,iY,iFlags,iParameters):
         if(self.mCurrentMode=="Dot"):
              if(iEvent==cv2.EVENT_LBUTTONDOWN):
                   (vR,vG,vB)=self.fGetSelectedRGBColor()
                   self.mDisplayImage[iY,iX,:]=[vB,vG,vR]
                   self.mDisplayImage[iY+1,iX,:]=[vB,vG,vR]
                   self.mDisplayImage[iY,iX+1,:]=[vB,vG,vR]
                   self.mDisplayImage[iY-1,iX,:]=[vB,vG,vR]
                   self.mDisplayImage[iY,iX-1,:]=[vB,vG,vR]

         elif(self.mCurrentMode=="Brush"):
              if(iEvent==cv2.EVENT_LBUTTONDOWN):
                   self.mBrushDrawing=True
              if(iEvent==cv2.EVENT_MOUSEMOVE):
                   if(self.mBrushDrawing==True):
                        (vR,vG,vB)=self.fGetSelectedRGBColor()
                        self.mDisplayImage[iY,iX,:]=[vB,vG,vR]
                        self.mDisplayImage[iY+1,iX,:]=[vB,vG,vR]
                        self.mDisplayImage[iY,iX+1,:]=[vB,vG,vR]
                        self.mDisplayImage[iY-1,iX,:]=[vB,vG,vR]
                        self.mDisplayImage[iY,iX-1,:]=[vB,vG,vR]
              if(iEvent==cv2.EVENT_LBUTTONUP):
                   self.mBrushDrawing=False

         elif self.mCurrentMode == "Line":
              if iEvent == cv2.EVENT_LBUTTONDOWN:
                   self.mStartingPoint = (iX, iY) 
              elif iEvent == cv2.EVENT_LBUTTONUP:
                   self.mEndingPoint = (iX, iY)
                   (vR, vG, vB) = self.fGetSelectedRGBColor()
                   cv2.line(self.mDisplayImage, self.mStartingPoint, self.mEndingPoint, (vB, vG, vR), 1)

         elif self.mCurrentMode == "Rectangle":
              if iEvent == cv2.EVENT_LBUTTONDOWN:
                   self.mStartingPoint = (iX, iY)
              elif iEvent == cv2.EVENT_LBUTTONUP:
                   self.mEndingPoint = (iX, iY)
                   (vR, vG, vB) = self.fGetSelectedRGBColor()
                   cv2.rectangle(self.mDisplayImage, self.mStartingPoint, self.mEndingPoint, (vB, vG, vR), 1)

                
         elif self.mCurrentMode == "Polygon":
             if iEvent == cv2.EVENT_LBUTTONDOWN:
                   self.mPolygonVertices.append((iX, iY))
             elif iEvent == cv2.EVENT_RBUTTONDOWN:
                   if len(self.mPolygonVertices) >= 3:
                        (vR, vG, vB) = self.fGetSelectedRGBColor()
                        cv2.polylines(self.mDisplayImage, [numpy.array(self.mPolygonVertices)], True, (vB, vG, vR), 1)
                        self.mPolygonVertices = []
           
         if(self.mCurrentMode=="Fill"):
              if(iEvent==cv2.EVENT_LBUTTONDOWN):
                   self.mFillDrawing=True
                   (vR,vG,vB)=self.fGetSelectedRGBColor()
                   for i in range(self.mcScreenHeight):
                      for j in range(self.mcScreenWidth):
                           self.mDisplayImage[i,j,:]=[vB,vG,vR]
              else:
                 self.mFillDrawing=False
             

    #UsedForGettingANewScreenImage
    def fRefreshScreen(self):
        self.mDisplayImage=numpy.zeros((self.mcScreenHeight,self.mcScreenWidth,3),numpy.uint8)
    #UsedForDrawingTextForUserNotification
    def fDrawString(self,iText,iXLocation,iYLocation):
        cv2.putText(self.mDisplayImage,iText,(iXLocation,iYLocation),cv2.FONT_HERSHEY_SIMPLEX,1,self.mTextColor,2)
    #UsedForDisplayingScreen
    def fDisplayScreen(self):
        cv2.imshow(self.mcTitle,self.mDisplayImage)
        vNewKey=cv2.waitKey(1)
        if(vNewKey!=-1):
            self.mPressedKey=vNewKey
    #UsedForLearningPressedKey
    #Returns_-1_IfNoKeyIsPressedYet
    #ResetsPressedKeyTo_-1_AfterReturn
    def fGetPressedKey(self):
        oPressedKey=self.mPressedKey
        self.mPressedKey=-1
        return oPressedKey
#UsedForGettingANewScreenImage
    def fRefreshScreen(self):
        self.mDisplayImage=numpy.zeros((self.mcScreenHeight,self.mcScreenWidth,3),numpy.uint8)
    #UsedForDrawingTextForUserNotification
    def fDrawString(self,iText,iXLocation,iYLocation):
        cv2.putText(self.mDisplayImage,iText,(iXLocation,iYLocation),cv2.FONT_HERSHEY_SIMPLEX,1,self.mTextColor,2)
    #UsedForDisplayingScreen
    def fDisplayScreen(self):
        cv2.imshow(self.mcTitle,self.mDisplayImage)
        vNewKey=cv2.waitKey(1)
        if(vNewKey!=-1):
            self.mPressedKey=vNewKey
    #UsedForLearningPressedKey
    #Returns_-1_IfNoKeyIsPressedYet
    #ResetsPressedKeyTo_-1_AfterReturn
    def fGetPressedKey(self):
        oPressedKey=self.mPressedKey
        self.mPressedKey=-1
        return oPressedKey
    #Used for updating the screen and User input processing.
    def fUpdate(self):
        vCurrentModeText="CurrentMode: "+self.mCurrentMode
        self.fDisplayScreen()# Displays the screen to the user. This line is need to have an display
        vPressedKey=self.fGetPressedKey()#This Line needs to Come after Display Screen to Get if a key is pressed
        #You can use similar if statements to check which keyboard is pressed also read ord() function
        #https://docs.python.org/3/library/functions.html#ord
        #Never checks for special keys, if you need special keys like up arrow button change waitkey to waitKeyEx
        #If you change to waitKeyEx use following codes https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
        if(vPressedKey==ord('q')):#Checks If the q button is pressed on keyboard
            exit()#Exits the program
        elif(vPressedKey==ord('a')):#This will reset The DrawMode To None again
            self.mCurrentMode="None"    
        elif(vPressedKey==ord('e')):#This will Refreshes the screen (Makes everything blank again)
            self.fRefreshScreen()#Creates an Empty Screen To Draw On
        elif(vPressedKey==ord('s')):#This will Draw a Single Dot To the Screen
            self.mCurrentMode="Dot"#We gave you this mode as a sample to look at
        elif(vPressedKey==ord('b')):
            #This Should Allow You To have a brush painting option
            self.mCurrentMode="Brush"
            self.mBrushDrawing=False
            #This brush painting will allow the user to paint using mouse movement
            #You will start painting with the pressing a Left mouse button
            #program needs to keeps painting until the mouse button is freed
            pass#remove pass when you are done
        elif(vPressedKey==ord('r')):
            self.mCurrentMode="Rectangle"
            #ThisShouldAllowYouToDraw a rectangle to the screen
            #Do not fill inside the rectangle
            #Rectangle needs to wait for two mouse click
            #First mouse click determines the top left corner
            #Second Mouse Click Determines the bottom right corner
            #After second click you can draw the rectangle
            pass#remove pass when you are done
        elif(vPressedKey==ord('l')):
            self.mCurrentMode="Line"
            #This Should Allow You To Draw a line to the screen
            #Line needs to wait two mouse click
            #First mouse click determines the starting point
            #Second Mouse Click Determines the ending point
            #After second click you can draw the line
            pass#remove pass when you are done
        elif(vPressedKey==ord('p')):
            self.mCurrentMode="Polygon"
            self.mPolygonVertices = []
            #This Should Allow You To Draw a polygon to the screen
            #Polygon can be in arbitrary size
            #the user will select the points and the program will draw line between them
            #First left mouse click starts the first point of the polygon
            #Consecutive left mouse clicks will add more points to you polygon
            #When you add a point to your polygon you need to draw a line between the previous point and the current point
            #When the user does a right mouse click the polygon drawing gets completed by drawing a line between last point and the first point 
            pass#remove pass when you are done
        elif(vPressedKey==ord('f')):
            self.mCurrentMode="Fill"
            self.mFillDrawing=False
            #This Should Allow You To color fill (Paint Bucket tool) and area
            #Color Region is started with the clicked location and the border of a different color(or the image) whichever comes first.
            #When you select color fill and press mouse button on the screen it should color fill the region that you select with the color that is selected
            #The algorithm that you need to implement here is called floodfill and recursive version of the algorithm wont work in python 
            #For every colorfill you start with a list that contains a single element which is first pixel to color(Mouse click location). 
            #For every pixel location in your list you check up,down,left and right of the pixel locations and add them to you list if they share same color with the pixel that is in your list and they are not in the list already. Afterwards color the pixel location. You do this until there is nothing left in your list.
            pass#remove pass when you are done

#Do Not Modify Main Function
#All Your Code Should be In the cProgramScreen class
#***************************************************************************************
def Main():
    vProgramScreen=cProgramScreen()#This line is need to create a Screen For the Program
    #MainProgramLoop
    while(True):
        vProgramScreen.fUpdate() 
#***************************************************************************************
Main()#Calls Main To start The game DO NOT DELETE