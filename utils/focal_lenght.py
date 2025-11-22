import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
import numpy as np
 


"""
______________________ ce script pour  calculer la focale de notre camera 
______________________ en  utilisant la largeur reelle entre les yeux et la distance entre la camera et le visage
 ______________________on utilise la formule : f= (w*d)/W
"""

cap = cv2.VideoCapture("test/input.jpeg")

detector = FaceMeshDetector(maxFaces=1) 

success,img = cap.read()
img, faces =detector.findFaceMesh(img,draw=True) 

if faces:

    face=faces[0]  

    pointleft=face[145] 
    pointright=face[374] 
    w,_=detector.findDistance(pointleft,pointright)  # largeur en pixels de l'oeil
    W=6.3   
    d=50

    f= (w*d)/W 
    print(f)

    cvzone.putTextRect(img,f'Focale : {int(f)} px',(face[10][0] - 98, face[10][1] - 60),scale=2,thickness=2,offset=10)
    cv2.imshow("Image",img)
   
    cv2.imwrite("test/demo_2.jpg",img)
    if cv2.waitKey(0)==ord('q'):
        cv2.destroyAllWindows()
