
from picar import back_wheels, front_wheels
import picar
import cv2
import os
from keyboard import is_pressed
from datetime import datetime
from keyboard import on_press_key, read_key,is_pressed, wait


folderNr = len(os.listdir('/home/pi/DataCapturePiCar/Data/'))+1
folder = '/home/pi/DataCapturePiCar/Data/' + 'capture' + str(folderNr)
if not os.path.isdir(folder):
	os.mkdir(folder)
	print('made dir')

count = 0
dir = 0
changedDir = False
speed = 0
camera = cv2.VideoCapture(-1)
camera.set(3, 640)
camera.set(4, 480)

waitCount =0

def captureData():
	global count,dir,speed
    
	_, image = camera.read()    
	print(cv2.imwrite(folder+"/nr%s_%s_dir_%s.png" %(folderNr,count,dir), image))
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
bw.speed = 60
 
SPEED = 60
bw_status = 0

def  cangeDir(x):
    global dir, changedDir
    if(dir == x):
        changedDir = False
    else:
        changedDir = True
    dir = x


while True:
    if is_pressed("up"):
        speed = 1
        bw.forward()
        bw.speed = SPEED
    elif is_pressed("down"):
        speed = -1
        bw.backward()
        bw.speed = SPEED/2
    else:
        speed = 0
        bw.stop()
        bw.speed = 0
    if is_pressed("left") and is_pressed("right"):
        cangeDir(0)
        fw.turn_straight()
    elif is_pressed("right"):
        cangeDir(1)
        fw.turn_right()
    elif is_pressed("left"):
        cangeDir(-1)
        fw.turn_left()
    else:
        cangeDir(0)
        fw.turn_straight()
    if is_pressed("esc") or is_pressed("q"):
        break 
    print("speed:"+ str(speed) + "|dir:"+str(dir))
    if (waitCount >4 or changedDir) and speed == 1:
        waitCount = 0
        captureData()
    else:
        waitCount +=1
