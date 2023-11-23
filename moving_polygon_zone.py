import supervision as sv
import cv2
import numpy as np
import argparse
import yaml
from ultralytics import YOLO
from typing import Union

def custom_type(input:str)->Union[str,int]:
    '''
    Check if user provided number for camera input

    -Args:
        input (str): User input for video source
    -Return:
        input (str | int): Returns integer if provided for camera source, otherwise video name
    '''
    try:
        return int(input)
    except ValueError:
        return input

parser = argparse.ArgumentParser(description='Moving polygon zones')

# Define your command-line arguments
parser.add_argument("--source",
                    type=custom_type,
                    help="define the video source",
                    default="utils/people_walking.mp4")
parser.add_argument("--weights",
                    type=str,
                    help="path for yolov8 model weights",
                    default="yolov8m.pt")
parser.add_argument('--polygon',
                    type=str,
                    help="path for polygon points",
                    default="polygon.yaml")

args = parser.parse_args()


with open(args.polygon, 'r') as file:
    polygone = yaml.safe_load(file)


# load the YOLOv8 model
model = YOLO(args.weights)

# open the video file
video_path = args.source

cap = cv2.VideoCapture(video_path)

# build corner annotator
corner_annotator = sv.BoxCornerAnnotator(thickness=2, corner_length=14)

# set to False before first click assosication on frame
start = False


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

def find_center_coordinates(points:np.ndarray)->tuple:
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


def main():
    # loop through the video frames
    while cap.isOpened():
        # read a frame from the video
        success, frame = cap.read()

        if success:

            # run YOLOv8 inference on the frame
            results = model(frame)

            # annotator zone starts after the first click on frame
            if start:
                # unpacking of x,y coordinates
                x,y = point

                # initialize an empty NumPy array and fill the points
                points = np.empty((0, 2), dtype=int)
                for i in polygone.values():
                    points = np.append(points, [i], axis=0)

                x_center, y_center = find_center_coordinates(points=points)
                
                points = points + np.array([x-x_center, y-y_center])

                # building polygon zone and annotator
                zone = sv.PolygonZone(polygon=points,
                                    frame_resolution_wh=(frame.shape[1], frame.shape[0]),
                                    triggering_position=sv.Position.CENTER)
                zone_annotator = sv.PolygonZoneAnnotator(zone=zone,
                                                         color=sv.Color.red())

                # pass results to Detections Class and activate zone triggering
                detections = sv.Detections.from_ultralytics(results[0])
                mask = zone.trigger(detections=detections)
                
                # filter detections in polygon zone
                detections = detections[mask]

                # visualize the results on the frame
                frame = corner_annotator.annotate(scene=frame.copy(),
                                                  detections=detections)

                # plot zone annotator
                zone_annotator.annotate(frame)


            # display the annotated frame
            cv2.namedWindow("Moving polygon zone")
            cv2.setMouseCallback("Moving polygon zone", mouse_callback)
            cv2.imshow("Moving polygon zone", frame)


            # break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            # break the loop if the end of the video is reached
            break

    # release the video capture object and close the display window
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()