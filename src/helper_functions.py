import numpy

def find_list_mean(lst):
    sum = 0
    if len(lst) == 0:
         return 0
    for i in range (len(lst)):
        # Sum the values in the list
        sum += float(lst[i])
    # Divide the sum by the length of the list to find the mean    
    mean = sum/len(lst)
    return round(mean, 4)

def get_batch_means(buffer_occupancies):
    result = []
    for j in range (0,15):
        tmp = []
        for i in range (0, len(buffer_occupancies)):
                if list(buffer_occupancies.keys())[i] > (j * 100) and list(buffer_occupancies.keys())[i] <= ((j + 1) * 100):
                    tmp.append(list(buffer_occupancies.values())[i])
                    
        result.append(find_list_mean(tmp))

    return result
