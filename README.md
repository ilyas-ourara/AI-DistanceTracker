# Distance Estimation System 📏🤖

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Ultralytics YOLO](https://img.shields.io/badge/Ultralytics-YOLO-orange.svg)](https://github.com/ultralytics/ultralytics)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.5+-green.svg)](https://opencv.org/)
[![CVZone](https://img.shields.io/badge/CVZone-1.6.0-purple.svg)](https://github.com/cvzone/cvzone)

## 📋 Description

Système d'estimation de distance en temps réel basé sur YOLOv8-Face et OpenCV. Ce projet permet de détecter des visages et d'estimer leur distance par rapport à la caméra . Il est conçu pour des applications comme les interfaces interactives, la sécurité ou l'analyse comportementale.

## Demo 🎥

Affichage de démonstrations du système :

![Demo 1](demo/1.gif)


## ✨ Fonctionnalités principales

- **Détection de visages :** Utilisation de YOLOv8-Face pour une détection précise
- **Estimation de distance :** Calcul basé sur la largeur des yeux et la focale de la caméra
- **Tracking  :** Suivi persistant via ByteTrack
- **Visualisation :** Annotations en temps réel avec OpenCV et CVZone
- **Export vidéo :** Génération de vidéos annotées avec MoviePy

## 🚀 Installation

### Prérequis

```bash
Python 3.8+

```

### Installation rapide

```bash
# Cloner le repository
git clone https://github.com/ilyas-ourara/distance-estimation-system.git
cd distance-estimation-system

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### Requirements.txt

```
ultralytics>=8.0.0
opencv-python>=4.5.0
cvzone>=1.6.0
moviepy>=1.0.3
numpy>=1.21.0
matplotlib>=3.3.0
pandas>=1.3.0
```

## 🎯 Utilisation

### Lancement du système

```bash
python main.py
```


####  Estimation de Distance 
```python
# Dans main.py
estimator = DistanceEstimator(model_path, output_path)
```
- Détection des visages
- Estimation des distances
- Génération de vidéos annotées


⭐ **N'hésitez pas à star le projet s'il vous a aidé !** ⭐
