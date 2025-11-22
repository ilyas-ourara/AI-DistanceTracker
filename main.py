from distance import DistanceEstimator
import os

model_path= "models/yolov8s_face_lindevs.onnx"  
output_path="output/out.mp4"




if not os.path.exists(os.path.dirname(output_path)):
    os.makedirs(os.path.dirname(output_path))


    raise FileNotFoundError(f"Le modèle spécifié n'existe pas : {model_path}")


def run_tracking() :
    ot= DistanceEstimator(model_path,output_path)
    print("Début de l'estimation de distance...")
    ot.run_distance_estimation()
    print("Estimation de distance terminée. La vidéo annotée est enregistrée à :", output_path)


if __name__=="__main__" :
    run_tracking()
    
    




