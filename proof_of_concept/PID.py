import math as math

class PID:
    def __init__(self):
        """
        @brief PID controller for robot movement.
        """
        self.p_value = 0.0
        self.d_value = 0.0
        self.i_value = 0.0
        self.cross_track_error = 0.0
        self.previous_cross_track_error = 0.0

    def correct_heading(self):
        """
        @brief Function to correct the heading of the robot.
        @return Returns the change in heading necessary to correct the robot for this iteration.
        """
        self.p_value = self.cross_track_error
        self.d_value = (self.cross_track_error - self.previous_cross_track_error) / (1)
        self.i_value += self.cross_track_error * (1)

        proportion_coeff = 0.005
        derivate_coeff = 0.010
        integral_coeff = 0.000

        correction = (proportion_coeff * self.p_value) + (derivate_coeff * self.d_value) +\
                     (integral_coeff * self.i_value)
        self.previous_cross_track_error = self.cross_track_error
        return correction
    


    def calculateCrossTrackError(self, coord0: tuple, coord1: tuple, angle: float):
        """
        @brief    Calculates and stores the cross track error every time it is called
        @param coord0    A tuple containing the start coordinate of the path
        @param coord1    A tuple containing the current position of the robot
        @param angle    The heading of the robot at the start of the path (in degrees)
        """
        # print((abs(coord1[0] - coord0[0]) -\
        #                         (math.sqrt((coord1[0] -\
        #                         coord0[0])**2 + (coord1[1] -\
        #                         coord0[1])**2))*math.cos(math.radians(angle)))**2)
        self.cross_track_error = math.sqrt((abs(coord1[0] - coord0[0]) -\
                                (math.sqrt((coord1[0] -\
                                coord0[0])**2 + (coord1[1] -\
                                coord0[1])**2))*math.cos(math.radians(angle)))**2 +\
                                (abs(coord1[1] - coord0[1]) -\
                                (math.sqrt((coord1[0] -\
                                coord0[0])**2 + (coord1[1] -\
                                coord0[1])**2))*math.sin(math.radians(angle)))**2)
        if coord1[0] < 400: self.cross_track_error = -self.cross_track_error
        if abs(self.cross_track_error) < 1e-4:
            self.cross_track_error = 0.0
