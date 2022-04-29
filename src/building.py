import os
from csv import reader
from window import Window
from room import Room
import numpy as np
import platform
import csv

class Building():

    def __init__(self):
        # TODO: figure out definite meaning behind params
        # @param orientation: probably the degrees of the long edge of the building relative to north
        # @param location: probably world coordinates (like literal google maps coords)

        self.rooms = [] # a list of Room objects in this building
        self.events = [] # a list of Event objects in this building
        # self.orientation = orientation
        # self.location = location

    def map1(self, string):
        lst = string.split(" ")
        numbers = [ float(x) for x in lst ]
        return numbers



    def schedule(self):
        # TODO: figure out what to return here (a schedule object? void and just change the times within each event object?)
        # @param time: the time of year to schedule events for. This should go all the
        # way into window and change what file it is looking at (have files for every hour and every day, maybe)

        # directory = input("Enter the path to the directory containing the relevant .csv files: ")
        # energyFile = input("Enter the path to the directory containing all energy .csv files: ")
        # directory = ""
        # roomfiles = os.listdir(directory)
        # csvfile = roomfiles[0]

        directory = input("Enter the path to the building_info.csv file: ")
        buildingPointLocFile = input("Enter the path to the building_points.csv file: ")
        energyFile = input("Enter the path to the folder containing energy simulation result files: ")
        finalcsv = input("Enter the path to where you would like the results to be placed: ")
        # directory = "/Users/wyattsullivan/Desktop/Building.csv"
        # buildingPointLocFile = "/Users/wyattsullivan/Desktop/Building1/building_pts.csv"
        # energyFile = "/Users/wyattsullivan/Desktop/Energy"
        # finalcsv = energyFile
        finalcsv = finalcsv+"/"+"results.csv"
        finalcsv = finalcsv.replace('"','')
        if platform.system() == 'Windows':
            finalcsv = finalcsv.replace("\\","/")
            energystring = str(energyFile.replace("\\","/"))
            energystring = energystring.replace('"','')
            energyfiles = os.listdir(energystring)
            directory = directory.replace("\\","/")
            directory = directory.replace('"','')
            buildingPointLocFile = buildingPointLocFile.replace("\\","/")
            buildingPointLocFile = buildingPointLocFile.replace('"','')
        else:
            energyfiles = os.listdir(energyFile)
        if energyfiles.count(".DS_Store")>0:
            energyfiles.remove(".DS_Store")
        with open(directory, 'r') as roomInfo:
            csv_reader = reader(roomInfo)
            rows = list(csv_reader)
            for i in range(len(rows)):
                while("" in rows[i]):
                    rows[i].remove("")
            for room in range(1,len(rows)):
                numWindows = int(rows[room][1])

                window = rows[room][4:4+(8*numWindows)]
                lst = []
                for windowCorner in window:
                    lst = lst + [self.map1(windowCorner)]
                roomNumber = (rows[room][0][4:])
                roomCapacity = (rows[room][2])
                roomVolume = (rows[room][3])
                windowlst = []
                for i in range(1,numWindows+1):

                    windowlst = windowlst + [Window(lst[(i-1)*4:((i-1)*4)+4],buildingPointLocFile)]
                self.rooms = self.rooms + [Room(roomVolume, roomCapacity, windowlst, roomNumber)]    
        timeRoomMapping = {}

        for energycsv in energyfiles:
            roomEnergyFlows = {}
            day = int(energycsv[3:5])
            month = int(energycsv[0:2])
            hour = int(energycsv[6:8])
            for room in self.rooms:
                for window in room.windows:
                    window.setPointIndices(window.coordinates, window.pointLocFile)
                    if platform.system() == 'Windows':
                        string = energyFile+"\\"+energycsv
                        string = string.replace('"','')
                        window.setEnergyFlow(string) 
                    else:
                        window.setEnergyFlow(energyFile+"/"+energycsv) 
                room.setRoomEnergyFlow()
                roomEnergyFlows[room.roomNumber] = room.energyFlow

            roomEnergyFlows = dict(sorted(roomEnergyFlows.items(), key=lambda x: x[1]))
            roomsBestToWorst = list(roomEnergyFlows.keys())
            
            energyLst = []
            
            for i in range(289):
                energyLst.append(0)
            for i in roomsBestToWorst:
                print(i,len(energyLst))
                energyLst[int(i)] = roomEnergyFlows[i]
            if (month < 5 or month>10):
                roomsBestToWorst.reverse()
            print(energyLst)
            timeRoomMapping["MONTH "+str(month)+", DAY " +str(day) + ", HOUR "+str(hour)] = roomsBestToWorst
            
            with open(finalcsv, 'w') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow(energyLst)
        return timeRoomMapping  