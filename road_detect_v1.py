import cv2
import numpy as np

"""도로 인식"""


def roi_L(img):
    if len(img.shape)>2:
        color_cnt=img.shape[2]
        mask_color=(255)*color_cnt
    else:
        mask_color=255

    mask=np.zeros_like(img)    
    height,width=img.shape[:2]    
    vertice=np.array([[(90,339),(266,235),(310,235),(196,339)]],dtype=np.int32)
    cv2.fillPoly(mask,vertice,mask_color)
    
    return cv2.bitwise_and(img,mask)

def roi_R(img):
    if len(img.shape)>2:
        color_cnt=img.shape[2]
        mask_color=(255)*color_cnt
    else:
        mask_color=255

    mask=np.zeros_like(img)    
    height,width=img.shape[:2]    
    vertice=np.array([[(477,335),(355,235),(389,235),(556,328)]],dtype=np.int32)
    cv2.fillPoly(mask,vertice,mask_color)
    
    return cv2.bitwise_and(img,mask)

cap=cv2.VideoCapture('video/challenge.mp4')

while True:

    res,frame=cap.read()
    frame=cv2.resize(frame,None,fx=0.5,fy=0.5)
    

    img_gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    img_blur=cv2.GaussianBlur(img_gray,(5,5),0)
    img_canny=cv2.Canny(img_blur,50,210)
    img_roi_L=roi_L(img_canny)
    img_roi_R=roi_R(img_canny)
    img_roi=cv2.addWeighted(img_roi_L,1.0,img_roi_R,1.0,0)


    lines=cv2.HoughLinesP(img_roi,1,np.pi/180,30,minLineLength=10,maxLineGap=200)
    line_img=np.zeros((img_roi.shape[0],img_roi.shape[1],3),dtype=np.uint8)

    if np.all(lines==None):pass
    else:
        for line in lines:
            for x1,y1,x2,y2 in line:
                cv2.line(line_img,(x1,y1),(x2,y2),(0,0,255),3)

        img_line=cv2.addWeighted(frame,1.0,line_img,1.0,0.0)

    #cv2.imshow('1',img_line)
    cv2.imshow('2',img_canny)
    
    if cv2.waitKey(1)==27: break

cap.release()
cv2.destroyAllWindows()