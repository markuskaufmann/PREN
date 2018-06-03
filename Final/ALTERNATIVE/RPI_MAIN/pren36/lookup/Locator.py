import math

from pren36.lookup.DistanceLookup import DistanceLookup


class Locator:
    horizontal_x = DistanceLookup.DISTANCE_MAP[DistanceLookup.START_TO_CENTER_ROLL]
    x = DistanceLookup.DISTANCE_MAP[DistanceLookup.START_TO_CENTER_ROLL]
    xc = DistanceLookup.DISTANCE_MAP[DistanceLookup.CUBE_START_X]
    z = DistanceLookup.DISTANCE_MAP[DistanceLookup.START_HEIGHT_ABOVE_GROUND]
    zc = DistanceLookup.DISTANCE_MAP[DistanceLookup.CUBE_START_Z]
    angle = math.radians(DistanceLookup.DISTANCE_MAP[DistanceLookup.ANGLE_PITCH_DEGREES])
    cos = math.cos(angle)
    sin = math.sin(angle)
    cube_loc = False

    @staticmethod
    def update_loc_fahrwerk(step_distance_mm):
        dx = (step_distance_mm * Locator.cos)
        dz = (step_distance_mm * Locator.sin)
        Locator.horizontal_x += step_distance_mm
        Locator.x += dx
        Locator.z += dz
        if Locator.cube_loc:
            Locator.xc += dx
            Locator.zc += dz

    # direction - CW = 1 UP, CCW = 0 DOWN
    @staticmethod
    def update_loc_hub(step_distance_mm, direction):
        if direction == 1:
            Locator.z += step_distance_mm
            if Locator.cube_loc:
                Locator.zc += step_distance_mm
        else:
            Locator.z -= step_distance_mm
            if Locator.cube_loc:
                Locator.zc -= step_distance_mm
            if Locator.z < 0:
                Locator.z = 0
                Locator.zc = 0

    @staticmethod
    def real_distance_mm(x_distance_mm):
        return x_distance_mm / Locator.cos

    @staticmethod
    def loc():
        return "x: " + str(Locator.x) + ", z: " + str(Locator.z) + " [mm]"

    @staticmethod
    def loc_cube():
        return str(Locator.xc) + ";" + str(Locator.zc)

    @staticmethod
    def reset():
        Locator.xc = DistanceLookup.DISTANCE_MAP[DistanceLookup.CUBE_START_X]
        Locator.zc = DistanceLookup.DISTANCE_MAP[DistanceLookup.CUBE_START_Z]
