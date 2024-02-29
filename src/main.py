"""!
@file main.py
    This file modifies the basic_tasks.py file created by Dr. Ridgley and implements a co-tasking
    system to control the position of two motors at the same time.

@author JR Ridgely
@author Sydney Ulvick
@author Jared Sinasohn
@date   2021-Dec-15 JRR Created from the remains of previous example
@copyright (c) 2015-2021 by JR Ridgely and released under the GNU
    Public License, Version 2. 
"""
import utime
import gc
import pyb
import cotask
import task_share
from Lab4.encoder_reader import Encoder
from Lab4.motor_driver import MotorDriver
from Lab4.controller import CLController

def motor_fun_1():
    """!
    This function controls the first motor as part of the first task
    It runs the motor from 0 degrees to 180 degrees using a proportional controller
    """
    # motor setup
    en_pin =  pyb.Pin(pyb.Pin.board.PA10, mode = pyb.Pin.OPEN_DRAIN, pull = pyb.Pin.PULL_UP, value=1)
    in1pin = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
    in2pin = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
    timer = pyb.Timer(3, freq=20000) #setting frequency for motor 
    motor = MotorDriver(en_pin,in1pin,in2pin,timer) #create motor object
    # encoder setup
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
    con = CLController(1.5, 0, 0, angle1) 
 
    while True:
        encoder_reading = encoder.read() #read encoder
        encoder_angle = encoder_reading/16/256/4*360 #convert to ticks 
        eff = con.run(encoder_angle) 
        motor.set_duty_cycle(eff)
        if not pos1.full(): #if the position queue is not full
            pos1.put(con.get_pos()) #add position data to the queue
        if not time1.full():
            time1.put(con.get_curr_time())
        yield 0


def motor_fun_2():
    """!
    This function controls the second motor as part of the first task
    It runs the motor from 0 degrees to 180 degrees using a proportional controller
    """
    # motor setup
    en_pin =  pyb.Pin(pyb.Pin.board.PC1, mode = pyb.Pin.OPEN_DRAIN, pull = pyb.Pin.PULL_UP, value=1)
    in1pin = pyb.Pin(pyb.Pin.board.PA0, pyb.Pin.OUT_PP)
    in2pin = pyb.Pin(pyb.Pin.board.PA1, pyb.Pin.OUT_PP)
    timer = pyb.Timer(5, freq=20000) #setting frequency for motor 
    motor = MotorDriver(en_pin,in1pin,in2pin,timer) #create motor object
    # encoder setup
    # create the pin object to read encoder channel A
    pin1 = pyb.Pin(pyb.Pin.board.PB6, pyb.Pin.IN)
    # create the pin object to read encoder channel B
    pin2 = pyb.Pin(pyb.Pin.board.PB7, pyb.Pin.IN)
    # create the timer object.  For C6 and C7 use timer 8,
    # set the prescaler to zero and the period to the max 16bit number
    timer = pyb.Timer(4, prescaler = 0, period = 65535)
    # create the encoder object
    encoder = Encoder(pin1, pin2, timer)
    # create controller object
    con = CLController(1.5, 0, 0, angle2) 
 
    while True:
        encoder_reading = encoder.read()
        encoder_angle = encoder_reading/16/256/4*360
        eff = con.run(encoder_angle)
        motor.set_duty_cycle(eff)
        if not pos2.full():
            pos2.put(con.get_pos())
        if not time2.full():
            time2.put(con.get_curr_time())
        yield 0

def serial_communication():
    """!
    This function controls the serial communication between the microcontroller
    and the computer to plot responses if necessary.  It prints the list of values
    one value at a time.
    """
    while True:
        if not time1.full() or not pos1.full():
            yield 0
        else:
            while time1.any() and pos1.any():
                print(f"{time1.get()}, {pos1.get()}")
                yield 0
# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    print("Testing ME405 stuff in cotask.py and task_share.py\r\n"
          "Press Ctrl-C to stop and show diagnostics.")
    #set angle values (degrees) for motor 1 and motor 2, labeled accordingly
    angle1 = 180
    angle2 = 360
    #how long the queues will collect time and position data
    collection_time = 1.5 # in seconds
    #period for  motors, gotten from testing, max value which does not produce overshoot
    period_task = 20
    # Creating two queues to test function and diagnostic printouts
    time1 = task_share.Queue('I', int(1000/period_task*collection_time), thread_protect=False, overwrite=False,  #queue object
                          name="Time Queue")
    pos1 = task_share.Queue('d', int(1000/period_task*collection_time), thread_protect=False, overwrite=False,  #queue object
                          name="Position Queue")
    time2 = task_share.Queue('I', int(1000/period_task*collection_time), thread_protect=False, overwrite=False,  #queue object
                          name="Time Queue")
    pos2 = task_share.Queue('d', int(1000/period_task*collection_time), thread_protect=False, overwrite=False,  #queue object
                          name="Position Queue")
    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    
    task1 = cotask.Task(motor_fun_1, name="Task 1", priority=1,period=period_task,
                        profile=True, trace=False)
    task2 = cotask.Task(motor_fun_2, name="Task 2", priority=2,period=period_task,
                        profile=True, trace=False)
    task3 = cotask.Task(serial_communication, name="Task 3", priority=3,period=10,
                        profile=True, trace=False)
    
    # adding the tasks to task list, commenting out task3, used for acquiring data for plotting
    cotask.task_list.append(task1) #add tasks to scheduler list
    cotask.task_list.append(task2) #add tasks to scheduler list
    #cotask.task_list.append(task3)
    
    
    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect()
    # Run the scheduler with the chosen scheduling algorithm. Quit if ^C pressed
    while True:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            break

    # Print a table of task data and a table of shared information data
    print('\n' + str (cotask.task_list))
    print(task_share.show_all())
    print(task1.get_trace())
    print('')
