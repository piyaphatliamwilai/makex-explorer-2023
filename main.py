import event, time, gamepad, cyberpi, mbot2, math, mbuild # fuck off
auto = False
@event.start
def on_start():
    """Bot startup.
    """
    extra_battery = cyberpi.get_extra_battery()
    if extra_battery < 20:
        cyberpi.audio.play('low-energy')
    while True:
        if gamepad.is_key_pressed('L1') and gamepad.is_key_pressed('R1') and gamepad.is_key_pressed('N3'):
            cyberpi.stop_all()
        control_centre()

@event.is_press('a')
def is_btn_press():
    automatic_stage_left()

@event.is_press('b')
def is_b_press():
    automatic_stage_right()

@event.is_press('middle')
def is_joy_press():
    emergency_auto()

def control_centre():
    """Control whether the bot is moving, shooting etc.
    """
    if math.fabs(gamepad.get_joystick('Lx')) > 50 or math.fabs(gamepad.get_joystick('Ly')) > 50 or math.fabs(gamepad.get_joystick('Rx')) > 50 or math.fabs(gamepad.get_joystick('Ry')) > 50:
        control_moving()
    else:
        stop_moving()
    if gamepad.is_key_pressed('R1'):
        shooter.shoot()
    if gamepad.is_key_pressed('L1'):
        gripper.gripper()
        time.sleep(0.2)
    if gamepad.is_key_pressed('L2'):
        util.set_gripper_angle(45)        
    if gamepad.is_key_pressed('Start'):
        mbot2.servo_set(0, "S1")
    if gamepad.is_key_pressed('N1'):
        gripper.stage(2)
    if gamepad.is_key_pressed('N2'):
        gripper.stage(1)
    if gamepad.is_key_pressed('N3'):  
        shooter.load()
    if gamepad.is_key_pressed('N4'):
        gripper.stage(3)
    if gamepad.is_key_pressed('Up'):
        audio.record()
    if gamepad.is_key_pressed('Down'):
        audio.stop_record()
    if gamepad.is_key_pressed('Left'):
        auto_stage.left()
    if gamepad.is_key_pressed('Right'):
        auto_stage.right()
    if gamepad.is_key_pressed('Select'):
        audio.set_speed(100)
        audio.set_volume(100)
        audio.play_record()

def stop_moving():
    """Stop the robot movement.
    """
    global auto
    if not auto:
       omniwheel.stop()

def control_moving ():
    """Control the bot movement.
    """
    speed = 190
    if gamepad.is_key_pressed('R2'):
        speed = 100
    if gamepad.get_joystick('Ly') > 50:
        omniwheel.forward(speed)
        print("Forward")
    elif gamepad.get_joystick('Ly') < -50:
        omniwheel.backward(speed)
        print("Backward")
    if gamepad.get_joystick('Rx') > 50:
        omniwheel.turn_right(speed)
        print("Turning Right")
    elif gamepad.get_joystick('Rx') < -50:
        omniwheel.turn_left(speed)
        print("Turning Left")  

def emergency_auto ():
    global auto
    auto = True
    mbot2.drive_power(100, 105)
    omniwheel.stop()
    shooter.load()
    gripper.stage(2)
    gripper.grip()
    auto = False

def automatic_stage_left ():
    global auto
    auto = True
    auto_stage.left()
    auto = False
    
def automatic_stage_right ():
    global auto
    auto = True
    auto_stage.right()
    auto = False

class util:
    def rotate_into_angle(speed: int, angle: int, port: str):
        mbot2.EM_turn(angle, speed, port)
        
    def set_gripper_angle(degree: int):
        mbot2.servo_set(degree, "S4")

"""
Deprecated do not use.
"""   
class movement_control:
    
    def stop():
        mbot2.EM_set_speed(0, "all")
    
    def forward(speed: int):
        mbot2.forward(speed) # Inverted EM, therefore.
    
    def backward(speed: int):
        mbot2.backward(speed) # Inverted EM, therefore.
    
    def turn_left(speed: int):
        mbot2.turn_left(speed)
    
    def turn_right(speed: int):
        mbot2.turn_right(speed)
        
class omniwheel:
    
    def stop():
        mbot2.EM_set_speed(0, "EM1")
        mbot2.EM_set_speed(0, "EM2")
        mbot2.motor_set(0, "M2")
    
    def forward(speed: int):
        mbot2.drive_power(speed, -(speed-5))
        
    def backward(speed: int):
        mbot2.drive_power(-speed, (speed - 5))
    
    def turn_left(speed: int):
        mbot2.turn_left(speed)
    
    def turn_right(speed: int):
        mbot2.turn_right(speed)
    
