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

    HEIGHT_DELTA = {
        range(0, 540): (30, math.sin(math.radians(4.989)), math.cos(math.radians(4.989))),
        range(541, 640): (35, math.sin(math.radians(5.039)), math.cos(math.radians(5.039))),
        range(641, 740): (40, math.sin(math.radians(5.075)), math.cos(math.radians(5.075))),
        range(741, 840): (45, math.sin(math.radians(5.102)), math.cos(math.radians(5.102))),
        range(841, 940): (50, math.sin(math.radians(5.124)), math.cos(math.radians(5.124))),
        range(941, 1040): (60, math.sin(math.radians(4.868)), math.cos(math.radians(4.868))),
        range(1041, 1140): (64, math.sin(math.radians(4.956)), math.cos(math.radians(4.956))),
        range(1141, 1240): (68, math.sin(math.radians(5.03)), math.cos(math.radians(5.03))),
        range(1241, 1340): (70, math.sin(math.radians(5.178)), math.cos(math.radians(5.178))),
        range(1341, 1440): (71, math.sin(math.radians(5.344)), math.cos(math.radians(5.344))),
        range(1441, 1540): (71, math.sin(math.radians(5.526)), math.cos(math.radians(5.526))),
        range(1541, 1640): (71, math.sin(math.radians(5.686)), math.cos(math.radians(5.686))),
        range(1641, 1740): (72, math.sin(math.radians(5.794)), math.cos(math.radians(5.794))),
        range(1741, 1840): (70, math.sin(math.radians(5.983)), math.cos(math.radians(5.983))),
        range(1841, 1940): (68, math.sin(math.radians(6.153)), math.cos(math.radians(6.153))),
        range(1941, 2040): (62, math.sin(math.radians(6.417)), math.cos(math.radians(6.417))),
        range(2041, 2140): (57, math.sin(math.radians(6.629)), math.cos(math.radians(6.629))),
        range(2141, 2240): (50, math.sin(math.radians(6.873)), math.cos(math.radians(6.873))),
        range(2241, 2340): (40, math.sin(math.radians(7.168)), math.cos(math.radians(7.168))),
        range(2341, 2440): (33, math.sin(math.radians(7.369)), math.cos(math.radians(7.369))),
        range(2441, 2540): (20, math.sin(math.radians(7.687)), math.cos(math.radians(7.687))),
        range(2541, 2640): (10, math.sin(math.radians(7.917)), math.cos(math.radians(7.917))),
        range(2641, 2740): (0, math.sin(math.radians(8.13)), math.cos(math.radians(8.13))),
        range(2741, 2840): (0, math.sin(math.radians(8.13)), math.cos(math.radians(8.13))),
        range(2841, 2940): (0, math.sin(math.radians(8.13)), math.cos(math.radians(8.13))),
        range(2941, 3040): (0, math.sin(math.radians(8.13)), math.cos(math.radians(8.13))),
        range(3041, 3140): (0, math.sin(math.radians(8.13)), math.cos(math.radians(8.13))),
        range(3141, 3240): (0, math.sin(math.radians(8.13)), math.cos(math.radians(8.13))),
        range(3241, 3340): (0, math.sin(math.radians(8.13)), math.cos(math.radians(8.13))),
        range(3341, 3440): (0, math.sin(math.radians(8.13)), math.cos(math.radians(8.13))),
        range(3441, 3540): (0, math.sin(math.radians(8.13)), math.cos(math.radians(8.13)))
    }

    @staticmethod
    def get_delta(x):
        x = math.floor(x)
        return DistanceLookup.HEIGHT_DELTA[x][0]
