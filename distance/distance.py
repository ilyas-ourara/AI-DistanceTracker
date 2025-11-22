import ultralytics 
from ultralytics import YOLO
import cv2
import numpy as np 
import time
import matplotlib.pyplot as plt 
import moviepy as mp 
from cvzone.FaceMeshModule import FaceMeshDetector
import cvzone
import os



os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

class DistanceEstimator:
    def __init__(self,model_path,output_video) :
        self.model=YOLO(model_path)
     
        self.output=output_video
        self.bytetrack_yaml_path = "/home/ilyas-ourara/Bureau/venv/lib/python3.12/site-packages/ultralytics/cfg/trackers/bytetrack.yaml"   




    #___________________fonction pour calculer le centre d'un rectangle
    def centre_rectangle(self,x1,y1,x2,y2):
        
        cx=int((x1+x2)/2)
        cy=int((y1+y2)/2)
        return cx,cy
    


    #___________________fonction pour calculer la distance entre le camera et  l'objet 
    def distance_camera_objet(self,w) :
        #parametres de la caméra
        focal_lenght=753
        W=7  #largeur entre les yeux en cm (reel)
        # w largeur en pixels
        # W    #largeur en cm (reel)
        # d     #distance entre la camera et l'objet en cm

        
        """
                Calcul de la distance entre la caméra et un objet.

                Formules :
                    focal_length = (w * d) / W
                    d = (W * focal_length) / w

                Procédure :
                    1. Calibrer la focale : placer un objet de référence de largeur connue W
                    à une distance d connue, mesurer sa largeur en pixels w_ref et calculer
                    focal_length = (w_ref * d) / W.
                    2. En utilisation réelle : mesurer la largeur en pixels w_mesurée et estimer
                    la distance par d_estimée = (W * focal_length) / w_mesurée.
                
        """

        d= (W * focal_lenght)/w
        return d
    



    #_________#Dessine un rectangle stylisé sur l'image en ne traçant que les coins sous forme de crochets.

    def draw_corner_rectangle(self,img, x1,y1,x2,y2, color=(255,0,255), thickness=8, corner_length=40):
          
             
            cv2.line(img, (x1, y1), (x1 + corner_length, y1), color, thickness)
            cv2.line(img, (x1, y1), (x1, y1 + corner_length), color, thickness)

            cv2.line(img, (x2, y1), (x2 - corner_length, y1), color, thickness)
            cv2.line(img, (x2, y1), (x2, y1 + corner_length), color, thickness)

            
            cv2.line(img, (x1, y2), (x1 + corner_length, y2), color, thickness)
            cv2.line(img, (x1, y2), (x1, y2 - corner_length), color, thickness)

           
            cv2.line(img, (x2, y2), (x2 - corner_length, y2), color, thickness)
            cv2.line(img, (x2, y2), (x2, y2 - corner_length), color, thickness)





    #________fonction pour lancer la detection  et l'estimation de distance ______

    def run_distance_estimation(self):
        
        cap=cv2.VideoCapture(0)
        detector = FaceMeshDetector(maxFaces=1) 
        
        if not cap.isOpened():        
            raise RuntimeError(f"Impossible d'ouvrir  les videos")    
        
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps= cap.get(cv2.CAP_PROP_FPS)
        print(fps)
        frames=[]
        timestamps = []

        while True:
            ret,frame = cap.read()
            if not ret :
                 break 
            frame=cv2.resize(frame,(640,480))
            results=self.model.track(frame,tracker="bytetrack.yaml",persist=False,vid_stride=1)
            for res in results:
                boxes = res.boxes.xyxy.cpu().numpy()
               
                classes = res.boxes.cls.cpu().numpy().astype(int)
                classe_names = res.names
                print("*"*50,"classes",classe_names,"*"*50)

                masks = res.masks.data.cpu().numpy() if res.masks is not None else None
               
                ids = res.boxes.id.cpu().numpy().astype(int) if res.boxes.id is not None else []
                
                confidence = res.boxes.conf.cpu().numpy()
               
                for i in range(len(boxes)) :

                    class_name=classe_names[int(classes[i])]
                    
                    if class_name =="face":
                        if boxes is not None and confidence[i] > 0.6:
                            x1,y1,x2,y2=map(int,boxes[i])
                            id_i = int(ids[i]) if i < len(ids) else -1
                            id_text = f"ID:{id_i}" if id_i >= 0 else ""
                            cx,cy=self.centre_rectangle(x1,y1,x2,y2)
                            
                            
                            self.draw_corner_rectangle(frame, x1, y1, x2, y2, color=(255,0,255), thickness=3, corner_length=30)
                            
                            
                            frame, faces =detector.findFaceMesh(frame,draw=True)
                            if faces:

                                face=faces[0]  

                                pointleft=face[145] 
                                pointright=face[374] 
                                w,_=detector.findDistance(pointleft,pointright)  
                                cv2.line(frame, pointleft, pointright, (0, 200, 0), 3)
                                cv2.circle(frame, pointleft, 5, (255, 255, 0), cv2.FILLED)
                                cv2.circle(frame, pointright, 5, (255, 255, 0), cv2.FILLED)
                                d=self.distance_camera_objet(w)  
                                cvzone.putTextRect(frame,f'Distance : {int(d)} cm',(face[10][0] - 98, face[10][1] - 60),scale=2,thickness=2,offset=10)

            cv2.imshow("Tracking", frame)
            #if writer:
             #   writer.write(frame)
            frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
           
            frames.append(frame)
            timestamps.append(time.time())


            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        #if writer:
         #   writer.release()
        cv2.destroyAllWindows()
        
        video_clip = mp.ImageSequenceClip(frames, fps=6)
        video_clip.write_videofile(self.output, codec='libx264')

            

