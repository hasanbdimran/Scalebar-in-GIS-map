
def plotScaleBar(ax, barX, barY, barLength, figureCRS, percentHeight, segments, tickTextPad=0.002, unitTextPadV=0.5, unitTextPadH=0.5):
    import geopandas as gpd
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    import pyproj
    from pyproj import Transformer
    import pandas as pd
    import os

    '''
    ax = plot axis
    barX = Scale bar starting X coordinates
    barY = Scale bar starting Y coordinates
    barLength = Scale bar length
    figureCRS = Coordinate system of figure
    percentHeight = Percentage of scale bar height compared to total figure height
    segments = Segment of scalebar
    tickTextPad = segment length text padding from the scale bar in factor


    '''
    #barX = 91
    #barY = 26
    #barLength = 200_000

    barXT, barYT = Transformer.from_crs(figureCRS, 'EPSG:3857', always_xy=True).transform(barX, barY)
    barX1, barY1 =  Transformer.from_crs('EPSG:3857', figureCRS, always_xy=True).transform(barXT+barLength, barYT)
    
    xlimits = ax.get_xlim()
    ylimits = ax.get_ylim()


    barLengthAngle = np.diff([barX1,barX])[0]
    #percentHeight = 1/56
    #segments = 4

    facecolor=['k', 'none']

    singleRectLenAngle = barLengthAngle/segments
    singleRectLen = barLength/segments


    for i in range(segments):

        xb,yb = Transformer.from_crs('EPSG:3857', figureCRS, always_xy=True).transform(barXT+(singleRectLen*i),barYT)
        rect = patches.Rectangle((xb, barY1), 
                                 singleRectLenAngle, np.diff(ylimits)[0]*percentHeight, linewidth=1,
                                 edgecolor='k',facecolor=facecolor[i%2])

        # Add the patch to the Axes
        ax.add_patch(rect)
     
    for i in range(segments+1):

        xb,yb = Transformer.from_crs('EPSG:3857', figureCRS, always_xy=True).transform(barXT+(singleRectLen*i),barYT)
        ax.text(xb+singleRectLenAngle, barY1-(barY1*tickTextPad), f'{int(singleRectLen*(i)/1000)}', va='top', ha='center')
    ax.text(barX1-(barX1*unitTextPadH), barY1-(barY1*tickTextPad*unitTextPadV), 'km', ha='right', va='top')
