"""
COMP 614
Homework 2: Statistics
"""

import math


def arithmetic_mean(data):
    """
    Given a list of numbers representing a data set, computes and returns 
    the arithmetic mean of the data set.
    """
    len_data = len(data)
    sum_data = 0
    if len_data == 0: 
        return None
    for num in data:
        sum_data += num
    mean = sum_data/len_data
    return mean


def pop_variance(data):
    """
    Given a list of numbers representing a data set, computes and returns 
    the population variance of the data set.
    """
    len_data = len(data)
    mean_data = arithmetic_mean(data)
    pop_var = 0
    diff_num_mean_sum = 0
    if len_data == 0: 
        return None
    for num in data:
        diff_num_mean_sum += (num-mean_data) ** 2
    pop_var = diff_num_mean_sum/len_data    
    return pop_var


def std_deviation(data):
    """
    Given a list of numbers representing a data set, computes and returns 
    the standard deviation of the data set.
    """
    len_data = len(data)
    if len_data == 0: 
        return None
    pop_var = pop_variance(data)
    std_dev = math.sqrt(pop_var)
    
    return std_dev


def moving_avg(data, num_days):
    """
    Given a list of numbers representing a data set and an integer representing
    a number of days, builds and returns a new list where the i-th element is 
    the average of the data over the input number of days starting at position
    i in the data list.
    """
    output = []
    index = 0
    if num_days >= len(data):
        return [arithmetic_mean(data)]
    if num_days <= 0:
        return None
    while index < len(data) - num_days + 1:
        # current sliding window
        window = data[index:index + num_days]
        window_avg = sum(window)/num_days
        output.append(window_avg)
        index += 1
    return output


def clean_with_deletion(data):
    """
    Given a list of lists representing a data set, cleans the data by creating
    and returning a new list of lists that contains the same data, minus any 
    rows that were originally missing values (denoted by None). Should not 
    mutate the original list.
    """
    output = []
    for row in data:
        deleted_row = False
        for item in row:
            if item == None:
                deleted_row = True
                del row	
                break
        if deleted_row == False:
            output.append(row)        
    return output


def column_avgs(data):
    """
    Given a list of lists representing a data set, returns a new list where the
    i-th element is the arithmetic mean of the i-th column in the data set.
    """
    output = []
    if len(data) == 1:
        return [None, None]
    skip_first_row = data[1:]
    transpose_data = list(zip(*skip_first_row))
    for lst in transpose_data:
        sum_elements = 0
        length = 0
        for number in lst:
            if number == None:  
                pass
            else:
                sum_elements += number
                length += 1
        if length == 0 or sum_elements == 0:
            output.append(None)
        else:
            output.append(sum_elements/length)
    return output


def clean_with_mean(data):
    """
    Given a list of lists representing a data set, cleans the data by creating
    and returning a new list of lists that contains the same data, but with
    any values that were originally missing (denoted by None) filled in with 
    the arithmetic mean of the corresponding column.
    """
    output = []
    pre_transpose_output = []
    col_avg = column_avgs(data)
    #print(col_avg)
    transpose_data = list(zip(*data))
    lst = [list(x) for x in transpose_data]
    #print (lst)
    curr_avg_index = 0
    for lst_index in lst:
        temp_list = []
        replace_num = col_avg[curr_avg_index]
        #print(lst_index)
        for index in lst_index:
            #print (index)
            if index == None:
                temp_list.append(replace_num)
            else:
                temp_list.append(index)
        curr_avg_index += 1
        pre_transpose_output.append(temp_list)
        #print(lst)
    #print(pre_transpose_output)
    #convert list of tuples to list of lists
    conversion_tup_list = [list(x) for x in pre_transpose_output]
    #print(conversion_tup_list)
    #transpose list 
    transpose_output = [list(zip(*conversion_tup_list))]
    #print(need_transpose_output)
    output = [list(x) for x in transpose_output]
    #print(output)
    #remove outer brackets
    while isinstance(output[0], list):
        output = output[0]
    output = [list(x) for x in output]
    return output













print(clean_with_mean([['a', 'b'], [1, -2], [-3, 4], [None, 6], [7, 8]]))