import math


class DistanceLookup:
    HEIGHT_START = "height_start"
    HEIGHT_END = "height_end"
    WIDTH_START_AREA = "width_start_area"
    LENGTH_START_AREA = "length_start_area"
    START_TO_CENTER_ROLL = "start_to_center_roll"
    START_TO_CUBE = "start_to_cube"
    START_HEIGHT_ABOVE_GROUND = "start_height_above_ground"
    START_HEIGHT_CUBE = "start_height_cube"
    HEIGHT_WITH_CUBE_ABOVE_GROUND = "height_with_cube_above_ground"
    LENGTH_START_TO_TARGET_RANGE = "length_start_to_target_range"
    LENGTH_TARGET_RANGE = "length_target_range"
    LENGTH_TARGET_RANGE_TO_END = "length_target_range_to_end"
    WIDTH_TARGET_RANGE = "width_target_range"
    LENGTH_TARGET_AREA = "length_target_area"
    WIDTH_TARGET_AREA = "width_target_area"
    HEIGHT_TARGET_AREA = "height_target_area"
    LENGTH_TOTAL_W_MAST = "length_total_w_mast"
    LENGTH_TOTAL_WO_MAST = "length_total_wo_mast"
    HEIGHT_OBSTACLES = "height_obstacles"
    ANGLE_PITCH_DEGREES = "angle_pitch_degrees"
    CENTER_ROLL_TO_CAMERA = "center_roll_to_camera"
    CUBE_START_X = "cube_start_x"
    CUBE_START_Z = "cube_start_z"
    THRESHOLD_SLOW_END = "threshold_slow_end"

    # [mm]
    DISTANCE_MAP = {
        HEIGHT_START: 600,
        HEIGHT_END: 1100,
        WIDTH_START_AREA: 500,
        LENGTH_START_AREA: 500,
        START_TO_CENTER_ROLL: 195,
        START_TO_CUBE: 465,
        START_HEIGHT_ABOVE_GROUND: 210,
        START_HEIGHT_CUBE: 190,
        HEIGHT_WITH_CUBE_ABOVE_GROUND: 255,
        LENGTH_START_TO_TARGET_RANGE: 800,
        LENGTH_TARGET_RANGE: 2400,
        LENGTH_TARGET_RANGE_TO_END: 200,
        WIDTH_TARGET_RANGE: 20,
        LENGTH_TARGET_AREA: 185,
        WIDTH_TARGET_AREA: 185,
        HEIGHT_TARGET_AREA: 15,
        LENGTH_TOTAL_W_MAST: 3500,
        LENGTH_TOTAL_WO_MAST: 3400,
        HEIGHT_OBSTACLES: 200,
        ANGLE_PITCH_DEGREES: 8.13,
        CENTER_ROLL_TO_CAMERA: 140,
        CUBE_START_X: 650,
        CUBE_START_Z: 0,
        THRESHOLD_SLOW_END: 3200
    }

    HEIGHT_DELTA = {}

    @staticmethod
    def init_dict():
        for i in range(0, 541, 1):
            DistanceLookup.HEIGHT_DELTA[i] = (30, math.sin(math.radians(4.989)), math.cos(math.radians(4.989)))
        for i in range(541, 641, 1):
            DistanceLookup.HEIGHT_DELTA[i] = (35, math.sin(math.radians(5.039)), math.cos(math.radians(5.039)))
        for i in range(641, 741, 1):
            DistanceLookup.HEIGHT_DELTA[i] = (40, math.sin(math.radians(5.075)), math.cos(math.radians(5.075)))
        for i in range(741, 841, 1):
            DistanceLookup.HEIGHT_DELTA[i] = (45, math.sin(math.radians(5.102)), math.cos(math.radians(5.102)))
        for i in range(841, 941, 1):
            DistanceLookup.HEIGHT_DELTA[i] = (50, math.sin(math.radians(5.124)), math.cos(math.radians(5.124)))
        for i in range(941, 1041, 1):
            DistanceLookup.HEIGHT_DELTA[i] = (60, math.sin(math.radians(4.868)), math.cos(math.radians(4.868)))
        for i in range(1041, 1141, 1):
            DistanceLookup.HEIGHT_DELTA[i] = (64, math.sin(math.radians(4.956)), math.cos(math.radians(4.956)))
        for i in range(1141, 1241, 1):
            DistanceLookup.HEIGHT_DELTA[i] = (68, math.sin(math.radians(5.03)), math.cos(math.radians(5.03)))
        for i in range(1241, 1341, 1):
            DistanceLookup.HEIGHT_DELTA[i] = (70, math.sin(math.radians(5.178)), math.cos(math.radians(5.178)))
        for i in range(1341, 1441, 1):
            DistanceLookup.HEIGHT_DELTA[i] = (71, math.sin(math.radians(5.344)), math.cos(math.radians(5.344)))
        for i in range(1441, 1541, 1):
            DistanceLookup.HEIGHT_DELTA[i] = (71, math.sin(math.radians(5.526)), math.cos(math.radians(5.526)))
        for i in range(1541, 1641, 1):
            DistanceLookup.HEIGHT_DELTA[i] = (71, math.sin(math.radians(5.686)), math.cos(math.radians(5.686)))
        for i in range(1641, 1741, 1):
            DistanceLookup.HEIGHT_DELTA[i] = (72, math.sin(math.radians(5.794)), math.cos(math.radians(5.794)))
        for i in range(1741, 1841, 1):
            DistanceLookup.HEIGHT_DELTA[i] = (70, math.sin(math.radians(5.983)), math.cos(math.radians(5.983)))
        for i in range(1841, 1941, 1):
            DistanceLookup.HEIGHT_DELTA[i] = (68, math.sin(math.radians(6.153)), math.cos(math.radians(6.153)))
        for i in range(1941, 2041, 1):
            DistanceLookup.HEIGHT_DELTA[i] = (62, math.sin(math.radians(6.417)), math.cos(math.radians(6.417)))
        for i in range(2041, 2141, 1):
            DistanceLookup.HEIGHT_DELTA[i] = (57, math.sin(math.radians(6.629)), math.cos(math.radians(6.629)))
        for i in range(2141, 2241, 1):
            DistanceLookup.HEIGHT_DELTA[i] = (50, math.sin(math.radians(6.873)), math.cos(math.radians(6.873)))
        for i in range(2241, 2341, 1):
            DistanceLookup.HEIGHT_DELTA[i] = (40, math.sin(math.radians(7.168)), math.cos(math.radians(7.168)))
        for i in range(2341, 2441, 1):
            DistanceLookup.HEIGHT_DELTA[i] = (33, math.sin(math.radians(7.369)), math.cos(math.radians(7.369)))
        for i in range(2441, 2541, 1):
            DistanceLookup.HEIGHT_DELTA[i] = (20, math.sin(math.radians(7.687)), math.cos(math.radians(7.687)))
        for i in range(2541, 2641, 1):
            DistanceLookup.HEIGHT_DELTA[i] = (10, math.sin(math.radians(7.917)), math.cos(math.radians(7.917)))
        for i in range(2641, 3541, 1):
            DistanceLookup.HEIGHT_DELTA[i] = (0, math.sin(math.radians(8.13)), math.cos(math.radians(8.13)))

    @staticmethod
    def get_delta(x):
        x = math.floor(x)
        return DistanceLookup.HEIGHT_DELTA[x][0]
