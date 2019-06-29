import sys
import glob
import serial


# odczytywanie z portu
def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for porty in ports:  # for some reason 'port' is shadowed WHY?
        try:
            s = serial.Serial(porty)
            s.close()
            result.append(porty)
        except (OSError, serial.SerialException):
            pass
    # print(result)
    return result


serials = serial_ports()
theserial = serial.Serial(serials[0], baudrate=115200, timeout=2)


def read_serial():
    return theserial.readline()
