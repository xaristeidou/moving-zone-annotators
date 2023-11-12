import supervision as sv
import cv2
import numpy as np
from ultralytics import YOLO


def mouse_callback(event, x, y, flags, params)->None:
    '''
    Mouse callback function based on OpenCV functionalities
    '''
    # make global the point in order to access x,y coordinates
    global point, start

    # assign left-click down button as event
    if event == cv2.EVENT_LBUTTONDOWN:
        start = True
        point = (x,y)

def find_center_coordinates(points):
    '''
    Finds x,y coordinates of any given array of shape (N, >=3)

    -Args:
        points (np.ndarray): numpy array with shape (N,2) and N>=3

    -Returns:
        x_center (int): center coordinates of x-axis
        y_center (int): center coordinates of y-axis
    '''
    x_center = int(np.mean(points[:, 0]))
    y_center = int(np.mean(points[:, 1]))
    return x_center, y_center


# load the YOLOv8 model
model = YOLO('/home/christoforos/Documents/pytorch_files/yolov8/yolov8m.pt')

# open the video file
video_path = "/home/christoforos/Downloads/people_walking.mp4"
cap = cv2.VideoCapture(video_path)

# build corner annotator
corner_annotator = sv.BoxCornerAnnotator(thickness=2, corner_length=10)

# width and height parameters of zone
w,h = 250, 200

# set to False before first click assosication on frame
start = False

# loop through the video frames
while cap.isOpened():
    # read a frame from the video
    success, frame = cap.read()

    if success:

        # run YOLOv8 inference on the frame
        results = model(frame)

        if start:
            # unpacking of x,y coordinates
            x,y = point

            # building of zone annotator based on width and height parameters
            points = np.array([[x-w, y-h],
                            [x+w, y-h],
                            [x+w, y+h],
                            [x-w, y+h]])

            # building polygone zone and annotator
            zone = sv.PolygonZone(polygon=points,
                                  frame_resolution_wh=(frame.shape[1], frame.shape[0]))
            zone_annotator = sv.PolygonZoneAnnotator(zone=zone, color=sv.Color.red())



            # pass results to Detections Class and activate zone triggering
            detections = sv.Detections.from_ultralytics(results[0])
            mask = zone.trigger(detections=detections)
            
            # filter detections in polygone zone
            detections = detections[mask]

            # visualize the results on the frame
            frame = corner_annotator.annotate(scene=frame.copy(), detections=detections)

            # plot zone annotator
            zone_annotator.annotate(frame)



        # display the annotated frame
        cv2.namedWindow("YOLOv8 Inference")
        cv2.setMouseCallback("YOLOv8 Inference", mouse_callback)
        cv2.imshow("YOLOv8 Inference", frame)


        # break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # break the loop if the end of the video is reached
        break

# release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()