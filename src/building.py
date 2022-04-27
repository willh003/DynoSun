import os
from csv import reader
from window import Window
from room import Room
import numpy as np
import platform

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
        print(platform.system())
        directory = input("Enter the path to the building_info.csv file: ")
        buildingPointLocFile = input("Enter the path to the building_points.csv file: ")
        energyFile = input("Enter the path to the folder containing energy simulation result files: ")
        energyfiles = os.listdir(energyFile)
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
                    if platform.system == 'Windows':
                        window.setEnergyFlow(energyFile+"\\"+energycsv) 
                    else:
                        window.setEnergyFlow(energyFile+"/"+energycsv) 
                room.setRoomEnergyFlow()
                roomEnergyFlows[room.roomNumber] = room.energyFlow

            
            roomEnergyFlows = dict(sorted(roomEnergyFlows.items(), key=lambda x: x[1]))
            roomsBestToWorst = list(roomEnergyFlows.keys())
            if (month < 5 or month>10):
                roomsBestToWorst.reverse()
            timeRoomMapping["MONTH "+str(month)+", DAY " +str(day) + ", HOUR "+str(hour)] = roomsBestToWorst
        return timeRoomMapping       


    
    
                 







            
