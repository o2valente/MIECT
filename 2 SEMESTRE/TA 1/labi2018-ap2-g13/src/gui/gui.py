import sys
import os
import csv
import subprocess
import signal
from PyQt5.QtWidgets import *


def write_msg(data):
	wind = None
	humi = None
	temp = None
	try:
		wind = float(data[0])
		humi = float(data[1])
		temp = float(data[2])
	except:
		pass
	
	if wind == None:
		return
	if(wind < 30 and humi < 80 and temp > 15):
		msgText.setText("Está bom tempo")
	else:
		roupas = ""
		if(wind >= 30 or temp <= 15):
			roupas = roupas + ("casaco ")
		if(humi >= 80):
			roupas = roupas + ("guarda-chuva ")
		
		msgText.setText("O tempo não está muito bom, deve levar: " + roupas)


def update():
	file_csv = open("src/temp.csv", 'r')
	csv_reader = csv.reader(file_csv, delimiter=',')
	for row in csv_reader:
		windText.setText("Vento: " + str(row[0]))
		humiText.setText("Humidade: " + str(row[1]))
		tempText.setText("Temperatura: " + str(row[2]))
		write_msg(row)

def term():
	os.killpg(os.getpgid(client.pid), signal.SIGTERM)
	sys.exit(1)

try:
	file_csv = open("src/temp.csv", 'r')
except:
	file_csv = open("src/temp.csv", 'w')
	writer = csv.DictWriter(file_csv, fieldnames=['WIND', 'HUMIDITY', 'TEMPERATURE'])
	writer.writeheader()
	writer.writerow({'WIND': "---", 'HUMIDITY': "---", 'TEMPERATURE': "---"})
	file_csv.close()

client = subprocess.Popen(["python3", "src/client.py", "&"])

app = QApplication(sys.argv)

w = QWidget()
w.resize(500, 250)
w.move(300, 300)
w.setWindowTitle("Weather App")
btn = QPushButton("Update", w)
btn.resize(70,30)
btn.move(150, 200)

close = QPushButton("Close", w)
close.resize(70,30)
close.move(270, 200)

windText = QLineEdit(w)
humiText = QLineEdit(w)
tempText = QLineEdit(w)
msgText = QLineEdit(w)

windText.move(0, 10)
humiText.move(0, 60)
tempText.move(0,110)
msgText.resize(250, 50)
msgText.move(150, 60)
update()
btn.clicked.connect(update)
close.clicked.connect(term)
w.show()



sys.exit(app.exec_())
