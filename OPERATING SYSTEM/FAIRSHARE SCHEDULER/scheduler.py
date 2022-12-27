import threading

from timer import Timer
import process
import logging
from threading import Thread

class Scheduler:
    # waiting and ready queue
    waitingQueue = []
    readyQueue = []
    # user dict
    readyUserDict = {}
    # time quantum
    time_quant = 0

    t1=Timer()

    def __init__(self, list, quant):
        # copy list of all process to waiting queue
        self.waitingQueue.extend(list)

        #time quantum
        self.time_quant = quant

        # message configuration
        self.configureThreadMsg()


        while ((len(self.readyQueue) != 0) or (len(self.waitingQueue) != 0)):
            # check if process in waiting queue are ready
            self.checkReady()
            # allocate quantum to those in ready queue
            self.allocateQuantum()

            # run threads of processes in ready queue
            if len(self.readyQueue) != 0:
                for j in range(len(self.readyQueue)):
                    thread = threading.Thread(target=self.execute, args=(self.readyQueue.pop(0),))
                    thread.start()
                    thread.join()
            else:
                self.t1.timerRun(1)



    def configureThreadMsg(self):
        #configure logging info format
        logging.basicConfig(filename='output.txt', level=logging.INFO, format='Time %(time)s, User %(user)s, Process %(processId)s, %(message)s')


    def checkReady(self):
        if len(self.waitingQueue) !=0:
            for i in range(len(self.waitingQueue)):
                p = self.waitingQueue.pop(0)
                if p.arrival == self.t1.timer:
                    # add process to ready queue
                    self.addReadyQueue(p)
                else:
                    # append back to waiting
                    self.waitingQueue.append(p)


    def addReadyQueue(self, p):
        self.readyQueue.append(p)
        # add ready user to queue
        if(len(self.readyUserDict) == 0):
            self.readyUserDict[p.user] = 1
        else:
            if p.user in self.readyUserDict:
                self.readyUserDict[p.user] += 1
            else:
                self.readyUserDict[p.user] = 1



    def removeReadyDict(self, p):
        #check if need to remove from ready user dict
        if self.readyUserDict[p.user] == 1:
            self.readyUserDict.pop(p.user)
        elif self.readyUserDict[p.user] > 1:
            self.readyUserDict[p.user] -= 1

    # allocate quantum to processes in ready queue
    def allocateQuantum(self):
        if len(self.readyQueue) !=0:
            for p in self.readyQueue:
                allocQuantum = self.time_quant // len(self.readyUserDict) // self.readyUserDict[p.user]
                p.quantum = allocQuantum


    # execute process
    def execute(self, p):
        # define the custom thread name
        extra_info = {'time': self.t1.timer, 'user': p.user, 'processId': p.id}

        # update state and print msg
        if p.state == "New":
            p.state = "Started"
            extra_info = {'time': self.t1.timer, 'user': p.user, 'processId': p.id}
            logging.info('Started', extra=extra_info)
            p.state = "Resumed"
            extra_info = {'time': self.t1.timer, 'user': p.user, 'processId': p.id}
            logging.info('Resumed', extra=extra_info)
        elif p.state == "Paused":
            p.state = "Resumed"
            extra_info = {'time': self.t1.timer, 'user': p.user, 'processId': p.id}
            logging.info('Resumed', extra=extra_info)

        # run burst time for the allocated quantum
        while True:
            if p.burst <= p.quantum:
                # update time
                for i in range(p.burst):
                    self.t1.timerRun(1)
                    self.checkReady()

                # update burst time
                p.burst = 0

                # update state and print msg
                p.state = "Paused"
                extra_info = {'time': self.t1.timer, 'user': p.user, 'processId': p.id}
                logging.info('Paused', extra=extra_info)
                p.state = "Finished"
                logging.info('Finished', extra=extra_info)

                # check if we need to remove user
                self.removeReadyDict(p)
                break
            elif p.burst > p.quantum:
                # update process burst time left
                p.burst = p.burst - p.quantum
                # update time and check is waiting process ready
                for i in range(p.quantum):
                    self.t1.timerRun(1)
                    self.checkReady()

                # update state and print msg
                p.state = "Paused"
                extra_info = {'time': self.t1.timer, 'user': p.user, 'processId': p.id}
                logging.info('Paused', extra=extra_info)

                # add back to ready queue
                self.readyQueue.append(p)
                break


