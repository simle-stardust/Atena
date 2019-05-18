from tkinter import*  # biblioteka do tworzenia okien
"""from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad """
# dodaj pakiet PyCryptodome
import sys
import glob
import serial
import time


# czas systemowy
print(time.monotonic())
czas = int(time.monotonic())


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
    print(result)
    return result


def readserial():
    serials = serial_ports()
    theserial = serial.Serial(serials[0], baudrate=115200, timeout=1)
    # nie masz tylu wartości tablicy/portów na swoim komputerze żeby chcieć 13stą wartość
    print(theserial)

    return theserial


"""   
    serials = serial_ports()

    while czas % 10 < 1:
        theserial = serial.Serial(serials[0], baudrate=115200, timeout=1)
        print(serials)
        return theserial
"""

# definition of data received from port
mydata = str(readserial())

# data shift to string
payload = str(mydata)
print(payload)


# creates window
window = Tk()  # is closed at the end of code
window.title('stardust interface')


# wysokosc balonu
def pars_altitude():

    altitude = payload[0:8]
    conversed_altitude = int(altitude, 16)
    return str(conversed_altitude)


# szerokosc geograficzna
def pars_latitude():
    latitude = payload[8:16]
    conversed_latitude = int(latitude, 16)
    lat = conversed_latitude/10000  # czy dzielenie w strunie zadziałą? odp:NIE
    return str(lat)


# dlugosc geograficzna
def pars_longitude():
    longitude = payload[16:24]
    conversed_longititude = int(longitude, 16)
    long = conversed_longititude/10000
    return str(long)


# srednia temperatura probek
def pars_temperature():
    temperature = payload[24:28]
    conversed_temperature = int(temperature, 16)
    te = conversed_temperature/100
    return str(te)


def pars_status():
    # temperatura - status probek
    # zmiana zmiennej!!!!!!
    temp_info1 = payload[28:34]
    temp_info2 = int(temp_info1, 16)
    temp_info3 = bin(temp_info2)
    return temp_info3


onion = str(pars_status)

# brakuje konwersji na wartości  binarne
# S11 to probka nr 11 itd.
S11 = onion[0:2]
S10 = onion[2:4]
S9 = onion[4:6]
S8 = onion[6:8]
S7 = onion[8:10]
S6 = onion[10:12]
S5 = onion[12:14]
S4 = onion[14:16]
S3 = onion[16:18]
S2 = onion[18:20]
S1 = onion[20:22]
S0 = onion[22:24]

specimen = [S11, S10, S9, S8, S7, S6, S5, S4, S3, S2, S1, S0]
spec = str(specimen)

# WYSWIETLANIE W OKNIE
displayed_conversed_altitude = Label(window, text='Altitude: '+pars_altitude()+' m')
displayed_conversed_altitude.pack()

displayed_latitude = Label(window, text='Latitude: '+pars_latitude()+' N')
displayed_latitude.pack()

displayed_longitude = Label(window, text='Longitude: '+pars_longitude()+' E')
displayed_longitude.pack()

displayed_temperature = Label(window, text='Average temperature: '+pars_temperature()+u' \u2103')
displayed_temperature.pack()

# do zmiany
for specimen_status in specimen:
    if specimen_status == '00':
        displayed_specimen_status = Label(window, text='temperature apropriate', bg='green')
        displayed_specimen_status.pack()
    elif specimen_status == '01':
        displayed_specimen_status = Label(window, text='temperature too high', bg='red')
        displayed_specimen_status.pack()
    elif specimen_status == '10':
        displayed_specimen_status = Label(window, text='temperature too low', bg='blue')
        displayed_specimen_status.pack()
    elif specimen_status == '11':
        displayed_specimen_status = Label(window, text='hardware error', bg='black', fg='white')
        displayed_specimen_status.pack()
    else:
        displayed_specimen_status = Label(window, text='wrong statement: ', bg='yellow')
        displayed_specimen_status.pack()


window.mainloop()
