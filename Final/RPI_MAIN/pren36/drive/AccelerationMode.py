
class AccelerationMode:
    # start_position, end_position, acc_factor
    ACC_MODES = {
        "am_start": (0, 100, 1.01),
        "am_intermediate": (100, 200, 1.001),
        "am_end": (200, 340, 1.0001)
    }
    MODE_START = ACC_MODES["am_start"]
    MODE_INTERMEDIATE = ACC_MODES["am_intermediate"]
    MODE_END = ACC_MODES["am_end"]
