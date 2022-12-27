

from process import Process
from scheduler import Scheduler
import sys



if __name__ == '__main__':
    # dict storing username and num of process
    dict = {}
    # lists to store arrival, burst, processes
    arrival = []
    burst = []
    list = []

    # read from file and append to lists
    with open("input.txt", 'r') as data:
        # time quantum
        time_quant = int(data.readline())
        for line in data:
            input = line.split()
            if input[0].isalpha():
                dict[input[0]] = int(input[1])
            else:
                arrival.append(int(input[0]))
                burst.append(int(input[1]))


    # create processes and append to list
    count = 0
    for user in dict:
        for i in range(dict[user]):
            list.append(Process(i, arrival[count+i], burst[count+i], user))
        count += dict[user]

    # open output file
    output_file = open('output.txt', 'w')

    # scheduling
    scheduler = Scheduler(list, time_quant)

