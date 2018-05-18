##
# Sources:
# https://www.youtube.com/watch?v=h3l4qz76JhQ   <-for NNet in python
# https://www.youtube.com/watch?v=262XJe2I2D0   <-for NNet in python
# http://stackoverflow.com/questions/2148543/how-to-write-a-confusion-matrix-in-python  <-for conf matrix
# http://stackoverflow.com/questions/9001509/how-can-i-sort-a-dictionary-by-key  <-for sorting dictionaries

import numpy as np
from random import randrange
from math import exp
import pandas as pd
import sys

# Global Code
input_nodes_ct=(8*8*3)
hidden_nodes_ct = 16  # can be changed to test performance
output_nodes_ct = 4
#learning_rate = .5  # can be changed? #this gets reduced each gradient check? (1/t)
orientation_list = [0, 90, 180, 270]

# Correspond the 1s to the orientation_list
base_vector = [[1.0, 0, 0, 0], \
               [0, 1.0, 0, 0], \
               [0, 0, 1.0, 0], \
               [0, 0, 0, 1.0]]

def target_index(actual):
    if actual == '0':
        return base_vector[0]
    elif actual == '90':
        return base_vector[1]
    elif actual == '180':
        return base_vector[2]
    elif actual == '270':
        return base_vector[3]
    else:
        print "You broke it..."

# List of the nodes for the input, hidden, and output layer (hid_ln = "hidden layer nodes")
# Also works for ranges (used a lot)
inp_ln = range(0, input_nodes_ct)
hid_ln = range(input_nodes_ct, input_nodes_ct + hidden_nodes_ct)
out_ln = range(input_nodes_ct+hidden_nodes_ct, input_nodes_ct+hidden_nodes_ct+output_nodes_ct)


# Sigmoid and Derivative functions
def sigmoid(num):
    return float(1.0 / (1.0 + exp(-num)))

def deriv_sig(num):
    return float(sigmoid(num) * (1.0-sigmoid(num)))


# Saw something similar in a youtube video and can't find the video now to source...
#def rand(low_range, high_range):
    #return randrange(low_range, high_range)


# Sum-product of the weights and input values (w*a)
def sum_w_a(prop, weights, activated, n, node_range):
    Sum = 0
    if prop == "Forward":
        for i in node_range:
            Sum += weights[(i, n)] * activated[i]
    elif prop == "Backward":
        for i in node_range:
            Sum += weights[(n, i)] * activated[i]
    return Sum


def random_weights(Weights):
    for i in xrange(input_nodes_ct):
        for j in xrange(hidden_nodes_ct):
            Weights[(i, j + input_nodes_ct)] = float(np.random.uniform(-0.10, 0.10))
    for i in xrange(hidden_nodes_ct):
        for j in xrange(output_nodes_ct):
            Weights[(i + input_nodes_ct, j + input_nodes_ct + hidden_nodes_ct)] = float(np.random.uniform(-0.10, 0.10))
    return Weights


def trained_weights(Weights, Activation, Error, learning_rate):

    for i in xrange(input_nodes_ct):
        for j in xrange(hidden_nodes_ct):
            Weights[(i, j + input_nodes_ct)] += Activation[i] * Error[j + input_nodes_ct] * learning_rate

    for i in xrange(hidden_nodes_ct):
        for j in xrange(output_nodes_ct):
            Weights[(i + input_nodes_ct, j + input_nodes_ct + hidden_nodes_ct)] \
                += Activation[i + input_nodes_ct] * Error[j + input_nodes_ct + hidden_nodes_ct] * learning_rate
    #print "ADJUSTED W: ",Weights
    return Weights


def print_Conf_Matrix(Actuals, Predictions):

    actual = pd.Series(Actuals, name='Actual')
    predicted = pd.Series(Predictions, name='Predicted')
    return pd.crosstab(actual, predicted, rownames=['Actual'], colnames=['Predicted'], margins=True)


def write_model_file(Train_W, file_name):

    weights = open(file_name, 'w')
    for i, j in Train_W.items():
        weights.write(str(i[0])+" "+str(i[1])+" "+str(j)+"\n")
    weights.close()


def read_model_file(file_name):

    weights = open(file_name, 'r')
    data = {}
    for line in weights:
        line = line.split()
        data[(int(line[0]), int(line[1]))] = float(line[2])
    return data





