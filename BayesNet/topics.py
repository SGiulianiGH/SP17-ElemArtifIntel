#!/usr/bin/env python

import os
import sys
import math
from itertools import islice

class BayesNet():
    def __init__(self):

        self.Doc = 1.0 # Use 1 / |D| ? Constant
        self.T_given_D = {} # 1.0 / 20.0
        self.W_given_T = {}


    def train(self):

        total_T = 0
        totals_W = {}

        for (roots, dirs, files) in os.walk(_dataSetDir):
            print "Directory: ", roots

            topic = os.path.split(roots)[-1] 

            if topic == "train":
               continue

            self.T_given_D[topic] = 0 
            self.W_given_T[topic] = {}
            totals_W[topic] = 0

            for f in files:

                self.T_given_D[topic] += 1
                total_T += 1

                with open("%s/%s" % (roots, f), "r") as fp:

                    for line in fp.readlines():
                        for word in line.split():

                           word = ("".join([ c for c in word if c.isalpha() ])).lower()

                           if not word:
                               continue

                           if word in self.W_given_T[topic]:   
                              self.W_given_T[topic][word] += 1
                           else:
                              self.W_given_T[topic][word] = 1

                           totals_W[topic] += 1

        # Convert Counts to Probabilities
        for topic in topics:
            self.T_given_D[topic] = float(self.T_given_D[topic]) / float(total_T)

            for word in self.W_given_T[topic].keys():
                self.W_given_T[topic][word] = float(self.W_given_T[topic][word]) / float(totals_W[topic])


    def writeModelToFile(self, name):

        with open(_modelFile, "w") as fp:
            
            for key, val in self.T_given_D.iteritems():

                fp.write("%s %s\n" % (key, val))

            for topic in topics:

                fp.write("%s %d\n" % (topic, len(self.W_given_T[topic])))

                for word in self.W_given_T[topic].keys():
                    fp.write("%s %f\n" % (word, self.W_given_T[topic][word]))
                    

    def readModelFile(self, modelFile):

        with open(modelFile, "r") as fp:

            lines = fp.readlines()
                
            # Read Topic Lines (name, count)
            for row in range(len(topics)):
                line = lines[row].strip().split()
                bayesNet.T_given_D[line[0]] = float(line[1])
            l = len(topics)  
            lines = lines[l:]

            while lines:

                # Read Word Lines
                headerLine = lines[0].strip().split()
                topic = headerLine[0]
                count = int(headerLine[1])
                    
                bayesNet.W_given_T[topic] = {}

                for row in range(count):
                    line = lines[row].strip().split()
                    bayesNet.W_given_T[topic][line[0]] = float(line[1])

                lines = lines[(count+1):]


    def bayesLaw(self, topic, word):
        top = (self.W_given_T[topic][word] * self.T_given_D[topic]) if word in self.W_given_T[topic] else 0.0
        bottom = sum([ (self.W_given_T[topic_2][word] * self.T_given_D[topic_2]) if word in self.W_given_T[topic_2] else 1.0 for topic_2 in topics ])
        return top / bottom


def printConfusionMatrix(results_data): 
    print "\nConfusion Matrix:"
    print " a\p   athe auto base chri cryp elec fors grap guns hock  mac medi mide moto   pc poli reli spac wind xwin"
    print "      ----------------------------------------------------------------------------------------------------"   
        
       
    for row in range(len(topics)):
        current_row = headers[row] + " |"
        for col in range(len(topics)):
            current_row += " %4s" % (results_data[topics[row]][topics[col]],)
        print current_row
    print "\n"

# =====================================================================================================
# Program Start

_mode = sys.argv[1].lower()
_dataSetDir = sys.argv[2]
_modelFile = sys.argv[3]

