from os import remove
from picar import back_wheels, front_wheels
import picar
import cv2
import numpy as np
import tflite_runtime.interpreter as tflite

camera = cv2.VideoCapture(-1)
camera.set(3, 640)
camera.set(4, 480)

picar.setup()
db_file = "/home/pi/SunFounder_PiCar-V/remote_control/remote_control/driver/config"
fw = front_wheels.Front_Wheels(debug=False, db=db_file)
bw = back_wheels.Back_Wheels(debug=False, db=db_file)
bw.ready()
fw.ready()
bw.speed = 30
 
SPEED = 30

def img_preprocess(image):
    height, _, _ = image.shape
    image = image[int(height/2):,:,:]  # remove top half of the image, as it is not relevant for lane following
    #image = cv2.cvtColor(image, cv2.COLOR_RGB2YUV)  # Nvidia model said it is best to use YUV color space
    image = cv2.GaussianBlur(image, (3,3), 0)
    image = cv2.resize(image, (200,66)) # input image size (200,66) Nvidia model
    image = image / 255 # normalizing the values of the image. We dont need to normalize it in the model anny more
    return image


# loading the model
interpreter = tflite.Interpreter(model_path='model.tflite')

interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
print(input_details)
output_details = interpreter.get_output_details()


def compute_steering_angle(image):
    image = img_preprocess(image)
    input_data = np.array(image,dtype=np.float32)

    interpreter.set_tensor(input_details[0]['index'], input_data[np.newaxis,:,:,:])

    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]['index'])
    return output_data[0]





while True:
    bw.forward()
    bw.speed = SPEED
    _, image = camera.read()
    cv2.imwrite('image.png',image)
    savedImage = cv2.imread('image.png')
    image = img_preprocess(savedImage)
    steeringangle =compute_steering_angle(image)
    print(steeringangle)
    if steeringangle<60:
        fw.turn_left()
        print("left")
    elif steeringangle > 120:
        fw.turn_right()
        print("right")
    else:
        fw.turn_straight()
        print("straight")

    

