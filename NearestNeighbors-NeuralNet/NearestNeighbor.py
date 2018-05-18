#!/usr/bin/env python

"""


"""

import sys
import math
#from orient import Conf_Matrix

def euclidean_dist_calc(train_pixels, test_pixels):

    """
    dist = 0
    for i in xrange(0, len(train_pixels), 3):
        a = float(test_pixels[i]) - float(train_pixels[i])     # Red
        b = float(test_pixels[i+1]) - float(train_pixels[i+1]) # Green
        c = float(test_pixels[i+2]) - float(train_pixels[i+2]) # Blue
        dist += a**2 + b**2 + c**2 
    dist = sum([ (float(test_pixels[i]) for i in range(len(train)  - sum([float(train_pixels[i]))**2 for i in range(len(train_pixels)) ])
    """

    dist = sum([ (float(test_pixels[i]) - float(train_pixels[i]))**2 for i in range(len(train_pixels)) ])
    return math.sqrt(dist)

    # SOURCE: http://www.codehamster.com/2015/03/09/different-ways-to-calculate-the-euclidean-distance-in-python/
    # ANOTHER OPTION:
    # def euclidean4(vector1, vector2):
    # ''' use |from scipy.spatial import distance| to calculate the euclidean distance. '''
    #     dist = distance.euclidean(vector1, vector2)
    #     return dist

def NN(train_data, test_data):

    print "\nRunning Nearest Neighbor Classifier...\n"

    orients = ["0", "90", "180", "270"]
    correct = 0
    # for Confustion Matrix [Predicted, Actual]
    results_data = {}
    for orient in orients:
        results_data[orient] = {}
        for orient_2 in orients:
            results_data[orient][orient_2] = 0

    img_dist_to_zero = {}
    for train_key in train_data.keys():
        img_dist_to_zero[train_key] = euclidean_dist_calc(train_data[train_key][1], [0]*192)


    results_file = open("nearest_output.txt", "w")
    ct = 0
    for test_key in test_data.keys():
        #print test_key
        ct+=1
        if ct % 50 == 0:
            print "Testing image", ct,"of",len(test_data.keys())
        actual_orient = test_data[test_key][0]

        test_dist = euclidean_dist_calc(test_data[test_key][1], [0]*192)
        tmp = {}

        # Filter
        for key in train_data.keys():
            if math.fabs(img_dist_to_zero[key] - test_dist) < 10:
                tmp[key] = train_data[key]
        #print tmp_img_dist_to_zero

        nearest_neighbor_orient = None 
        nearest_neighbor_val = float("inf")

        for train_key in tmp.keys():
            
            current_val = euclidean_dist_calc(tmp[train_key][1], test_data[test_key][1])
            if current_val < nearest_neighbor_val:
                nearest_neighbor_orient = tmp[train_key][0]
                nearest_neighbor_val = current_val

            results_data[nearest_neighbor_orient][actual_orient] += 1

        results_file.write("%s %s" % (test_key, nearest_neighbor_orient)+"\n")

        if str(nearest_neighbor_orient) == str(actual_orient):
            correct+=1
    # Accuracy -- nevermind, prints via orient.py
    #print "Accuracy:",float(correct)/float(len(test_data.keys()))*100,"%"
    results_file.close()

    return results_data

