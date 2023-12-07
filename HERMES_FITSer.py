import numpy as np
import astropy.io.fits as pyfits 
from astropy.time import Time
import struct
import os

"""
Converter from PDHU binary buffer files to LV0 FITS
R. Campana INAF/OAS
2023-11-23 - Version 17

Based on raw data structure specification 2023-11-17 v12

Based on FITS LV0 and LV0.5 file structure specification 2023-11-17
"""


class Header(object):
    """
    Class for an HEADER object
    """
    def __init__(self, header_bytes):
        self.GPS_Time = {}
        self.BEE_HK = {}
        self.Det_Temp = [0.]*7
        self.CSAC_HK = {}
        self.recordCounter0 = 0
        self.recordCounter1 = 0
        self.recordCounter2 = 0
        self.recordCounter3 = 0
        assert len(header_bytes) == 128
        self.string_breakdown(header_bytes)
            
    def printGPSTime(self):
        print("GPS Time")     
        
        print("\t GPS Offset : \t\t", self.GPS_Time["GPSOffset"])   
        print("\t UTC Offset : \t\t", self.GPS_Time["UTCOffset"])   
        
        print("\t Week Seconds: \t\t", self.GPS_Time["WeekSeconds"])   
        print("\t Week : \t\t", self.GPS_Time["Week"])   
        
        print("\t GPS Status: \t\t", self.GPS_Time["GPSStatus"])   
   
    def printCSAC_HK(self):
        print("CSAC Housekeepings")
        
        print("\t Status:\t\t", self.CSAC_HK["CSACStatus"])
        print("\t Laser current:\t\t {:.2f} mA".format(self.CSAC_HK["LaserI"]))
        print("\t Heater power:\t\t {:.2f} mW".format(self.CSAC_HK["HeatP"]))
        print("\t Temperature:\t\t {:.2f} °C".format(self.CSAC_HK["Temp"]))
        
    def printBEE_HK(self):
        print("BEE Housekeepings")
        
        print("\t ABT OBT:\t\t", self.BEE_HK["ABT_OBT"])
        print("\t ABT ns counter:\t", self.BEE_HK["ABT_CNT"])
                
        print("\t Trigger counter: \t", self.BEE_HK["TriggerCounter"])
        print("\t Rejected evt counter: \t", self.BEE_HK["RejectedCounter"])
        print("\t Event counter: \t", self.BEE_HK["EventCounter"])
        print("\t Overflow counter: \t", self.BEE_HK["OverflowCounter"])
                
        print("\t Quadrant Status: \t", self.BEE_HK["QuadrantStatus"])
                
        print("\t 3V3D Voltage: \t\t {:.2f} V".format(self.BEE_HK["3V3D"]))
        print("\t 3V3D Current: \t\t {:.2f} mA".format(self.BEE_HK["3V3D_I"]))
        
        print("\t 3V3A Voltage: \t\t {:.2f} V".format(self.BEE_HK["3V3A"]))
        print("\t 3V3A Current: \t\t {:.2f} mA".format(self.BEE_HK["3V3A_I"]))
        
        print("\t 2V0 Voltage: \t\t {:.2f} V".format(self.BEE_HK["2V0"]))
        print("\t 2V0 Current:  \t\t {:.2f} mA".format(self.BEE_HK["2V0_I"]))
        
        print("\t 5V0-FEE Voltage: \t {:.2f} V".format(self.BEE_HK["5V0-FEE"]))
        print("\t 5V0-FEE Current:  \t {:.2f} mA".format(self.BEE_HK["5V0-FEE_I"]))
        
        print("\t 3V3-BEE Voltage: \t {:.2f} V".format(self.BEE_HK["3V3-BEE"]))
        print("\t 3V3-BEE Current: \t {:.2f} mA".format(self.BEE_HK["3V3-BEE_I"]))
        
        print("\t 5V0-BEE Voltage: \t {:.2f} V".format(self.BEE_HK["5V0-BEE"]))
        print("\t 5V0-BEE Current: \t {:.2f} mA".format(self.BEE_HK["5V0-BEE_I"]))
        
        print("\t 12V0 Voltage: \t\t {:.2f} V".format(self.BEE_HK["12V0"]))
        print("\t 12V0 Current: \t\t {:.2f} mA".format(self.BEE_HK["12V0_I"]))
        
        print("\t HV Voltage: \t\t {:.2f} V".format(self.BEE_HK["HV"]))
        
            
    
    def printDetectorTemperatures(self):
        print("Detector temperatures")
        
        print("\t BEE Temperature  :\t {:.1f} °C".format(self.Det_Temp[0]))
        print("\t FEE Temperature 1:\t {:.1f} °C".format(self.Det_Temp[1]))
        print("\t FEE Temperature 2:\t {:.1f} °C".format(self.Det_Temp[2]))
        print("\t FEE Temperature 3:\t {:.1f} °C".format(self.Det_Temp[3]))
        print("\t FEE Temperature 4:\t {:.1f} °C".format(self.Det_Temp[4]))
        print("\t FEE Temperature 5:\t {:.1f} °C".format(self.Det_Temp[5]))
        print("\t FEE Temperature 6:\t {:.1f} °C".format(self.Det_Temp[6]))
        

    def string_breakdown(self, header_bytes):
        """
        First 24 bytes (0:24) are the GPS time
        Structure:
            GPS Offset      8 bytes 
            UTC Offset      8 bytes 
            Week_seconds    4 bytes 
            Week            2 bytes 
            Status          1 byte  
            SPARE           1 byte  
        """
        gps_string = header_bytes[:24]
        
        # self.GPS_Time["GPSOffset"] = struct.unpack('Q', gps_string[0:8])[0]
        # self.GPS_Time["UTCOffset"] = struct.unpack('Q', gps_string[8:16])[0]
        # self.GPS_Time["WeekSeconds"] = struct.unpack('I', gps_string[16:20])[0]
        # self.GPS_Time["Week"] = struct.unpack('h', gps_string[20:22])[0]
        # self.GPS_Time["GPSStatus"] = int(gps_string[22:23].hex(), base=16)
        
        
        self.GPS_Time["GPSOffset"] = int(struct.unpack('d', gps_string[0:8])[0])
        self.GPS_Time["UTCOffset"] = int(struct.unpack('d', gps_string[8:16])[0])
        self.GPS_Time["WeekSeconds"] = int(struct.unpack('f', gps_string[16:20])[0])
        self.GPS_Time["Week"] = struct.unpack('h', gps_string[20:22])[0]
        self.GPS_Time["GPSStatus"] = int(gps_string[22:23].hex(), base=16)
        
        
        """
        Second chunk of 64 bytes (24:88) are the BEE HKs
        Structure:
            ABT                 8 bytes (4 bytes OBT, 4 bytes 100 ns counter)
            Trigger counter     8
            Rejected counter    8
            Event counter       8
            Event overflow      8
            Status              5
            Voltages/currents
        """
        hk_string = header_bytes[24:88]
        
        self.BEE_HK["ABT_OBT"] = struct.unpack('I', hk_string[0:4])[0] 
        self.BEE_HK["ABT_CNT"] = struct.unpack('I', hk_string[4:8])[0] 
        
        
        
        
        tmp_trgCnt = hk_string[8:16]
        triggerCounter = [0]*4
        for i,j in enumerate(range(0,7,2)):
            triggerCounter[i] = struct.unpack('h', tmp_trgCnt[j:j+2])[0]
        self.BEE_HK["TriggerCounter"] = triggerCounter
        
        tmp_rejCnt = hk_string[16:24]
        rejectedCounter = [0]*4
        for i,j in enumerate(range(0,7,2)):
            rejectedCounter[i] = struct.unpack('h', tmp_rejCnt[j:j+2])[0]
        self.BEE_HK["RejectedCounter"] = rejectedCounter
         
        tmp_evtCnt = hk_string[24:32]
        eventCounter = [0]*4
        for i,j in enumerate(range(0,7,2)):
            eventCounter[i] = struct.unpack('h', tmp_evtCnt[j:j+2])[0]
        self.BEE_HK["EventCounter"] = eventCounter
        
        tmp_ovfCnt = hk_string[32:40]
        overflowCounter = [0]*4
        for i,j in enumerate(range(0,7,2)):
            overflowCounter[i] = struct.unpack('h', tmp_ovfCnt[j:j+2])[0]
        self.BEE_HK["OverflowCounter"] = overflowCounter
        
        
        status0        = [int(x) for x in format(int(hk_string[40:41].hex(), base=16), '08b')]
        status1        = [int(x) for x in format(int(hk_string[41:42].hex(), base=16), '08b')]
        status2        = [int(x) for x in format(int(hk_string[42:43].hex(), base=16), '08b')]
        status3        = [int(x) for x in format(int(hk_string[43:44].hex(), base=16), '08b')]
        status4        = [int(x) for x in format(int(hk_string[44:45].hex(), base=16), '08b')]
        
        self.BEE_HK["QuadrantStatus"] = status0+status1+status2+status3+status4
        
        
        # Conversion factors for voltage and current HKs
        gain_3V3D        = 1.561797753
        gain_3V3A        = 1.561797753
        gain_3V3_BEE     = 1.561797753
        gain_2V0         = 1.0
        gain_5V0_FEE     = 2.395348837
        gain_HV          = 101
        gain_12V0        = 5.4
        gain_5V0_BEE     = 2.395348837
        
        offset_3V3D      = 6
        offset_3V3A      = 6
        offset_3V3_BEE   = 6
        offset_2V0       = 0
        offset_5V0_FEE   = 6
        offset_HV        = 0
        offset_12V0      = 6
        offset_5V0_BEE   = 6
        
        gain_current = 20
        offset_current = 0
        
        rsense_3V3D      = 0.5
        rsense_3V3A      = 0.5
        rsense_3V3_BEE   = 0.01
        rsense_2V0       = 0.5	
        rsense_5V0_FEE   = 0.33	
        rsense_12V0      = 0.33	
        rsense_5V0_BEE   = 0.33	        
        
        lsb_adc = 0.009765625
        
        self.BEE_HK["3V3D_raw"]         = int(hk_string[48:49].hex(), base=16)
        self.BEE_HK["3V3A_raw"]         = int(hk_string[49:50].hex(), base=16)
        self.BEE_HK["3V3-BEE_raw"]      = int(hk_string[50:51].hex(), base=16)
        self.BEE_HK["2V0_raw"]          = int(hk_string[51:52].hex(), base=16)
        self.BEE_HK["5V0-FEE_I_raw"]    = int(hk_string[52:53].hex(), base=16)
        self.BEE_HK["5V0-FEE_raw"]      = int(hk_string[53:54].hex(), base=16)
        self.BEE_HK["2V0_I_raw"]        = int(hk_string[54:55].hex(), base=16)
        self.BEE_HK["5V0-BEE_I_raw"]    = int(hk_string[55:56].hex(), base=16)
        self.BEE_HK["3V3-BEE_I_raw"]    = int(hk_string[56:57].hex(), base=16)
        self.BEE_HK["HV_raw"]           = int(hk_string[57:58].hex(), base=16)
        self.BEE_HK["12V0_I_raw"]       = int(hk_string[58:59].hex(), base=16)
        self.BEE_HK["12V0_raw"]         = int(hk_string[59:60].hex(), base=16)
        self.BEE_HK["5V0-BEE_raw"]      = int(hk_string[60:61].hex(), base=16)
        self.BEE_HK["3V3D_I_raw"]       = int(hk_string[61:62].hex(), base=16)
        self.BEE_HK["3V3A_I_raw"]       = int(hk_string[62:63].hex(), base=16)
        
                    
        self.BEE_HK["3V3D"]      = (self.BEE_HK["3V3D_raw"]      + offset_3V3D) * gain_3V3D * lsb_adc
        self.BEE_HK["3V3A"]      = (self.BEE_HK["3V3A_raw"]      + offset_3V3A) * gain_3V3A * lsb_adc
        self.BEE_HK["3V3-BEE"]   = (self.BEE_HK["3V3-BEE_raw"]   + offset_3V3_BEE) * gain_3V3_BEE * lsb_adc
        self.BEE_HK["2V0"]       = (self.BEE_HK["2V0_raw"]       + offset_2V0) * gain_2V0 * lsb_adc
        self.BEE_HK["5V0-FEE_I"] = (self.BEE_HK["5V0-FEE_I_raw"] + offset_current) * lsb_adc/(gain_current * rsense_5V0_FEE) * 1000
        self.BEE_HK["5V0-FEE"]   = (self.BEE_HK["5V0-FEE_raw"]   + offset_5V0_BEE) * gain_5V0_BEE * lsb_adc
        self.BEE_HK["2V0_I"]     = (self.BEE_HK["2V0_I_raw"]     + offset_current) * lsb_adc/(gain_current * rsense_2V0) * 1000
        self.BEE_HK["5V0-BEE_I"] = (self.BEE_HK["5V0-BEE_I_raw"] + offset_current) * lsb_adc/(gain_current * rsense_5V0_BEE) * 1000
        self.BEE_HK["3V3-BEE_I"] = (self.BEE_HK["3V3-BEE_I_raw"] + offset_current) * lsb_adc/(gain_current * rsense_3V3_BEE) * 1000
        self.BEE_HK["HV"]        = (self.BEE_HK["HV_raw"]        + offset_HV) * gain_HV * lsb_adc
        self.BEE_HK["12V0_I"]    = (self.BEE_HK["12V0_I_raw"]    + offset_current) * lsb_adc/(gain_current * rsense_12V0) * 1000
        self.BEE_HK["12V0"]      = (self.BEE_HK["12V0_raw"]      + offset_12V0) * gain_12V0 * lsb_adc
        self.BEE_HK["5V0-BEE"]   = (self.BEE_HK["5V0-BEE_raw"]   + offset_5V0_BEE) * gain_5V0_BEE * lsb_adc
        self.BEE_HK["3V3D_I"]    = (self.BEE_HK["3V3D_I_raw"]    + offset_current)* lsb_adc/(gain_current * rsense_3V3D) * 1000
        self.BEE_HK["3V3A_I"]    = (self.BEE_HK["3V3A_I_raw"]    + offset_current)* lsb_adc/(gain_current * rsense_3V3A) * 1000
        
        
        """
        Third chunk of 16 bytes (88:104) are the detector temperatures
        Each is a 2-bytes signed integer (decimal Celsius with a 0.1 degrees step)
        Structure:
            BEE Temp 1      2 bytes 
            FEE Temp 1      2 bytes 
            FEE Temp 2      2 bytes 
            FEE Temp 3      2 bytes 
            FEE Temp 4      2 bytes 
            FEE Temp 5      2 bytes 
            FEE Temp 6      2 bytes 
            SPARE           2 bytes 
        """
        temp_string = header_bytes[88:104]
        for i,j in enumerate(range(0,14,2)):
            single_temp = temp_string[j:j+2]
            self.Det_Temp[i] = struct.unpack("h", single_temp)[0]/10.
            
        """
        Fourth chunk of 7 bytes (111:115) is the CSAC HKs
        4-bytes unsigned integer
        """
        csac_string = header_bytes[104:111]
        self.CSAC_HK["CSACStatus"] = int(csac_string[0:1].hex(), base=16)
        self.CSAC_HK["LaserI"] = (struct.unpack('H', csac_string[1:3])[0]) * 0.01
        self.CSAC_HK["HeatP"]  = (struct.unpack('H', csac_string[3:5])[0]) * 0.01
        self.CSAC_HK["Temp"]   = (struct.unpack('H', csac_string[5:7])[0]) * 0.01
            
            
        """
        Fifth, sixth, seventh and eight chunks of 4 bytes (111:127) are the record counters
        4-bytes unsigned integers
        """
        self.recordCounter0 = struct.unpack('I', header_bytes[111:115])[0]
        self.recordCounter1 = struct.unpack('I', header_bytes[115:119])[0]
        self.recordCounter2 = struct.unpack('I', header_bytes[119:123])[0]
        self.recordCounter3 = struct.unpack('I', header_bytes[123:127])[0]
        
        
        """
        Final chunk is spare
        """   


