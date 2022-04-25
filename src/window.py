import csv 
import numpy as np
import pandas as pd
# TODO: we may want to make separate methods from loading in our csv files, since we are going to be doing it a lot
# TODO: more testing

class Window():

    def __init__(self, windowCoords, pointLocFile, windowPointOffset=1, energyFlow=0, transfer_coefficient=1):        
        # @param windowCoords: a list of 4 points (x, y, z) indicating the window corners
        # @param pointLocFile: the path to the file containing the locations in 3 space of the points 
        # @param transfer_coefficient: value 0-1, where 1 is completely transparent - sort of arbritray for now
        
        self.coordinates = windowCoords
        self.offset = windowPointOffset
        self.area = self.getArea(self.coordinates) # Area of the window
        self.transfer_coefficient = transfer_coefficient
        self.pointLocFile = pointLocFile
        
  
        self.pointIndices = self.getPointIndices(self.coordinates, pointLocFile, windowPointOffset)
        print(self.pointIndices)
        self.energyFlow = energyFlow # initialize to 0 (user can override)
        
        
    def cleanData(self, data):
        for i in range(len(data)):
            for j in range(len(data[0])):
                data[i][j] = data[i][j].replace("{","")
                data[i][j] = data[i][j].replace("}","")
                data[i][j] = float(data[i][j])
        
    def getWindowCoords(self, filepath):
        # @param filepath: path to file containing window coordinates 
        # @return: a list of eight coordinates defining the location of the window's eight corners (its a box)
        with open(filepath, encoding="utf8", errors='ignore') as f:
            reader = csv.reader(f)
            window = list(reader)
        
        window = window[:-1] # last row is text, which we don't want
        self.cleanData(window)
        return window

    def getPoint4Indices(self, windowCoords, pointCoords):
        # @param indexList: a list of indices of the points in this window in the specified csv files
        # https://stackoverflow.com/questions/21037241/how-to-determine-a-point-is-inside-or-outside-a-cube#:~:text=Construct%20the%20direction%20vector%20from,is%20outside%20of%20the%20cube
        
        with open(pointCoords) as f:
            reader = csv.reader(f)
            points = list(reader)
        self.cleanData(points)

        # absolute values so the coordinate system is never negative (want +x, +y, +z)
        # this might be a problem - may need to manually find the larger points and use those as the references
        xvect = list(map(abs, np.subtract(windowCoords[1], windowCoords[0])))
        yvect = list(map(abs, np.subtract(windowCoords[2], windowCoords[0])))
        zvect = np.cross(xvect, yvect)

        xlocal = xvect/np.linalg.norm(xvect)
        ylocal = yvect/np.linalg.norm(yvect)
        zlocal = zvect/np.linalg.norm(zvect)

        transMatrix = np.array([xlocal, ylocal, zlocal]).T # transformation matrix with new coordinate axes as columns
        
        filteredList = []
        indexList = []
        for point in points:
            transPoint = np.matmul(transMatrix, np.array([point]).T) # transform the point to new axes
            
            if self.isInAlignedBox(transPoint, np.linalg.norm(xvect), np.linalg.norm(yvect), self.offset): # TODO: construct the point first!!
                filteredList.append(point) # not used atm, but contains a list of point locations
                indexList.append(i) # contains a list of point indices

        return indexList

    def getPointIndices(self, window, pointCoords, offset):
        # @param indexList: a list of indices of the points in this window in the specified csv files
        # https://stackoverflow.com/questions/21037241/how-to-determine-a-point-is-inside-or-outside-a-cube#:~:text=Construct%20the%20direction%20vector%20from,is%20outside%20of%20the%20cube
        
        with open(pointCoords) as f:
            reader = csv.reader(f)
            points = list(reader)
        self.cleanData(points)

        # absolute values so the coordinate system is never negative (want +x, +y, +z)
        # this might be a problem - may need to manually find the larger points and use those as the references
        xvect = list(map(abs, np.subtract(window[1], window[0])))
        yvect = list(map(abs, np.subtract(window[2], window[0])))
        zvect = np.cross(xvect, yvect)
        zvect = offset * zvect/np.linalg.norm(zvect)

        for i in range(len(window[:4])):
            window.append(np.add(window[i], zvect))
            window[i] = np.add(window[i], -1*zvect)

        xlocal = xvect/np.linalg.norm(xvect)
        ylocal = yvect/np.linalg.norm(yvect)
        zlocal = zvect/np.linalg.norm(zvect)

        transMatrix = np.array([xlocal, ylocal, zlocal]).T # transformation matrix with new coordinate axes as columns
        
        filteredList = []
        indexList = []
        for i in range(len(points)):
            point = points[i]
            transPoint = np.matmul(transMatrix, np.array([point]).T) # transform the point to new axes
            if self.isInAlignedBox(point, window, self.offset):
                filteredList.append(point) # not used atm, but contains a list of point locations
                indexList.append(i) # contains a list of point indices

        return indexList

    def isInAlignedBox(self, point, boundingBox, error):
        # TODO: figure out where error should be added (probably either x or y)

        box = np.array(boundingBox)
        mins = box.min(axis=0)
        maxs = box.max(axis=0)

        x = point[0]
        y = point[1]
        z = point[2]

        return mins[0] <= x and maxs[0] >= x and mins[1] <= y and maxs[1] >= y and mins[2] <= z and maxs[2] >= z

    def isInAlignedBox4(self, point, xbound, ybound, zbound):
        # TODO: figure out where error should be added (probably either x or y)

        x = point[0]
        y = point[1]
        z = point[2]

        return x <= xbound and y <= ybound and z >= -1*zbound and z <= zbound
        #return mins[0] <= x and maxs[0] >= x and mins[1] <= y and maxs[1] >= y and mins[2] <= z and maxs[2] >= z

    def setPointIndices(self, windowCoords, pointLocFile):
        # used to change filepath for this window after initialization
        self.coordinates = windowCoords

        self.pointIndices = self.getPoints(self.coordinates, pointLocFile)


    def getArea(self, coordinates):
        # @return: area of window, based on window coordinates (for a rectangle, just base * height) 
        # |u x v| -> area of parallelogram in 3 space
        # TODO: test this method
        
        v1 = [coordinates[0][0] - coordinates[1][0], coordinates[0][1] - coordinates[1][1], coordinates[0][2] - coordinates[1][2]]
        v2 = [coordinates[0][0] - coordinates[2][0], coordinates[0][1] - coordinates[2][1], coordinates[0][2] - coordinates[2][2]]
        
        cross = np.cross(v1, v2)
        return np.sqrt(np.dot(cross, cross))
        

    def setEnergyFlow(self, energyFile):
        self.energyFlow = self.getEnergyFlow(energyFile)
        

    def getEnergyFlow(self, energyFile):
        # @param filepath: the path to the file containing the energy of the points (enumerated by index)
        # @return: comparison metric for energy flow through this window
        # average(energy at points in pointIndices) * window area * transfer_coefficient 
        # higher point energy, higher window area, and higher coefficient return a larger energyflow metric
        with open(energyFile) as f:
            reader = pd.read_csv(f)
           
            data = reader.values.tolist()
        
        energies = []

        if self.pointIndices == []:
            return 0
        for i in self.pointIndices:
            energies.append(data[i])

        # print(np.average(energies) * self.area * self.transfer_coefficient)
        return np.average(energies) * self.area * self.transfer_coefficient 
        
