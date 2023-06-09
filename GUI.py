from tkinter import *
from tkinter import font
from matplotlib.pyplot import fill

def mouse(event):
    print ("miss")
    import cv2
    import numpy as np
    import HandTrackingModule as htm
    import time
    import autopy
    if __name__=="__main__":
    
    ##########################
        wCam, hCam = 640, 480
        frameR = 100 # Frame Reduction
        smoothening = 7
        #########################

        pTime = 0
        plocX, plocY = 0, 0
        clocX, clocY = 0, 0

        cap = cv2.VideoCapture(0)
        cap.set(3, wCam)
        cap.set(4, hCam)
        detector = htm.handDetector(maxHands=1)
        wScr, hScr = autopy.screen.size()
        # print(wScr, hScr)

        while True:
            # 1. Find hand Landmarks
            success, img = cap.read()
            img = detector.findHands(img)
            lmList,box= detector.findPosition(img)
            # 2. Get the tip of the index and middle fingers
            if len(lmList)!= 0:
                x1=lmList[8][1] 
                y1=lmList[8][2]
                x2=lmList[12][1]
                y2=lmList[12][2]
                # print(x1, y1, x2, y2)
            
                # 3. Check which fingers are up
                fingers = detector.fingersUp()
                #print(fingers)
                # 4. Only Index Finger : Moving Mode
                if fingers[1] == 1 and fingers[2] == 0 and fingers[3]==0 and fingers[4]==0 and fingers[0]==0:
                    # 5. Convert Coordinates
                    try:
                        x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                        y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
                        # 6. Smoothen Values
                        clocX = plocX + (x3 - plocX) / smoothening
                        clocY = plocY + (y3 - plocY) / smoothening
                        # 7. Move Mouse
                        autopy.mouse.move(wScr - clocX, clocY)
                        cv2.circle(img,(x1, y1), 15, (255, 0, 255), cv2.FILLED)
                        plocX, plocY = clocX, clocY
                    except:
                        pass
                    
                # 8. Both Index and middle fingers are up : Clicking Mode
                if fingers[1] == 1 and fingers[2] == 1 and fingers[3]==0 and fingers[4]==0 and fingers[0]==0:
                    # 9. Find distance between fingers
                    length, img, lineInfo = detector.findDistance(8, 12, img)
                    print(length)
                    # 10. Click mouse if distance short
                    if length < 40:
                        cv2.circle(img, (lineInfo[4], lineInfo[5]),15, (0, 255, 0), cv2.FILLED)
                        autopy.mouse.click()
            
            # 11. Frame Rate

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,(255, 0, 0), 3)
            #12. Display
            
            cv2.waitKey(1)




root=Tk()
root.title("WELCOME TO AI VIRTUAL SYSTEM")
root.geometry("170x115")
#root.minsize(155,100)
#root.maxsize(155,100)
b1=Button(root,text="AI VIRTUAL🖱️",font="bold")
b1.pack(fill=X)
b1.bind('<Button-1>',mouse)
b1.bind('<Double-1>',quit)
b2=Button(root,text="AI VIRTUAL⌨️",font="bold").pack(fill=X)
b3=Button(root,text="AI VIRTUAL📸",font="bold").pack(fill=X)
root.mainloop()
