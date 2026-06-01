import serial

ser = serial.serial_for_url('loop://', timeout=1)
ser.timeout = None
ser.reset_input_buffer()
ser.reset_output_buffer()

print('Ingrese un comando:\n')

while 1:
    char_v = []
    data = input("ToSent: ")

    if data == 'exit':
        ser.close()
        break
    else:
        for ptr in range(len(data)):
            char_v.append(data[ptr])
        print(char_v)

        for ptr in range(len(char_v)):
            ser.write(char_v[ptr].encode())

        out = ''
        while ser.in_waiting > 0:
            out += ser.read(1).decode()

        if out != '':
            print(">> " + out)