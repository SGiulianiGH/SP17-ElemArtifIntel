#!/usr/bin/env python

"""
#    Orient Classifier
"""

import time
import sys
import math
from NearestNeighbor import NN
from NeuralNet import nnet


def neighbor_main(train_file, test_file, algo):

    train_data = {}
    test_data = {}

    print "\nLoading Training File...\n"

    # Dictionary Format: { Picture file name : orientation, r11, g11, b11, r12, g12...b88 }
    with open(train_file, "r") as trainFile:

        for img in trainFile.readlines():
            img_data = img.split()
            train_data[img_data[0] + " " + img_data[1]] = (img_data[1], img_data[2:])

    print "\nLoading Test File...\n"

    with open(test_file, "r") as testFile:

        for img in testFile.readlines():
            img_data = img.split()
            test_data[img_data[0]] = (img_data[1], img_data[2:])

    if algo.lower() == "nearest":
        # 36,976 train img, 943 test img. 943 * 36,976 = 34,868,368 comparisons!
        results = NN(train_data, test_data)
        Conf_Matrix(results)
    else:
        sys.exit("Tried for Nearest Neightbors, check arguments")

def nnet_main(data_file, model_file, algo, mode):

    all_data = {}

    print "\nLoading File...\n"

    # Dictionary Format: { Picture file name : orientation, r11, g11, b11, r12, g12...b88 }
    with open(data_file, "r") as dataFile:

        for img in dataFile.readlines():
            img_data = img.split()
            all_data[img_data[0] + " " + img_data[1]] = (img_data[1], img_data[2:])
    """
    print "\nLoading Test File...\n"

    with open(data_file, "r") as testFile:

        for img in testFile.readlines():
            img_data = img.split()
            test_data[img_data[0]] = (img_data[1], img_data[2:])
    """
    if algo == 'nnet':
        results = nnet(mode, all_data, model_file)
    else:
        sys.exit("Tried for Nearest Neightbors, check arguments")


def Conf_Matrix(results_data):
    header = ["0   | ", "90  | ", "180 | ", "270 | "]

    print "             0       90      180      270"
    print "     ------------------------------------"

    for i in range(4):
        current_row = header[i]
        for j in range(4):
            current_row += "%8s " % (results_data[orients[i]][orients[j]])
        print current_row

    n = float(sum([sum(results_data[orient].values()) for orient in orients]))

    print "Accuracy: ", (sum([results_data[orient][orient] for orient in orients]) / n)*100,"%"

    error = 0
    for orient in orients:
        for orient_2 in orients:
            if orient != orient_2:
                error += results_data[orient][orient_2]

    print "Misclassification Rate(Error Rate): ", (error / n)*100,"%"
    print "             True Rates        False Rates"

    for orient in orients:
        print "%8s : %-15s   %-15s" % ( \
            orient, \
            results_data[orient][orient] / float(sum([results_data[orient_2][orient] for orient_2 in orients])), \
            sum([results_data[orient_2][orient] for orient_2 in orients if orient_2 != orient]) / float(
                sum([results_data[orient_2][orient] for orient_2 in orients])))

    print "\n"


#======================================================================
# Program Start
start_time = time.time()

orients = ["0", "90", "180", "270"]

# FOR TESTING PURPOSES
#neighbor_main('train-data.txt','test-data.txt','nearest')
#nnet_main('test-data.txt','model-file.txt','nnet', 'test')


# ./orient.py nearest train_file.txt test_file.txt
if sys.argv[1].lower() == 'nearest':
    if len(sys.argv) > 4:
        sys.exit(
            "For Nearest Neightbor, expecting a command similar to:\n"
            "./orient.py nearst train-data.txt test-data.txt")
    _algo = sys.argv[1].lower()
    _train_file = sys.argv[2]
    _test_file = sys.argv[3]
    # Executes Nearest Neighbor
    neighbor_main(_train_file, _test_file, _algo)

# ./orient.py nnet train train_file.txt model_file.txt
# ./orient.py nnet test test_file.txt model_file.txt
if sys.argv[1].lower() == 'nnet':
    if len(sys.argv) < 5:
        sys.exit(
            "For Neural Net, expecting a command similar to:\n"
            "./orient.py nnet train train_file.txt model_file.txt   or\n"
            "./orient.py nnet test test_file.txt model_file.txt")
    _algo = sys.argv[1].lower()
    _mode = sys.argv[2].lower()
    _train_file = sys.argv[3]
    _model_file = sys.argv[4]
    nnet_main(_train_file, _model_file, _algo, _mode)


# Stephan, just add time at the beginning of the unix terminal command "time ./orient.py mode train test"
"Won't adding another argument to the command ruin the pickups from sys.argv?"

TotalTime = time.time() - start_time
print "Total TIME:    in Minutes:  ", TotalTime / 60.0
print "               in Seconds:  ", TotalTime
