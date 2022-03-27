
class Event():

    def __init__(self, attendees, time):
        self.attendees = attendees
        self.time = time
        self.roomAssignment = None

    def adequateSize(self, room):
        # @param room: a Room object
        # @return true if room is large enough for this event, false otherwise
        # something like: return room.volume > (attendees * ventilation heuristic) && room.maxCapacity > attendees
        # or maybe just return room.maxCapacity > attendees

        pass