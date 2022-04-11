import csv 
import numpy as np
import pandas as pd
# TODO: we may want to make separate methods from loading in our csv files, since we are going to be doing it a lot
# TODO: unit test all methods

class Window():

    def __init__(self, coordinates, area, pointLocFile, energyFlow=0, transfer_coefficient=1):        
        # @param coordinates: a list of four coordinates defining the location of the window's four corners
        # The order of coordinates is top left, rop right, bottom left, bottom right
        # ex. for a rectangular window, [[320, 412.43, 413.34], [325, 412.43, 413.34], [320, 408.43, 410.34], [325, 408.43, 410.34]]

        # @param pointIndices: a list of indices of the points in this window in the specified 
        # csv files (returned by getPointIndices())

        # @param area: the area of the window (returned by getArea) 

        # @param transfer_coefficient: value 0-1, based on transparency of window (1 is completely transparent)
        # sort of arbritray for now

        # @param pointLocFile: the path to the file containing the locations in 3 space of the points
        
        self.coordinates = coordinates
        self.area = self.getArea(coordinates)
        self.transfer_coefficient = transfer_coefficient
        self.setPointIndices(pointLocFile)
        self.energyFlow = energyFlow # initialize to 0 (user can override)

    def cleanData(self, data):
        for i in range(len(data)):
            for j in range(len(data[0])):
                data[i][j] = data[i][j].replace("{","")
                data[i][j] = data[i][j].replace("}","")
                data[i][j] = float(data[i][j])
        
    def setPointIndices(self, filepath):
        self.pointIndices = self.getPoints(self.coordinates, filepath)

    def getPoints(self, pointCoords, windowCoords):
        with open(pointCoords) as f:
            reader = csv.reader(f)
            points = list(reader)
        self.cleanData(points)

        with open(windowCoords) as f:
            reader = csv.reader(f)
            window = list(reader)
        self.cleanData(window) # TODO: write a different cleanData method for window data (different format)

        # absolute values so the coordinate system is never negative (want +x, +y, +z)
        # this might be a problem
        xvect = list(map(abs, window[1] - window[0]))
        yvect = list(map(abs, window[3] - window[0]))
        zvect = list(map(abs, window[4] - window[0]))

        xlocal = xvect/np.linalg.norm(xvect)
        ylocal = yvect/np.linalg.norm(yvect)
        zlocal = zvect/np.linalg.norm(zvect)

        transMatrix = np.array([x, y, z]).T # transformation matrix with new coordinate axes as columns
        
        filteredList = []
        indexList = []
        for point in points:
            transPoint = np.matmul(transMatrix, np.array([point]).T) # transform the point to new axes
            if self.isInAlignedBox(point, window):
                filteredList.append([points[i]]) # not used atm, but contains a list of point locations
                indexList.append(i) # contains a list of point indices
        
        return indexList

    def isInAlignedBox(self, point, boundingBox):
        box = np.array(boundingBox)
        mins = box.min(axis=0)
        maxs = box.max(axis=0)
        x = point[0]
        y = point[1]
        z = point[2]

        return mins[0] <= x and maxs[0] >= x and mins[1] <= y and maxs[1] >= y and mins[2] <= z and maxs[2] >= z


    def getPointsOld(self, coordinates, filepath):        
        # @param filepath: path to open the csv containing point locations
        # @return: the points from the simulation contained within the window (format: index referring to the points in the csv file)
        # TODO: where do we enter filepath? Who calls it?
        # TODO: how do we clean the data (format is list of '{}' at the moment)

        with open(filepath) as f:
            reader = csv.reader(f)
            data = list(reader)
        self.cleanData(data)
        
        filteredList = []
        indexList = []

        v1 = [coordinates[0][0] - coordinates[1][0], coordinates[0][1] - coordinates[1][1], coordinates[0][2] - coordinates[1][2]]
        v2 = [coordinates[0][0] - coordinates[2][0], coordinates[0][1] - coordinates[2][1], coordinates[0][2] - coordinates[2][2]]
        
        normVect = np.cross(v1, v2) # vector perpendicular to plane of window
        planePoint = coordinates[0] # point on plane (given by coordinates at 0, in this case)
        d = -np.dot(normVect, planePoint) # ax + by + cz = d plane equation

        for i in range(len(data)):
            data[i] = poi
            normDist = abs(np.dot(normVect, poi) + d) / (np.linalg.norm(normVect))

            pointVect = np.subtract(poi, planePoint)

            v1_norm = np.linalg.norm(v1)
            proj = (np.dot(pointVect, v1) / (v1_norm ** 2))*v1 # proj of pointvect along v1

            # if normal distance to plane is less than offset and 
            # magnitude of projection along vector is less than vector magnitude
            if normDist <= offset and np.linalg.norm(proj) <= v1_norm: 
                filteredList.append([data[i]])
                indexList.append(i)

        # for i in range(len(data)):
        #     if (float(data[i][0]) > self.coordinates[0][0] and float(data[i][0]) < self.coordinates[1][0] and 
        #     float(data[i][1]) > self.coordinates[2][1] and float(data[i][1]) < self.coordinates[0][1]):
        #         filteredList.append([data[i]])
        #         indexList.append(i)


        return indexList

    def getArea(self, coordinates):
        # @return: area of window, based on window coordinates (for a rectangle, just base * height) 
        # |u x v| -> area of parallelogram in 3 space
        # TODO: test this method
        v1 = [coordinates[0][0] - coordinates[1][0], coordinates[0][1] - coordinates[1][1], coordinates[0][2] - coordinates[1][2]]
        v2 = [coordinates[0][0] - coordinates[2][0], coordinates[0][1] - coordinates[2][1], coordinates[0][2] - coordinates[2][2]]
        
        cross = np.cross(v1, v2)
        return np.sqrt(np.dot(cross, cross))
        

    def setEnergyFlow(self, filepath):
        self.energyFlow = self.getEnergyFlow(filepath)

    def getEnergyFlow(self, filepath):
        # @param filePath: the path to the file containing the energy of the points (enumerated by index)
        # @return: comparison metric for energy flow through this window
        # average(energy at points in pointIndices) * window area * transfer_coefficient 
        # higher point energy, higher window area, and higher coefficient return a larger energyflow metric 
        
        with open(filepath) as f:
            reader = pd.read_csv(f)
           
            data = reader.values.tolist()
        
        energies = []
        for i in self.pointIndices:
            energies.append(data[i])
        
        return np.average(energies) * self.area * self.transfer_coefficient 
        
        
window = Window(coordinates=[[800, 250, 413.34], [900, 250, 413.34], [800, 200, 410.34], [900, 200, 410.34]]
, area=20, pointLocFile='resources/point_locations.csv')
# window.setEnergyFlow('resources/energy_at_points.csv')
# print(window.energyFlow)

window.getPoints(window.coordinates, "resources/point_locations.csv")        