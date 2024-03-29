# -*- coding: utf-8 -*-
"""heatMapTool.ipynb


Class TSVreader
"""

# TSVreader Class
# Group Members: Bhavna Mahi (bmahi), Noah Williams (nomuwill)
# Date: 15 Mar 2024

"""
Program Overview:
    TSV reader is a class designed to parse a tab seperated value text file
      for the purpose of data with only the first two columns and filename
      being of interest. The program also is able to re-direct stdin if the
      file path is given from a CLI.

Input:
    The program takes a tab seperated value text file as input, either from
      within the code or from a CLI. Note that every file in the filepath must
      have the same first column. Differences in the first colum can result in
      errors with the output indexing of data to probe ID.

Output:
    The program returns three possible values: header, list of probe names,
      and list of values. The index of the probe names and values are the same.

Necessary Modules:
    sys
    numpy
"""


import sys # For stdin
import numpy as np # For data manipulation and computation


class TSVreader:
    """
    Class with methods to read Tab-Separated-Value Files.

    Assumes file format: "PROBE_ID \t PROBE_VAL".

    Sample Usage:
      fileList = ['testfile1.txt','testfile2.txt']
      for file in fileList:
          thisReader = TSVreader(file).readTSV()
          print(thisReader)

      .readTSV()[0] -> header
      .readTSV()[1] -> probe name list
      .readTSV()[2] -> probe values
    """

    # Initializes class instance with optional file name parameter
    def __init__(self, fname=None):
      """ Initialize TSVreader object. """

      self.fname = fname

    def doOpen(self):
      """
      Redirect to stdin.

      Checks if fname is provided and opens, otherwise redirects to stdin.
      """
      if self.fname is None:
          return sys.stdin
      else:
          return open(self.fname)


    def readTSV(self):
        """ Return list with tab separated values. """

        # Open input file
        with self.doOpen() as fileH:

            # Header
            # Read first line of file and split into a list by tabs
            header = fileH.readline().split('\t')

            # Return lists for probes and values
            valueList = []
            probeList = []
            for line in fileH:
                sepped = line.split('\t')
                # Appends second element of sepped and converts to float before
                # adding to value list
                valueList.append(float([i for i in sepped][1]))
                # Appends first element of sepped to list of probes
                probeList.append([i for i in sepped][0])

        return header, probeList, valueList

"""Heatmap Program"""

# heatMap.py
# Group Members: Bhavna Mahi (bmahi), Noah Williams (nomuwill)
# Date: 15 Mar 2024

"""
Program Overview:
  heatMap.py is a program to take in gene expression data and output a searbon
  /matplotlib plot.

Input:
  The input for the program is a filepath to a folder containing the TSV files
    for each sample. See TSVreader class for more information about input
    formatting requirements. There are optional parameters for dataFilter meant
    to be easily changed for different input sizes.

Output:
  The program outputs a matplotlib window which can be manipulated and/or saved
    from the matplotlib GUI.

Necessary Modules:
    plt
    seaborn
    matplotlib.pyplot
"""


import matplotlib.pyplot as plt  # Creates graphical output
import seaborn as sn  # Creates heatmap
import os  # Handles user filepath to data


###############################################################################
# CHANGE THRESHOLD VALUES BELOW ---------------(if you want, no pressure)-----
###############################################################################

def dataFilter(data, probeList, minValue=10000, tickThresh=11500):

    """
    Return filtered versions of input params.

    Probes with a median value across samples that are below threshold are
      removed from the data. Only tick marks above a threshold value are plotted
      to reduce text overlap on figure. Reducing values to small numbers may
      cause the program to take longer due to matplotlib's text generation
      bottleneck.

    params:
      minValue: integer minimum value for median of probe value across samples.
      tickThresh: integer minimum value for tick marks to be labled.
    """

    # Boolean array of rows below median threshold
    boolArr = np.median(data, axis=0) < minValue
    # Array of indecies of values below threshold
    valThresh = np.where(boolArr == True)[0]
    # Remove probe data from all samples
    outData = np.delete(data, valThresh, axis=1)
    # Remove prove from probe list bank
    probeList = np.delete(probeList, valThresh)

    # Boolean array of rows aove median tick threshold
    boolArr = np.median(outData, axis=0) > tickThresh
    # Array of indecies of values above threshold
    abvThresh = np.where(boolArr == True)[0]
    # Array of probe values above threshold
    xTicks = probeList[abvThresh]

    return xTicks, outData, abvThresh