class Event(object):
    def __init__(self, time_mark, multiplicity):
        self.time_mark = time_mark
        self.multiplicity = multiplicity
        self.pixelEvents = []
        self.rejectedMap = None
    
    def __str__(self):
        output_str = "Event: \n"
        output_str += "Time mark: {:d}\n".format(self.time_mark)
        output_str += "Multiplicity: {:d}\n".format(self.multiplicity)
        for i, pixelevent in enumerate(self.pixelEvents):
            if pixelevent.evtype == 1 or pixelevent.evtype == 2:
                output_str += "Pixel event. ASIC: {:d}, Address: {:d}, ADC: {:d}\n".format(pixelevent.asicID, pixelevent.channel, pixelevent.adc)
            if pixelevent.evtype == 0:
                output_str += "ABT event. OBT seconds {:d}, OBT nanoseconds: {:d}\n".format(pixelevent.obt_s, pixelevent.obt_ns)
        if self.rejectedMap is not None:
                output_str += "REJECTED event. Rejected map: {:s}\n".format(self.rejectedMap)
        return output_str
        
    def addPixelEvent(self, pixel):
        self.pixelEvents.append(pixel)
   
    def addRejectedMap(self, rej_map):
        self.rejectedMap = rej_map
       
 
class PixelEvent(object):
    def __init__(self, evtype, asicID=0, channel=0, adc=0, obt_s=0, obt_ns=0):
        self.evtype = evtype
        self.asicID = asicID
        self.channel = channel
        self.adc = adc
        self.obt_s = obt_s
        self.obt_ns = obt_ns
 
 
def parseRecordData(buf, verbose=False):
    """
    Parses the buffer data (record list) and identify Event types.
    Input:
        buf = buffer of bytes
    Output:
        eventBuffer, (timeCounter, pixelCounter, abtCounter, rejCounter)
        where:
            eventBuffer = array of Event objects
            timeCounter = counter of TIME records detected
            pixelCounter = counter of PIXEL events detected
            abtCounter = counter of ABT events detected
            rejCounter = counter of REJ events detected
    """ 
    timeCounter = 0
    pixelCounter = 0
    abtCounter = 0
    rejCounter = 0
    
    time_mark_lsb_timeEvt = 0
    mult = 0

    try:
        assert len(buf) % 4 == 0
    except AssertionError:
        print("\n*** ERROR ***")
        print("Buffer is not an integer number of records!\n")
        exit(1)
    

    n_records = len(buf)//4
    
    print("N. of records in the byte buffer:", n_records)

    eventBuffer = []
    event = None
    abt_found = False
    rej_found = False
    obt_s = None
    
    flushEmptyEvent = False
    
    for i in range(n_records):
        if verbose:
            print("--> Current record", i, "that is", i+1, "of", n_records)

        # Convert the record bytes in a string with its binary representation               
        record_buf = buf[i*4:i*4+4]
        record_string = ''
        for b in record_buf:
            record_string += f'{b:0>8b}'
        if verbose:
            print(record_string)
            
        # Check that we are not in the next record after a first ABT/REJ record
        if (not abt_found) and (not rej_found):
            # Time event
            if record_string[:3] == '101':
                sdd_multiplicity = int(record_string[3:8], base=2)
                time_mark = int(record_string[8:], base=2)
                time_mark_lsb_timeEvt = record_string[-4:]
                
                if verbose:
                    print("TIME EVENT", "with multiplicity", sdd_multiplicity)
                    print("Time mark", record_string[8:], time_mark)
        
                # Push previous event(s) in the buffer
                if event is not None:
                    eventBuffer.append(event)
        
                # Initialise a new Event object
                event = Event(time_mark, sdd_multiplicity)
        
                mult = 1
                if sdd_multiplicity > 1:
                    mult = 2
            
                timeCounter += 1
                
            # Pixel event    
            elif record_string[:1] == '0':
                
                # Quadrant ID
                asicID = int(record_string[1:3], base=2)
                # LYRA-BE channel value
                channel = int(record_string[3:8], base=2)
                
                # Time mark should be checked for consistency with the TIME event!
                time_mark_lsb = record_string[8:12]
                if time_mark_lsb != time_mark_lsb_timeEvt:
                    print("WARNING: Time mark LSB mismatch!")
                    
                trigger = int(record_string[15:16])
                adc = int(record_string[16:], base=2) 

                if verbose:
                    print("PIXEL EVENT", "ASIC", asicID, "Channel", channel, "Time mark LSB", time_mark_lsb, "ADC", adc)
            
                # Define a new PixelEvent object and append it to the relative Event object member
                pixel = PixelEvent(mult, asicID=asicID, channel=channel, adc=adc)
                if event is not None:
                    event.addPixelEvent(pixel)

                pixelCounter += 1
             
            # First record of ABT event    
            elif record_string[:3] == '111':
                abt_found = True
                obt_s = int(record_string[3:], base=2)
                abtCounter += 1

                if verbose:
                    print("ABT EVENT PART 1", "with OBT", obt_s)
                
                
            # First record of REJ event (REJ TIME EVENT)
            elif record_string[:3] == '100':
                rej_found = True
                
                time_mark = int(record_string[8:], base=2)
                
                if verbose:
                    print("REJ TIME EVENT", "with time_mark", time_mark)
                
                # Initialise a new Event object with multiplicity -1 (REJECTED)
                event = Event(time_mark, -1)
                
        # In case we are on the second record of an ABT event
        elif abt_found and (not rej_found):
            # Second record of ABT event
            if verbose:
                print("ABT EVENT RECORD PART 2")

            obt_ns = int(record_string[7:], base=2)

            abt = PixelEvent(0, obt_s=obt_s, obt_ns=obt_ns)
            
            if event is not None:
                # If an event object already exists, add the ABT to its pixel event list
                event.addPixelEvent(abt)
                
                # print("len(event.pixelEvents)", len(event.pixelEvents))
                # print("event.time_mark", event.time_mark)
                # for x in event.pixelEvents:
                #     print("event.pixelEvent", x.evtype, x.asicID, x.channel, x.adc, x.obt_s, x.obt_ns)
                
            else:
                # Create a fake event (timemark 0, multiplicity 0) to handle buffers starting with an ABT record
                event = Event(0, 0)
                event.addPixelEvent(abt)
                print("FAKE EVENT CREATED -- Apparently the buffer starts with an ABT.")
            abt_found = False
            
        # In case we are at the second record of a REJ event        
        elif (not abt_found) and rej_found:
            # Second record of REJ event (REJ PIXEL EVENT)

            rej = record_string[:]
            
            if verbose:
                print("REJ PIXEL EVENT", "with map", rejMap)

            if event is not None:
                # If an event object already exists (should always be the case), assign the Rejected Events map to its corresponding member
                event.addRejectedMap(rej)
            else:
                # This should not happen.
                print("*** ERROR! REJECTED PIXEL EVENT WITHOUT PRIOR REJECTED TIME EVENT!")

            rej_found = False
            rejCounter += 1
        
        else:
            # This should not happen.
            print("*** ERROR! UNKNOWN STATE!")
        
        # If we are at the end of the record list, flush everything.        
        if (event is not None) and (i == n_records-1):
            eventBuffer.append(event)
            flushEmptyEvent = False
        
        
    return eventBuffer, (timeCounter, pixelCounter, abtCounter, rejCounter)
    

