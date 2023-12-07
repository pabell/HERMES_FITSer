import sys
import os
import struct
import glob

from HERMES_FITSer import *
    
dirname = sys.argv[1] 
outputs = []

# Options
# TODO: pass them as command-line arguments?
fm = "FM2"
gps_ok = True
aggregated = True

# Get the list of files contained in the directory, ordered by their hex value 
# (filename is the hex representation of the UNIX timestamp of the buffer)
files = glob.glob(dirname + os.sep + "*")
# The first option works if the file does not have any extension,
# the second should work in any case
# files.sort(key=lambda f: int(f.split(os.sep)[-1], base=16))
files.sort(key=lambda f: int(os.path.splitext(f)[0].split(os.sep)[-1], base=16))

# Cycle on every file in the directory and extract the byte buffer
# TODO: add exception if filesize=0 or less than minimum size
for filein in files:
    output = ingest_buffer(filein, verbose=True, aggregated=aggregated)
    outputs.append(output)
    
print("Readout", len(files), "files")

    
# Create FITS files    
writeFITS_LV0d5(outputs, dirname + "_LV0d5.fits", fm=fm, gps_ok=gps_ok)
writeFITS_HK(outputs, dirname + "_HK.fits", fm=fm)
writeFITS_LV0(outputs, dirname + "_LV0.fits", fm=fm, gps_ok=gps_ok)

