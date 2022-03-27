import csv 


class Window():

    def __init__(self, coordinates, pointIndices, area, energyFlow=1, transfer_coefficient=1):        
        # @param coordinates: a list of coordinates defining the location of the window
        # ex. for a rectangular window, [[325, 412.43, 413.34], [320, 412.43, 413.34], [325, 408.43, 410.34]]

        # @param pointIndices: a list of indices of the points in this window in the specified 
        # csv files (returned by getPointIndices())

        # @param area: the area of the window (returned by getArea) 
        # @param transfer_coefficient: value 0-1, based on transparency of window (1 is completely transparent)
        # sort of arbritray for now
        
        self.coordinates = coordinates
        self.pointIndices = pointIndices
        self.area = area
        self.energyFlow = energyFlow
        self.transfer_coefficient = transfer_coefficient
        

    def getPointIndices(self):
        self.pointIndices = getPoints(self.coordinates, filepath)

    def getPoints(self, filepath):        
        # @param filepath: path to open the csv containing point locations
        # @return: the points from the simulation contained within the window (format: index referring to the points in the csv file)
        # TODO: where do we enter filepath? Who calls it?
        # TODO: how do we clean the data (format is list of '{}' at the moment)

        with open(filepath) as f:
            reader = csv.reader(f)
            data = list(reader)

        pass 

    def getArea(self):
        # @return: area of window, based on window coordinates (for a rectangle, just base * height) 
        
        pass

    def getWindowEnergyFlow(self):
        # @return: comparison metric for energy flow through this window
        # sum(energy at points in pointIndices) * window area * transfer_coefficient / # of points 
        # higher window area, higher point energy, and higher coefficient return a larger energyflow metric 

        pass

window = Window([214], 20, 10)
window.getPoints('resources/point_locations.csv')



        