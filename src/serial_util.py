import serial

class SerialUsb:
    def __init__(self, tty_name):
        self.ser = serial.Serial()
        self.ser.port = tty_name
        # If it breaks try the below
        #self.serConf() # Uncomment lines here till it works

        self.ser.open()
        self.ser.flushInput()
        self.ser.flushOutput()

    def write(self, cmd_str):
        return self.ser.write(cmd_str)

    def read(self, n_bytes):
        return self.ser.read(n_bytes)

    def serConf(self):
        self.ser.baudrate = 9600
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_ONE
        #self.ser.timeout = 0
        self.ser.xonxoff = False # Disable Software Flow Control
        self.ser.rtscts = False # Disable (RTS/CTS) flow Control
        self.ser.dsrdtr = False # Disable (DSR/DTR) flow Control
        self.ser.writeTimeout = 2

    def close(self):
        self.ser.close()