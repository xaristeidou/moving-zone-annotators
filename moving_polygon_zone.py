import supervision as sv
import cv2
import numpy as np
import argparse
from ultralytics import YOLO
from typing import Union, Tuple

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
                    default="assets/people_walking.mp4")
parser.add_argument("--weights",
                    type=str,
                    help="path for yolov8 model weights",
                    default="yolov8m.pt")


args = parser.parse_args()



# load the YOLOv8 model
model = YOLO(args.weights)


class MovingZoneAnnotator:
    zone_completed = False
    points = []
    start = False

    def __init__(self,
                 model = model,
                 video_source = args.source,
                 annotator = sv.BoxCornerAnnotator(thickness=2, corner_length=14),
                 cap = cv2.VideoCapture(args.source),
                 ):
        
        self.model = model
        self.video_source = video_source
        self.annotator = annotator
        self.cap = cap


    def mouse_callback(self, event, x, y, flags, params)->None:
        '''
        Mouse callback function based on OpenCV functionalities
        '''
        # capture point to draw the polygon
        if event == cv2.EVENT_LBUTTONDOWN and not self.zone_completed:
            self.start = True
            self.points.append([x,y])
            self.point = x,y
        
        # capture left click to move the polygon
        elif event == cv2.EVENT_LBUTTONDOWN:
            self.moving = True
        
        # capture mouse move for moving the polygon
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.moving:
                self.point = x,y

        # capture left click release to stop moving the polygon
        elif event == cv2.EVENT_LBUTTONUP:
            self.moving = False
            self.point = x,y

    def find_center_coordinates(self, points:np.ndarray)->Tuple[int, int]:
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

    def predict(self):
        # loop through the video frames
        while self.cap.isOpened():
            # read a frame from the video
            success, frame = self.cap.read()

            if success:

                # run YOLOv8 inference on the frame
                results = model(frame)

                # annotator zone starts after the first click on frame
                if self.zone_completed:
                    # unpacking of x,y coordinates
                    x,y = self.point

                    # initialize an empty NumPy array and fill the points
                    points = np.empty((0, 2), dtype=int)
                    for i in self.points:
                        points = np.append(points, [i], axis=0)

                    x_center, y_center = self.find_center_coordinates(points=points)
                    
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
                    frame = self.annotator.annotate(scene=frame.copy(),
                                                    detections=detections)

                    # plot zone annotator
                    zone_annotator.annotate(frame)


                if not self.zone_completed:
                    for circle in self.points:
                        cv2.circle(img=frame,
                                   center=tuple(circle),
                                   radius=8,
                                   color=(0,0,255),
                                   thickness=-1)

                # display the annotated frame
                cv2.namedWindow("Moving polygon zone")
                cv2.setMouseCallback("Moving polygon zone", self.mouse_callback)
                cv2.imshow("Moving polygon zone", frame)


                # capture keys
                key = cv2.waitKey(1)

                # stop if key is 'q'
                if key == 113:
                    break
                # complete polygon if key is 'Enter'
                elif key == 13:
                    self.zone_completed = True
                    points = np.empty((0, 2), dtype=int)
                    for i in self.points:
                        points = np.append(points, [i], axis=0)
                    self.point = self.find_center_coordinates(points=points)
            else:
                # break the loop if the end of the video is reached
                break

        # release the video capture object and close the display window
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    MovingZoneAnnotator().predict()