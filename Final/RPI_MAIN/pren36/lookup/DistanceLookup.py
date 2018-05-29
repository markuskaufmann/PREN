import math

from pren36.lookup.Locator import Locator


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
    HEIGHT_WOC = "height_woc"
    THRESHOLD_SLOW_END = "threshold_slow_end"

    # [mm]
    DISTANCE_MAP = {
        HEIGHT_START: 600,
        HEIGHT_END: 1100,
        WIDTH_START_AREA: 500,
        LENGTH_START_AREA: 500,
        START_TO_CENTER_ROLL: 195,
        START_TO_CUBE: 460,  # 65 - START_TO_CENTER_ROLL
        START_HEIGHT_ABOVE_GROUND: 200,
        START_HEIGHT_CUBE: 180,
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
        HEIGHT_WOC: 220,
        THRESHOLD_SLOW_END: 3200
    }

    HEIGHT_DELTA = {
        range(0, 54): 30,
        range(55, 64): 35,
        range(65, 74): 40,
        range(75, 84): 45,
        range(85, 94): 50,
        range(95, 104): 60,
        range(105, 114): 64,
        range(115, 124): 68,
        range(125, 134): 70,
        range(135, 144): 71,
        range(145, 154): 71,
        range(155, 164): 71,
        range(165, 174): 72,
        range(175, 184): 70,
        range(185, 194): 68,
        range(195, 204): 62,
        range(205, 214): 57,
        range(215, 224): 50,
        range(225, 234): 40,
        range(235, 244): 33,
        range(245, 254): 20,
        range(255, 264): 10,
        range(265, 274): 0,
        range(275, 284): 0,
        range(285, 294): 0,
        range(295, 304): 0,
        range(305, 314): 0,
        range(315, 324): 0,
        range(325, 334): 0,
        range(335, 344): 0,
        range(345, 354): 0
    }

    @staticmethod
    def get_delta():
        x = math.floor(Locator.horizontal_x)
        return DistanceLookup.HEIGHT_DELTA[x]