topics = ["atheism", "religion", "christian", "motorcycles", "pc", "windows", "medical", "space", "crypto", "xwindows", "autos", "mac", "baseball", "hockey", "mideast", "graphics", "politics", "electronics", "forsale", "guns"]
headers = ["athe", "auto", "base", "chri", "cryp", "elec", "fors", "grap", "guns", "hock", "mac ", "medi", "mide", "moto", "pc  ", "poli", "reli", "spac", "wind", "xwin"]
topics.sort()

#topic neutral words
#neutralWords = ["the", "a", "of", "an", "there"]


if not os.path.isdir(_dataSetDir):
    sys.exit("Error! Invalid Data Set Directory.")


if _mode == "train":
    print "\nTraining...\n"
    
    bayesNet = BayesNet()
    bayesNet.train()
    bayesNet.writeModelToFile(_modelFile)

    with open("distinctive_words.txt", "w") as fp:

        for topic in topics:

            bestWords = []

            for word in bayesNet.W_given_T[topic].keys():
                bestWords.append( (word, bayesNet.bayesLaw(topic, word)) )

            bestWords = list(sorted(bestWords, key=lambda tup: tup[1]))

            #print bestWords[-10:]
            fp.write("%s\n" % topic)
            for entry in bestWords[-11:-1]:
                fp.write("%s\n" % (entry[0]))
            fp.write("\n")

        # output 10 words with max P(T=t_i | W_j)

elif _mode == "test":
    print "\nTesting...\n"

    bayesNet = BayesNet()
    bayesNet.readModelFile(_modelFile)

    # Set up data for Confusion Matrix
    results_data =  {}

    for topic in topics:
        results_data[topic] = {}
        for topic_2 in topics:
            results_data[topic][topic_2] = 0.0

    for (roots, dirs, files) in os.walk(_dataSetDir, topdown=False):
        print "Next directory: ", roots

        actual = os.path.split(roots)[-1] 
        for f in files:

            with open("%s/%s" % (roots, f), "r") as fp:

                # Iterate through words
                wordSet = " ".join(fp.readlines()).split()

                for word in range(len(wordSet)):
                    wordSet[word] = ("".join([ c for c in wordSet[word] if c.isalpha() ])).lower()

                # Remove empty strings and neutral words
                wordSet = [ word for word in wordSet if word ]

                maxValue = float("inf")
                predicted = None

                for topic in topics:

                    tmp_wordSet = wordSet[:]
                    tmp_wordSet = [ word for word in tmp_wordSet if word in bayesNet.W_given_T[topic] ]
                    currentValue = math.log(bayesNet.T_given_D[topic]) + sum([ math.log(bayesNet.W_given_T[topic][word]) for word in tmp_wordSet ])

                    if currentValue < maxValue:
                        maxValue = currentValue
                        predicted = topic
                        
                results_data[actual][predicted] += 1
                #if actual != predicted:
                #    print predicted, actual

    printConfusionMatrix(results_data)

    #Accuracy Report
    n = float(sum([ sum(results_data[topic].values()) for topic in topics ]))

    print "Accuracy: ", sum([ results_data[topic][topic] for topic in topics]) / n

    error = 0
    for topic in topics:
        for topic_2 in topics:
            if topic != topic_2:
                error += results_data[topic][topic_2]

    print "Misclassification Rate(Error Rate): ", error / n

    print "             True Rates        False Rates"
    for i in range(len(topics)):

        topic_error = {}
        for topic in topics:
            for topic_2 in topics:
                if topic != topic_2:
                    error += results_data[topic][topic_2]

        print "%8s : %-15s   %-15s" % ( \
              headers[i], \
              results_data[topics[i]][topics[i]] / sum([ results_data[topic_2][topics[i]] for topic_2 in topics]), \
              sum([ results_data[topic_2][topics[i]] for topic_2 in topics if topic_2 != topics[i] ]) / sum([ results_data[topic_2][topics[i]] for topic_2 in topics]))

    print "\n"    

else:
    sys.exit("Error! Invalid mode.")

