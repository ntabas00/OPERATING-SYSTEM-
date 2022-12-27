
class Process:
    def __init__(self, id, arrival, burst, userName):
        self.id = id
        self.arrival = arrival
        self.burst = burst
        self.user = userName
        self.state = "New"
        self.quantum = 0

    # setters
    def setId(self, i):
        self.id = i

    def setArrival(self, a):
        self.arrival = a

    def setBurst(self, b):
        self.burst = b

    def setUser(self, u):
        self.user = u

    def setState(self, s):
        self.state = s

    def setQuantum(self, q):
        self.quantum = q


    # getters
    def getId(self):
        return self.id

    def getArrival(self):
        return self.arrival

    def getBurst(self):
        return self.burst

    def getUser(self):
        return self.user

    def getState(self):
        return self.state

    def getQuantum(self):
        return self.quantum
