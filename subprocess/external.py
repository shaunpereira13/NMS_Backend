import cv2   
from scipy.spatial import distance as dist
import time
import json
import base64


refmeasure=10
img = cv2.imread('images/scale.jpg', 1)
img1=img.copy()
points=[]
i=0
data=[]
pixelsMeasure=None

def click_event(event, x, y, flags, params):
    global points,i
    
    if (event == cv2.EVENT_LBUTTONDOWN):
        points.append((x,y))   
        # print(points) 
        cv2.drawMarker(img1, points[i], (0, 255, 255),cv2.MARKER_CROSS, 25, 3)
        if ((i%2)!=0):
            cv2.line(img1,(x,y),points[i-1],(0,0,0),2)
        i=i+1
    elif event==cv2.EVENT_RBUTTONDOWN:
        points.clear()
        i=0
img_counter=0
while True:
    cv2.imshow('image', img1)
    cv2.setMouseCallback('image', click_event)
    l=len(points)
    
    if (l==6):
        for p in range(0,l,2):
            leng = dist.euclidean(points[p], points[p+1])
            if pixelsMeasure is None:
                pixelsMeasure = leng / refmeasure
            
            actdist=leng/pixelsMeasure
            
            
            data.append(actdist)
            
            cv2.putText(img1,"{:.1f}in".format(actdist),points[p],cv2.FONT_HERSHEY_SIMPLEX,
            1.65, (90, 0, 250), 3)
        
        
        _, encoded_image = cv2.imencode('.jpg', img1)
        image = base64.b64encode(encoded_image).decode('utf-8')   
        
        output_data = {
        'status': 'success',
        'message': 'List generated successfully',
        'result_list': data,
        'result_img':image,
        }
        output_json = json.dumps(output_data)
        print(output_json)
        
        break
    elif (l==0):
        img1=img.copy()
    elif (l>6):
        break
    
    k=cv2.waitKey(10)
    if (k==ord('q')):
        break
    
   
    
    
    
    
