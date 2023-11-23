import numpy as np
import astropy.io.fits as pyfits 
from astropy.time import Time
import struct
import os
import sys

from pylab import *

def readSRA(filein):
    # Get buffer file size
    filesize = os.path.getsize(filein)
    
    print(filein)
    
    print("Filesize is", filesize)
    
    n_seconds = int(filesize/124)
    
    print("So we should have", n_seconds, "seconds of data")
    
    n_of_points = 10*n_seconds

    lowEn_A = []
    lowEn_B = []
    lowEn_C = []
    lowEn_D = []
    midEn_A = []
    midEn_B = []
    midEn_C = []
    midEn_D = []
    higEn_A = []
    higEn_B = []
    higEn_C = []
    higEn_D = []
    
    abt_v = []
    
    f = open(filein, "rb")

    for k in range(n_seconds):
        # Parse and unpack the ABT (unsigned int)
        my_bytes = f.read(4)

        abt = int(struct.unpack('I', my_bytes)[0])
    
        # print("ABT is", abt)
        
        abt_v.append(abt)
    
        datapoint = []
        for band in range(3):
            for quadrant in range(4):
                for timepoint in range(10):
                    my_bytes = f.read(1)
                    datapoint.append(int(struct.unpack('B', my_bytes)[0]))
    
        for x in datapoint[:10]:
            lowEn_A.append(x)
        for x in datapoint[10:20]:
            lowEn_B.append(x)
        for x in datapoint[20:30]:
            lowEn_C.append(x)
        for x in datapoint[30:40]:
            lowEn_D.append(x)
        
    
        for x in datapoint[40:50]:
            midEn_A.append(x)
        for x in datapoint[50:60]:
            midEn_B.append(x)
        for x in datapoint[60:70]:
            midEn_C.append(x)
        for x in datapoint[70:80]:
            midEn_D.append(x)
        
    
        for x in datapoint[80:90]:
            higEn_A.append(x)
        for x in datapoint[90:100]:
            higEn_B.append(x)
        for x in datapoint[100:110]:
            higEn_C.append(x)
        for x in datapoint[110:120]:
            higEn_D.append(x)
        

    return lowEn_A, lowEn_B, lowEn_C, lowEn_D, midEn_A, midEn_B, midEn_C, midEn_D, higEn_A, higEn_B, higEn_C, higEn_D, abt_v

lowEn_A, lowEn_B, lowEn_C, lowEn_D, midEn_A, midEn_B, midEn_C, midEn_D, higEn_A, higEn_B, higEn_C, higEn_D, abt_v = readSRA(sys.argv[1])

fm = "DM"
time = np.arange(len(lowEn_A))*0.1 + abt_v[0]

unixtime = sys.argv[1].split("/")[-1]
t = Time(int(unixtime, base=16), format='unix')

print("UNIX time is", unixtime, "corresponding to", t.iso)


met_reference = Time(1325030381, format='gps')
print("MET reference time is", met_reference.iso)

met_start = t - met_reference
print("The observation thus starts at MET", met_start.sec)

outputfilename = sys.argv[1] + "_SRA.fits"

time_met = np.arange(len(lowEn_A))*0.1 + met_start.sec

fig, ax = plt.subplots(1,3, figsize=(16,6))

ax[0].plot(time_met, lowEn_A, drawstyle='steps-mid', label='A')
ax[0].plot(time_met, lowEn_B, drawstyle='steps-mid', label='B')
ax[0].plot(time_met, lowEn_C, drawstyle='steps-mid', label='C')
ax[0].plot(time_met, lowEn_D, drawstyle='steps-mid', label='D')
ax[0].set_title("Low energy band")
ax[0].set_xlabel("Mission Elapsed Time [s]")
ax[0].set_ylabel("Counts in 100 ms")
ax[0].legend()

ax[1].plot(time_met, midEn_A, drawstyle='steps-mid', label='A')
ax[1].plot(time_met, midEn_B, drawstyle='steps-mid', label='B')
ax[1].plot(time_met, midEn_C, drawstyle='steps-mid', label='C')
ax[1].plot(time_met, midEn_D, drawstyle='steps-mid', label='D')
ax[1].set_title("Mid energy band")
ax[1].set_xlabel("Mission Elapsed Time [s]")
ax[1].set_ylabel("Counts in 100 ms")
ax[1].legend()

ax[2].plot(time_met, higEn_A, drawstyle='steps-mid', label='A')
ax[2].plot(time_met, higEn_B, drawstyle='steps-mid', label='B')
ax[2].plot(time_met, higEn_C, drawstyle='steps-mid', label='C')
ax[2].plot(time_met, higEn_D, drawstyle='steps-mid', label='D')
ax[2].set_title("High energy band")
ax[2].set_xlabel("Mission Elapsed Time [s]")
ax[2].set_ylabel("Counts in 100 ms")
ax[2].legend()

