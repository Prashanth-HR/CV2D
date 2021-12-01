import cv2 as cv
import mediapipe as mp # pip install mediapipe
import time

mp_objectron = mp.solutions.objectron
mp_draw = mp.solutions.drawing_utils

cap = cv.VideoCapture(0)

# Define the codec and create VideoWriter object
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('objectDetection.avi', fourcc, 20.0, (640,  480))

with mp_objectron.Objectron(static_image_mode=False,
                            max_num_objects=2,
                            min_detection_confidence=0.5,
                            min_tracking_confidence=0.8,
                            model_name='Cup') as objectron:

    while cap.isOpened():

        success, image = cap.read()

        start = time.time()


        # Convert the BGR image to RGB
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

        # Process the image and find objects
        image.flags.writeable = False
        results = objectron.process(image)
        
        # Convert the image color back so it can be displayed
        image.flags.writeable = True
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)


        if results.detected_objects:
            for id, detected_object in enumerate(results.detected_objects):
                mp_draw.draw_landmarks(image, detected_object.landmarks_2d, mp_objectron.BOX_CONNECTIONS)
                mp_draw.draw_axis(image, detected_object.rotation, detected_object.translation)


        end = time.time()
        totalTime = end - start

        fps = 1 / totalTime
        print("FPS: ", fps)

        cv.putText(image, f'FPS: {int(fps)}', (20,70), cv.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 2)

        cv.imshow('Object Detection', image)

        # write the image frame to a video file
        # out.write(image)

        if cv.waitKey(5) & 0xFF == 27:
            break

cap.release()
out.release()