
class DistanceLookup:
    HEIGHT_START = "height_start"
    HEIGHT_END = "height_end"
    WIDTH_START_AREA = "width_start_area"
    LENGTH_START_AREA = "length_start_area"
    START_TO_CENTER_ROLL = "start_to_center_roll"
    START_TO_CUBE = "start_to_cube"
    START_HEIGHT_ABOVE_GROUND = "start_height_above_ground"
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

    DISTANCE_MAP = {
        HEIGHT_START: 60,
        HEIGHT_END: 110,
        WIDTH_START_AREA: 50,
        LENGTH_START_AREA: 50,
        START_TO_CENTER_ROLL: 20,  # TODO
        START_TO_CUBE: 45,  # 65 - START_TO_CENTER_ROLL
        START_HEIGHT_ABOVE_GROUND: 2.5,  # TODO
        HEIGHT_WITH_CUBE_ABOVE_GROUND: 27.5,  # TODO
        LENGTH_START_TO_TARGET_RANGE: 80,
        LENGTH_TARGET_RANGE: 240,
        LENGTH_TARGET_RANGE_TO_END: 20,
        WIDTH_TARGET_RANGE: 2,
        LENGTH_TARGET_AREA: 18.5,
        WIDTH_TARGET_AREA: 18.5,
        HEIGHT_TARGET_AREA: 1.5,
        LENGTH_TOTAL_W_MAST: 350,
        LENGTH_TOTAL_WO_MAST: 340,
        HEIGHT_OBSTACLES: 20,
        ANGLE_PITCH_DEGREES: 8.13,
        CENTER_ROLL_TO_CAMERA: 10  # TODO
    }
