import sys
import glob
import serial
from serial import Serial
import datetime


def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except Exception as e:
            #print(f"{datetime.datetime.now()} - AVISO - {e}")
            pass
    return result

def Main():
    
    s_port = serial_ports()
    baudrate = [2400, 4800, 9600, 19200, 38400, 57600, 115200]
    packet = ""

    if len(s_port) > 0:
        print("Portas disponíveis:")
        for i in range (0, len(s_port)):
            #print(serial_ports())
            print(f"{i} - {s_port[i]}")
    else:
        print("Não há portas seriais disponíveis.")
        exit()

    #print("\nSelecione o número da porta desejada:")
    selected_port = int(input("\nSelecione o número da porta desejada: "))

    print("Velocidade de comunicação:")
    for i in range (0, len(baudrate)):
        #print(serial_ports())
        print(f"{i} - {baudrate[i]}")

    selected_br = int(input("\nSelecione a velocidade da porta desejada: "))
    
    print(f"\nSelecionada porta '{s_port[selected_port]}' com velocidade {baudrate[selected_br]}")

    sp = serial.Serial(port = s_port[selected_port],
                       baudrate = baudrate[selected_br],
                       parity = serial.PARITY_NONE,
		               stopbits = serial.STOPBITS_ONE,
		               bytesize = serial.EIGHTBITS,
		               timeout = 1)

    while True:
        
        x = b''
        packet = ""

        while x != b'\n':
            x = sp.read()
            packet += x.decode("utf-8", "ignore")
        print(packet)

if __name__ == '__main__':
    Main()
    
    