def ingest_buffer(filein, verbose=True, aggregated=False):
    """
    Ingests a PDHU buffer file.
    Returns the Header and Event Data arrays found for each quadrant,
    i.e., an array of tuples (HEADER, [EVENT DATA])
    Input: 
        filein = name of the binary buffer file
    Output:
        array of tuples [(HEADER, [EVENT DATA]), ...]
    One element for each buffer found in the file (at least four elements, if one buffer per file)

    Header is the first 128 bytes
    GPS time            24 bytes
    BEE HKs             64 bytes
    Det. temp.          16 bytes
    CSAC HKs            7 bytes
    Record counter 0    4 bytes
    Record counter 1    4 bytes
    Record counter 2    4 bytes
    Record counter 3    4 bytes
    SPARE               1 byte

    Each event data record is 4 bytes long
    The number of records is defined by bytes 111:115, 115:119, 119:123, 123:127 in the header
    for each quadrant
    """
    # Initialise output
    output = []
    
    # Get buffer file size
    filesize = os.path.getsize(filein)
    
    header_size = 128
    aggHeader_size = 25
    
    if aggregated:
        print("*** PARSING AGGREGATED FILES ***")
    
    try:
        assert filesize > header_size
    except AssertionError:
        print("\n***ERROR***")
        print("In buffer", filein)
        print("Buffer file size smaller than minimum!")
        print("Detected file size:", filesize,"\n")
        exit(1)
    
    print(filein)
    f = open(filein, "rb")
    
    endOfFileReached = False
    output_buffer = None

    while(not endOfFileReached):
        # Flush the output
        if output_buffer is not None:
            output.append(output_buffer)
        output_buffer = []
    
        if aggregated:
            # If the file has been aggregated with headers
            # parse skipping the headers
            # Parse the aggregated header
            my_bytes = f.read(aggHeader_size)
            print("Parsed aggregated header.")
            
            for b in my_bytes:
                print(hex(b), int(b), chr(b))
            
            print(my_bytes)
            
            # Aggregated header structure:
            # 8 byte: filename string
            # 1 byte: "-"
            # 8 byte: filesize (u32_FileSize)
            # 1 byte: " " (empty char)
            # 1 byte:"B"
            agg_filename = str(struct.unpack('13s', my_bytes[0:13])[0])
            #agg_hypen    = struct.unpack('1s', my_bytes[14])[0]
            agg_filesize = struct.unpack('8s', my_bytes[15:23])[0]
            #agg_control  = struct.unpack('c', my_bytes[18])[0]
            print("*** Aggregated header ***")
            print("\t Filename", agg_filename)
            print("\t Hypen", my_bytes[14])
            print("\t Filesize", agg_filesize)
            # print("\t Control", agg_control)
            
    
        # Parse the header
        my_bytes = f.read(header_size)
        print("Parsed an header.")

        # Unpack the header
        header = Header(my_bytes)
    
        if verbose:
            # Print header info
            header.printGPSTime()
            header.printCSAC_HK()
            header.printBEE_HK()
            header.printDetectorTemperatures()
            print("Record counter quadrant A: \t\t", header.recordCounter0)
            print("Record counter quadrant B: \t\t", header.recordCounter1)
            print("Record counter quadrant C: \t\t", header.recordCounter2)
            print("Record counter quadrant D: \t\t", header.recordCounter3)

        # Parse the event data.
        # Fetch the next sum_i(4*header.recordCounter_i) bytes
        # If there is only one quadrant buffer, this is down to the end of file!
        # There are at maximum 4 quadrants, so we check if we are at the end of file 
        # before iterating next to header + record_list.
        counters = [header.recordCounter0, header.recordCounter1, header.recordCounter2, header.recordCounter3]
    
        assert len(counters) == 4
    
        for asicid, quadrant in enumerate(counters):
            print("Reading quadrant", asicid, "with", counters[asicid], "records...")
        
            if counters[asicid] > 0:
                # If the expected number of records is greater than zero,
                # read out 4 bytes for each record
                record_list_bytes = 4*counters[asicid]
                my_bytes = f.read(record_list_bytes)
        
                # Unpack the event data buffer
                eventBuffer, (timeCounter, pixelCounter, abtCounter, rejCounter) = parseRecordData(my_bytes)
                header.ASIC_ID = asicid
        
                # Add to the output the (header, event_data) tuple read out just now 
                output_buffer.append((header, eventBuffer))
                        
                # Debug code                
                # print(  "Triggers: ", header.BEE_HK["TriggerCounter"][asicid], \
                #         "Events: ", header.BEE_HK["EventCounter"][asicid], \
                #         "Rejected events: ", header.BEE_HK["RejectedCounter"][asicid], \
                #         "Overflow events: ", header.BEE_HK["OverflowCounter"][asicid])
                # print("Check if BEE counters match:", header.BEE_HK["TriggerCounter"][asicid]==\
                #     header.BEE_HK["EventCounter"][asicid]+header.BEE_HK["RejectedCounter"][asicid]+header.BEE_HK["OverflowCounter"][asicid])
                #
                # print("TIME events: ", timeCounter, "PIXEL events: ", pixelCounter, "ABT events: ", abtCounter, "REJ events: ", rejCounter)
                # if timeCounter + pixelCounter + rejCounter + abtCounter*2 == counters[asicid]:
                #     print("Parsed all records")
                # else:
                #     print("*** MISMATCH ***", timeCounter + pixelCounter + rejCounter + abtCounter*2)
                # print("*** DEVIATION ", header.BEE_HK["EventCounter"][asicid]-timeCounter, (header.BEE_HK["EventCounter"][asicid]-timeCounter)/timeCounter)
            else:
                print("Flushing quadrants with zero counts...")
                output_buffer.append((header, []))
    
        if f.tell() == filesize:
            print("End of file reached.\n\n")
            # Final flush
            if output_buffer is not None:
                output.append(output_buffer)
            endOfFileReached = True
        else:
            print("We are at byte", f.tell(), "of filesize", filesize)
            print("Continue reading...")
            
    f.close()
    return output






def ingest_BEE_file(filein, verbose=True, len_packet_file=False):
    """
    Ingests a BEE ASCII buffer file.
    Returns an array of None and an array of Event Data:
    i.e., an array of tuples (None, [EVENT DATA])
    Input: 
        filein = name of the binary buffer file
    Output:
        array of tuples (None, [EVENT DATA])
    (Header is missing here!)
    """
    event_list = []
    event_packet = []
    s = 0
    good_buffer = True
    bufcount = 0
    bufcount_good = 0
    
    final_event_buffer = []
    found_start = False
    f = open(filein)
    
    eventBuffer = []
    quadrantInfoBuffer = []
    
    if len_packet_file:
        bf = open("buffer_len.dat","w")
    for line in f.readlines()[5:]:
        if not line[:1] == 'B':
            if line[:1] == 'Q': 
                # Check if this is a good buffer
                #print(line)
                quadrant_from_buffer = int(line.split(":")[1].split(";")[0])
                good_buffer = eval(line.split(":")[2].strip())
                if good_buffer:
                    bufcount_good += 1                             
                bufcount += 1
            elif line[:1] != 'Q' and good_buffer and not found_start:
                found_start = True
            if found_start:
                buf = line.split()
                if len(buf) % 4 == 0:
                    if len_packet_file:
                        if len(buf)>0:
                            bf.write("{:d}\n".format(len(buf)))
                    k = 0
                    buf_reshaped = np.array(buf).reshape(int(len(buf)/4), 4)
                    for x in buf_reshaped:
                        final_event_buffer.append(x)
                        quadrantInfoBuffer.append(quadrant_from_buffer)
            # else:
            #     print("Skipping...")
    if len_packet_file:
        bf.close()         
    final_event_buffer = np.array(final_event_buffer)
    # Parse final buffer
    abt = False
    event = None
    
    waitEvent = None
    
    for k in range(len(final_event_buffer)):
    
        if final_event_buffer[k][0] == 'E0':
            # That is an ABT event
            hexstring = ''.join(final_event_buffer[k])+''.join(final_event_buffer[k+1])
            # print(hexstring)
            abt = True
            binstring = '{:064b}'.format(int(hexstring, base=16))
            data_type = int(binstring[:3], base=2)
            obt_s = int(binstring[4:32], base=2)
            obt_ns = int(binstring[-24:], base=2)
            if verbose:
                print("ABT evt", data_type, obt_s, obt_ns)
            abt_event = PixelEvent(0, asicID=quadrantInfoBuffer[k], obt_s=obt_s, obt_ns=obt_ns)
           
            if (quadrantInfoBuffer[k]-quadrantInfoBuffer[k-1]) != 0:
                print(quadrantInfoBuffer[k]-quadrantInfoBuffer[k-1], obt_s)
                print("Buffer starting with ABT. Inserting a fake TIME/PIXEL evt")
                event = Event(0, 1)
                fake_pixel = PixelEvent(1, asicID=quadrantInfoBuffer[k], channel=0, adc=0)
                event.addPixelEvent(fake_pixel)
                event.addPixelEvent(abt_event)
            else:
                if event is not None:
                    event.addPixelEvent(abt_event)
                
        else:
            if not abt:
                hexstring = ''.join(final_event_buffer[k])
                binstring = '{:032b}'.format(int(hexstring, base=16))
                if binstring[:3] == '101':
                    # TIME event
                    # print(hexstring)
                    # print(binstring)
                    sdd_fired = int(binstring[3:8], base=2)
                    time_mark_100ns = int(binstring[8:], base=2)
                    if verbose:
                        print("TIME evt", sdd_fired, time_mark_100ns)
                    # Push previous event(s) in the buffer
                    if event is not None:
                        eventBuffer.append(event)
                    # Initialise a new Event object
                    event = Event(time_mark_100ns, sdd_fired)
                    
                if binstring[:1] == '0':
                    # PIXEL event                    
                    asic_id = int(binstring[1:3], base=2)
                    channel = int(binstring[3:8], base=2)
                    time_nibble = int(binstring[8:12], base=2)
                    adc = int(binstring[-16:], base=2)
                    if verbose:
                        print("PIXEL evt", asic_id, channel, time_nibble, adc)
                    # Define a new PixelEvent object and add it to the Event object
                    pixel = PixelEvent(sdd_fired, asicID=asic_id, channel=channel, adc=adc)
                    if event is not None:
                        event.addPixelEvent(pixel)
                        if waitEvent is not None:
                            event.addPixelEvent(waitEvent)
                    
                    # print(hexstring)
                    # print(binstring)
                    # print(asic_id, channel, time_nibble, adc)
                    
                    
            if abt:
                # That is the last 4 bytes of an ABT, skip
               abt = False
                                   
        
    f.close()
    
    print("Found a total of {:d} buffers, of which {:d} were good buffers.".format(bufcount, bufcount_good))
    print("Length of the final event buffer:", len(final_event_buffer))
   
    return [(None, eventBuffer)]
    
    
    
