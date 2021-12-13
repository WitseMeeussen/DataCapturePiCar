from picar import back_wheels, front_wheels
import picar
import cv2
import os
from keyboard import is_pressed
from datetime import datetime
from keyboard import on_press_key, read_key,is_pressed, wait



folder = '/home/pi/DataCapturePiCar/Data/' + 'test1'
if not os.path.isdir(folder):
	os.mkdir(folder)
	print('made dir')

count = 0
dir = 0
speed = 0

def captureData():
	global count,dir,speed
	# if(ControlerData['drive']==0):
	# 	return

	camera = cv2.VideoCapture(-1)
	camera.set(3, 640)
	camera.set(4, 480)


	
	_, image = camera.read()    
	print(folder+"/test%s.png" %(count))
	print(cv2.imwrite(folder+"/test%s.png" %(count), image))
	#cv2.imwrite(folder+"/%s_%03d_%03d.png" % ( count, ControlerData['speed'], ControlerData['direction']), image)
	count += 1
    


picar.setup()
db_file = "/home/pi/SunFounder_PiCar-V/remote_control/remote_control/driver/config"
fw = front_wheels.Front_Wheels(debug=False, db=db_file)
bw = back_wheels.Back_Wheels(debug=False, db=db_file)
#cam = camera.Camera(debug=False, db=db_file)
#cam.ready()
bw.ready()
fw.ready()
 
SPEED = 60
bw_status = 0




while True:
    if is_pressed("up"):
        speed = 1
        bw.forward()
    elif is_pressed("down"):
        speed = -1
        bw.backward()
    else:
        speed = 0
        bw.stop()
    if is_pressed("left") and is_pressed("right"):
        dir = 0
        fw.turn_straight()
    elif is_pressed("right"):
        dir = 1
        fw.turn_right()
    elif is_pressed("left"):
        dir = -1
        fw.turn_left()
    else:
        dir = 0
        fw.turn_straight()
    print("speed:"+ str(speed) + "|dir:"+str(dir))
    

print(stream.start())

def home(request):
	return render_to_response("base.html")

def runOld(request):
	### this contains al the controller input
	global ControlerData
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
		
		
		# # ================ Camera =================
		# elif action == 'camready':
		# 	cam.ready()
		# elif action == "camleft":
		# 	cam.turn_left(40)
		# elif action == 'camright':
		# 	cam.turn_right(40)
		# elif action == 'camup':
		# 	cam.turn_up(20)
		# elif action == 'camdown':
		# 	cam.turn_down(20)	
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
	# # streaming
	#host = stream.get_host().decode('utf-8').split(' ')[0]
	
	return render_to_response("run.html")

def cali(request):
	if 'action' in request.GET:
		action = request.GET['action']
		# # ========== Camera calibration =========
		# if action == 'camcali':
		# 	print('"%s" command received' % action)
		# 	cam.calibration()
		# elif action == 'camcaliup':
		# 	print('"%s" command received' % action)
		# 	cam.cali_up()
		# elif action == 'camcalidown':
		# 	print('"%s" command received' % action)
		# 	cam.cali_down()
		# elif action == 'camcalileft':
		# 	print('"%s" command received' % action)
		# 	cam.cali_left()
		# elif action == 'camcaliright':
		# 	print('"%s" command received' % action)
		# 	cam.cali_right()
		# elif action == 'camcaliok':
		# 	print('"%s" command received' % action)
		# 	cam.cali_ok()

		# ========= Front wheel cali ===========
		if action == 'fwcali':
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