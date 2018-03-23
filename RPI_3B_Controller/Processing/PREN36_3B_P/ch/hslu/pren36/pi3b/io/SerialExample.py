from threading import Thread
import time
import serial


class SerialExample:
    t_read = None
    readable = False
    ser = serial.Serial(
       port="/dev/serial0",
       baudrate=9600,
       parity=serial.PARITY_NONE,
       stopbits=serial.STOPBITS_ONE,
       bytesize=serial.EIGHTBITS,
       timeout=10
    )

    def initialize(self):
        print("initialize")
        if self.ser.is_open:
            self.ser.close()
        self.ser.open()
        self.readable = True
        self.t_read = Thread(target=self.read)
        self.t_read.start()

    def write(self, data):
        print("write " + str(data))
        data = str(data + '\n')
        encoded = data.encode('raw_unicode_escape')
        self.ser.write(encoded)

    def read(self):
        while self.readable:
            data = self.ser.readline().rstrip()
            print("read " + str(data.decode('utf-8')))


if __name__ == '__main__':
    serialExample = SerialExample()
    serialExample.initialize()
    time.sleep(2)
    for i in range(1, 20):
        serialExample.write("test " + str(i))
