import os
from csv import reader
from window import Window
from room import Room
import numpy as np

class Building():

    def __init__(self):
        # TODO: figure out definite meaning behind params
        # @param orientation: probably the degrees of the long edge of the building relative to north
        # @param location: probably world coordinates (like literal google maps coords)

        self.rooms = [] # a list of Room objects in this building
        self.events = [] # a list of Event objects in this building
        # self.orientation = orientation
        # self.location = location

    def oldSchedule(self):
        # TODO: figure out what to return here (a schedule object? void and just change the times within each event object?)
        # @param time: the time of year to schedule events for. This should go all the
        # way into window and change what file it is looking at (have files for every hour and every day, maybe)

        # directory = input("Enter the path to the directory containing the relevant .csv files: ")
        # energyFile = input("Enter the path to the directory containing all energy .csv files: ")
        directory = "/Users/wyattsullivan/Desktop/Building1"
        energyFile = "/Users/wyattsullivan/Desktop/Energy"
        roomfiles = os.listdir(directory)
        energyfiles = os.listdir(energyFile)
        energyfiles.remove(".DS_Store")
        roomfiles.remove(".DS_Store")
        buildingPointLocFile = "building_pts.csv"
        for roomfile in roomfiles:
            windows = []

            # if roomfile == "building_pts.csv":
            #     buildingPointLocFile = roomfile

            if roomfile != "building_pts.csv":
                newdir = directory+"/"+roomfile

                with open(newdir+"/roominfo.csv", 'r') as roomInfo:
                    csv_reader = reader(roomInfo)
                    rows = list(csv_reader)
                    roomNumber = int(rows[0][0])
                    capacity = int(rows[1][0])
                    volume = int(rows[2][0])
                windowfiles = os.listdir(newdir)
                if windowfiles.count(".DS_Store") > 0:

                    windowfiles.remove(".DS_Store")

                for windowfile in windowfiles:
                    if windowfile != "roominfo.csv":
                        windows = windows + [Window(newdir+"/"+windowfile,directory+"/"+buildingPointLocFile)]

                self.rooms = self.rooms + [Room(volume, capacity, windows, roomNumber)]
        
        timeRoomMapping = {}
        for energycsv in energyfiles:
            roomEnergyFlows = {}
            for room in self.rooms:
                for window in room.windows:
                    window.setPointIndices(window.windowLocFile, window.pointLocFile)
                    window.setEnergyFlow(energyFile+"/"+energycsv) 
                room.setRoomEnergyFlow()
                roomEnergyFlows[room.roomNumber] = room.energyFlow

            
            roomEnergyFlows = dict(sorted(roomEnergyFlows.items(), key=lambda x: x[1]))
            roomsBestToWorst = list(roomEnergyFlows.keys())
            roomsBestToWorst.reverse()
            timeRoomMapping[energycsv[0:8]] = roomsBestToWorst
        return timeRoomMapping

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
        directory = ""
        buildingPointLocFile = "building_pts.csv"

        energyFile = "/Users/wyattsullivan/Desktop/Energy"
        energyfiles = os.listdir(energyFile)
        energyfiles.remove(".DS_Store")
        with open("/Users/wyattsullivan/Documents/GitHub/DynoSun/src/resources/building.csv", 'r') as roomInfo:
           csv_reader = reader(roomInfo)
           rows = list(csv_reader) 
           for room in range(len(rows)):
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

                    windowlst = windowlst + [Window(lst[(i-1)*8:((i-1)*8)+8],directory+"/"+buildingPointLocFile)]
                self.rooms = self.rooms + [Room(roomVolume, roomCapacity, windowlst, roomNumber)]    
        timeRoomMapping = {}

        for energycsv in energyfiles:
            roomEnergyFlows = {}
            for room in self.rooms:
                for window in room.windows:
                    window.setPointIndices(window.coordinates, window.pointLocFile)
                    window.setEnergyFlow(energyFile+"/"+energycsv) 
                room.setRoomEnergyFlow()
                roomEnergyFlows[room.roomNumber] = room.energyFlow

            
            roomEnergyFlows = dict(sorted(roomEnergyFlows.items(), key=lambda x: x[1]))
            roomsBestToWorst = list(roomEnergyFlows.keys())
            roomsBestToWorst.reverse()
            timeRoomMapping[energycsv[0:8]] = roomsBestToWorst

            print(roomEnergyFlows)
        return timeRoomMapping       


    
    
                 







        # timeRoomMapping = {}
        # for energycsv in energyfiles:
        #     roomEnergyFlows = {}
        #     for room in self.rooms:
        #         for window in room.windows:
        #             window.setPointIndices(window.windowLocFile, window.pointLocFile)
        #             window.setEnergyFlow(energyFile+"/"+energycsv) 
        #         room.setRoomEnergyFlow()
        #         roomEnergyFlows[room.roomNumber] = room.energyFlow

            
        #     roomEnergyFlows = dict(sorted(roomEnergyFlows.items(), key=lambda x: x[1]))
        #     roomsBestToWorst = list(roomEnergyFlows.keys())
        #     roomsBestToWorst.reverse()
        #     print(roomEnergyFlows)
        #     timeRoomMapping[energycsv[0:8]] = roomsBestToWorst
        # return timeRoomMapping

            