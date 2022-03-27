import csv 


class Window():
    TRANSFER_COEFFICIENT = 1 # value 0-1, based on transparency of window

    def __init__(self, energyFlow, area, coordinates, pointIndices):
        
        pass

    def getPointIndices():
        self.pointIndices = getPoints(self.coordinates, filepath)

    def getPoints(coordinates, filepath): # TODO where do we enter filepath?
        """
        @param coordinates: a list of coordinates defining the location of the window
        ex. for a rectangular window, [325, 412.43, 413.34]

        """
        with open(filepath) as f:
            reader = csv.reader(f)
            data = list(reader)
        
        