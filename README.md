# 🚀 Moving Zone Annotators
**A repository that utilizes Supervision 🦊 library and enables user to move zone annotators simply by clicking on video frame** 🌟

## 🖥️ Installation
`git clone https://github.com/xaristeidou/moving-zone-annotators.git`

`cd moving-zone-annotators`

### Libraries installation

#### PyTorch installation (skip if installed already)
It is recommended to install PyTorch before running requirements installation, especially if you want to download PyTorch with CUDA.

https://pytorch.org/get-started/locally/

For Linux with latest CUDA run:

`pip3 install torch torchvision torchaudio`

For Windows with latest CUDA run:

`pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121`

#### Requirements

`pip install requirements.txt`


## 💪 Run/Execute
`cd path_to_folder/`

Run with default arguments:

`python3 moving_polygone_zone.py`

Specify arguments using parser:

`python3 moving_polygone_zone.py --source people_walking.mp4 --weights yolov8m.pt --polygone polygone.yaml`