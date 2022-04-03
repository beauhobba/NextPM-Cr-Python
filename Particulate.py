import time
import serial
from binascii import *
from Sensors.PM.ParticulateVariables import *

import ENVIRONMENTAL_VARIABLES as EV

class PMCSensor:
    """
    | Particulate Sensor: 
    """
    def __init__(self):
        self.ser = serial.Serial(
        port=EV.PM_PORT,
        baudrate=EV.PM_BAUDRATE,
        timeout=EV.PM_TIMEOUT,
        parity=serial.PARITY_EVEN,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS)


    def openSerial(self):
        """
        Opens a serial connection to the PM Sensor 
        """
        self.ser.isOpen()
        print("particulate serial open")


    def powerOn(self):
        pass
    
    
    def isActive(self):
        pass
    
    
    def cleanSensor(self):
        pass

        
    def callError(self):
        """
        Calls an error for the PM Sensor 
        """
        print("NEXT PM Sensor is in Error State")


    def checkStatus(self):
        """
        Checks the status of the PM Sensor 

        :return: Status of the PM Sensor
        :rtype: String 
        """
        return_bytes = self.returnBytes(sen_state, 4)
        status = self.getState(return_bytes)
        status_string = status_table.get(status)
        return status_string


    def getState(self, bytes_val):
        """
        Gets the state of the PM Sensor

        :param bytes_val: Bytes value to be input into the PM Sensor 
        :type bytes_val: Binary String
        :return: The status byte value (corresponds to the status_table)
        :rtype: Int
        """
        res = (bytes_val[2])
        return res


    def mean5Min(self):
        """
        Average value of the PM sensor over 5 mins

        :return: PM0_3, PM0_5, PM1, PM2_5, PM_5
        :rtype: [float, float, ....]
        """
        results = self.readXTime(mean5min)
        return results


    def read1Min(self):
        """
        Average value of the PM sensor over 1 min

        :return: PM0_3, PM0_5, PM1, PM2_5, PM_5
        :rtype: [float, float, ....]
        """
        results = self.readXTime(mean1min)
        return results


    def read10Sec(self):
        """
        Average value of the PM sensor over 10 seconds

        :return: PM0_3, PM0_5, PM1, PM2_5, PM_5
        :rtype: [float, float, ....]
        """        
        results = self.readXTime(mean10sec)
        return results
        
        
    def readXTime(self, protocol):
        """
        Sends a binary string to the PM sensor to obtain the current binary value 

        :param protocol: The binary string
        :type protocol: Binary String
        :return: PM0_3, PM0_5, PM1, PM2_5, PM_5
        :rtype: [float, float, ....]
        """
        return_bytes = self.returnBytes(protocol, 32)
        results = self.convertToPM(return_bytes)
        return results


    def returnBytes(self, protocol, byteLength):
        """Returns the bytes stored on the PM (which contain data)

        :param protocol: Binary string to be sent to the PM sensor
        :type protocol: Binary String
        :param byteLength:The length of the bytes to be returned (either 8 or 16)
        :type byteLength: Int
        :return: Data stored on the Next PM 
        :rtype: Bytes
        """
        self.ser.write(protocol)
        return_bytes = None
        time.sleep(0.350)
        while (self.ser.in_waiting):
            try:
                return_bytes = self.ser.read(byteLength)
            except:
                break
        return return_bytes


    def convertToPM(self, bytes_val):
        """
        Converts the bytes to the appropriate PM sensor values 

        :param bytes_val: Bytes string from the data stored on the PM sensor 
        :type bytes_val: Bytes
        :return: PM0_3, PM0_5, PM1, PM2_5, PM5 values 
        :rtype: [floats]
        """
        PM0_3 = self.PMBinaryCalculation(3, bytes_val)
        PM0_5 = self.PMBinaryCalculation(7, bytes_val)
        PM1 = self.PMBinaryCalculation(11, bytes_val)
        PM2_5 = self.PMBinaryCalculation(15, bytes_val)
        PM5 = self.PMBinaryCalculation(19, bytes_val)
        results = [PM0_3, PM0_5, PM1, PM2_5, PM5]
        return results


    def PMBinaryCalculation(self, n, bytes_val):
        """Calculation to turn the byte string into PM sensor data 

        :param n: Location of bytes data within the PM Sensor
        :type n: int 
        :param bytes_val: Bytes string from the data stored on the PM sensor
        :type bytes_val: Bytes 
        :return: PM sensor value
        :rtype: float
        """
        res = (bytes_val[n] << 32 | bytes_val[n+1] << 16 | bytes_val[n+2] << 8 | bytes_val[n+3])
        return res


    def  readTempHumidity(self):
        """Reads the temperature and humidity of the PM sensor

        :return: humidity and temperature data
        :rtype: [float, float]
        """
        return_bytes = self.returnBytes(temp_hum, 8)
        res = None 
        if(return_bytes != None):
            res = self.convertTempHum(return_bytes)
        else:
            self.callError() 
        return res


    def convertTempHum(self, bytes_val):
        """Converts the data stored on the PM sensor into humidity and temeprature data 

        :param bytes_val: Bytes string from the data stored on the PM sensor
        :type bytes_val: Bytes 
        :return: humidity and temperature
        :rtype: [float, float]
        """
        hum = (bytes_val[5] << 8 | bytes_val[6])/100
        temp = (bytes_val[3] << 8 | bytes_val[4])/100
        return [hum, temp]


    
