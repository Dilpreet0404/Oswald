from flask import Flask,render_template
import RPi.GPIO as GPIO

import os,time
from itertools import cycle
GPIO.setmode(GPIO.BOARD)


app=Flask(__name__)
fire={15 : {'state' : GPIO.LOW}}
bath = {22 : {'state' : GPIO.LOW},18 : { 'state' : GPIO.LOW}}
kit={29 : {'state' : GPIO.LOW},31 : { 'state' : GPIO.LOW}}
live={33 : {'state' : GPIO.LOW},37 : { 'state' : GPIO.LOW},36 : {'state' : GPIO.LOW},32 : { 'state' : GPIO.LOW}}
bed={16 : {'state' : GPIO.LOW},12 : { 'state' : GPIO.LOW},7 : {'state' : GPIO.LOW}}
doo={13: {'state' : 'off'}}

def robot(text):
    os.system("espeak ' " + text + " ' ")
state_cycle = cycle(['on', 'off'])

for pin in kit:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)

for pin in fire:
   GPIO.setup(pin, GPIO.IN)

for pin in doo:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)

for pin in live:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)

for pin in bath:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)

for pin in bed:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)


@app.route('/')
def hello1():
	return render_template("index1.html")
@app.route('/main')
def hello():
	return render_template("main.html",a=1)
@app.route('/bedroom')
def bedroom():
	return render_template("bedroom.html",a=bed)
@app.route('/bathroom')
def bathroom():
	return render_template("bathroom.html",a=bath)
@app.route('/firealarm')
def firealarm():
	button_status=GPIO.input(15)
	return render_template("firealarm.html",a=button_status)
@app.route('/living')
def livingroom():
	return render_template("livingroom.html",a=live)	
@app.route('/kitchen')
def kitchen():
	return render_template("kitchen.html",a=kit)	
@app.route('/door')
def door():
	return render_template("main_door.html",a=doo)
@app.route('/schedule')
def sche():
	return render_template("schedule.html")

@app.route('/change/<pin>/<action>')
def change(pin,action):
	pin=int(pin)
	if(pin==15):
		button_status=GPIO.input(15)
		if button_status == 1:
			for i in range(0,4):
				robot("Fire Alert")
		return render_template("firealarm.html",a=button_status)
	if(pin==29 or pin==31):
		if action == 'on':
			GPIO.output(pin,GPIO.HIGH)
			kit[pin]['state']=1
		else:
			GPIO.output(pin,GPIO.LOW)
			kit[pin]['state']=0
		return render_template("kitchen.html",a=kit)
	if(pin==33 or pin==37 or pin==36 or pin==32):
		if action == 'on':
			GPIO.output(pin,GPIO.HIGH)
			live[pin]['state']=1
		else:
			GPIO.output(pin,GPIO.LOW)
			live[pin]['state']=0
		return render_template("livingroom.html",a=live)
	if(pin==16 or pin==12 or pin==7):
		if action =='on':
			GPIO.output(pin,GPIO.HIGH)
			bed[pin]['state']=1
		else:
			GPIO.output(pin,GPIO.LOW)
			bed[pin]['state']=0
		return render_template("bedroom.html",a=bed)	
	if(pin==13):
		if action == 'on':
			GPIO.output(pin,GPIO.HIGH)
			doo[pin]['state']=1
		else:
			doo[pin]['state']=0
			GPIO.output(pin,GPIO.LOW)
		return render_template("main_door.html",a=doo)		
	if(pin==22 or pin==18 ):
		if action == 'on':
			GPIO.output(pin,GPIO.HIGH)
			bath[pin]['state']=1
		else:
			GPIO.output(pin,GPIO.LOW)
			bath[pin]['state']=0
		return render_template("bathroom.html",a=bath)
	if(pin==155):
		robot("Sir! Your Schedule for the day")
		robot("Do your Exercise from 6AM to 7AM")
		time.sleep(0.4)
		robot("Prepare for Project Presentation")
		time.sleep(0.4)
		robot("Project Setup at 12 Noon ")
		time.sleep(0.4)
		robot("Project Presenstation from 1 to 5")
		time.sleep(0.4)
		robot("Go for Pik-cell Art Competetion")
		time.sleep(0.4)
		robot("7:30 Dinner Time")
		time.sleep(0.4)
		robot("Call home")
		time.sleep(0.4)
		robot("Prepare for the Next day")
		time.sleep(0.4)

		return render_template("bathroom.html",a=bath)

if __name__=="__main__":
	app.run(host='0.0.0.0', port=80, debug = True)