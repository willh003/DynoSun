import os
from csv import reader
from window import Window
from room import Room

class Building():

    def __init__(self):
        # TODO: figure out definite meaning behind params
        # @param orientation: probably the degrees of the long edge of the building relative to north
        # @param location: probably world coordinates (like literal google maps coords)

        self.rooms = [] # a list of Room objects in this building
        self.events = [] # a list of Event objects in this building
        # self.orientation = orientation
        # self.location = location

    def schedule(self):
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
        for roomfile in roomfiles:
            windows = []

            if roomfile == "building_pts.csv":
                buildingPointLocFile = roomfile

            if roomfile != "building_pts.csv":
                newdir = directory+"/"+roomfile

                with open(newdir+"/roominfo.csv", 'r') as roomInfo:
                    csv_reader = reader(roomInfo)
                    rows = list(csv_reader)
                    roomNumber = int(rows[0][0])
                    capacity = int(rows[1][0])
                    volume = int(rows[2][0])
                windowfiles = os.listdir(newdir)
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
        print(timeRoomMapping)

            


                        
                    # TODO: open window csv and add it to room.windows
                    # TODO: For each room's windows, do window.setEnergyFlow(energy file derived from Ladybug) 
                    # PULL FROM DATABASE of every time's energy csv for building
                    # TODO: Run algorithm