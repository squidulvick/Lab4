"""!
@file controller.py
This file contains the class implementation for controlling a plant based on a sensor.
The controller class implements a PID controller to control a sensor input based on a setpoint.
This file also creates a test file to run an Ametek Pittman Motor to a set position based on
an encoder input reading.

@author Jared Sinasohn, Sydney Ulvick, Sean Nakashimo
@date 22-Feb-2024
"""

import micropython
import pyb
import utime
from Lab3.encoder_reader import Encoder
from Lab3.motor_driver import MotorDriver

class CLController:
    """! 
    This class implements a closed loop controller based on an input sensor.  This class uses previously created . 
    """

    def __init__ (self, kp, ki, kd, setpoint):
        """! 
        Creates a motor driver by initializing GPIO
        pins and turning off the motor for safety. 
        @param sensor - the sensor the controller will be using and reading to calculate error
        @param kp - proportional controller constant
        @param ki - integral controller constant
        @param kd - derivative controller constant
        @param reference - the target postition for the controller to aim for
        """
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        # the effort the controller will send to the motor in percentage
        self.eff = 0
        # current value is the current reading of the sensor
        self.curr = 0
        # error is how far current value is from sensor
        self.err = self.setpoint - self.curr
        self.err_acc = 0
        self.prev_err_list = []
        self.deriv_amount = 10
        self.update_time = 10
        self.initial_time = utime.ticks_ms()
        self.curr_time = utime.ticks_diff(utime.ticks_ms(),self.initial_time)
    
    # why would this method accept the setpoint
    def run(self, measured):
        """!
        This method calculates the the effort to apply to an actuator based
        measured sensor value and a desired setpoint.  This method implements a
        PID Controller approach
        """
        self.curr = measured
        self.curr_time = utime.ticks_diff(utime.ticks_ms(),self.initial_time)
        self.err = self.setpoint - self.curr
        self.err_acc += self.err
        self.eff = self.kp*self.err + self.ki*self.err_acc
        if self.kd > 0:
            self.prev_err_list.append(self.err)
        if self.kd > 0 and len(self.prev_err_list) >= self.deriv_amount:
            err_slope = (self.prev_err_list[self.deriv_amount-1]-self.prev_err_list[0])/(self.deriv_amount*self.update_time)
            self.eff += self.kd*err_slope
            self.prev_err_list.pop(0)
        return self.eff

    def set_setpoint(self, setpoint):
        self.setpoint = setpoint
        
    def set_kp(self, kp):
        self.kp = kp
    
    def set_ki(self, ki):
        self.ki = self.ki
        
    def get_pos(self):
        return self.curr
    
    def get_curr_time(self):
        return self.curr_time
    
    def reset_controller(self):
        self.t_list = []
        self.pos_list = []
        self.err = 0
        self.eff = 0
        self.err_acc = 0
        self.curr = 0
        self.initial_time = utime.ticks_ms()
        self.curr_time = utime.ticks_ms()-self.initial_time
        
        
if __name__ == "__main__":
    # create pin to power motor
    en_pin =  pyb.Pin(pyb.Pin.board.PA10, mode = pyb.Pin.OPEN_DRAIN, pull = pyb.Pin.PULL_UP, value=1)
    
    # create first pwm pin
    in1pin = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
    
    # create first pwm pin
    in2pin = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
    
    # create timer for pwm
    timer = pyb.Timer(3, freq=25000) #setting frequency for motor
    
    # create motor object
    motor = MotorDriver(en_pin,in1pin,in2pin,timer) #call to the motor class you just made!

    # create the pin object to read encoder channel A
    pin1 = pyb.Pin(pyb.Pin.board.PC6, pyb.Pin.IN)
    
    # create the pin object to read encoder channel B
    pin2 = pyb.Pin(pyb.Pin.board.PC7, pyb.Pin.IN)
    
    # create the timer object.  For C6 and C7 use timer 8,
    # set the prescaler to zero and the period to the max 16bit number
    timer = pyb.Timer(8, prescaler = 0, period = 65535)
    
    # create the encoder object
    encoder = Encoder(pin1, pin2, timer)
    
    # create controller object
    con = CLController(1.63, 0, 0.3, 90)
    while True:
        try:
            encoder_reading = encoder.read()
            encoder_angle = encoder_reading/16/256/4*360
            eff = con.run(encoder_angle)
            motor.set_duty_cycle(eff)
        except KeyboardInterrupt:
            motor.set_duty_cycle(0)
            raise KeyboardInterrupt
        except ValueError:
            motor.set_duty_cycle(0)
            raise ValueError
        utime.sleep_ms(1)
