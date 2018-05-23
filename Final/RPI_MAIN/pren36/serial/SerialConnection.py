import serial


class SerialConnection:
    ser = serial.Serial(
        port="/dev/serial0",
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=None,
        write_timeout=None
    )

    def initialize(self):
        self.ser.open()

    def write(self, data):
        data = str(data + '\n')
        encoded = data.encode('raw_unicode_escape')
        self.ser.write(encoded)

    def read(self):
        data = self.ser.readline()
        return str(data.decode('utf-8')).strip()
