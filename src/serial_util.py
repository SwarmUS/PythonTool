import serial
import sys
import glob

class SerialUsb:
    def __init__(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/ttyACM*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        print("Serial port:")
        for i, port in enumerate(ports):
            print(f'{i}. {port}')

        choice = int(input(">"))

        self.ser = serial.Serial()
        self.ser.port = ports[choice]
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