def writeFITS_LV0d5(packets_readout, outputfilename, write_packets_extension=True, gps_ok=False, fm="FM2"):
    """
    Write HERMES level 0.5 FITS file
    """
    print("\n*** WRITING LV0.5 FITS FILE ***\n")
    
    # Number of packets: one packet corresponds to one file
    # However, one file can have more buffers!
    n_packets = len(packets_readout)
    print("Number of packets: ", n_packets)
    
    # Number of headers: 
    # count total number of (header, event_data) tuples in each packet for each buffer
    # Number of time events: 
    # count total length of event_data summing over each (header, event_data) tuples in each packet
    n_buffers = 0
    n_headers = 0
    n_time_events = 0
    n_total_events = 0
    for i,packet in enumerate(packets_readout):
        #print("Number of buffers in packet ID {:d}: {:d}".format(i,len(packet)))
        n_buffers += len(packet)
        for j,buf in enumerate(packet):
            #print("Number of event lists in buffer ID {:d}: {:d}".format(j,len(buf)))
            n_headers += len(buf)
            assert len(buf) == 4
            for k,evlist in enumerate(buf):
                a,b = evlist
                n_time_events += len(b)
                for event in b:
                    n_total_events += len(event.pixelEvents)
    print("Number of buffers:", n_buffers)    
    print("Number of headers:", n_headers)    
    print("Number of time events:", n_time_events)
    print("Number of total event entries:", n_total_events)
        
    
    if write_packets_extension:
        # Extension 1 is "PACKETS". 
        packetID            = np.zeros(n_buffers)
        bufferID            = np.zeros(n_buffers)
        gps_offset          = np.zeros(n_buffers)
        utc_offset          = np.zeros(n_buffers, dtype=np.int64)
        week_sec            = np.zeros(n_buffers)
        week_num            = np.zeros(n_buffers)
        gps_status          = np.zeros(n_buffers)
        obt_s               = np.zeros(n_buffers)
        obt_ns              = np.zeros(n_buffers)
        quad_status         = np.zeros((n_buffers,40))
        trigger_counter     = np.zeros((n_buffers,4))
        rejected_counter    = np.zeros((n_buffers,4))
        event_counter       = np.zeros((n_buffers,4))
        overflow_counter    = np.zeros((n_buffers,4))
        plvolt_phys         = np.zeros((n_buffers,8))
        plcurr_phys         = np.zeros((n_buffers,7))
        fee_temp            = np.zeros((n_buffers,6))
        bee_temp            = np.zeros(n_buffers)
        csac_info           = np.zeros((n_buffers,4))   
        record_counter0     = np.zeros(n_buffers)
        record_counter1     = np.zeros(n_buffers)
        record_counter2     = np.zeros(n_buffers)
        record_counter3     = np.zeros(n_buffers)
    
    # Extension 2 is "EVENTS"
    events_packetID     = []
    events_bufferID     = []
    events_evtID        = []
    events_evtype       = []
    events_obts         = []
    events_obterr       = []
    events_time         = []
    events_quadid       = []
    events_nmult        = []
    events_channel      = []

    events_channel_0      = []
    events_adc_0          = []
    events_channel_1      = []
    events_adc_1          = []
    events_channel_2      = []
    events_adc_2          = []
    events_channel_3      = []
    events_adc_3          = []
    events_channel_4      = []
    events_adc_4          = []
    events_channel_5      = []
    events_adc_5          = []
    
    kp = 0
    
    obt_read_from_abtEvt          = np.zeros(4)
    obt_nsec_difference           = np.zeros(4)
    obt_read_from_abtEvt_previous = np.zeros(4)
    obt_nsec_difference_previous  = np.zeros(4)
    
    for i,packet in enumerate(packets_readout):
        # print("Parsing packet ID {:d} with {:d} buffers".format(i,len(packet)))
        
        for j, buf in enumerate(packet):
            # print("Parsing buffer ID {:d} with {:d} event lists".format(j,len(buf)))
            
            for k, event_list in enumerate(buf):
                header, data = buf[k]
                if k == 0:
                    # The header data of the first event list is the same of the other three
                    # so we put its info for the packets FITS extension
                    if write_packets_extension:
                        packetID[kp]     = i
                        bufferID[kp]     = j
                        gps_offset[kp]   = header.GPS_Time["GPSOffset"]
                        utc_offset[kp]   = header.GPS_Time["UTCOffset"]
                        week_sec[kp]     = header.GPS_Time["WeekSeconds"]
                        week_num[kp]     = header.GPS_Time["Week"]
                        gps_status[kp]   = header.GPS_Time["GPSStatus"]
                        obt_s[kp]        = header.BEE_HK["ABT_OBT"]
                        obt_ns[kp]       = header.BEE_HK["ABT_CNT"]
                        quad_status[kp]  = header.BEE_HK["QuadrantStatus"]
                        trigger_counter[kp]  = header.BEE_HK["TriggerCounter"]
                        rejected_counter[kp] = header.BEE_HK["RejectedCounter"]
                        event_counter[kp]    = header.BEE_HK["EventCounter"]
                        overflow_counter[kp] = header.BEE_HK["OverflowCounter"]
                        plvolt_phys[kp] = [header.BEE_HK["3V3D"]         , \
                                        header.BEE_HK["3V3A"]      , \
                                        header.BEE_HK["3V3-BEE"]   , \
                                        header.BEE_HK["2V0"]       , \
                                        header.BEE_HK["5V0-FEE"]   , \
                                        header.BEE_HK["HV"]        , \
                                        header.BEE_HK["12V0"]      , \
                                        header.BEE_HK["5V0-BEE"]   ]            
                        plcurr_phys[kp] = [header.BEE_HK["3V3D_I"]         , \
                                        header.BEE_HK["3V3A_I"]      , \
                                        header.BEE_HK["3V3-BEE_I"]   , \
                                        header.BEE_HK["2V0_I"]       , \
                                        header.BEE_HK["5V0-FEE_I"]   , \
                                        header.BEE_HK["12V0_I"]      , \
                                        header.BEE_HK["5V0-BEE_I"]   ]
                        for temperature in range(6):
                            fee_temp[kp][temperature] = header.Det_Temp[temperature+1]
                        bee_temp[kp] = header.Det_Temp[0]
                        csac_info[kp] = [header.CSAC_HK["CSACStatus"]  , \
                                        header.CSAC_HK["LaserI"]      , \
                                        header.CSAC_HK["HeatP"]       , \
                                        header.CSAC_HK["Temp"]        ]
                        record_counter0[kp] = header.recordCounter0
                        record_counter1[kp] = header.recordCounter1
                        record_counter2[kp] = header.recordCounter2
                        record_counter3[kp] = header.recordCounter3
            
                        kp += 1
            
                    if j==0 and i==0:
                        # Get the ABT from the first packet and first buffer in the acquisition
                        if write_packets_extension:
                            # obt_read_from_abtEvt[header.ASIC_ID] = header.BEE_HK["ABT_OBT"]
                            # obt_nsec_difference[header.ASIC_ID] = 9999999 - header.BEE_HK["ABT_CNT"]
                            # obt_read_from_abtEvt_previous[header.ASIC_ID] = header.BEE_HK["ABT_OBT"]
                            # obt_nsec_difference_previous[header.ASIC_ID] = 9999999 - header.BEE_HK["ABT_CNT"]
                            obt_read_from_abtEvt           = np.ones(4) * header.BEE_HK["ABT_OBT"] + 1
                            obt_nsec_difference            = np.ones(4) * (9999999 - header.BEE_HK["ABT_CNT"])
                            obt_read_from_abtEvt_previous  = np.ones(4) * header.BEE_HK["ABT_OBT"] + 1
                            obt_nsec_difference_previous   = np.ones(4) * (9999999 - header.BEE_HK["ABT_CNT"])
                            # print(obt_read_from_abtEvt)
                            # print(obt_nsec_difference)
                            # print(obt_read_from_abtEvt_previous)
                            # print(obt_nsec_difference_previous)
                        else:
                            obt_read_from_abtEvt           = np.zeros(4)
                            obt_nsec_difference            = np.zeros(4)
                            obt_read_from_abtEvt_previous  = np.zeros(4)
                            obt_nsec_difference_previous   = np.zeros(4)
            
                # The k-th buffer is the same as asicID
                asicid = k

                for m, event in enumerate(data):                
                    # Initialise arrays
                    mult = event.multiplicity
                    # Discard REJECTED events
                    if mult > -1:
                        pixel_event_channel   = np.zeros(6) - 1
                        pixel_event_adc       = np.zeros(6) - 1
                        kkk = 0
                        isThereAnABT = False
                        for n, entry in enumerate(event.pixelEvents): 
                            if entry.evtype == 0: 
                                # ABT event found: use this value to set next event
                                # ABT second and offset values
                                # independently for each quadrant
                                obt_read_from_abtEvt[asicid] = entry.obt_s
                                obt_nsec_difference[asicid]  = 9999999 - entry.obt_ns
                                isThereAnABT = True
                            else: 
                                # Loop on the pixelEvents array
                                # only if multiplicity lower than 6
                                assert asicid == entry.asicID
                                # if asicid != entry.asicID:
                                #     print("entry.asicID is", entry.asicID, "while asicid is", asicid)
                                if (len(event.pixelEvents)) <= 6:                 
                                    # Pixel event
                                    # If multiplicity lower than N_PIX_MAX = 6
                                    # populate the arrays
                                    pixel_event_channel[kkk] = entry.channel
                                    pixel_event_adc[kkk] = entry.adc
                                    kkk += 1       
            
                        events_packetID.append(i)
                        events_bufferID.append(j)
                        events_evtID.append(m)
                        if event.multiplicity > 1:
                            events_evtype.append(2)
                        else:
                             events_evtype.append(1)
                        events_obts.append(obt_read_from_abtEvt_previous[asicid])
                        events_obterr.append(obt_nsec_difference_previous[asicid])
                        time_of_event = (event.time_mark - obt_nsec_difference_previous[asicid])*1e-7 \
                                        + obt_read_from_abtEvt_previous[asicid]
                        events_time.append(time_of_event)
                        events_quadid.append(asicid)
                        events_nmult.append(event.multiplicity)

                        events_channel_0.append(pixel_event_channel[0])
                        events_channel_1.append(pixel_event_channel[1])
                        events_channel_2.append(pixel_event_channel[2])
                        events_channel_3.append(pixel_event_channel[3])
                        events_channel_4.append(pixel_event_channel[4])
                        events_channel_5.append(pixel_event_channel[5])
        
                        events_adc_0.append(pixel_event_adc[0])
                        events_adc_1.append(pixel_event_adc[1])
                        events_adc_2.append(pixel_event_adc[2])
                        events_adc_3.append(pixel_event_adc[3])
                        events_adc_4.append(pixel_event_adc[4])
                        events_adc_5.append(pixel_event_adc[5])
                        if isThereAnABT:
                            obt_read_from_abtEvt_previous[asicid] = obt_read_from_abtEvt[asicid]
                            obt_nsec_difference_previous[asicid] = obt_nsec_difference[asicid]

    events_time = np.array(events_time)
    
    # Remember that for the BEE-only acquisitions we do not have headers
    # If we have GPS then we will add the offset needed to align to MET
    # If we have a standard acquisition without GPS the ABT will be a mostly random value, so we zero-align too
    # so all times are zero-aligned (i.e., assume time in the data starts at 0)
    
    # Zero-align event time (reset the clock!)
    # All event times in the acquisition will now start from zero
    mask_nonzero_floor = np.floor(events_time) != 0
    events_time[mask_nonzero_floor] = events_time[mask_nonzero_floor] - np.floor(np.min(events_time[np.floor(events_time) > 0])) + 1
    
    if write_packets_extension and gps_ok:
        # Calculate GPS time for the first header
        # gps_offset is the receiver clock offset
        # utc_offset is the offset of gps system from utc time (should be about 18 leap secs)
        # week_num is the number of weeks since 1980-01-06 00:00:00 UTC
        # week_sec is the number of seconds in that week
        gps_time_ref = -gps_offset[0]+utc_offset[0]+ week_sec[0] + week_num[0]*7*86400
        # print("gps_time_ref", gps_time_ref)
        # print(gps_offset[0], utc_offset[0], week_sec[0], week_num[0])
        # Convert in MET: the GPS time at MET reference time is 1325030381.0 
        met_offset = gps_time_ref - 1325030381.0 
        print("MET of the observation start", met_offset)
        
    else:
        met_offset = 0
    # Add to events_time
    events_time += met_offset
    
    # Extensions
    if write_packets_extension:
        #sel_single_pkt = np.array([np.where(packetID == x)[0][0] for x in set(packetID)])
        sel_single_pkt = range(n_buffers)
        #sel_single_pkt = np.array([np.where(obt_s == x)[0][0] for x in sorted(set(obt_s))])
        t1hdu = pyfits.BinTableHDU.from_columns([
                                                  pyfits.Column(name='PACKETID',
                                                                format='1J',
                                                                array=packetID[sel_single_pkt]),
                                                  pyfits.Column(name='BUFFERID',
                                                                format='1J',
                                                                array=bufferID[sel_single_pkt]),
                                                  pyfits.Column(name='GPSOFFSET',
                                                                format='1K',
                                                                array=gps_offset[sel_single_pkt]),
                                                  pyfits.Column(name='UTCOFFSET',
                                                                format='1K',
                                                                # array=utc_offset[sel_single_pkt]-9223372036854775808),
                                                                array=utc_offset[sel_single_pkt]),
                                                  pyfits.Column(name='WEEKSEC',
                                                                format='1J',
                                                                array=week_sec[sel_single_pkt]),
                                                  pyfits.Column(name='WEEKNUM',
                                                                format='1I',
                                                                array=week_num[sel_single_pkt]),
                                                  pyfits.Column(name='GPSSTATUS',
                                                                format='1I',
                                                                array=gps_status[sel_single_pkt]),
                                                  pyfits.Column(name='OBTSEC',
                                                                format='1J',
                                                                array=obt_s[sel_single_pkt]),
                                                  pyfits.Column(name='OBTNSEC',
                                                                format='1J',
                                                                array=obt_ns[sel_single_pkt]),
                                                  pyfits.Column(name='QUADSTS',
                                                                format='40I',
                                                                array=quad_status[sel_single_pkt]),
                                                  pyfits.Column(name='TRGCNT',
                                                                format='4I',
                                                                array=trigger_counter[sel_single_pkt]),
                                                  pyfits.Column(name='REJCNT',
                                                                format='4I',
                                                                array=rejected_counter[sel_single_pkt]),
                                                  pyfits.Column(name='EVTCNT',
                                                                format='4I',
                                                                array=event_counter[sel_single_pkt]),
                                                  pyfits.Column(name='OVFCNT',
                                                                format='4I',
                                                                array=overflow_counter[sel_single_pkt]),
                                                  pyfits.Column(name='PLVOLTP',
                                                                format='8D',
                                                                array=plvolt_phys[sel_single_pkt]),
                                                  pyfits.Column(name='PLCURRP',
                                                                format='7D',
                                                                array=plcurr_phys[sel_single_pkt]),
                                                  pyfits.Column(name='FEETEMPP',
                                                                format='6D',
                                                                array=fee_temp[sel_single_pkt]),
                                                  pyfits.Column(name='BEETEMPP',
                                                                format='1D',
                                                                array=bee_temp[sel_single_pkt]),
                                                  pyfits.Column(name='CSACINFOP',
                                                                format='4D',
                                                                array=csac_info[sel_single_pkt]),
                                                  pyfits.Column(name='RECCNT0',
                                                                format='1I',
                                                                array=record_counter0[sel_single_pkt]),
                                                  pyfits.Column(name='RECCNT1',
                                                                format='1I',
                                                                array=record_counter1[sel_single_pkt]),
                                                  pyfits.Column(name='RECCNT2',
                                                                format='1I',
                                                                array=record_counter2[sel_single_pkt]),
                                                  pyfits.Column(name='RECCNT3',
                                                                format='1I',
                                                                array=record_counter3[sel_single_pkt])
                                                ])

    
    mask_fake_events = np.array(events_nmult) > 0
    
    t2hdu = pyfits.BinTableHDU.from_columns([
                                              pyfits.Column(name='PACKETID',
                                                            format='1J',
                                                            array=np.array(events_packetID)[mask_fake_events]),
                                              pyfits.Column(name='BUFFERID',
                                                            format='1J',
                                                            array=np.array(events_bufferID)[mask_fake_events]),
                                              pyfits.Column(name='EVTID',
                                                            format='1J',
                                                            array=np.array(events_evtID)[mask_fake_events]),
                                              pyfits.Column(name='EVTTYPE',
                                                            format='1B',
                                                            array=np.array(events_evtype)[mask_fake_events]),
                                              pyfits.Column(name='OBTSEC',
                                                            format='1J',
                                                            array=np.array(events_obts)[mask_fake_events]),
                                              pyfits.Column(name='OBTERR',
                                                            format='1J',
                                                            array=np.array(events_obterr)[mask_fake_events]),
                                              pyfits.Column(name='TIME',
                                                            format='1D',
                                                            array=np.array(events_time)[mask_fake_events]),
                                              pyfits.Column(name='QUADID',
                                                            format='1B',
                                                            array=np.array(events_quadid)[mask_fake_events]),
                                              pyfits.Column(name='NMULT',
                                                            format='1B',
                                                            array=np.array(events_nmult)[mask_fake_events]),
                                             pyfits.Column(name='CHANNEL0',
                                                            format='1J',
                                                            array=np.array(events_channel_0)[mask_fake_events]),
                                              pyfits.Column(name='ADC0',
                                                            format='1J',
                                                            array=np.array(events_adc_0)[mask_fake_events]),
                                             pyfits.Column(name='CHANNEL1',
                                                            format='1J',
                                                            array=np.array(events_channel_1)[mask_fake_events]),
                                              pyfits.Column(name='ADC1',
                                                            format='1J',
                                                            array=np.array(events_adc_1)[mask_fake_events]),
                                             pyfits.Column(name='CHANNEL2',
                                                            format='1J',
                                                            array=np.array(events_channel_2)[mask_fake_events]),
                                              pyfits.Column(name='ADC2',
                                                            format='1J',
                                                            array=np.array(events_adc_2)[mask_fake_events]),
                                             pyfits.Column(name='CHANNEL3',
                                                            format='1J',
                                                            array=np.array(events_channel_3)[mask_fake_events]),
                                              pyfits.Column(name='ADC3',
                                                            format='1J',
                                                            array=np.array(events_adc_3)[mask_fake_events]),
                                             pyfits.Column(name='CHANNEL4',
                                                            format='1J',
                                                            array=np.array(events_channel_4)[mask_fake_events]),
                                              pyfits.Column(name='ADC4',
                                                            format='1J',
                                                            array=np.array(events_adc_4)[mask_fake_events]),
                                             pyfits.Column(name='CHANNEL5',
                                                            format='1J',
                                                            array=np.array(events_channel_5)[mask_fake_events]),
                                              pyfits.Column(name='ADC5',
                                                            format='1J',
                                                            array=np.array(events_adc_5)[mask_fake_events])
                                            ])
    
    
    
    
    # Write FITS file
    # "Null" primary array
    prhdu = pyfits.PrimaryHDU()
    
    if write_packets_extension:
        t1hdu.header.set('EXTNAME', 'PACKETS', 'Name of this binary table extension')
        # t1hdu.header.set('TFORM4', '1K',  'Scaling of 64 bit unsigned int')
        # t1hdu.header.set('TZERO4', 9223372036854775808,  'Scaling of 64 bit unsigned int')
        t1hdu.header.set('TELESCOP', 'HERMES',  'Telescope name')
        t1hdu.header.set('INSTRUME', fm,  'Instrument name')
        
    t2hdu.header.set('EXTNAME', 'EVENTS',  'Name of this binary table extension')
    t2hdu.header.set('TELESCOP', 'HERMES',  'Telescope name')
    t2hdu.header.set('INSTRUME', fm,  'Instrument name')

    if write_packets_extension:
        hdulist = pyfits.HDUList([prhdu, t1hdu, t2hdu])
    else:
        hdulist = pyfits.HDUList([prhdu, t2hdu])
    hdulist.writeto(outputfilename, overwrite=True)
    
    
    
    
    
