"""
COMP 614
Homework 3: Stock Prediction
"""

import comp614_module3 as stocks
import random


def markov_chain(data, order):
    """
    Creates and returns a Markov chain with the given order from the given data.

    inputs:
        - data: a list of ints or floats representing previously collected data
        - order: an integer repesenting the desired order of the Markov chain

    returns: a dictionary that represents the Markov chain
    """ 
    
    # temp dict
    # keys are transition states
    # values list value that comes after transition state
    # temp dict
    # keys are transition states
    # values list value that comes after transition state 
    # find all states
    temp_dict = {}
    window_size = order
    #windows = []
    for index_i in range(len(data) - window_size):
        key_state = tuple(data[index_i:index_i+order])
        trans_state = data[index_i+order]
        if key_state in temp_dict.keys():
            temp_dict[key_state].append(trans_state)
        else:
            temp_dict[key_state] = [trans_state]
    
    # dictionary for number of occurances for each bin
    out_put = {}
    for key, value in temp_dict.items():
        out_put[key] = dict((x, value.count(x)) for x in set(value))

    for _, prob in out_put.items():
        total_num = 0
        #print (prob)
        for bi_n, occur in prob.items():
            total_num += occur
        for bi_n, occur in prob.items():
            prob[bi_n] = occur/total_num
    
    return out_put


def predict(model, last, num):
    """
    Predicts the next num values given the model and the last values.

    inputs:
        - model: a dictionary representing a Markov chain
        - last: a list (with length of the order of the Markov chain)
                representing the previous states
        - num: an integer representing the number of desired future states

    returns: a list of integers that are the next num states
    """
    
    if len(model) == 0 or num == 0:
        return []

    last_tup = tuple(last)

    out_put = []
    for _ in range(num):
        if last_tup in model:
            val_dict = model.get(last_tup)
            weight_choice = list(val_dict.keys())
            val_prob = list(val_dict.values())
            
            rand_w = random.random()
            for ind_i in range(len(weight_choice)):
                print(rand_w)
                if rand_w <= val_prob[ind_i]:
                    add_c = weight_choice[ind_i]
                    break
                rand_w -= val_prob[ind_i]
        else:
            weight_choice = [0, 1, 2, 3]
            add_c = (random.choice(weight_choice))
        out_put.append(add_c)
        l_t = list(last_tup)
        f_1 = l_t[1:]
        f_1.append(add_c)
        last_tup = tuple(f_1)
    return out_put


print(predict({(0,): {1: 1}, (1,): {0: 1}}, [0], 1))


def mse(result, expected):
    """
    Calculates the mean squared error between two data sets. Assumes that the 
    two data sets have the same length.
    
    inputs:
        - result: a list of integers or floats representing the actual output
        - expected: a list of integers or floats representing the predicted output

    returns: a float that is the mean squared error between the two data sets
    """
    sum_vals = 0  
    len_n = len(result) 
    for index_i in range (0,len_n):  
        diff_s = result[index_i] - expected[index_i]  
        squared_difference = diff_s**2  
        sum_vals = sum_vals + squared_difference  
    m_s_e = sum_vals/len_n
    return m_s_e


def run_experiment(train, order, test, future, actual, trials):
    """
    Runs an experiment to predict the future of the test data based on the
    given training data.

    inputs:
        - train: a list of integers representing past stock price data
        - order: an integer representing the order of the markov chain
                 that will be used
        - test: a list of integers of length "order" representing past
                stock price data (different time period than "train")
        - future: an integer representing the number of future days to
                  predict
        - actual: a list representing the actual results for the next
                  "future" days
        - trials: an integer representing the number of trials to run

    returns: a float that is the mean squared error over the number of trials
    """
    trials_arr = []
    for _ in range(trials):
        mark_ch = markov_chain(train, order)
        predicted_res = predict(mark_ch, test, future)
        trials_arr.append(mse(predicted_res, actual))
    out_put = sum(trials_arr)/trials
    return out_put


def run():
    """
    Runs the stock prediction application. You should not modify this function!
    """
    # Get the supported stock symbols
    symbols = stocks.get_supported_symbols()

    # Load the training data
    changes = {}
    bins = {}
    for symbol in symbols:
        prices = stocks.get_historical_prices(symbol)
        changes[symbol] = stocks.compute_daily_change(prices)
        bins[symbol] = stocks.bin_daily_changes(changes[symbol])

    # Load the test data
    testchanges = {}
    testbins = {}
    for symbol in symbols:
        testprices = stocks.get_test_prices(symbol)
        testchanges[symbol] = stocks.compute_daily_change(testprices)
        testbins[symbol] = stocks.bin_daily_changes(testchanges[symbol])

    # Display data
    stocks.plot_daily_change(changes)
    stocks.plot_bin_histogram(bins)

    # Run experiments
    orders = [1, 3, 5, 7, 9]
    ntrials = 500
    days = 5

    for symbol in symbols:
        print(symbol)
        print("====")
        print("Actual:", testbins[symbol][-days:])
        for order in orders:
            error = run_experiment(bins[symbol], order,
                                   testbins[symbol][-order-days:-days], days,
                                   testbins[symbol][-days:], ntrials)
            print("Order", order, ":", error)
        print()

        
# You may want to keep this call commented out while you're writing & testing
# your code. Uncomment it when you're ready to run the experiments.
# run()