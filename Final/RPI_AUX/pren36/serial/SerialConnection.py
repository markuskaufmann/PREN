import serial


class SerialConnection:
    ser = serial.Serial(
       port="/dev/serial0",
       baudrate=9600,
       parity=serial.PARITY_NONE,
       stopbits=serial.STOPBITS_ONE,
       bytesize=serial.EIGHTBITS,
       timeout=10
    )

    def initialize(self):
        if self.ser.is_open:
            self.ser.close()
        self.ser.open()

    def write(self, data):
        data = str(data + '\n')
        encoded = data.encode('raw_unicode_escape')
        self.ser.write(encoded)

    def read(self):
        data = self.ser.readline().rstrip()
        return str(data.decode('utf-8'))