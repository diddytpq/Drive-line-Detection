import cv2
import numpy as np


"""도로 인식"""


def roi_L(img):  #왼쪽 도로만 추출
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
    

def roi_R(img): #오른쪽 도로만 추출
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


def detect_yollow(img): #HSV영역에서 yollow만 추출

    low_yellow=np.array([18,94,140])
    high_yellow=np.array([48,255,255])
    yellow_img=cv2.inRange(img,low_yellow,high_yellow)

    return yellow_img

video_path='video/challenge.mp4'



cap=cv2.VideoCapture(video_path)

while True:

    res,frame=cap.read()

    frame=cv2.resize(frame,None,fx=0.5,fy=0.5)

    img_blur=cv2.GaussianBlur(frame,(5,5),0)
    img_HSV=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    img_gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    
    img_yellow=detect_yollow(img_HSV)  #HSV영역에서 Yollow색 영역만 추출

    img_canny_1=cv2.Canny(img_gray,150,300)
    img_canny_2=cv2.Canny(img_yellow,75,150)

    img_canny=cv2.addWeighted(img_canny_1,1.0,img_canny_2,1.0,0) #그레이 스케일 엣지 + HSV 스케일 엣지

    img_roi_L=roi_L(img_canny)
    img_roi_R=roi_R(img_canny)
    
    img_roi=cv2.addWeighted(img_roi_L,1.0,img_roi_R,1.0,0)

    

    lines=cv2.HoughLinesP(img_roi,1,np.pi/180,25,minLineLength=1,maxLineGap=210) #확률 허브 변환을 통한 차선 후보

    line_img=np.zeros((img_roi.shape[0],img_roi.shape[1],3),dtype=np.uint8)

    if np.all(lines==None):pass
    else:
        for line in lines:
            for x1,y1,x2,y2 in line:
                if ((70<np.abs(np.arctan2(y2-y1,x2-x1))*180)/np.pi): #line 후보중 각도가 70도 이상만 출력
                    cv2.line(line_img,(x1,y1),(x2,y2),(0,0,255),3)
                else:
                    continue

        img_line=cv2.addWeighted(frame,1.0,line_img,1.0,0.0)

    cv2.imshow('1',img_line)
    cv2.imshow('2',img_roi)

    if cv2.waitKey(1)==27: break

cap.release()
cv2.destroyAllWindows()
