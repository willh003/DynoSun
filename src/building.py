import os

class Building():

    def __init__(self, orientation, location):
        # TODO: figure out definite meaning behind params
        # @param orientation: probably the degrees of the long edge of the building relative to north
        # @param location: probably world coordinates (like literal google maps coords)

        self.rooms = [] # a list of Room objects in this building
        self.events = [] # a list of Event objects in this building
        self.orientation = orientation
        self.location = location

    def schedule(self, day, month, hour):
        # TODO: figure out what to return here (a schedule object? void and just change the times within each event object?)
        # @param time: the time of year to schedule events for. This should go all the
        # way into window and change what file it is looking at (have files for every hour and every day, maybe)
        # TODO: figure out how to represent time

        directory = input("Enter the path to the directory containing the relevant .csv files: ")
        roomfiles = os.listdir(directory)
        for roomfile in roomfiles:
            if roomfile != ".DS_Store":
                newdir = directory+"/"+roomfile
                with open(newdir+"/roominfo.csv", 'r') as f:
                    roomData = f.read()
                    # TODO: create room object using room data, create window objects
            windowfiles = os.listdir(roomfile)
            for windowfile in windowfiles:
                if windowfile != "/roominfo.csv":
                    # TODO: open window csv and add it to room.windows

            # self.rooms = self.rooms + [Room()]
            # windows = os.listdir(roomfile)
            # room.windows = windows


    #     roomEnergies = []
    # #   energy = file derived from script
    #     for room in self.rooms
    #         tempList = []
    #         for window in room.windows
    #             tempList = tempList + [window.getEnergyFlow]
    #         roomEnergy = sum(tempList)
    #         roomEnergies = roomEnergies + [roomEnergy]
    #     # Very basic output
    #     bestRoomSummer = roomEnergies(index(max(roomEnergies)))
    #     bestRoomWinter = roomEnergies(index(min(roomEnergies)))
        


