import numpy as np
import astropy.io.fits as pyfits 
import sys
import os
import struct
import glob

from HERMES_FITSer import *
    

dirname = sys.argv[1] 
outputs = []

# Get the list of files contained in the directory, ordered by their hex value 
files = glob.glob(dirname + os.sep + "*")
#files.sort(key=lambda f: int(f.split(os.sep)[-1], base=16))
files.sort(key=lambda f: int(os.path.splitext(f)[0].split(os.sep)[-1], base=16))

for filein in files:
    output = ingest_buffer(filein, verbose=True)
    outputs.append(output)
    
print("Readout", len(files), "files")

    
writeFITS_LV0d5(outputs, dirname + "_LV0d5.fits", fm="DM", gps_ok=True)
writeFITS_HK(outputs, dirname + "_HK.fits", fm="DM")
writeFITS_LV0(outputs, dirname + "_LV0.fits", fm="DM", gps_ok=True)

