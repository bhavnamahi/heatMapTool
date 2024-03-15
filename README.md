# heatMapTool
Gene Expression Heatmap Tool (Developed for UCSC BME-160) by [Noah Williams](https://www.linkedin.com/in/nmuwilliams/) (UCSC '25) and [Bhavna Mahi](https://www.linkedin.com/in/bhavnamahi/) (UCSC '25)

# Description 
The Heat Map Tool is a Python tool used to generate heatmaps for pre-processed data in the form of a tab separated text file and create a 3D model of your heatmap.

# Running heatMapTool
You can run heatMapTool.py in virutally any Python IDE, such as [PyCharm](https://www.jetbrains.com/pycharm/). Just open the file in your IDE, and make sure to change minimum values and threshold values for your probes and probe display:
```python
def dataFilter(data, probeList, minValue={enter your value}, tickThresh={enter your value})
```
Be sure to also change the directory to your own that contains your sample data:
```python
os.chdir('/path/to/your/data/directory')
path = os.listdir('/path/to/your/data/directory')
```

# 3D Modeling
Developed by Noah Williams (UCSC '25)

mesh3D.py uses numpy for array handling, numpy-stl for mesh generation, and matplotlib.image for image manipulation. The program takes a png as input, and converts the image to a 3D mesh model. Each pixel of the image serves as two triangle faces, with the z axis controlled by the luminance value of that pixel. Ideally the input image is downscaled to approximately 1280 x 720 to keep runtime to a few seconds. Each block on the heatmap must be a minimum of 9x9 pixels to maintain a flat top, otherwise the mesh creates a point (16x or 32x is ideal).

# Acknowledgements 
Dr. David Bernick (UCSC) - FastAreader (inspiration for TSVreader)

Reto Stamm (UCSC) - 3D Model

# From the Creators
[Project Presentation](https://docs.google.com/presentation/d/1-0XLzpBCIC0Vlrad1KpUzddQMG5pUpMVwSKTYu1px6A/edit?usp=sharing)

[Project Report](https://docs.google.com/document/d/1b20teRT3hwaOq0Uu5fxLqieKzpSzDW34BWp42YyDRzc/edit?usp=sharing)
