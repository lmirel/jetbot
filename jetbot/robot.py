import time
import traitlets
from traitlets.config.configurable import SingletonConfigurable
#from Adafruit_MotorHAT import Adafruit_MotorHAT
from .motor import Motor

#--
class P_DCMotor:
    def __init__(self, controller, num):
        self.MC = controller
        self.motornum = num
        pwm = in1 = in2 = 0

        if (num == 0):
                 pwm = 8
                 in2 = 9
                 in1 = 10
        elif (num == 1):
                 pwm = 13
                 in2 = 12
                 in1 = 11
        elif (num == 2):
                 pwm = 2
                 in2 = 3
                 in1 = 4
        elif (num == 3):
                 pwm = 7
                 in2 = 6
                 in1 = 5
        else:
            raise NameError('MotorHAT Motor must be between 1 and 4 inclusive')
        self.PWMpin = pwm
        self.IN1pin = in1
        self.IN2pin = in2

    def run(self, command):
        if not self.MC:
            return
        if (command == P_MotorHAT.FORWARD):
            self.MC.setPin(self.IN2pin, 0)
            self.MC.setPin(self.IN1pin, 1)
        if (command == P_MotorHAT.BACKWARD):
            self.MC.setPin(self.IN1pin, 0)
            self.MC.setPin(self.IN2pin, 1)
        if (command == P_MotorHAT.RELEASE):
            self.MC.setPin(self.IN1pin, 0)
            self.MC.setPin(self.IN2pin, 0)
    def setSpeed(self, speed):
        if (speed < 0):
            speed = 0
        if (speed > 255):
            speed = 255
        #extras
        self.MC.setPWM(self.PWMpin, 0, speed*16)
#--HAT
class P_MotorHAT:
    FORWARD = 1
    BACKWARD = 2
    BRAKE = 3
    RELEASE = 4

    SINGLE = 1
    DOUBLE = 2
    INTERLEAVE = 3
    MICROSTEP = 4

    def __init__(self, addr = 0x60, freq = 1600, i2c=None, i2c_bus=None):
        #self._frequency = freq
        self.motors = [ P_DCMotor(self, m) for m in range(4) ]
        #self.steppers = [ Adafruit_StepperMotor(self, 1), Adafruit_StepperMotor(self, 2) ]
        #self._pwm = PWM(addr, debug=False, i2c=i2c, i2c_bus=i2c_bus)
        #self._pwm.setPWMFreq(self._frequency)

    def setPin(self, pin, value):
        if (pin < 0) or (pin > 15):
            raise NameError('PWM pin must be between 0 and 15 inclusive')
        if (value != 0) and (value != 1):
            raise NameError('Pin value must be 0 or 1!')
        if (value == 0):
          print("#w:setPin pin {} val {}".format(pin, value))
            #self._pwm.setPWM(pin, 0, 4096)
        if (value == 1):
          print("#w:setPin pin {} val {}".format(pin, value))
            #self._pwm.setPWM(pin, 4096, 0)

    def getMotor(self, num):
        if (num < 1) or (num > 4):
            raise NameError('MotorHAT Motor must be between 1 and 4 inclusive')
        return self.motors[num-1]
    def setPWM(self, channel, on, off):
        "Sets a single PWM channel"
        print("#w:setPWM chn {} on {} off {}".format(channel, on, off))
#--Robot
class Robot(SingletonConfigurable):
    
    left_motor = traitlets.Instance(Motor)
    right_motor = traitlets.Instance(Motor)

    # config
    i2c_bus = traitlets.Integer(default_value=1).tag(config=True)
    left_motor_channel = traitlets.Integer(default_value=1).tag(config=True)
    left_motor_alpha = traitlets.Float(default_value=1.0).tag(config=True)
    right_motor_channel = traitlets.Integer(default_value=2).tag(config=True)
    right_motor_alpha = traitlets.Float(default_value=1.0).tag(config=True)
    
    def __init__(self, *args, **kwargs):
        super(Robot, self).__init__(*args, **kwargs)
        self.motor_driver = P_MotorHAT (i2c_bus=self.i2c_bus)
        self.left_motor = Motor(self.motor_driver, channel=self.left_motor_channel, alpha=self.left_motor_alpha)
        self.right_motor = Motor(self.motor_driver, channel=self.right_motor_channel, alpha=self.right_motor_alpha)
        
    def set_motors(self, left_speed, right_speed):
        self.left_motor.value = left_speed
        self.right_motor.value = right_speed
        
    def forward(self, speed=1.0, duration=None):
        self.left_motor.value = speed
        self.right_motor.value = speed

    def backward(self, speed=1.0):
        self.left_motor.value = -speed
        self.right_motor.value = -speed

    def left(self, speed=1.0):
        self.left_motor.value = -speed
        self.right_motor.value = speed

    def right(self, speed=1.0):
        self.left_motor.value = speed
        self.right_motor.value = -speed

    def stop(self):
        self.left_motor.value = 0
        self.right_motor.value = 0