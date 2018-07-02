import math

from pren36.lookup.DistanceLookup import DistanceLookup


class Locator:
    x = DistanceLookup.DISTANCE_MAP[DistanceLookup.START_TO_CENTER_ROLL]
    xc = DistanceLookup.DISTANCE_MAP[DistanceLookup.CUBE_START_X]
    z = DistanceLookup.DISTANCE_MAP[DistanceLookup.START_HEIGHT_ABOVE_GROUND]
    zc = DistanceLookup.DISTANCE_MAP[DistanceLookup.CUBE_START_Z]
    fact = 0.965318627
    fact_inv = 1 / fact
    cube_loc = False

    @staticmethod
    def update_loc_fahrwerk(step_distance_mm):
        lx = math.floor(Locator.x)
        (delta, sin, cos) = DistanceLookup.HEIGHT_DELTA[lx]
        # dx = (step_distance_mm * Locator.fact_inv)
        dx = step_distance_mm * cos
        # dz = (step_distance_mm * sin)
        Locator.x += dx
        # Locator.z += dz
        if Locator.cube_loc:
            Locator.xc += dx
            # Locator.zc += dz

    # direction - CW = 1 UP, CCW = 0 DOWN
    @staticmethod
    def update_loc_hub(step_distance_mm, direction):
        if direction == 1:
            # Locator.z += step_distance_mm
            if Locator.cube_loc:
                Locator.zc += step_distance_mm
        else:
            # Locator.z -= step_distance_mm
            if Locator.cube_loc:
                Locator.zc -= step_distance_mm
            # if Locator.z < 0:
            #     Locator.z = 0
            #     Locator.zc = 0
            if Locator.zc < 0:
                Locator.zc = 0

    @staticmethod
    def real_distance_mm(x_distance_mm):
        lx = math.floor(Locator.x)
        (delta, sin, cos) = DistanceLookup.HEIGHT_DELTA[lx]
        return x_distance_mm / cos

    # @staticmethod
    # def update_z(z):
    #     Locator.z = float(z)

    @staticmethod
    def loc_cube():
        return str(Locator.xc) + ";" + str(Locator.zc)

    @staticmethod
    def reset():
        Locator.x = DistanceLookup.DISTANCE_MAP[DistanceLookup.START_TO_CENTER_ROLL]
        Locator.z = DistanceLookup.DISTANCE_MAP[DistanceLookup.START_HEIGHT_ABOVE_GROUND]
        Locator.xc = DistanceLookup.DISTANCE_MAP[DistanceLookup.CUBE_START_X]
        Locator.zc = DistanceLookup.DISTANCE_MAP[DistanceLookup.CUBE_START_Z]
