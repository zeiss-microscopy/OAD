from pylibCZIrw import czi as pyczi
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from pathlib import Path
from processing_tools import segment_czi
from shapely.geometry import Polygon
from shapely.affinity import scale

# downscale CZI upon reading
sf = 0.2

min_objectsize = int(np.round(100000 / (1 / sf**2), 0))
max_holsize = int(np.round(1000 / (1 / sf**2), 0))

filepath = r"data\OverViewScan.czi"
savename_seg, results, csvfile, objects = segment_czi(
    filepath,
    savepath=r"data",
    chindex=0,
    filter_method="gaussian",
    filter_size=5,
    zoomlevel=sf,
    min_objectsize=min_objectsize,
    max_holesize=max_holsize,
    add_polygons=True,
)

# open original CZI and scaled CZI
with pyczi.open_czi(str(filepath)) as czidoc:
    # read a 2d image plane
    img = czidoc.read(plane={"C": 0})
    img_sc = czidoc.read(plane={"C": 0}, zoom=sf)

# open scaled segmented CZI
with pyczi.open_czi(str(savename_seg)) as czidoc:
    # read a 2d image plane
    img_seg = czidoc.read(plane={"C": 0})

# show the 2D image plane
fig1, ax = plt.subplots(3, 1, figsize=(12, 12))
ax[0].imshow(img_seg[..., 0], cmap=cm.inferno, vmin=img_seg.min(), vmax=img_seg.max())
ax[1].imshow(img_sc[..., 0], cmap=cm.inferno, vmin=img_sc.min(), vmax=img_sc.max())
ax[2].imshow(img[..., 0], cmap=cm.inferno, vmin=img.min(), vmax=img.max())


for tr_id in range(results.shape[0]):

    # get list with X and Y positions for polygon
    xpos = results["polygon"][tr_id][1]
    ypos = results["polygon"][tr_id][0]

    ax[0].plot(xpos, ypos, "w--", lw=2, alpha=1.0)
    ax[1].plot(xpos, ypos, "w--", lw=2, alpha=1.0)

    # get list of xy coordinates
    xy_coordinates = list(
        zip(results["polygon"][tr_id][1], results["polygon"][tr_id][0])
    )
    # Create the polygon
    polygon = Polygon(xy_coordinates)

    # scale the polygon to fit to the original CZI
    polygon = scale(polygon, xfact=1 / sf, yfact=1 / sf, origin=(0, 0))

    # Extract the exterior coordinates
    xy = polygon.exterior.coords.xy
    ax[2].plot(xy[0], xy[1], "w--", lw=2, alpha=1.0)


ax[0].set_title("Segmented Image Scale = " + str(sf))
ax[1].set_title("Scaled Image + Polygons")
ax[2].set_title("Original Image + Upscaled Polygons")
plt.show()
