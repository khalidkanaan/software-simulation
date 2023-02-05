import numpy

def find_list_mean(lst):
    sum = 0
    for i in range (len(lst)):
        sum += float(lst[i])
    return sum/len(lst)

def exponential_dist(lst):
    return numpy.random.exponential(find_list_mean(lst))