def writeFITS_LV0(packets_readout, outputfilename, write_packets_extension=True, gps_ok=False, ORTrigger=False, fm="FM2"):
    """
    Write HERMES level 0 FITS file
    """
    print("\n*** WRITING LV0 FITS FILE ***\n")
    
    # Number of packets: one packet corresponds to one file
    # However, one file can have more buffers!
    n_packets = len(packets_readout)
    print("Number of packets: ", n_packets)
    
    # Number of headers: 
    # count total number of (header, event_data) tuples in each packet for each buffer
    # Number of time events: 
    # count total length of event_data summing over each (header, event_data) tuples in each packet
    n_buffers = 0
    n_headers = 0
    n_time_events = 0
    n_total_events = 0
    for i,packet in enumerate(packets_readout):
        #print("Number of buffers in packet ID {:d}: {:d}".format(i,len(packet)))
        n_buffers += len(packet)
        for j,buf in enumerate(packet):
            #print("Number of event lists in buffer ID {:d}: {:d}".format(j,len(buf)))
            n_headers += len(buf)
            assert len(buf) == 4
            for k,evlist in enumerate(buf):
                a,b = evlist
                n_time_events += len(b)
                for event in b:
                    n_total_events += len(event.pixelEvents)
    print("Number of buffers:", n_buffers)    
    print("Number of headers:", n_headers)    
    print("Number of time events:", n_time_events)
    print("Number of total event entries:", n_total_events)        
    
    if write_packets_extension:
        # Extension 1 is "PACKETS". 
        packetID            = np.zeros(n_buffers)
        bufferID            = np.zeros(n_buffers)
        gps_offset          = np.zeros(n_buffers)
        utc_offset          = np.zeros(n_buffers, dtype=np.int64)
        week_sec            = np.zeros(n_buffers)
        week_num            = np.zeros(n_buffers)
        gps_status          = np.zeros(n_buffers)
        obt_s               = np.zeros(n_buffers)
        obt_ns              = np.zeros(n_buffers)
        quad_status         = np.zeros((n_buffers,40))
        trigger_counter     = np.zeros((n_buffers,4))
        rejected_counter    = np.zeros((n_buffers,4))
        event_counter       = np.zeros((n_buffers,4))
        overflow_counter    = np.zeros((n_buffers,4))
        plvolt              = np.zeros((n_buffers,8))
        plcurr              = np.zeros((n_buffers,7))
        fee_temp            = np.zeros((n_buffers,6))
        bee_temp            = np.zeros(n_buffers)
        csac_info           = np.zeros((n_buffers,4))   
        record_counter0      = np.zeros(n_buffers)
        record_counter1      = np.zeros(n_buffers)
        record_counter2      = np.zeros(n_buffers)
        record_counter3      = np.zeros(n_buffers)
        
    
    # Extension 2 is "EVENTS"
    events_packetID     = []
    events_bufferID     = []
    events_evtID        = []
    events_evtype       = []
    events_obts         = []
    events_obtns        = []
    events_time_mark    = []
    events_time         = []
    events_quadid       = []
    events_nmult        = []
    events_channel      = []
    events_adc          = []
    
    # Extension 4 (if present) is "REJECTED"
    rejected_packetID     = []
    rejected_bufferID     = []
    rejected_evtID        = []
    rejected_evtype       = []
    rejected_obts         = []
    rejected_obtns        = []
    rejected_time_mark    = []
    rejected_quadid       = []
    rejected_rejmap       = []
    
    kp = 0
    
    obt_read_from_abtEvt          = np.zeros(4)
    obt_nsec_difference           = np.zeros(4)
    obt_read_from_abtEvt_previous = np.zeros(4)
    obt_nsec_difference_previous  = np.zeros(4)
    

    for i,packet in enumerate(packets_readout):
        #print("Parsing packet ID {:d} with {:d} buffers".format(i,len(packet)))
        
        for j, buf in enumerate(packet):
            #print("Parsing buffer ID {:d} with {:d} event lists".format(j,len(buf)))
            
            for k, event_list in enumerate(buf):
                header, data = buf[k]
                if k == 0:
                    # The header data of the first event list is the same of the other three
                    # so we put its info for the packets FITS extension
                    if write_packets_extension:
                        packetID[kp]     = i
                        bufferID[kp]     = j
                        gps_offset[kp]   = header.GPS_Time["GPSOffset"]
                        utc_offset[kp]   = header.GPS_Time["UTCOffset"]
                        week_sec[kp]     = header.GPS_Time["WeekSeconds"]
                        week_num[kp]     = header.GPS_Time["Week"]
                        gps_status[kp]   = header.GPS_Time["GPSStatus"]
                        obt_s[kp]        = header.BEE_HK["ABT_OBT"]
                        obt_ns[kp]       = header.BEE_HK["ABT_CNT"]
                        quad_status[kp]  = header.BEE_HK["QuadrantStatus"]
                        
                        trigger_counter[kp]  = header.BEE_HK["TriggerCounter"]
                        rejected_counter[kp] = header.BEE_HK["RejectedCounter"]
                        event_counter[kp]    = header.BEE_HK["EventCounter"]
                        overflow_counter[kp] = header.BEE_HK["OverflowCounter"]

                        plvolt[kp] = [header.BEE_HK["3V3D_raw"]         , \
                                        header.BEE_HK["3V3A_raw"]      , \
                                        header.BEE_HK["3V3-BEE_raw"]   , \
                                        header.BEE_HK["2V0_raw"]       , \
                                        header.BEE_HK["5V0-FEE_raw"]   , \
                                        header.BEE_HK["HV_raw"]        , \
                                        header.BEE_HK["12V0_raw"]      , \
                                        header.BEE_HK["5V0-BEE_raw"]   ]
            
            
                            
                        plcurr[kp] = [header.BEE_HK["3V3D_I_raw"]         , \
                                        header.BEE_HK["3V3A_I_raw"]      , \
                                        header.BEE_HK["3V3-BEE_I_raw"]   , \
                                        header.BEE_HK["2V0_I_raw"]       , \
                                        header.BEE_HK["5V0-FEE_I_raw"]   , \
                                        header.BEE_HK["12V0_I_raw"]      , \
                                        header.BEE_HK["5V0-BEE_I_raw"]   ]



                        for temperature in range(6):
                            fee_temp[kp][temperature] = int(header.Det_Temp[temperature+1]*10)
                        bee_temp[kp] = int(header.Det_Temp[0]*10)
    
                        csac_info[kp] = [header.CSAC_HK["CSACStatus"]   , \
                                        int(header.CSAC_HK["LaserI"]*100)       , \
                                        int(header.CSAC_HK["HeatP"]*100)       , \
                                        int(header.CSAC_HK["Temp"]*100)     ]
    
                        record_counter0[kp] = header.recordCounter0
                        record_counter1[kp] = header.recordCounter1
                        record_counter2[kp] = header.recordCounter2
                        record_counter3[kp] = header.recordCounter3
            
                        kp += 1

                    if j==0 and i==0:
                        # Get the ABT from the first packet and first buffer in the acquisition
                        if write_packets_extension:
                            # obt_read_from_abtEvt[header.ASIC_ID] = header.BEE_HK["ABT_OBT"]
                            # obt_nsec_difference[header.ASIC_ID] = 9999999 - header.BEE_HK["ABT_CNT"]
                            # obt_read_from_abtEvt_previous[header.ASIC_ID] = header.BEE_HK["ABT_OBT"]
                            # obt_nsec_difference_previous[header.ASIC_ID] = 9999999 - header.BEE_HK["ABT_CNT"]
                            obt_read_from_abtEvt           = np.ones(4) * header.BEE_HK["ABT_OBT"] + 1
                            obt_nsec_difference            = np.ones(4) * (9999999 - header.BEE_HK["ABT_CNT"]) 
                            obt_read_from_abtEvt_previous  = np.ones(4) * header.BEE_HK["ABT_OBT"] + 1
                            obt_nsec_difference_previous   = np.ones(4) * (9999999 - header.BEE_HK["ABT_CNT"])
                            # print(obt_read_from_abtEvt)
                            # print(obt_nsec_difference)
                            # print(obt_read_from_abtEvt_previous)
                            # print(obt_nsec_difference_previous)
                            
                        else:
                            obt_read_from_abtEvt           = np.zeros(4)
                            obt_nsec_difference            = np.zeros(4)
                            obt_read_from_abtEvt_previous  = np.zeros(4)
                            obt_nsec_difference_previous   = np.zeros(4)


                for m, event in enumerate(data):                
                    # Initialise arrays
                    mult = event.multiplicity
                    # Discard rejected events
                    if mult > -1:
                        pixel_event_channel   = []
                        pixel_event_sddid     = []
                        pixel_event_adc       = []

                        asicid = m
                        isThereAnABT = False
                        for n, entry in enumerate(event.pixelEvents):      
                            if entry.evtype == 0:                         
                                # There is an ABT event in the pixelEvents buffer
                                # Let's append it LAST to the final array
                                # since the ABT would be reset for the next PIXEL events
                                # (i.e. after the next TIME)
                                # ABT event found: use this value to set next event
                                # ABT second and offset values
                                # independently for each quadrant
                                if asicid >= 4:
                                    print("asicid is higher than 4!!!", asicid)
                                    asicid = 0
                                obt_read_from_abtEvt[asicid] = entry.obt_s
                                obt_nsec_difference[asicid]  = 9999999 - entry.obt_ns
                                isThereAnABT = True

                                abt_event_packetID = i
                                abt_event_bufferID = j
                                abt_event_evtID = 0
                                abt_event_evtype = entry.evtype
                                abt_event_obts = entry.obt_s
                                abt_event_obtns = entry.obt_ns
                                abt_event_time_mark = 0
                                abt_event_quadid = asicid
                                abt_event_nmult = 0
                                abt_event_channel = []
                                abt_event_adc = []
                                                
                            else: 
                                # Loop on the pixelEvents array
                                # Pixel event, pack multiplicity
                                pixel_event_channel.append(entry.channel)
                                pixel_event_adc.append(entry.adc)
                                asicid = entry.asicID
                
                        events_packetID.append(i)
                        events_bufferID.append(j)
                        events_evtID.append(m)
                        events_obts.append(obt_read_from_abtEvt_previous[asicid])
                        events_obtns.append(obt_nsec_difference_previous[asicid])
                        events_time_mark.append(event.time_mark)
            
                        time_of_event = (event.time_mark - obt_nsec_difference_previous[asicid])*1e-7 \
                                        + obt_read_from_abtEvt_previous[asicid]
                        events_time.append(time_of_event)

                        events_quadid.append(asicid)
                        if ORTrigger:
                            events_evtype.append(2)
                            events_nmult.append(32)
                        else:
                            if event.multiplicity > 1:
                                events_evtype.append(2)
                            else:
                                 events_evtype.append(1)
                        events_nmult.append(event.multiplicity)
                        events_channel.append(pixel_event_channel)
                        events_adc.append(pixel_event_adc)
            
                        if isThereAnABT:
                            # Now we can append also the ABT event
                            events_packetID.append(abt_event_packetID)
                            events_bufferID.append(abt_event_bufferID)
                            events_evtID.append(abt_event_evtID)
                            events_evtype.append(abt_event_evtype)
                            events_obts.append(abt_event_obts)
                            events_obtns.append(abt_event_obtns)
                            events_time_mark.append(abt_event_time_mark)
                            events_time.append(0)
                            events_quadid.append(abt_event_quadid)
                            events_nmult.append(abt_event_nmult)
                            events_channel.append(abt_event_channel)
                            events_adc.append(abt_event_adc)
                
                            obt_read_from_abtEvt_previous[asicid] = obt_read_from_abtEvt[asicid]
                            obt_nsec_difference_previous[asicid] = obt_nsec_difference[asicid]
                            
                            
                    elif mult == -1:
                        # REJECTED events
                        rejected_packetID.append(i)
                        rejected_bufferID.append(j)
                        rejected_evtID.append(m)
                        rejected_evtype.append(4)
                        # rejected_obts.append(obt_read_from_abtEvt_previous[m])
                        # rejected_obtns.append(obt_nsec_difference_previous[m])
                        rejected_time_mark.append(event.time_mark)
                        rejected_quadid.append(k)
                        rejected_rejmap.append(int(event.rejectedMap, base=2))
                            
        
    # Shift for something in the integer representation (to make it work...)
    for i in range(len(events_adc)):
        for j in range(len(events_adc[i])):
            events_adc[i][j] -= 32768


    events_time = np.array(events_time)
    # if write_packets_extension:
    #     print("*** TIME DEBUG: First obt_s value in header", obt_s[0])
    # print("*** TIME DEBUG: First events_time value", events_time[0])
    # print("*** TIME DEBUG: Minimum non-zero events_time value", np.min(events_time[np.floor(events_time) > 0]))
    
    # Remember that for the BEE acquisitions we do not have headers
    # If we have GPS then we will add the offset needed to align to MET
    # If we have a standard acquisition without GPS the ABT will be a mostly random value, so we zero-align too
    # so all times are zero-aligned (i.e., assume time in the data starts at 0)
    
    # Zero-align event time (reset the clock!)
    # All event times in the acquisition will now start from zero
    mask_nonzero_floor = np.floor(events_time) != 0
    events_time[mask_nonzero_floor] = events_time[mask_nonzero_floor] - np.floor(np.min(events_time[np.floor(events_time) > 0])) + 1
    
    if write_packets_extension and gps_ok:
        # Calculate GPS time for the first header
        # gps_offset is the receiver clock offset
        # utc_offset is the offset of gps system from utc time (should be about 18 leap secs)
        # week_num is the number of weeks since 1980-01-06 00:00:00 UTC
        # week_sec is the number of seconds in that week
        gps_time_ref = -gps_offset[0]+utc_offset[0]+ week_sec[0] + week_num[0]*7*86400
        # Convert in MET: the GPS time at MET reference time is 1325030381.0 
        met_offset = gps_time_ref - 1325030381.0 
    else:
        met_offset = 0
    # Add to events_time
    events_time += met_offset
    
    exposure = np.max(events_time)-np.min(events_time)
    
    mask_fake_events = np.logical_or(np.array(events_nmult) > 0, np.array(events_evtype) == 0)
        
    # Extensions
    if write_packets_extension:
        #sel_single_pkt = np.array([np.where(packetID == x)[0][0] for x in set(packetID)])
        sel_single_pkt = range(n_buffers)
        pkthdu = pyfits.BinTableHDU.from_columns([
                                                  pyfits.Column(name='PACKETID',
                                                                format='1J',
                                                                array=packetID[sel_single_pkt]),
                                                  pyfits.Column(name='BUFFERID',
                                                                format='1J',
                                                                array=bufferID[sel_single_pkt]),
                                                  pyfits.Column(name='GPSOFFSET',
                                                                format='1K',
                                                                array=gps_offset[sel_single_pkt]),
                                                  pyfits.Column(name='UTCOFFSET',
                                                                format='1K',
                                                                # array=utc_offset[sel_single_pkt]-9223372036854775808),
                                                                array=utc_offset[sel_single_pkt]),
                                                  pyfits.Column(name='WEEKSEC',
                                                                format='1J',
                                                                array=week_sec[sel_single_pkt]),
                                                  pyfits.Column(name='WEEKNUM',
                                                                format='1I',
                                                                array=week_num[sel_single_pkt]),
                                                  pyfits.Column(name='GPSSTATUS',
                                                                format='1I',
                                                                array=gps_status[sel_single_pkt]),
                                                  pyfits.Column(name='OBTSEC',
                                                                format='1J',
                                                                array=obt_s[sel_single_pkt]),
                                                  pyfits.Column(name='OBTNSEC',
                                                                format='1J',
                                                                array=obt_ns[sel_single_pkt]),
                                                  pyfits.Column(name='QUADSTS',
                                                                format='40I',
                                                                array=quad_status[sel_single_pkt]),
                                                  pyfits.Column(name='TRGCNT',
                                                                format='4I',
                                                                array=trigger_counter[sel_single_pkt]),
                                                  pyfits.Column(name='REJCNT',
                                                                format='4I',
                                                                array=rejected_counter[sel_single_pkt]),
                                                  pyfits.Column(name='EVTCNT',
                                                                format='4I',
                                                                array=event_counter[sel_single_pkt]),
                                                  pyfits.Column(name='OVFCNT',
                                                                format='4I',
                                                                array=overflow_counter[sel_single_pkt]),
                                                  pyfits.Column(name='PLVOLT',
                                                                format='8B',
                                                                array=plvolt[sel_single_pkt]),
                                                  pyfits.Column(name='PLCURR',
                                                                format='7B',
                                                                array=plcurr[sel_single_pkt]),
                                                  pyfits.Column(name='FEETEMP',
                                                                format='6I',
                                                                array=fee_temp[sel_single_pkt]),
                                                  pyfits.Column(name='BEETEMP',
                                                                format='I',
                                                                array=bee_temp[sel_single_pkt]),
                                                  pyfits.Column(name='CSACINFO',
                                                                format='4I',
                                                                array=csac_info[sel_single_pkt]),
                                                  pyfits.Column(name='RECCNT0',
                                                                format='1I',
                                                                array=record_counter0[sel_single_pkt]),
                                                  pyfits.Column(name='RECCNT1',
                                                                format='1I',
                                                                array=record_counter1[sel_single_pkt]),
                                                  pyfits.Column(name='RECCNT2',
                                                                format='1I',
                                                                array=record_counter2[sel_single_pkt]),
                                                  pyfits.Column(name='RECCNT3',
                                                                format='1I',
                                                                array=record_counter3[sel_single_pkt])
                                                ])

    
    evthdu = pyfits.BinTableHDU.from_columns([
                                              pyfits.Column(name='PACKETID',
                                                            format='1J',
                                                            array=np.array(events_packetID)[mask_fake_events]),
                                              pyfits.Column(name='BUFFERID',
                                                            format='1J',
                                                            array=np.array(events_bufferID)[mask_fake_events]),
                                              pyfits.Column(name='EVTID',
                                                            format='1J',
                                                            array=np.array(events_evtID)[mask_fake_events]),
                                              pyfits.Column(name='EVTTYPE',
                                                            format='1B',
                                                            array=np.array(events_evtype)[mask_fake_events]),
                                              pyfits.Column(name='OBTSEC',
                                                            format='1J',
                                                            array=np.array(events_obts)[mask_fake_events]),
                                              pyfits.Column(name='OBTNSEC',
                                                            format='1J',
                                                            array=np.array(events_obtns)[mask_fake_events]),
                                              pyfits.Column(name='TIMEMARK',
                                                            format='1J',
                                                            array=np.array(events_time_mark)[mask_fake_events]),
                                              pyfits.Column(name='TIME',
                                                            format='1D',
                                                            unit='s',
                                                            array=np.array(events_time)[mask_fake_events]),
                                              pyfits.Column(name='QUADID',
                                                            format='1B',
                                                            array=np.array(events_quadid)[mask_fake_events]),
                                              pyfits.Column(name='NMULT',
                                                            format='1B',
                                                            array=np.array(events_nmult)[mask_fake_events]),
                                              pyfits.Column(name='CHANNEL',
                                                            format='1QB(30)',
                                                            array=np.array(events_channel, dtype=object)[mask_fake_events]),
                                              pyfits.Column(name='PHA',
                                                            format='1QI(30)',
                                                            array=np.array(events_adc, dtype=object)[mask_fake_events])
                                            ])
    
    gtihdu = pyfits.BinTableHDU.from_columns([                                
                                              pyfits.Column(name='START',
                                                            format='1D',
                                                            unit='s',
                                                            array=np.array([0.])),
                                              pyfits.Column(name='STOP',
                                                            format='1D',
                                                            unit='s',
                                                            array=np.array([exposure])),
                                            ])
    
    rejhdu = pyfits.BinTableHDU.from_columns([
                                              pyfits.Column(name='PACKETID',
                                                            format='1J',
                                                            array=rejected_packetID),
                                              pyfits.Column(name='BUFFERID',
                                                            format='1J',
                                                            array=rejected_bufferID),
                                              pyfits.Column(name='EVTID',
                                                            format='1J',
                                                            array=rejected_evtID),
                                              pyfits.Column(name='EVTTYPE',
                                                            format='1B',
                                                            array=rejected_evtype),
                                              # pyfits.Column(name='OBTSEC',
                                              #               format='1J',
                                              #               array=rejected_obts),
                                              # pyfits.Column(name='OBTNSEC',
                                              #               format='1J',
                                              #               array=rejected_obtns),
                                              pyfits.Column(name='TIMEMARK',
                                                            format='1J',
                                                            array=rejected_time_mark),
                                              pyfits.Column(name='QUADID',
                                                            format='1B',
                                                            array=rejected_quadid),
                                              pyfits.Column(name='REJMAP',
                                                            format='1J',
                                                            array=rejected_rejmap)
                                            ])
    
    
    # Write FITS file
    # "Null" primary array
    prhdu = pyfits.PrimaryHDU()

    print("Exposure", exposure)
    tref = Time(59580+0.00080074074, format='mjd')
    tstop = Time(59580+0.00080074074+exposure/86400, format='mjd')
    
    prhdu.header.set('TELESCOP', 'HERMES',  'Telescope name')
    prhdu.header.set('INSTRUME', fm,  'Instrument name')
    
    prhdu.header.set('TIMESYS', 'TT',  'Terrestrial Time: synchronous with, but 32.184')
    prhdu.header.set('TIMEREF', 'LOCAL',  'Time reference')
    prhdu.header.set('TIMEUNIT', 's',  'Time unit for timing header keywords')
    prhdu.header.set('MJDREFI', 59580,  'MJD reference day 01 Jan 2022 00:00:00 UTC')
    prhdu.header.set('MJDREFF', 0.00080074074,  'MJD reference (fraction part: 32.184 secs + 37')
    prhdu.header.set('CLOCKAPP', False,  'Set to TRUE if correction has been applied to t')
    
    prhdu.header.set('TSTART', 0,  'Start: Elapsed secs since HERMES epoch')
    prhdu.header.set('TSTOP', exposure,  'Stop: Elapsed secs since HERMES epoch')
    prhdu.header.set('TELAPSE', exposure,  'TSTOP-TSTART')
    prhdu.header.set('ONTIME', exposure,  'Sum of GTIs')
    prhdu.header.set('EXPOSURE', exposure,  'Exposure time')
    prhdu.header.set('DATE-OBS', tref.fits,  'Start date of observations')
    prhdu.header.set('DATE-END', tstop.fits,  'End date of observations')
    
    
    if write_packets_extension:
        pkthdu.header.set('EXTNAME', 'PACKETS', 'Name of this binary table extension')
        pkthdu.header.set('TELESCOP', 'HERMES',  'Telescope name')
        pkthdu.header.set('INSTRUME', fm,  'Instrument name')
        # pkthdu.header.set('TFORM4', '1K',  'Scaling of 64 bit unsigned int')
        # pkthdu.header.set('TZERO4', 9223372036854775808,  'Scaling of 64 bit unsigned int')
        pkthdu.header.set('TIMESYS', 'TT',  'Terrestrial Time: synchronous with, but 32.184')
        pkthdu.header.set('TIMEREF', 'LOCAL',  'Time reference')
        pkthdu.header.set('TIMEUNIT', 's',  'Time unit for timing header keywords')
        pkthdu.header.set('MJDREFI', 59580,  'MJD reference day 01 Jan 2022 00:00:00 UTC')
        pkthdu.header.set('MJDREFF', 0.00080074074,  'MJD reference (fraction part: 32.184 secs + 37')
        pkthdu.header.set('CLOCKAPP', False,  'Set to TRUE if correction has been applied to t')
        pkthdu.header.set('EXPOSURE', exposure,  'Exposure time')
        pkthdu.header.set('TSTART', 0,  'Start: Elapsed secs since HERMES epoch')
        pkthdu.header.set('TSTOP', exposure,  'Stop: Elapsed secs since HERMES epoch')
        pkthdu.header.set('TELAPSE', exposure,  'TSTOP-TSTART')
        pkthdu.header.set('ONTIME', exposure,  'Sum of GTIs')
        pkthdu.header.set('EXPOSURE', exposure,  'Exposure time')
        pkthdu.header.set('DATE-OBS', tref.fits,  'Start date of observations')
        pkthdu.header.set('DATE-END', tstop.fits,  'End date of observations')
            

    evthdu.header.set('EXTNAME', 'EVENTS',  'Name of this binary table extension')
    evthdu.header.set('TELESCOP', 'HERMES',  'Telescope name')
    evthdu.header.set('INSTRUME', fm,  'Instrument name')
    evthdu.header.set('TZERO12', 32768,  'Scaling of 16 bit unsigned int')
    evthdu.header.set('TIMESYS', 'TT',  'Terrestrial Time: synchronous with, but 32.184')
    evthdu.header.set('TIMEREF', 'LOCAL',  'Time reference')
    evthdu.header.set('TIMEUNIT', 's',  'Time unit for timing header keywords')
    evthdu.header.set('MJDREFI', 59580,  'MJD reference day 01 Jan 2022 00:00:00 UTC')
    evthdu.header.set('MJDREFF', 0.00080074074,  'MJD reference (fraction part: 32.184 secs + 37')
    evthdu.header.set('CLOCKAPP', False,  'Set to TRUE if correction has been applied to t')
    evthdu.header.set('TSTART', 0,  'Start: Elapsed secs since HERMES epoch')
    evthdu.header.set('TSTOP', exposure,  'Stop: Elapsed secs since HERMES epoch')
    evthdu.header.set('TELAPSE', exposure,  'TSTOP-TSTART')
    evthdu.header.set('ONTIME', exposure,  'Sum of GTIs')
    evthdu.header.set('EXPOSURE', exposure,  'Exposure time')
    evthdu.header.set('DATE-OBS', tref.fits,  'Start date of observations')
    evthdu.header.set('DATE-END', tstop.fits,  'End date of observations')

    gtihdu.header.set('EXTNAME', 'GTI',  'Name of this binary table extension')
    gtihdu.header.set('TELESCOP', 'HERMES',  'Telescope name')
    gtihdu.header.set('INSTRUME', fm,  'Instrument name')
    gtihdu.header.set('TIMESYS', 'TT',  'Terrestrial Time: synchronous with, but 32.184')
    gtihdu.header.set('TIMEREF', 'LOCAL',  'Time reference')
    gtihdu.header.set('TIMEUNIT', 's',  'Time unit for timing header keywords')
    gtihdu.header.set('MJDREFI', 59580,  'MJD reference day 01 Jan 2022 00:00:00 UTC')
    gtihdu.header.set('MJDREFF', 0.00080074074,  'MJD reference (fraction part: 32.184 secs + 37')
    gtihdu.header.set('CLOCKAPP', False,  'Set to TRUE if correction has been applied to t')
    gtihdu.header.set('TSTART', 0,  'Start: Elapsed secs since HERMES epoch')
    gtihdu.header.set('TSTOP', exposure,  'Stop: Elapsed secs since HERMES epoch')
    gtihdu.header.set('TELAPSE', exposure,  'TSTOP-TSTART')
    gtihdu.header.set('ONTIME', exposure,  'Sum of GTIs')
    gtihdu.header.set('EXPOSURE', exposure,  'Exposure time')
    gtihdu.header.set('DATE-OBS', tref.fits,  'Start date of observations')
    gtihdu.header.set('DATE-END', tstop.fits,  'End date of observations')
    gtihdu.header.set('HDUCLASS', 'OGIP',  'End date of observations')
    gtihdu.header.set('HDUCLAS1', 'GTI',  'File contains Good Time Intervals')
    gtihdu.header.set('HDUCLAS2', 'STANDARD',  'File contains Good Time Intervals')
    gtihdu.header.set('HDUNAME', 'GTI',  'ASCDM block name')


    if len(rejected_packetID) > 0:
        rejhdu.header.set('EXTNAME', 'REJECTED',  'Name of this binary table extension')
        rejhdu.header.set('TELESCOP', 'HERMES',  'Telescope name')
        rejhdu.header.set('INSTRUME', fm,  'Instrument name')
        rejhdu.header.set('TIMESYS', 'TT',  'Terrestrial Time: synchronous with, but 32.184')
        rejhdu.header.set('TIMEREF', 'LOCAL',  'Time reference')
        rejhdu.header.set('TIMEUNIT', 's',  'Time unit for timing header keywords')
        rejhdu.header.set('MJDREFI', 59580,  'MJD reference day 01 Jan 2022 00:00:00 UTC')
        rejhdu.header.set('MJDREFF', 0.00080074074,  'MJD reference (fraction part: 32.184 secs + 37')
        rejhdu.header.set('CLOCKAPP', False,  'Set to TRUE if correction has been applied to t')
        rejhdu.header.set('TSTART', 0,  'Start: Elapsed secs since HERMES epoch')
        rejhdu.header.set('TSTOP', exposure,  'Stop: Elapsed secs since HERMES epoch')
        rejhdu.header.set('TELAPSE', exposure,  'TSTOP-TSTART')
        rejhdu.header.set('ONTIME', exposure,  'Sum of GTIs')
        rejhdu.header.set('EXPOSURE', exposure,  'Exposure time')
        rejhdu.header.set('DATE-OBS', tref.fits,  'Start date of observations')
        rejhdu.header.set('DATE-END', tstop.fits,  'End date of observations')
        
        if write_packets_extension:
            hdulist = pyfits.HDUList([prhdu, pkthdu, evthdu, gtihdu, rejhdu])
        else:
            hdulist = pyfits.HDUList([prhdu, evthdu, gtihdu, rejhdu])
            
    else:
        if write_packets_extension:
            hdulist = pyfits.HDUList([prhdu, pkthdu, evthdu, gtihdu])
        else:
            hdulist = pyfits.HDUList([prhdu, evthdu, gtihdu])
            
    hdulist.writeto(outputfilename, overwrite=True, checksum=True)


