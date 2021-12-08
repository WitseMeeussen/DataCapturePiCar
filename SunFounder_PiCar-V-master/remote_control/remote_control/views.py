'''
**********************************************************************
* Filename    : views
* Description : views for server
* Author      : Cavon
* Brand       : SunFounder
* E-mail      : service@sunfounder.com
* Website     : www.sunfounder.com
* Update      : Cavon    2016-09-13    New release
**********************************************************************
'''

from django.shortcuts import render_to_response
from .driver import camera, stream
from picar import back_wheels, front_wheels
from django.http import HttpResponse
import picar
import cv2
import os
from datetime import datetime


folder = '/root/Data/' + datetime.now()

def captureData():
	if(ControlerData['drive']==0): 
		return
	if not os.path.isdir(folder): 
		os.mkdir(folder)
	camera = cv2.VideoCapture(-1)
	camera.set(3, 640)
	camera.set(4, 480)


	
	_, image = camera.read()        
	cv2.imwrite("%s_%03d_%03d.png" % ( datetime.hour+datetime.minute, ControlerData['speed'], ControlerData['direction']), image)
        
    


picar.setup()
db_file = "/home/pi/SunFounder_PiCar-V/remote_control/remote_control/driver/config"
fw = front_wheels.Front_Wheels(debug=False, db=db_file)
bw = back_wheels.Back_Wheels(debug=False, db=db_file)
cam = camera.Camera(debug=False, db=db_file)
cam.ready()
bw.ready()
fw.ready()
 
SPEED = 60
bw_status = 0

ControlerData = {
		'speed':1,
		'drive':0,
		'direction':0
}

print(stream.start())

def home(request):
	return render_to_response("base.html")

def run(request):
	### this contains al the controller input
	ControlerData = {
		'speed':0,
		'drive':0,
		'direction':0
	}
	global SPEED, bw_status
	debug = ''
	if 'action' in request.GET:
		action = request.GET['action']
		# ============== Back wheels =============
		if action == 'bwready':
			ControlerData['drive'] = 0
			bw.ready()
			bw_status = 0
		elif action == 'forward':
			ControlerData['drive'] = 1
			bw.speed = SPEED
			bw.forward()
			bw_status = 1
			debug = "speed =", SPEED
		elif action == 'backward':
			ControlerData['drive'] = 0
			bw.speed = SPEED
			bw.backward()
			bw_status = -1
		elif action == 'stop':
			ControlerData['drive'] = 0
			bw.stop()
			bw_status = 0

		# ============== Front wheels =============
		elif action == 'fwready':
			fw.ready()
		elif action == 'fwleft':
			ControlerData['direction'] = -1
			fw.turn_left()
		elif action == 'fwright':
			ControlerData['direction'] = 0
			fw.turn_right()
		elif action == 'fwstraight':
			ControlerData['direction'] = 1
			fw.turn_straight()
		elif 'fwturn' in action:
			print("turn %s" % action)
			fw.turn(int(action.split(':')[1]))
		
		# ================ Camera =================
		elif action == 'camready':
			cam.ready()
		elif action == "camleft":
			cam.turn_left(40)
		elif action == 'camright':
			cam.turn_right(40)
		elif action == 'camup':
			cam.turn_up(20)
		elif action == 'camdown':
			cam.turn_down(20)	
	if 'speed' in request.GET:
		speed = int(request.GET['speed'])
		if speed < 0:
			speed = 0
		if speed > 100:
			speed = 100
		SPEED = speed
		if bw_status != 0:
			bw.speed = SPEED
		debug = "speed =", speed
	captureData()
	host = stream.get_host().decode('utf-8').split(' ')[0]
	return render_to_response("run.html", {'host': host})

def cali(request):
	if 'action' in request.GET:
		action = request.GET['action']
		# ========== Camera calibration =========
		if action == 'camcali':
			print('"%s" command received' % action)
			cam.calibration()
		elif action == 'camcaliup':
			print('"%s" command received' % action)
			cam.cali_up()
		elif action == 'camcalidown':
			print('"%s" command received' % action)
			cam.cali_down()
		elif action == 'camcalileft':
			print('"%s" command received' % action)
			cam.cali_left()
		elif action == 'camcaliright':
			print('"%s" command received' % action)
			cam.cali_right()
		elif action == 'camcaliok':
			print('"%s" command received' % action)
			cam.cali_ok()

		# ========= Front wheel cali ===========
		elif action == 'fwcali':
			print('"%s" command received' % action)
			fw.calibration()
		elif action == 'fwcalileft':
			print('"%s" command received' % action)
			fw.cali_left()
		elif action == 'fwcaliright':
			print('"%s" command received' % action)
			fw.cali_right()
		elif action == 'fwcaliok':
			print('"%s" command received' % action)
			fw.cali_ok()

		# ========= Back wheel cali ===========
		elif action == 'bwcali':
			print('"%s" command received' % action)
			bw.calibration()
		elif action == 'bwcalileft':
			print('"%s" command received' % action)
			bw.cali_left()
		elif action == 'bwcaliright':
			print('"%s" command received' % action)
			bw.cali_right()
		elif action == 'bwcaliok':
			print('"%s" command received' % action)
			bw.cali_ok()
		else:
			print('command error, error command "%s" received' % action)
	return render_to_response("cali.html")

def connection_test(request):
	return HttpResponse('OK')