# Training Begins!!!
def train(train_data):
    print "-- TRAINING BEGINS --"
    correct_count = 0
    temp = {}
    weights = random_weights(temp)
    ct = 0
    tally =0
    learning_rate=5
    for i in train_data.keys():
        Activation = {}
        input_dict = {}  # Dictionary for Input values (x)
        error_dict = {}  # Dictionary for Error values
        output_orientation = []
        check = None  # will use this for accuracy check
        likely_orientation = 0
        actual_orientation = train_data[i][0]
        ct += 1
        for node in inp_ln:
            Activation[node] = float(train_data[i][1][node])/float(255)  # 255 because of the color scale

        for node in hid_ln:
            input_dict[node] = 1+sum_w_a("Forward", weights, Activation, node, inp_ln)
            Activation[node] = sigmoid(input_dict[node])

        for node in out_ln:
            input_dict[node] = 1+sum_w_a("Forward", weights, Activation, node, hid_ln)+1

            Activation[node] = sigmoid(input_dict[node])
            output_orientation.append(Activation[node])

        likely_orientation += orientation_list[output_orientation.index(max(output_orientation))]

        if str(likely_orientation) == str(actual_orientation):
            correct_count += 1
            check = 1
        else:
            check = 0

        # Code for Back Propagation error calculations
        for node in out_ln:
            error_dict[node] = deriv_sig(input_dict[node])*(target_index(actual_orientation)[node - (input_nodes_ct+hidden_nodes_ct)] - Activation[node])
        for node in hid_ln:
            error_dict[node] = deriv_sig(input_dict[node])*sum_w_a("Backward", weights, Activation, node, out_ln)

        weights = trained_weights(weights, Activation, error_dict,learning_rate)
        learning_rate = learning_rate*.9
        tally+=1
    print "TRAINING NOW COMPLETE"
    return weights


# Testing Begins!!!
def test(test_data, Weights):  # uses the weights from the training -> see "def trained_weights"
    print "-- TESTING BEGINS --"
    output_file = open("nnet_output.txt", 'w')
    Activation = {}
    input_dict = {}  # Dictionary for Input values (x)
    actual_orient_list = []  # for CM
    calc_orient_list = []  # for CM
    correct_count = 0
    correct_list=[]
    for i in test_data.keys():
        output_orientation = []

        CM={}
        check = None  # will use this for accuracy check
        likely_orientation = 0
        actual_orientation = test_data[i][0]
        actual_orient_list.append(int(actual_orientation))

        for node in inp_ln:
            Activation[node] = float(test_data[i][1][node]) / float(255)  # 255 because of the color scale

        for node in hid_ln:
            input_dict[node] = 1+sum_w_a('Forward', Weights, Activation, node, inp_ln)
            Activation[node] = sigmoid(input_dict[node])

        for node in out_ln:
            input_dict[node] = 1+sum_w_a('Forward', Weights, Activation, node, hid_ln)
            Activation[node] = sigmoid(input_dict[node])
            output_orientation.append(Activation[node])

        """Here is the output that can drive you mad..."""
        #print output_orientation

        likely_orientation += orientation_list[output_orientation.index(max(output_orientation))] #-1
        calc_orient_list.append(likely_orientation)
        output_file.write(str(i) + ' ' + str(likely_orientation) + '\n')

        if str(likely_orientation) == str(actual_orientation):
            correct_count += 1
            correct_list.append(i)

    print "CORRECTLY COMPUTED:  ",correct_count,correct_list
    print "ACCURACY:  ",float(correct_count)/float(len(test_data))*100,"%"
    print "\n   CONFUSION MATRIX"
    print print_Conf_Matrix(actual_orient_list, calc_orient_list)  # prints the conf matrix from Pandas
    output_file.close()

def nnet(mode, file_data, output_model):
    if mode.lower() == 'train':
        write_model_file(train(file_data),str(output_model))  # may need to pass the last sys.argv for the file name
    if mode.lower() == 'test':
        test_weights = read_model_file(str(output_model))  # may need to pass the last sys.argv for the file name
        test(file_data, test_weights)
    "./orient.py nnet train train_file.txt model_file.txt   or\n"
    "./orient.py nnet test test_file.txt model_file.txt"
