from tkinter import* 
import main_code
import _thread
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from math import sqrt

sem = threading.Semaphore()


# wysokosc balonu
def pars_altitude(payload_string):

    altitude = payload_string[2:10]
    conversed_altitude = int(altitude, 16)
    return str(conversed_altitude)


# szerokosc geograficzna
def pars_latitude(payload_string):
    latitude = payload_string[10:18]
    conversed_latitude = int(latitude, 16)
    lat = conversed_latitude/10000  # czy dzielenie w strunie zadziałą? odp:NIE
    return str(lat)


# dlugosc geograficzna
def pars_longitude(payload_string):
    longitude = payload_string[18:26]
    conversed_longititude = int(longitude, 16)
    long = conversed_longititude/10000
    return str(long)


# srednia temperatura probek
def pars_temperature(payload_string):
    temperature = payload_string[26:30]
    conversed_temperature = int(temperature, 16)
    te = conversed_temperature/100
    return str(te)


def pars_status(payload_string):
    # temperatura - status probek
    # zmiana zmiennej!!!!!!
    temp_info1 = payload_string[30:36]
    print ("temp_info1: " + temp_info1)
    temp_info2 = int(temp_info1, 16)
    #temp_info3 = bin(temp_info2)
    return temp_info2


lati = []
longi = []
hight = []


# KONTROLOWAC ROZMIAR
bufer = []


def process_serial():
    global lati
    global longi
    global hight
    file = open('payload.txt', 'w+')

    exitLoop = False
    while not exitLoop:
        # definition of data received from port
        # payload_data = readserial()
        payload_data = main_code.read_serial()
        # data shift to string
        payload_string = str(payload_data.decode())
        sem.acquire()
        bufer.append(payload_data)

        lati.append(float(pars_latitude(payload_string)))
        longi.append(float(pars_longitude(payload_string)))
        hight.append(float(pars_altitude(payload_string)))

        sem.release()


        #print("payload_string: " + payload_string)

        # saving into the created file
        file.write(payload_string)
        file.flush()


t = _thread.start_new_thread(process_serial, ())

exit_loop = False
while not exit_loop:
    sem.acquire()
    if bufer != []:
        exit_loop = True
    sem.release()

# creates window
window = Tk()  # is closed at the end of code
window.title('stardust interface')
frame = Frame(window)

def update_window():

    global frame
    frame.destroy()
    frame = Frame(window)
    sem.acquire()
    payload_data = bufer[-1]
    sem.release()
    payload_string = payload_data.decode()
    print(payload_string)


    onion = format(pars_status(payload_string), '#026b')
    print("onion: " + onion)
    # S11 to probka nr 11 itd.
    S11 = onion[2:4]
    S10 = onion[4:6]
    S9 = onion[6:8]
    S8 = onion[8:10]
    S7 = onion[10:12]
    S6 = onion[12:14]
    S5 = onion[14:16]
    S4 = onion[16:18]
    S3 = onion[18:20]
    S2 = onion[20:22]
    S1 = onion[22:24]
    S0 = onion[24:26]

    specimen = [S11, S10, S9, S8, S7, S6, S5, S4, S3, S2, S1, S0]
    spec = str(specimen)

    # WYSWIETLANIE W OKNIE
    displayed_conversed_altitude = Label(frame, text='Altitude: '+pars_altitude(payload_string)+' m')
    displayed_conversed_altitude.pack()

    displayed_latitude = Label(frame, text='Latitude: '+pars_latitude(payload_string)+' N')
    displayed_latitude.pack()

    displayed_longitude = Label(frame, text='Longitude: '+pars_longitude(payload_string)+' E')
    displayed_longitude.pack()

    displayed_temperature = Label(frame, text='Average temperature: '+pars_temperature(payload_string)+u' \u2103')
    displayed_temperature.pack()

    # do zmiany
    for specimen_status in specimen:
        if specimen_status == '00':
            displayed_specimen_status = Label(frame, text='temperature apropriate', bg='green')
            displayed_specimen_status.pack()
        elif specimen_status == '01':
            displayed_specimen_status = Label(frame, text='temperature too high', bg='red')
            displayed_specimen_status.pack()
        elif specimen_status == '10':
            displayed_specimen_status = Label(frame, text='temperature too low', bg='blue')
            displayed_specimen_status.pack()
        elif specimen_status == '11':
            displayed_specimen_status = Label(frame, text='hardware error', bg='black', fg='white')
            displayed_specimen_status.pack()
        else:
            displayed_specimen_status = Label(frame, text='wrong statement: ', bg='yellow')
            displayed_specimen_status.pack()
    frame.pack()
    window.after(1000, update_window)


window.after(1000, update_window)


fig = plt.figure()
axis1 = fig.add_subplot(1, 1, 1)

def baloon_path(i):
    global lati
    global longi
    global hight
    # arguments = sqrt(lati**2 + longi**2)
    arguments = []
    #sem.acquire()
    for j in range(0, len(lati)):
        arguments.append(sqrt(lati[j]**2 + longi[j]**2))
    variables = hight
    #sem.release()

    xar = arguments
    yar = variables

    axis1.clear()
    axis1.plot(xar, yar)


ani = animation.FuncAnimation(fig, baloon_path, interval=1000)

plt.show()

window.mainloop()
