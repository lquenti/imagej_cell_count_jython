# Cell Counter using Labkit and Jython
Also counts as an example on how to use Jython in ImageJ.

## Use-Case `tif_to_particle_count.ijm.ijm.py`
We have a folder with multiple different pictures of different cells. Therefore, each folder needs their own trained labkit classifiers for counting those cells with specific attributes.

So the script expects the following substructure
```
.
├── DMSO
│   ├── AsPc1_blue.classifier
│   ├── AsPc1_total.classifier
│   ├── DMSO1.czi
│   ├── DMSO1.tif
│   ├── DMSO2_2.czi
│   ├── DMSO2_2.tif
│   ├── DMSO2.czi
│   ├── DMSO2.tif
│   ├── DMSO3.czi
│   ├── DMSO3.tif
│   ├── DMSO4.czi
│   ├── DMSO4.tif
│   ├── DMSO5.czi
│   └── DMSO5.tif
└── PM
    ├── AsPc1_blue.classifier
    ├── AsPc1_total.classifier
    ├── PM1.czi
    ├── PM1.tif
    ├── PM2.czi
    ├── PM2.tif
    ├── PM3.czi
    ├── PM3.tif
    ├── PM4.czi
    ├── PM4.tif
    ├── PM5_2.czi
    ├── PM5_2.tif
    ├── PM5.czi
    └── PM5.tif
```
As you can see, each classifier ends with `.classifier` and each file with `.tif`, all other files get ignored.
Now

- for each experiment
- for each classifier in that experiment
- run the following
- get all images in the same folder
- image segment all images
- use particle analysis on all images to find particles
- count them, dump them to a file

Note that the script does automatically fetch all files, as long as the structure is fine it it fully reusable.

After that, it creates subfolders based on the classifier name with all segmentation images as well as the counts (be careful, the area is in inch not pixel).
Just change the upper variables to configure it for your usecase.

## Postprocessing `get_counts.py`
I also wrote a script to collect all generated txt files in Python3 (run it externally, not in imagej). Just put it into the folder where your subexperiments are.

## Other tips
- The IJ.run() just takes the same name as the macro scripts
- use the macro recorder to get a feel of how to interact
- many functions expect the physical window to be opened beforehand

## Further resources
It was posted [in the imageJ forums](https://forum.image.sc/t/cell-counter-using-labkit-and-jython-code-example/95830/1) when it first was drafted.
