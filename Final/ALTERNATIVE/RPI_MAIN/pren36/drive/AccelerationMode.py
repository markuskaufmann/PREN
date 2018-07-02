
class AccelerationMode:
    # end_position [mm], acc_factor
    ACC_MODES = {
        "am_start": (1450, 1.01),
        "am_intermediate": (1950, 1.0095),
        "am_end": (4000, 1.001)
    }
    MODE_START = ACC_MODES["am_start"]
    MODE_INTERMEDIATE = ACC_MODES["am_intermediate"]
    MODE_END = ACC_MODES["am_end"]

    @staticmethod
    def determine_acc_mode(x):
        if x <= AccelerationMode.MODE_START[0]:
            return AccelerationMode.MODE_START
        elif x <= AccelerationMode.MODE_INTERMEDIATE[0]:
            return AccelerationMode.MODE_INTERMEDIATE
        else:
            return AccelerationMode.MODE_END