class audio:
    
    def record():
        cyberpi.audio.record()
        
    def stop_record():
        cyberpi.audio.stop_record()
        
    def play_record():
        cyberpi.audio.play_record()
        
    def set_speed(speed: int):
        cyberpi.audio.set_tempo(speed)
        
    def set_volume(vol: int):
        cyberpi.audio.set_vol(vol)
    
class shooter:
    def shoot():
        """Shoot.
        """
        mbot2.servo_set(165,"S1") # Shoot
        time.sleep(0.5)
        mbot2.servo_set(0,"S1") # Set the angle back to 0
        time.sleep(0.5)
        shooter.load() # Reload again.
        
    def load():
        mbot2.servo_set(125,"S1")
        
class gripper:
    def grip(auto: bool = False):
        if auto:
            time.sleep(0.2)
        mbot2.servo_set(55, "S2")
        mbot2.servo_set(55, "S3")
        
    def release(auto: bool = False):
        if auto:
            time.sleep(0.2)
        mbot2.servo_set(110, "S2")
        mbot2.servo_set(110, "S3")
        
    def gripper():
        angle = mbot2.servo_get("S2")
        check = False
        if angle > 50 and angle < 60 and check == False:
            gripper.release()
            check = True
            print("change to 55 ong sar")
            return check
        else:
            if angle > 100 and angle < 120 and check == False:
                gripper.grip()
                print("change to 110 ong sar")
                check = True
                return check
            else:
                gripper.release()
                check = True
                return check
            
    def stage(stage: int):
        if stage == 1:
            util.set_gripper_angle(0) # Stage 1
        if stage == 2:
            util.set_gripper_angle(80) # Stage 2
        if stage == 3:
            util.set_gripper_angle(180) # Stage 3

class rotater:
    def rotate_left_90():
        omniwheel.turn_left(100)
        time.sleep(0.6)
        omniwheel.stop()
    def rotate_right_90():
        omniwheel.turn_right(100)
        time.sleep(0.6)
        omniwheel.stop()
    
class lineFollower:
    """
    Honestly, this is just legit witchcraft.
    """
    def line_follow(kp: int = 2.5, basePower: int = 40):
        left_power = (basePower - kp * mbuild.quad_rgb_sensor.get_offset_track(1))
        right_power = -1 * ((basePower + kp * mbuild.quad_rgb_sensor.get_offset_track(1)))
        mbot2.drive_power(left_power, right_power)

class auto_stage:
    def right():
        gripper.release(True)
        omniwheel.forward(50)
        time.sleep(1)
        omniwheel.stop()
        time.sleep(0.2)
        while not mbuild.quad_rgb_sensor.get_ground_sta("all", 1) == 1:
            lineFollower.line_follow()            
        omniwheel.stop()
        time.sleep(0.5)
        while not mbuild.quad_rgb_sensor.get_ground_sta("all", 1) == 0:
            lineFollower.line_follow()
        omniwheel.stop()
        time.sleep(0.5)
        mbot2.straight(15)
        gripper.stage(1)
        gripper.release(True) # grip block
        mbot2.straight(-15)
        gripper.stage(2)
        time.sleep(0.2)
        omniwheel.turn_left(100)
        time.sleep(0.3)
        omniwheel.stop()
        mbot2.straight(20)
        gripper.stage(1)
        gripper.grip(True) # release block
        mbot2.straight(-20)
        omniwheel.turn_right(100)  
        time.sleep(0.3)
        omniwheel.stop()
        mbot2.straight(30)
        gripper.release(True) # grip ball
        mbot2.straight(-30)
        rotater.rotate_right_90()
        time.sleep(0.2)
        gripper.stage(3)
        gripper.grip(True) # release ball
        gripper.stage(2)
    def left():
        mbot2.straight(80)
        time.sleep(0.5)
        while not mbuild.quad_rgb_sensor.get_ground_sta("all", 1) == 9:
            omniwheel.turn_right(30)
        omniwheel.stop()
        while not mbuild.quad_rgb_sensor.get_ground_sta("all", 1) == 0:
            lineFollower.line_follow()
        omniwheel.stop()
        time.sleep(0.5)
        mbot2.straight(15)
        gripper.stage(1)
        gripper.release(True)
        mbot2.straight(-15)
        gripper.stage(2)
        time.sleep(0.2)
        omniwheel.turn_right(100)
        time.sleep(0.3)
        omniwheel.stop()
        mbot2.straight(50)
        gripper.stage(1)
        gripper.grip(True)
        mbot2.straight(-50)
        omniwheel.turn_left(100)  
        time.sleep(0.3)
        omniwheel.stop()
        mbot2.straight(30)
        gripper.release(True)
        mbot2.straight(-30)
        rotater.rotate_left_90()
        gripper.stage(2)
