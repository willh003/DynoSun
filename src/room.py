
class Room():

    def __init__(self, dimensions, maxCapacity, windows, location, heatLag=0):
        # TODO: standardize room location format. Do we use room numbers? Or another arbritray system
        # @param dimensions: the xyz dimensions of the room (in meters)
        # @param heatLag: the estimated lag of heat in the room from light (low priority right now)

        self.volume = getVolume(dimensions)
        self.surfaceAreas = getSurfaceAreas(dimensions)
        self.maxCapacity = maxCapacity
        self.windows = windows # list of window objects in this room
        self.location = location
        self.energyFlow = 0

    def getVolume(self, dimensions):
        # return x*y*z
        pass

    def getSurfaceAreas(self, dimensions):
        # return list containing surface areas for walls, floors, ceilings
        # low priority (not necessary for prototype)
        pass

    def getRoomEnergyFlow(self):
        # return heuristic value for this room
        # sum of window energy flows divided by room volume
        pass