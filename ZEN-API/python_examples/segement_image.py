from processing_tools import segment_czi
from pylibCZIrw import czi as pyczi
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from zenapi_tools import set_logging

logger = set_logging()

filepath_overview = r"data\OverViewScan.czi"
open_czi = True

logger.info(f"Segment File: {filepath_overview}")
logger.error(f"Segment File: {filepath_overview}")
logger.debug(f"Segment File: {filepath_overview}")
logger.critical(f"Segment File: {filepath_overview}")
logger.warning(f"Segment File: {filepath_overview}")

savename_seg, results, csvfile, objects = segment_czi(
    filepath_overview,
    savepath=r"data",
    chindex=0,
    filter_method="gaussian",
    filter_size=7,
    min_objectsize=100000,
    max_holesize=1000,
    add_polygons=True,
)

if open_czi:

    with pyczi.open_czi(str(savename_seg)) as czidoc:
        # read a 2d image plane
        img2d = czidoc.read(plane={"C": 0})

    # show the 2D image plane
    fig1, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.imshow(img2d[..., 0], cmap=cm.inferno, vmin=img2d.min(), vmax=img2d.max())

    for tr_id in range(results.shape[0]):

        # get list with X and Y positions for polygon
        xpos = results["polygon"][tr_id][1]
        ypos = results["polygon"][tr_id][0]

        ax.plot(xpos, ypos, "w--", lw=2, alpha=1.0)

    ax.set_title(savename_seg)
    plt.show()

a = 1
