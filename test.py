from keyboard import on_press_key, read_key,is_pressed, wait

dir = 0
speed = 0

while True:
    if is_pressed("up"):
        speed =1
    elif is_pressed("down"):
        speed = -1
    else:
        speed = 0
    if is_pressed("left") and is_pressed("right"):
        dir = 0
    elif is_pressed("right"):
        dir = 1
    elif is_pressed("left"):
        dir = -1
    else:
        dir = 0
    print("speed:"+ str(speed) + "|dir:"+str(dir))
