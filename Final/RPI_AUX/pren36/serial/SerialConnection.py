import serial


class SerialConnection:
    EOL = bytes('\n', encoding='ascii')
    LEN_EOL = len(EOL)

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
        if self.ser.is_open:
            self.ser.close()
        self.ser.open()

    def write(self, data):
        data = str(data + '\n')
        self.ser.write(bytes(data, encoding='ascii'))

    def read(self):
        data = self.readline()
        return str(data, encoding='ascii').strip()

    def readline(self):
        line = bytearray()
        while True:
            c = self.ser.read(1)
            if c:
                line += c
                if line[-SerialConnection.LEN_EOL:] == SerialConnection.EOL:
                    break
            else:
                break
        return bytes(line)
