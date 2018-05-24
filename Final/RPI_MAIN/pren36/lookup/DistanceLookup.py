
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
    CUBE_START_X = "cube_start_x"
    CUBE_START_Z = "cube_start_z"

    # [mm]
    DISTANCE_MAP = {
        HEIGHT_START: 600,
        HEIGHT_END: 1100,
        WIDTH_START_AREA: 500,
        LENGTH_START_AREA: 500,
        START_TO_CENTER_ROLL: 195,
        START_TO_CUBE: 460,  # 65 - START_TO_CENTER_ROLL
        START_HEIGHT_ABOVE_GROUND: 200,
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
        CUBE_START_Z: 0
    }
