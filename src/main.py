from window import Window
from building import Building
import os

# TODO: figure out the call procedure for scheduling
# TODO: add resources to .gitignore (so we don't take all of my repo space)

def main():    
    # rooms = input("How many rooms are in the building?: ")
    # windowsInRoomIndex = []
    # for i in range(int(rooms)):
    #     windowInRoom = input("How many windows are in room "+str(i+1)+"?: ")
    #     windowsInRoomIndex = windowsInRoomIndex + [windowInRoom]
    
    # windowCornerPts = []
    # for i in windowsInRoomIndex:
    #     windowPts = input("Enter the window's four corner points (separated by a comma): ")
    #     windowCornerPts
    month = input("Month: ")
    day = input("Day: ")
    hour = input("Hour: ")

    building = Building(0,0)
    optRoom = building.schedule(month, day, hour)



    window1 = Window(windowLocFile='resources/window_east1_pts.csv', pointLocFile='resources/point_locations.csv')
    window2 = Window(windowLocFile='resources/window_west1_pts.csv', pointLocFile='resources/point_locations.csv')

    #print(window1.pointIndices, window2.pointIndices)
    #window.getPoints(window.coordinates, "resources/point_locations.csv")     
    energy9 = 'resources/06_24_09_energy.csv'
    energy14 = 'resources/06_24_14_energy.csv'
    
    window1.setEnergyFlow(energy9)
    window2.setEnergyFlow(energy9)
    print("\nEast 9am energy flow:", window1.energyFlow, "\nWest 9am energy flow:", window2.energyFlow)

    window1.setEnergyFlow(energy14)
    window2.setEnergyFlow(energy14)
    print("\nEast 2pm energy flow:", window1.energyFlow, "\nWest 2pm energy flow:", window2.energyFlow)

if  __name__ == "__main__":
    main()