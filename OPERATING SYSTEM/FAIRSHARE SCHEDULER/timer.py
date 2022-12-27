
import time

class Timer:
    def __init__(self):
        self.timer=0;


    def timerRun(self, t):
        self.timer = self.timer + t

    def getTime(self):
        return self.timer

