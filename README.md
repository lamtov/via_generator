wget https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh
bash Anaconda3-2020.11-Linux-x86_64.sh
conda create -n minimal_example python=3.7 pyinstaller
conda activate minimal_example
conda install -y -c anaconda tk
conda install -y -c anaconda pillow

pip install selenium
pip install beautifulsoup4
pip install lxml