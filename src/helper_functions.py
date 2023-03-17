import numpy

def find_list_mean(lst):
    sum = 0
    for i in range (len(lst)):
        # Sum the values in the list
        sum += float(lst[i])
    # Divide the sum by the length of the list to find the mean    
    mean = sum/len(lst)
    return round(mean, 4)
