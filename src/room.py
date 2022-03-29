import numpy as np

class Room():

    def __init__(self, dimensions, maxCapacity, windows, location, energyFlow = 0, heatLag=0):
        # TODO: standardize room location format. Do we use room numbers? Or another arbritray system (maybe Rhino coords?)
        # @param dimensions: the xyz dimensions of the room (in meters) OR MAYBE we should use corner points (then we can locate it)
        # @param heatLag: the estimated lag of heat in the room from light (low priority right now)

        self.volume = getVolume(dimensions)
        self.surfaceAreas = getSurfaceAreas(dimensions)
        self.maxCapacity = maxCapacity
        self.windows = windows # list of window objects in this room
        self.location = location
        self.energyFlow = energyFlow

    def getVolume(self, dimensions):
        # May need to change this, based on dimensions spec
        return np.prod(dimensions)

    def getSurfaceAreas(self, dimensions):
        # return list containing surface areas for walls, floors, ceilings
        # low priority (not necessary for prototype)
        pass

    def setRoomEnergyFlow(self):
        self.energyFlow = getRoomEnergyFlow()

    def getRoomEnergyFlow(self):
        # return heuristic value for this room
        # sum of window energy flows divided by room volume (maybe multiply by some scalar)
        return np.sum(self.windows) / self.volume