'''
Programming Assignment 1
Mergesort using Multithreading

Team members:
Laura Hang
Nabila Tabassum
Jaskirat Kaur


'''



from math import ceil
import logging
from threading import Thread, current_thread

#divides our list to two sub-lists
def divide_the_arraylist(array: list):
    #length of the array
    length = len(array)
    #index of the middle of the array, ceil is used to round a number upward to its nearest integer, in case the array length is odd
    mid_index = ceil(length/2)
    #retrun all the values of the left till mid_index in one sub array list and from the mid_index to the right most value into another sub array list
    return array[0:mid_index], array[mid_index:]


def merge_sort(i: list, j: list):
    #we denoted left and right by the following, i=left, j=right

    #merged_arr
    merged_arr =[]

    #we stored the reference of the original array by creating a shallow copy
    i_copy = i[:]
    j_copy = j[:]

    #we compare the first element from i array and j array
    #We need to exhaust both lists
    while len(i_copy) > 0 or len(j_copy) > 0 :
        if len(i_copy) > 0 and len(j_copy) > 0:     #if both lists are not exhausted, then:
            if i_copy[0] <= j_copy[0]:
                merged_arr.append(i_copy.pop(0))
            else:
                merged_arr.append(j_copy.pop(0))
        elif len(i_copy) > 0:   #If either one of the two lists is exhausted then continue extracting elements from the non-empty list.
            merged_arr.append(i_copy.pop(0))
        elif len(j_copy) > 0:
            merged_arr.append(j_copy.pop(0))
    return merged_arr                       #Finally, the function returns the merged list which now contains all initial elements in ascending order.


def threaded_mergesort(array: list, sorted_arr: list):
    #define the custom thread name
    extra_info = {'name id': current_thread().name}
    #add the extra info and 'started' to logging info
    logging.info('started', extra=extra_info)

    #array i which is 0 to mid, array j which is mid to the end
    i, j = divide_the_arraylist(array)

    if not j:
        #add elements of array to results array
        for x in array:
            sorted_arr.append(x)

        #print finished msg with added extra info (name id)
        logging.info(f'finished: {sorted_arr}', extra=extra_info)
        return

    #
    i_result = []
    j_result = []

    #
    i_thread = Thread(target=threaded_mergesort, args=(i,i_result))
    j_thread = Thread(target=threaded_mergesort, args=(j,j_result))

    #change name of the thread, adding 0 or 1 to the name id
    i_thread.name = current_thread().name + '0'
    j_thread.name = current_thread().name + '1'


    #start threads
    i_thread.start()
    j_thread.start()

    #join threads
    i_thread.join()
    j_thread.join()

    #add each element of sorted array from merge_sort function into sorted_arr
    sorted_arr.extend(merge_sort(i_result, j_result))

    #finished msg with sorted_arr and add extra info (name id)
    logging.info(f'finished: {sorted_arr}', extra=extra_info)



def call_threaded_mergesort(array: list):
    #modify the basic logging configurations
    #output into 'output.txt', what level we want to modify in, format of the printed str
    logging.basicConfig(filename='output.txt', level=logging.INFO, format='Thread %(name id)s %(message)s')


    #array to store results
    sorted_arr = []

    #change the name of the thread to 1
    current_thread().name = '1'
    #current_thread().ident = 1

    #call the threaded mergesort
    threaded_mergesort(array, sorted_arr)
    return





if __name__ == '__main__':
    #array = [3304, 8221, 26849, 14038, 1509, 6367, 7856, 21362]

    array = []

    #open input text file in read mode
    file = open('inputs.txt', 'r')

    #copy each element in the file as an integer into array
    for x in file:
        if type(x) == int:
            array.append(int(x))
        else:
            array.append(round(float(x)))

    #open an output text file, if it exists it overwrites it, if not, the file is created
    output_file = open('output.txt', 'w')

    #call the threaded mergesort func
    call_threaded_mergesort(array)