fig.suptitle("Observation starts at " + t.iso)

savefig(sys.argv[1] + "_SRA.pdf", bbox_inches='tight')

t1hdu = pyfits.BinTableHDU.from_columns([
                                            pyfits.Column(name='TIME',
                                                           format='1D',
                                                           unit='s',
                                                           array=time_met),        
                                             pyfits.Column(name='BEE_ABT',
                                                            format='1D',
                                                            unit='s',
                                                            array=time),        
                                              pyfits.Column(name='LOW_QA',
                                                            format='1I',
                                                            array=lowEn_A),
                                              pyfits.Column(name='LOW_QB',
                                                            format='1I',
                                                            array=lowEn_B),
                                              pyfits.Column(name='LOW_QC',
                                                            format='1I',
                                                            array=lowEn_C),
                                              pyfits.Column(name='LOW_QD',
                                                            format='1I',
                                                            array=lowEn_D),
                                              pyfits.Column(name='MID_QA',
                                                            format='1I',
                                                            array=midEn_A),
                                              pyfits.Column(name='MID_QB',
                                                            format='1I',
                                                            array=midEn_B),
                                              pyfits.Column(name='MID_QC',
                                                            format='1I',
                                                            array=midEn_C),
                                              pyfits.Column(name='MID_QD',
                                                            format='1I',
                                                            array=midEn_D),
                                              pyfits.Column(name='HIG_QA',
                                                            format='1I',
                                                            array=higEn_A),
                                              pyfits.Column(name='HIG_QB',
                                                            format='1I',
                                                            array=higEn_B),
                                              pyfits.Column(name='HIG_QC',
                                                            format='1I',
                                                            array=higEn_C),
                                              pyfits.Column(name='HIG_QD',
                                                            format='1I',
                                                            array=higEn_D),
                                            ])

# Write FITS file
# "Null" primary array
prhdu = pyfits.PrimaryHDU()

met_offset = 0
exposure = abt_v[-1]-abt_v[0]

tref = Time(59580+0.00080074074 + met_offset, format='mjd')
tstop = Time(59580+0.00080074074+exposure/86400 + met_offset, format='mjd')

    
prhdu.header.set('TELESCOP', 'HERMES',  'Telescope name')
prhdu.header.set('INSTRUME', fm,  'Instrument name')
prhdu.header.set('TIMESYS', 'TT',  'Terrestrial Time: synchronous with, but 32.184')
prhdu.header.set('TIMEREF', 'LOCAL',  'Time reference')
prhdu.header.set('TIMEUNIT', 's',  'Time unit for timing header keywords')
prhdu.header.set('MJDREFI', 59580,  'MJD reference day 01 Jan 2022 00:00:00 UTC')
prhdu.header.set('MJDREFF', 0.00080074074,  'MJD reference (fraction part: 32.184 secs + 37')
prhdu.header.set('CLOCKAPP', False,  'Set to TRUE if correction has been applied to t')
prhdu.header.set('TELAPSE', exposure,  'TSTOP-TSTART')
prhdu.header.set('EXPOSURE', exposure,  'Exposure time')
prhdu.header.set('DATE-OBS', tref.fits,  'Start date of observations')
prhdu.header.set('DATE-END', tstop.fits,  'End date of observations')


t1hdu.header.set('EXTNAME', 'SRA',  'Name of this binary table extension')
t1hdu.header.set('TELESCOP', 'HERMES',  'Telescope name')
t1hdu.header.set('INSTRUME', fm,  'Instrument name')
t1hdu.header.set('TIMESYS', 'TT',  'Terrestrial Time: synchronous with, but 32.184')
t1hdu.header.set('TIMEREF', 'LOCAL',  'Time reference')
t1hdu.header.set('TIMEUNIT', 's',  'Time unit for timing header keywords')
t1hdu.header.set('MJDREFI', 59580,  'MJD reference day 01 Jan 2022 00:00:00 UTC')
t1hdu.header.set('MJDREFF', 0.00080074074,  'MJD reference (fraction part: 32.184 secs + 37')
t1hdu.header.set('CLOCKAPP', 'F',  'Set to TRUE if correction has been applied to t')
t1hdu.header.set('EXPOSURE', exposure,  'Exposure time')
t1hdu.header.set('TSTART', 0,  'Start: Elapsed secs since HERMES epoch')
t1hdu.header.set('TSTOP', exposure,  'Stop: Elapsed secs since HERMES epoch')
t1hdu.header.set('TELAPSE', exposure,  'TSTOP-TSTART')
t1hdu.header.set('DATE-OBS', tref.fits,  'Start date of observations')
t1hdu.header.set('DATE-END', tstop.fits,  'End date of observations')

hdulist = pyfits.HDUList([prhdu, t1hdu])
hdulist.writeto(outputfilename, overwrite=True, checksum=True)


show()