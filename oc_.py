import RPi.GPIO as GPIO
import time
import csv
from datetime import datetime

#設接腳編號方式
GPIO.setmode(GPIO.BCM)

in_1 = 17
in_2 = 27
in_3 = 22
in_4 = 5

oc_out_1 = 12
oc_out_2 = 16
oc_out_3 = 20
oc_out_4 = 21

#設GPIO輸出輸入
GPIO.setup(in_1, GPIO.OUT)
GPIO.setup(in_2, GPIO.OUT)
GPIO.setup(in_3, GPIO.OUT)
GPIO.setup(in_4, GPIO.OUT)

GPIO.setup(oc_out_1, GPIO.IN, GPIO.PUD_DOWN) 
GPIO.setup(oc_out_2, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(oc_out_3, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(oc_out_4, GPIO.IN, GPIO.PUD_DOWN)

now = datetime.now()
formatted_time_for_filename = now.strftime("%Y%m%d%H%M%S")
filename = f'{formatted_time_for_filename}_4oc_log.csv'

fields = ['日期', '時間', '4ch_oc輸入值', '4ch_oc輸出值']

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

    get_oc_1 = GPIO.input(oc_out_1)
    get_oc_2 = GPIO.input(oc_out_2)
    get_oc_3 = GPIO.input(oc_out_3)
    get_oc_4 = GPIO.input(oc_out_4)

    get_oc_values = ''.join(str(bit) for bit in [get_oc_1, get_oc_2, get_oc_3, get_oc_4])
    print(f"get_oc_values: {get_oc_values}")

    row_data = [formatted_date, formatted_time, input_value, get_oc_values]
    with open(filename, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(row_data)

    time.sleep(1)

