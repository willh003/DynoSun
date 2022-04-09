

class Building():

    def __init__(self, orientation, location):
        # TODO: figure out definite meaning behind params
        # @param orientation: probably the degrees of the long edge of the building relative to north
        # @param location: probably world coordinates (like literal google maps coords)

        self.rooms = [] # a list of Room objects in this building
        self.events = [] # a list of Event objects in this building
        self.orientation = orientation
        self.location = location

    def schedule(self, time):
        # TODO: figure out what to return here (a schedule object? void and just change the times within each event object?)
        # @param time: the time of year to schedule events for. This should go all the
        # way into window and change what file it is looking at (have files for every hour and every day, maybe)
        # TODO: figure out how to represent time
        
        """
        h = minHeap(self.rooms, priority = energyFlow)
        while h:
            r = peek(h)
            for e in sorted(self.events, high to low attendees):
                if e.adequateSize(r):
                    e.room_assignment = r
                    break
            pop(h)
        """

        pass