def writeFITS_HK(packets_readout, outputfilename, gps_ok=False, fm="FM2"):
    """
    Write HERMES housekeepings FITS file
    """
    print("\n*** WRITING HK FITS FILE ***\n")
    
    # Number of packets: one packet corresponds to one file
    # However, one file can have more buffers!
    n_packets = len(packets_readout)
    print("Number of packets: ", n_packets)
    
    # Number of headers: 
    # count total number of (header, event_data) tuples in each packet for each buffer
    # Number of time events: 
    # count total length of event_data summing over each (header, event_data) tuples in each packet
    n_buffers = 0
    n_headers = 0
    n_time_events = 0
    n_total_events = 0
    for i,packet in enumerate(packets_readout):
        #print("Number of buffers in packet ID {:d}: {:d}".format(i,len(packet)))
        n_buffers += len(packet)
        for j,buf in enumerate(packet):
            #print("Number of event lists in buffer ID {:d}: {:d}".format(j,len(buf)))
            n_headers += len(buf)
            assert len(buf) == 4
            for k,evlist in enumerate(buf):
                a,b = evlist
                n_time_events += len(b)
                for event in b:
                    n_total_events += len(event.pixelEvents)
    print("Number of buffers:", n_buffers)    
    print("Number of headers:", n_headers)    
    print("Number of time events:", n_time_events)
    print("Number of total event entries:", n_total_events)
        
    # Extension 1 is "PACKETS". 
    packetID            = np.zeros(n_buffers)
    bufferID            = np.zeros(n_buffers)
    asic_ID             = np.zeros(n_buffers)
    gps_offset          = np.zeros(n_buffers)
    utc_offset          = np.zeros(n_buffers, dtype=np.int64)
    week_sec            = np.zeros(n_buffers)
    week_num            = np.zeros(n_buffers)
    gps_status          = np.zeros(n_buffers)
    obt_s               = np.zeros(n_buffers)
    obt_ns              = np.zeros(n_buffers)
    quad_status         = np.zeros((n_buffers,40))
    trigger_counter     = np.zeros((n_buffers,4))
    rejected_counter    = np.zeros((n_buffers,4))
    event_counter       = np.zeros((n_buffers,4))
    overflow_counter    = np.zeros((n_buffers,4))
    plvolt              = np.zeros((n_buffers,8))
    plcurr              = np.zeros((n_buffers,7))
    plvolt_phys         = np.zeros((n_buffers,8))
    plcurr_phys         = np.zeros((n_buffers,7))
    fee_temp_phys       = np.zeros((n_buffers,6))
    bee_temp_phys       = np.zeros(n_buffers)
    csac_info_phys      = np.zeros((n_buffers,4))   
    
    kp = 0
        
    for i,packet in enumerate(packets_readout):
        #print("Parsing packet ID {:d} with {:d} buffers".format(i,len(packet)))
        
        for j, buf in enumerate(packet):
            #print("Parsing buffer ID {:d} with {:d} event lists".format(j,len(buf)))
            
            # The header data of the first event list is the same of the other three
            # so we put its info for the packets FITS extension
            header, data = buf[0]
            
            packetID[kp]     = i
            bufferID[kp]     = j
            asic_ID[kp]      = header.ASIC_ID
            gps_offset[kp]   = header.GPS_Time["GPSOffset"]
            utc_offset[kp]   = header.GPS_Time["UTCOffset"]
            week_sec[kp]     = header.GPS_Time["WeekSeconds"]
            week_num[kp]     = header.GPS_Time["Week"]
            gps_status[kp]   = header.GPS_Time["GPSStatus"]
            obt_s[kp]        = header.BEE_HK["ABT_OBT"]
            obt_ns[kp]       = header.BEE_HK["ABT_CNT"]
            quad_status[kp]  = header.BEE_HK["QuadrantStatus"]
            trigger_counter[kp]  = header.BEE_HK["TriggerCounter"]
            rejected_counter[kp] = header.BEE_HK["RejectedCounter"]
            event_counter[kp]    = header.BEE_HK["EventCounter"]
            overflow_counter[kp] = header.BEE_HK["OverflowCounter"]
            
            plvolt[kp] = [header.BEE_HK["3V3D_raw"]         , \
                            header.BEE_HK["3V3A_raw"]      , \
                            header.BEE_HK["3V3-BEE_raw"]   , \
                            header.BEE_HK["2V0_raw"]       , \
                            header.BEE_HK["5V0-FEE_raw"]   , \
                            header.BEE_HK["HV_raw"]        , \
                            header.BEE_HK["12V0_raw"]      , \
                            header.BEE_HK["5V0-BEE_raw"]   ]            
            plcurr[kp] = [header.BEE_HK["3V3D_I_raw"]         , \
                            header.BEE_HK["3V3A_I_raw"]      , \
                            header.BEE_HK["3V3-BEE_I_raw"]   , \
                            header.BEE_HK["2V0_I_raw"]       , \
                            header.BEE_HK["5V0-FEE_I_raw"]   , \
                            header.BEE_HK["12V0_I_raw"]      , \
                            header.BEE_HK["5V0-BEE_I_raw"]   ]
                            
            plvolt_phys[kp] = [header.BEE_HK["3V3D"]         , \
                            header.BEE_HK["3V3A"]      , \
                            header.BEE_HK["3V3-BEE"]   , \
                            header.BEE_HK["2V0"]       , \
                            header.BEE_HK["5V0-FEE"]   , \
                            header.BEE_HK["HV"]        , \
                            header.BEE_HK["12V0"]      , \
                            header.BEE_HK["5V0-BEE"]   ]            
            plcurr_phys[kp] = [header.BEE_HK["3V3D_I"]         , \
                            header.BEE_HK["3V3A_I"]      , \
                            header.BEE_HK["3V3-BEE_I"]   , \
                            header.BEE_HK["2V0_I"]       , \
                            header.BEE_HK["5V0-FEE_I"]   , \
                            header.BEE_HK["12V0_I"]      , \
                            header.BEE_HK["5V0-BEE_I"]   ]
                            
                                                        
            for temperature in range(6):
                fee_temp_phys[kp][temperature] = header.Det_Temp[temperature+1]
            bee_temp_phys[kp] = header.Det_Temp[0]
            csac_info_phys[kp] = [header.CSAC_HK["CSACStatus"]  , \
                            header.CSAC_HK["LaserI"]      , \
                            header.CSAC_HK["HeatP"]       , \
                            header.CSAC_HK["Temp"]        ]
                                    
            kp += 1
            

    
    
    # Extensions
    sel_single_pkt = range(n_buffers)
    
    # TODO: Test conversion of GPS time in MET

    # Zero-align times
    obt_s = obt_s[sel_single_pkt]-obt_s[0]
    
    if gps_ok:
        # Calculate GPS time for the first header
        # gps_offset is the receiver clock offset
        # utc_offset is the offset of gps system from utc time (should be about 18 leap secs)
        # week_num is the number of weeks since 1980-01-06 00:00:00 UTC
        # week_sec is the number of seconds in that week
        gps_time_ref = -gps_offset[0]+utc_offset[0]+ week_sec[0] + week_num[0]*7*86400
        # Convert in MET: the GPS time at MET reference time is 1325030381.0 
        met_offset = gps_time_ref - 1325030381.0 
    else:
        met_offset = 0
        
    # Add to the time
    obt_s += met_offset
    
    t1hdu = pyfits.BinTableHDU.from_columns([
                                              pyfits.Column(name='TIME',
                                                            format='1D',
                                                            unit='s',
                                                            array=obt_s[sel_single_pkt]),        
                                              pyfits.Column(name='PACKETID',
                                                            format='1J',
                                                            array=packetID[sel_single_pkt]),
                                              pyfits.Column(name='BUFFERID',
                                                            format='1J',
                                                            array=bufferID[sel_single_pkt]),
                                              pyfits.Column(name='QUADSTS',
                                                            format='40I',
                                                            array=quad_status[sel_single_pkt]),
                                              pyfits.Column(name='TRGCNT',
                                                            format='4I',
                                                            array=trigger_counter[sel_single_pkt]),
                                              pyfits.Column(name='REJCNT',
                                                            format='4I',
                                                            array=rejected_counter[sel_single_pkt]),
                                              pyfits.Column(name='EVTCNT',
                                                            format='4I',
                                                            array=event_counter[sel_single_pkt]),
                                              pyfits.Column(name='OVFCNT',
                                                            format='4I',
                                                            array=overflow_counter[sel_single_pkt]),
                                              pyfits.Column(name='PLVOLT',
                                                            format='8B',
                                                            array=plvolt[sel_single_pkt]),
                                              pyfits.Column(name='PLCURR',
                                                            format='7B',
                                                            array=plcurr[sel_single_pkt]),
                                              pyfits.Column(name='PLVOLTP',
                                                            format='8D',
                                                            array=plvolt_phys[sel_single_pkt]),
                                              pyfits.Column(name='PLCURRP',
                                                            format='7D',
                                                            array=plcurr_phys[sel_single_pkt]),
                                              pyfits.Column(name='FEETEMPP',
                                                            format='6D',
                                                            array=fee_temp_phys[sel_single_pkt]),
                                              pyfits.Column(name='BEETEMPP',
                                                            format='1D',
                                                            array=bee_temp_phys[sel_single_pkt]),
                                              pyfits.Column(name='CSACINFP',
                                                            format='4D',
                                                            array=csac_info_phys[sel_single_pkt])
                                            ])

    # Write FITS file
    # "Null" primary array
    prhdu = pyfits.PrimaryHDU()
    
    # TODO: check and test
    exposure = np.max(obt_s)-np.min(obt_s)
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
    
    
    t1hdu.header.set('EXTNAME', 'HK',  'Name of this binary table extension')
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
