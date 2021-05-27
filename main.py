from ctypes import *
import time
from dwfconstants import *
import sys

if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")

hdwf = c_int()
currentChannel = c_int(0) #purple
voltageChannel = c_int(1) #blue
version = create_string_buffer(16)
dwf.FDwfGetVersion(version)
dwf.FDwfParamSet(DwfParamOnClose, c_int(0)) # Turn on
dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

if hdwf.value == hdwfNone.value:
    print("failed to open device")
    quit()

dwf.FDwfDeviceAutoConfigureSet(hdwf, c_int(0))
dwf.FDwfAnalogOutNodeEnableSet(hdwf, currentChannel, AnalogOutNodeCarrier, c_bool(True))
dwf.FDwfAnalogOutNodeFunctionSet(hdwf, currentChannel, AnalogOutNodeCarrier, funcDC)
dwf.FDwfAnalogOutNodeOffsetSet(hdwf, currentChannel, AnalogOutNodeCarrier, c_double(.026))
dwf.FDwfAnalogOutConfigure(hdwf, currentChannel, c_bool(True))

dwf.FDwfAnalogOutNodeEnableSet(hdwf, voltageChannel, AnalogOutNodeCarrier, c_bool(True))
dwf.FDwfAnalogOutNodeFunctionSet(hdwf, voltageChannel, AnalogOutNodeCarrier, funcDC)
dwf.FDwfAnalogOutNodeOffsetSet(hdwf, voltageChannel, AnalogOutNodeCarrier, c_double(5))
dwf.FDwfAnalogOutConfigure(hdwf, voltageChannel, c_bool(True))


time.sleep(5)


dwf.FDwfDeviceAutoConfigureSet(hdwf, c_int(0))
dwf.FDwfAnalogOutNodeEnableSet(hdwf, currentChannel, AnalogOutNodeCarrier, c_bool(True))
dwf.FDwfAnalogOutNodeFunctionSet(hdwf, currentChannel, AnalogOutNodeCarrier, funcDC)
dwf.FDwfAnalogOutNodeOffsetSet(hdwf, currentChannel, AnalogOutNodeCarrier, c_double(0))
dwf.FDwfAnalogOutConfigure(hdwf, currentChannel, c_bool(True))

dwf.FDwfAnalogOutNodeEnableSet(hdwf, voltageChannel, AnalogOutNodeCarrier, c_bool(True))
dwf.FDwfAnalogOutNodeFunctionSet(hdwf, voltageChannel, AnalogOutNodeCarrier, funcDC)
dwf.FDwfAnalogOutNodeOffsetSet(hdwf, voltageChannel, AnalogOutNodeCarrier, c_double(0))
dwf.FDwfAnalogOutConfigure(hdwf, voltageChannel, c_bool(True))
dwf.FDwfParamSet(DwfParamOnClose, c_int(1)) # Turn off
dwf.FDwfDeviceClose(hdwf)


# sts = c_byte()
# rgdSamples = (c_double*4000)()

# cBufMax = c_int()
# dwf.FDwfAnalogInBufferSizeInfo(hdwf, 0, byref(cBufMax))
# print("Device buffer size: "+str(cBufMax.value)) 

# #set up acquisition
# dwf.FDwfAnalogInFrequencySet(hdwf, c_double(20000000.0))
# dwf.FDwfAnalogInBufferSizeSet(hdwf, c_int(4000)) 
# dwf.FDwfAnalogInChannelEnableSet(hdwf, c_int(-1), c_bool(True))
# dwf.FDwfAnalogInChannelRangeSet(hdwf, c_int(-1), c_double(5))
# dwf.FDwfAnalogInChannelFilterSet(hdwf, c_int(-1), filterDecimate)

# #wait at least 2 seconds for the offset to stabilize
# time.sleep(2)

# print("Starting oscilloscope")
# dwf.FDwfAnalogInConfigure(hdwf, c_int(1), c_int(1))


# while True:
#     dwf.FDwfAnalogInStatus(hdwf, c_int(1), byref(sts))
#     if sts.value == DwfStateDone.value :
#         break
#     time.sleep(0.1)
# print("Acquisition done")

# dwf.FDwfAnalogInStatusData(hdwf, 1, rgdSamples, 4000) # get channel 2 data
# dwf.FDwfDeviceCloseAll()

# dc = sum(rgdSamples)/len(rgdSamples)
# print("DC: "+str(dc)+"V")

#  Gaussmeter Voltage     Gauss Measured  Output Voltage for current Control
# .15964887385060214  V   = 1600 Gauss    = .41  V
# .1432985029617699   V   = 1440 Gauss    = .372 V
# .12729598176626933  V   = 1280 Gauss    = .329 V
# .11104186054986227  V   = 1120 Gauss    = .287 V
# .09504567156965277  V   =  960 Gauss    = .243 V
# .07894090620458431  V   =  800 Gauss    = .202 V
# .06283208822172708  V   =  640 Gauss    = .158 V
# .046774941115647055 V   =  480 Gauss    = .116 V
# .030817927440706272 V   =  320 Gauss    = .071 V
# .014510784474927393 V   =  160 Gauss    = .026 V