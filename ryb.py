import RPi.GPIO as GPIO
import time
import csv
from datetime import datetime

GPIO.setmode(GPIO.BCM)

in_1 = 23 
in_2 = 24 
in_3 = 25  
in_4 = 8  

relay_out_1 = 26   
relay_out_2 = 19   
relay_out_3 = 13  
relay_out_4 = 6   

GPIO.setup(in_1, GPIO.OUT)
GPIO.setup(in_2, GPIO.OUT)
GPIO.setup(in_3, GPIO.OUT)
GPIO.setup(in_4, GPIO.OUT)

GPIO.setup(relay_out_1, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(relay_out_2, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(relay_out_3, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(relay_out_4, GPIO.IN, GPIO.PUD_DOWN)

now = datetime.now()
formatted_time_for_filename = now.strftime("%Y%m%d%H%M%S")
filename = f'{formatted_time_for_filename}_4relay_log.csv'

fields = ['日期', '時間', '4ch_relay輸入值', '4ch_relay輸出值']

with open(filename, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)

while True:
    input_value = input("請輸入4位數二進位值，輸入'q'離開: ")

    if input_value.lower() == 'q':
        break

    if len(input_value) != 4 or not all(bit in '01' for bit in input_value):
        print("無效輸入，請輸入4位數的二進位值。")
        continue

    # 將輸入的字串依序assign給4個GPIO接腳
    set_in_1 = int(input_value[0])
    set_in_2 = int(input_value[1])
    set_in_3 = int(input_value[2])
    set_in_4 = int(input_value[3])

    now = datetime.now()
    formatted_date = now.strftime("%Y/%m/%d")
    formatted_time = now.strftime("%H:%M:%S")
   
    GPIO.output(in_1, GPIO.HIGH if set_in_1 == 1 else GPIO.LOW)
    GPIO.output(in_2, GPIO.HIGH if set_in_2 == 1 else GPIO.LOW)
    GPIO.output(in_3, GPIO.HIGH if set_in_3 == 1 else GPIO.LOW)
    GPIO.output(in_4, GPIO.HIGH if set_in_4 == 1 else GPIO.LOW)

    time.sleep(0.5)

    get_relay_1 = GPIO.input(relay_out_1)
    get_relay_2 = GPIO.input(relay_out_2)
    get_relay_3 = GPIO.input(relay_out_3)
    get_relay_4 = GPIO.input(relay_out_4)

    get_relay_values = ''.join(str(bit) for bit in [get_relay_1, get_relay_2, get_relay_3, get_relay_4])
    print(f"get_relay_values: {get_relay_values}")

    row_data = [formatted_date, formatted_time, input_value, get_relay_values]
    with open(filename, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(row_data)

    time.sleep(1)



