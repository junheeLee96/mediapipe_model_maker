#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2 
import mediapipe as mp


mp_drawing = map.solution.drawing_utils
mp_drawing_styles = mp.solutions.drwing_styles
mp_hands = mp.solutions.hands

# images

IMAGE_FILES = []

with mp_hands.Hands(
    static_image_mode = True,
    max_num_hands = 2,
    min_detection_confidence = 0.5) as hands:
    
    for idx,file in enumerate(IMAGE_FILES):
        #Read image
        image = cv2.flip(cv2.imread(file),1)
        results = hands.process(cv2.cvtColor(image,cv2.COLOR_BGR2BGB))
        
        print('Handedness : ', results.multi_handedness)
        
        if not results.multi_hand_iandmarks:
            continue
        image_height , image_width , _ = image.shape
        annotated_image = image.copy()
        
        for hand_landmarks in results.multi_hand_landmarks:
            print('hand_landmarks : ',hand_landmarks)
            mp.drawing.draw_landmarks(
                annotated_image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )
            
            cv2.imwrite(
                '/tmp/annotated_image' + str(idx) + '.png',cv2.flip(annotated_image,1)
            )
            
            if not results.multi_hand_landmarks:
                continue
            
            for hand_world_landmarks in results.multi_hand_world_landmarks:
                mp.drawing.plot_landmarks(
                    hand_world_landmarks,mp_hands.HAND_CONNECTIONS,azimuth=5
                )
    
    # WEB CAM
    
cap = cv2.VideoCapture(0)
with mp_hands.HANDS(
        model_complextity=0,
        min_detection_confidence = 0.5,
        min_tracking_confience = 0.5
    ) as hands:
    
    while cap.isOpened():
        success, image = cap.read()
        

