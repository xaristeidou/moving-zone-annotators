# 🚀 Moving Zone Annotators
**A repository that utilizes Supervision 🦊 library and enables user to move zone annotators simply by clicking on video frame** 🌟

## 🖥️ Installation
`git clone https://github.com/xaristeidou/moving-zone-annotators.git`

`cd moving-zone-annotators`

`python3 moving_polygon_zone.py`<br></br>

### Libraries installation

#### PyTorch installation (skip if installed already)
It is recommended to install PyTorch before running requirements installation, especially if you want to download PyTorch with CUDA.

https://pytorch.org/get-started/locally/

For Linux with latest CUDA run:

`pip3 install torch torchvision torchaudio`<br></br>

For Windows with latest CUDA run:

`pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121`<br></br>

#### Requirements

`pip install requirements.txt`<br></br>


## 💪 Run/Execute
Move to repository path

`cd path_to_folder/`<br></br>


Run with default arguments:

`python3 moving_polygone_zone.py`<br></br>

Specify arguments using parser like following:

`python3 moving_polygone_zone.py --source people_walking.mp4 --weights yolov8m.pt --polygone polygone.yaml`<br></br>

You can specify some of the arguments you only want to modify, for example use camera input 0:

`python3 moving_polygone_zone.py --source 0`


## █ 🖊️ Specify polygone zone
You can specify any shape of zone you want:  

🔶 Triangle (3 points)  
🔶 Rectangle (4 points)  
🔶 Any polygone shape with >= 5 points

Open `polygone.yaml` and modify it as needed for your case in yaml format.<br></br>

### Find coordinates of polygone using PolygonZone tool from Roboflow:

https://roboflow.github.io/polygonzone/

1) Open the above link ⬆️ 
2) Drag and drop an image
3) Draw the your own polygone
4) Press Enter to close enclose the polygon
5) Use the calculated points in yaml file