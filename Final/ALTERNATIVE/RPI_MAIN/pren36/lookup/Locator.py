import math

from pren36.lookup.DistanceLookup import DistanceLookup


class Locator:
    horizontal_x = DistanceLookup.DISTANCE_MAP[DistanceLookup.START_TO_CENTER_ROLL]
    x = DistanceLookup.DISTANCE_MAP[DistanceLookup.START_TO_CENTER_ROLL]
    xc = DistanceLookup.DISTANCE_MAP[DistanceLookup.CUBE_START_X]
    z = DistanceLookup.DISTANCE_MAP[DistanceLookup.START_HEIGHT_ABOVE_GROUND]
    zc = DistanceLookup.DISTANCE_MAP[DistanceLookup.CUBE_START_Z]
    angle = math.radians(DistanceLookup.DISTANCE_MAP[DistanceLookup.ANGLE_PITCH_DEGREES])
    cube_loc = False
    comm_object = None

    @staticmethod
    def update_loc_fahrwerk(step_distance_mm):
        (delta, sin, cos) = DistanceLookup.HEIGHT_DELTA[Locator.horizontal_x]
        dx = (step_distance_mm * cos)
        dz = (step_distance_mm * sin)
        Locator.horizontal_x += step_distance_mm
        Locator.x += dx
        Locator.z += dz
        if Locator.cube_loc:
            Locator.xc += dx
            Locator.zc += dz
            Locator.comm_object.update_loc(Locator.xc, Locator.zc)

    # direction - CW = 1 UP, CCW = 0 DOWN
    @staticmethod
    def update_loc_hub(step_distance_mm, direction):
        if direction == 1:
            Locator.z += step_distance_mm
            if Locator.cube_loc:
                Locator.zc += step_distance_mm
                Locator.comm_object.update_loc(Locator.xc, Locator.zc)
        else:
            Locator.z -= step_distance_mm
            if Locator.cube_loc:
                Locator.zc -= step_distance_mm
                Locator.comm_object.update_loc(Locator.xc, Locator.zc)
            if Locator.z < 0:
                Locator.z = 0
                Locator.zc = 0
                Locator.comm_object.update_loc(Locator.xc, Locator.zc)

    @staticmethod
    def real_distance_mm(x_distance_mm):
        (delta, sin, cos) = DistanceLookup.HEIGHT_DELTA[Locator.horizontal_x]
        return x_distance_mm / cos

    # @staticmethod
    # def loc():
    #     return "x: " + str(Locator.x) + ", z: " + str(Locator.z) + " [mm]"
    #
    # @staticmethod
    # def loc_cube():
    #     return str(Locator.xc) + ";" + str(Locator.zc)

    @staticmethod
    def reset():
        Locator.xc = DistanceLookup.DISTANCE_MAP[DistanceLookup.CUBE_START_X]
        Locator.zc = DistanceLookup.DISTANCE_MAP[DistanceLookup.CUBE_START_Z]
        Locator.comm_object.update_loc(Locator.xc, Locator.zc)