def plotHeatmap(xTicks, data, abvThresh):

    """ Plot and display seaborn heatmap from dataFilter(). """

    # Create Y-Axis Labels, removing _norm.txt from filename
    yAxisList = [i.rstrip('_norm.txt') for i in fileList]

    # Displays the reference value
    cbar = True

    # Plots heatmap using seaborn heatmap method
    hm = sn.heatmap(data=data, cbar=cbar)

    # Set axis labels
    hm.set_xlabel('Probe ID')
    hm.set_ylabel('Sample ID')

    # Set x ticks & tick labels
    plt.xticks(abvThresh + .5)
    plt.xticks(rotation=90)
    hm.set_xticklabels(xTicks)

    # Set y ticks & tick labels
    hm.set_yticklabels(yAxisList)

    # Set color bar label
    hm.collections[0].colorbar.set_label('Gene Expression Values',
                                         rotation=270,
                                         labelpad=20)

    # Displays the plotted heatmap in a tight layout
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':

    ###########################################################################
    # CHANGE FILEPATH TO YOUR DATA DIRECTORY BELOW ----------------------------
    ###########################################################################

    # Changes current directory to specified path with data
    os.chdir('/path/to/your/data/directory')
    # Specifies path to folder with files
    path = os.listdir('/path/to/your/data/directory')

    # Create list of visible files (remove OS hidden files)
    fileList = [filename for filename in path if filename[0] != '.']

    # Creates numpy array from data
    npData = np.array([TSVreader(file).readTSV()[2] for file in fileList])

    # Creates list of probe names
    probeList = np.array([TSVreader(file).readTSV()[1] for file in fileList][0])

    # Plot heatmap with filtered data
    plotHeatmap(dataFilter(npData, probeList)[0],   # xTicks
                dataFilter(npData, probeList)[1],   # Data
                dataFilter(npData, probeList)[2])   # abvThresh

"""3D Mesh Program"""

# mesh3D.py
# Group Members: Bhavna Mahi (bmahi), Noah Williams (nomuwill)
# Date: 15 Mar 2024

"""
Program Overview:
    mesh3D is a program to convert an image to 3D mesh, output as an STL file
    with the origional file name. The program uses matplotlib's img processing,
    numpy for large array manipulation, and numpy-stl for mesh processing.
Input:
    Program takes image as input. Ideally the input image is downscaled to
      approximately 1280 x 720 to keep runtime to a few seconds. Each block on
      the heatmap must be a minimum of 9x9 pixels to maintain a flat top,
      otherwise the mesh algorithm creates a point (16x or 32x is ideal).
Output:
    Program outputs a gaussian stl model of the input image with the same
    filename.
Necessary Modules:
    numpy
    matplotlib.image
    numpy-stl
"""


import numpy as np
import matplotlib.image as mpimg
from stl import mesh


def threeDMesh(fname):

    """ Return 3D stl file of the input file. """

    # Process Image
    img = mpimg.imread(fname)  # Read in image
    lum_img = np.array(img[:, :, 0])  # Keep luminosity values
    (lnth, wdth) = lum_img.shape  # Get image dimensions

    # Scale array
    scaleVal = 100
    lum_img /= np.max(np.abs(lum_img))  # normalize values
    lum_img *= scaleVal / lum_img.max()  # scale array

    # Construct empty numpy array & account for edges
    verts = np.zeros((lnth, wdth, 3))

    # Assign skirts
    for y in range(0, wdth):
        verts[0][y] = (0, y, 0)
    for x in range(0, lnth):
        verts[x][0] = (x, 0, 0)
    for y in range(0, wdth):
        verts[lnth - 1][y] = (lnth - 1, y, 0)
    for x in range(0, lnth):
        verts[x][wdth - 1] = (x, wdth - 1, 0)

    # Assign lum from image to vertices array for heatmap values
    for y in range(1, wdth - 1):
        for x in range(1, lnth - 1):
            z = lum_img[x][y]
            verts[x][y] = (x, y, z)

    # Construct numpy array of faces
    faces = []
    for y in range(0, wdth - 1):
        for x in range(0, lnth - 1):
            tri1 = np.array([verts[x][y], verts[x + 1][y], verts[x + 1][y + 1]])
            tri2 = np.array([verts[x][y], verts[x][y + 1], verts[x + 1][y + 1]])
            faces.append(tri1)
            faces.append(tri2)

    # Assign Bottom (2 big triangles)
    botTri1 = np.array([verts[0][0], verts[lnth - 1][0], verts[lnth - 1][wdth - 1]])
    botTri2 = np.array([verts[0][0], verts[0][wdth - 1], verts[lnth - 1][wdth - 1]])
    faces.append(botTri1)
    faces.append(botTri2)

    # Construct mesh from faces
    facesNp = np.array(faces)
    surface = mesh.Mesh(np.zeros(facesNp.shape[0], dtype=mesh.Mesh.dtype))
    for index, face in enumerate(faces):
        for vertex in range(3):
            surface.vectors[index][vertex] = facesNp[index][vertex]

    # Save file
    getName = fname.strip('.png')
    surface.save(getName + '.stl')


if __name__ == '__main__':
    threeDMesh('lg_hm.png')
