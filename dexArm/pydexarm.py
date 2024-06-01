import serial
import re
import math #needed for fuzzy feet

class Dexarm:
    """ Python class for Dexarm
    """
      # Constants for fuzzy feet placement
    SPEED_ROBOT = 6000
    SPEED2_ROBOT = 100
    PICK_X = -50
    PICK_Y = 229
    PICK_Z = -88
    OFFSET_Z = 8
    OFFSET_2 = 1
    FOOT_SPACING_X = 24.5
    FOOT_SPACING_Y = 23.66
    PLACEMENT_RADIUS = 70 / math.sqrt(3)  # Calculation as a class attribute
    TRIANGLE_ANGLE = math.radians(120)
    COASTER_X = -217
    COASTER_Y = 171
    HOVER_Z = -84
    PLACEMENT_OFFSET_Z = 6


    def __init__(self, port):
        """
        Args:
            port (string): the serial port of Dexarm, e.g, "COM3"
        """
        self.ser = serial.Serial(port, 115200, timeout=None)
        self.is_open = self.ser.isOpen()
        if self.is_open:
            print('pydexarm: %s open' % self.ser.name)
        else:
            print('failed to open serial port')

    def _send_cmd(self, data, wait=True):
        """
        Send command to the arm.

        Args:
            data (string): the command
            wait (bool): wait for response from the arm (ok) or not.
                If True, this function will block until the arm response "ok"
                If False, this function will not block here. But the command could be ignored if buffer of the arm is full.
        """
        self.ser.write(data.encode())
        if not wait:
            self.ser.reset_input_buffer()
            return
        while True:
            serial_str = self.ser.readline().decode("utf-8")
            if len(serial_str) > 0:
                if serial_str.find("ok") > -1:
                    print("read ok")
                    break
                else:
                    print("read：", serial_str)

    def go_home(self):
        """
        Go to home position and enable the motors. Should be called each time when power on.
        """
        self._send_cmd("M1112\r")

    def set_workorigin(self):
        """
        Set the current position as the new work origin.
        """
        self._send_cmd("G92 X0 Y0 Z0 E0\r")

    def set_acceleration(self, acceleration, travel_acceleration, retract_acceleration=60):
        """
        Set the preferred starting acceleration for moves of different types.

        Args:
            acceleration (int): printing acceleration. Used for moves that employ the current tool.
            travel_acceleration (int): used for moves that include no extrusion.
            retract_acceleration (int): used for extruder retraction moves.
        """
        cmd = "M204"+"P" + str(acceleration) + "T"+str(travel_acceleration) + "T" + str(retract_acceleration) + "\r\n"
        self._send_cmd(cmd)

    def set_module_type(self, module_type):
        """
        Set the type of end effector.

        Args:
            module_type (int):
                0 for Pen holder module
                1 for Laser engraving module
                2 for Pneumatic module
                3 for 3D printing module
        """
        self._send_cmd("M888 P" + str(module_type) + "\r")

    def get_module_type(self):
        """
        Get the type of end effector.

        Returns:
            string that indicates the type of the module
        """
        self.ser.reset_input_buffer()
        self.ser.write('M888\r'.encode())
        while True:
            serial_str = self.ser.readline().decode("utf-8")
            if len(serial_str) > 0:
                if serial_str.find("PEN") > -1:
                    module_type = 'PEN'
                if serial_str.find("LASER") > -1:
                    module_type = 'LASER'
                if serial_str.find("PUMP") > -1:
                    module_type = 'PUMP'
                if serial_str.find("3D") > -1:
                    module_type = '3D'
            if len(serial_str) > 0:
                if serial_str.find("ok") > -1:
                    return module_type

    def move_to(self, x=None, y=None, z=None, e=None, feedrate=2000, mode="G1", wait=True):
        """
        Move to a cartesian position. This will add a linear move to the queue to be performed after all previous moves are completed.

        Args:
            mode (string, G0 or G1): G1 by default. use G0 for fast mode
            x, y, z (int): The position, in millimeters by default. Units may be set to inches by G20. Note that the center of y axis is 300mm.
            feedrate (int): set the feedrate for all subsequent moves
        """
        cmd = mode + "F" + str(feedrate)
        if x is not None:
            cmd = cmd + "X"+str(round(x))
        if y is not None:
            cmd = cmd + "Y" + str(round(y))
        if z is not None:
            cmd = cmd + "Z" + str(round(z))
        if e is not None:
            cmd = cmd + "E" + str(round(e))
        cmd = cmd + "\r\n"
        self._send_cmd(cmd, wait=wait)

    def fast_move_to(self, x=None, y=None, z=None, feedrate=2000, wait=True):
        """
        Fast move to a cartesian position, i.e., in mode G0

        Args:
            x, y, z (int): the position, in millimeters by default. Units may be set to inches by G20. Note that the center of y axis is 300mm.
            feedrate (int): sets the feedrate for all subsequent moves
        """
        move_to(self, x=x, y=y, z=z, feedrate=feedrate, mode="G0", wait=wait)

    def get_current_position(self):
        """
        Get the current position
        
        Returns:
            position x,y,z, extrusion e, and dexarm theta a,b,c
        """
        self.ser.reset_input_buffer()
        self.ser.write('M114\r'.encode())
        x, y, z, e, a, b, c = None, None, None, None, None, None, None
        while True:
            serial_str = self.ser.readline().decode("utf-8")
            if len(serial_str) > 0:
                if serial_str.find("X:") > -1:
                    temp = re.findall(r"[-+]?\d*\.\d+|\d+", serial_str)
                    x = float(temp[0])
                    y = float(temp[1])
                    z = float(temp[2])
                    e = float(temp[3])
            if len(serial_str) > 0:
                if serial_str.find("DEXARM Theta") > -1:
                    temp = re.findall(r"[-+]?\d*\.\d+|\d+", serial_str)
                    a = float(temp[0])
                    b = float(temp[1])
                    c = float(temp[2])
            if len(serial_str) > 0:
                if serial_str.find("ok") > -1:
                    return x, y, z, e, a, b, c

    def dealy_ms(self, value):
        """
        Pauses the command queue and waits for a period of time in ms

        Args:
            value (int): time in ms
        """
        self._send_cmd("G4 P" + str(value) + '\r')

    def dealy_s(self, value):
        """
        Pauses the command queue and waits for a period of time in s

        Args:
            value (int): time in s
        """
        self._send_cmd("G4 S" + str(value) + '\r')

    def soft_gripper_pick(self):
        """
        Close the soft gripper
        """
        self._send_cmd("M1001\r")

    def soft_gripper_place(self):
        """
        Wide-open the soft gripper
        """
        self._send_cmd("M1000\r")

    def soft_gripper_nature(self):
        """
        Release the soft gripper to nature state
        """
        self._send_cmd("M1002\r")

    def soft_gripper_stop(self):
        """
        Stop the soft gripper
        """
        self._send_cmd("M1003\r")

    def air_picker_pick(self):
        """
        Pickup an object
        """
        self._send_cmd("M1000\r")

    def air_picker_place(self):
        """
        Release an object
        """
        self._send_cmd("M1001\r")

    def air_picker_nature(self):
        """
        Release to nature state
        """
        self._send_cmd("M1002\r")

    def air_picker_stop(self):
        """
        Stop the picker
        """
        self._send_cmd("M1003\r")

    def laser_on(self, value=0):
        """
        Turn on the laser

        Args:
            value (int): set the power, range form 1 to 255
        """
        self._send_cmd("M3 S" + str(value) + '\r')

    def laser_off(self):
        """
        Turn off the laser
        """
        self._send_cmd("M5\r")

    """Conveyor Belt"""
    def conveyor_belt_forward(self, speed=0):
        """
        Move the belt forward
        """
        self._send_cmd("M2012 F" + str(speed) + 'D0\r')

    def conveyor_belt_backward(self, speed=0):
        """
        Move the belt backward
        """
        self._send_cmd("M2012 F" + str(speed) + 'D1\r')

    def conveyor_belt_stop(self, speed=0):
        """
        Stop the belt
        """
        self._send_cmd("M2013\r")

    """Sliding Rail"""
    def sliding_rail_init(self):
        """
        Sliding rail init.
        """
        self._send_cmd("M2005\r")

    def close(self):
        """
        Release the serial port.
        """
        self.ser.close()
    

    ## Fuzzy feet stuff is under here. Also, NOTE: None of this actualyl works. You can probably remove this, but as of writing we have like a week left and I don't want to break anything uncessarily. -Alex
    def pick_fuzzy_foot(self, index_x, index_y):
        """ Picks a fuzzy foot based on provided grid coordinates. """
        target_x = self.PICK_X + (index_x - 1) * self.FOOT_SPACING_X
        target_y = self.PICK_Y + (index_y - 1) * self.FOOT_SPACING_Y
        self.go_home()  # Ensure the arm starts from a known position

        self.move_to(target_x, target_y, 0, self.SPEED_ROBOT)
        self.move_to(target_x, target_y, self.PICK_Z, self.SPEED_ROBOT)
        self.move_to(target_x, target_y, self.PICK_Z - self.OFFSET_Z, self.SPEED2_ROBOT)
        self.move_to(target_x, target_y + self.OFFSET_2, self.PICK_Z - self.OFFSET_Z, self.SPEED2_ROBOT / 2)
        self.move_to(target_x, target_y + self.OFFSET_2, self.PICK_Z, self.SPEED2_ROBOT)
        self.move_to(target_x, target_y + self.OFFSET_2, 0, self.SPEED_ROBOT)
        print(f"Attempted pick at [{index_x}, {index_y}]")

    def calculate_triangle_positions(self):
        """ Calculates the positions for placing fuzzy feet in a triangle pattern. """
        positions = []
        for i in range(3):
            angle = self.TRIANGLE_ANGLE * i - math.pi / 2
            x = self.COASTER_X + self.PLACEMENT_RADIUS * math.cos(angle)
            y = self.COASTER_Y + self.PLACEMENT_RADIUS * math.sin(angle)
            positions.append((x, y))
        return positions

    def placeFuzzyFeet(self, pick_indices, num_to_place):
        """ Places fuzzy feet in specified positions on a coaster. """
        if not 1 <= num_to_place <= 3:
            print("Invalid number of feet to place. Please choose between 1 and 3.")
            return

        positions = self.calculate_triangle_positions()
        for i in range(num_to_place):
            idx_x, idx_y = pick_indices[i]
            self.pick_fuzzy_foot(idx_x, idx_y)
            placement_x, placement_y = positions[i]
            self.move_to(placement_x, placement_y, 0, self.SPEED_ROBOT)
            self.move_to(placement_x, placement_y, self.HOVER_Z, self.SPEED_ROBOT)
            self.move_to(placement_x, placement_y, self.HOVER_Z - self.PLACEMENT_OFFSET_Z, self.SPEED2_ROBOT * 2)
            self.move_to(placement_x, placement_y, self.HOVER_Z + self.PLACEMENT_OFFSET_Z, self.SPEED2_ROBOT * 2)
            self.move_to(placement_x, placement_y, 0, self.SPEED_ROBOT)
            print(f"Placed fuzzy foot {i + 1} at [{placement_x}, {placement_y}]")




