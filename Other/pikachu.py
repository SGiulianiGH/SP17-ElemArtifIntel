#! /usr/bin/env python
###
# So here's to hoping you review the code itself:
# My partner and I were unable to develop a successor function that captures 'legal moves' for Pichus and Pikachus
# We realize that without the successor function there is no way to evaluate the value of each state; however we would
# like to explain our intentions to demonstrate we understand the application of using a completed algorithm.
#
# Minimax can be used to traverse the successors but this is a large feat as the state space is too large. Thus, we
# designed the code to take the min/max values as alpha and beta after evaluation, depending on which turn/node it was.
# Pichus are assigned values as 1 and -1, with Pikachus having 10x the pichu value. This is used within the evaluation
# function. After taking the successors at some depth and storing them in an external file as either a list of tuples
# or dictionary with the depth and new state (S'), the evaluation function determines a numerical value af each S'.
# the evaluation uses the position depth of each list of the board so that white pichus in positions closer to the
# len(N) list are more favorable (aka, it's better to become a Pikachu). Additionally, the evaluation function includes
# a sum of the overall board. This is to ensure a Pikachu and Pichus do not remain at the end of their boards.
# Finally, the recommended move is the move with the highest evaluation value (for the 'white' player).
#
# I am not personally experienced in python enough to develop a successor function and have therefore failed to
# produce a recommended move. Please review the code itself to determine the intended application.
#
# Feedback always welcome. It may not seem like it, but more hours went into this than my full-time job...
#   -Stephen

#########################################
import sys


print"++ GAME ON ++"
## Initial Setup
w_pichu = 1
b_pichu = -1
w_pikachu = 10*w_pichu
b_pikachu = 10*b_pichu

#takes a board (list of lists) and converts it to the required printable format
def final_print_conversion(B):
    cnv = []
    for i in B:
        for ii in i:
            cnv.append(ii)
    CNV = ['w' if x==w_pichu else 'b' if x==b_pichu else 'W' if x==w_pikachu else 'B' if x==b_pikachu else\
        '.' if x==0 else x for x in cnv]
    print ''.join(str(i) for i in CNV)

#counts the "1"s in the board, not used but may be needed later
c1=[]
def count_ones(board):
    for i in board:
        c = i.count(1)
        c1.append(c)
        print "SUM 1: ",sum(c1)
    return "Return 1: ",sum(c1)

#counts the "-1"s in the board, not used but may be needed later
cn1=[]
def count_neg_ones(board):
    for i in board:
        c = i.count(-1)
        cn1.append(c)
        print "SUM -1: ", sum(cn1)
    return "Return -1: ",cn1

#converts the board to a list so it can be counted in terminal state check
def counts(board):
    ct = []
    for i in board:
        for ii in i:
            ct.append(ii)
    return ct

#checks to see if the count of pichus/pikachus results in a win (if count for one color is 0, the other color wins)
def terminal(s):
    if counts(s).count(b_pichu) == 0 and counts(s).count(b_pikachu) == 0:
        print "'White' Wins!!"
    if counts(s).count(w_pichu) == 0 and counts(s).count(w_pikachu) == 0:
        print "'Black' Wins!!"
    else:
        return False


##Successor function for all states, s
#def succ(s):
print "_________________________________________________________________________________"
print "Unable to develop a successor function." \
      " Please see comments at head of .py file."


#Alpha-Beta Decision Action
# ...No function available as there is no SUCC() function
print "...therefore no actual application to test alpha-beta pruning action."
print "_________________________________________________________________________________\n"

## MAX Value
def max_value(s, alpha, beta):
    if terminal(s):
        return s
    for i in succ(s):
        alpha = max(alpha,min_value(i,alpha,beta))
        if alpha >= beta:
            return alpha
        return alpha

## MIN Value
def min_value(s, alpha, beta):
    if terminal(s):
        return s
    for i in succ(s):
        beta = min(beta,max_value(i, alpha, beta))
        if alpha >= beta:
            return beta
        return beta

## Evaluation Algorithm
def evaluation(B):

    #sums the rows of the board and multiplies by the row# for a weighted progress to get to row n
    def weight_row(B):
        n = 0
        ttl = 0
        for i in map(sum, B):
            n += 1
            if i == N * w_pichu:
                ttl += i * n
        return ttl

    #sum of the board * 10, so more favorable with more Pikachus and less b-pichus/pikachus
    def board_total(B):
        return 10*sum(map(sum,B))
    #returning the sum of these elements as the evaluation total
    #print "Weighted Row: ",weight_row(B)
    #print "Board Total: ",board_total(B)
    return weight_row(B)+board_total(B)

#converts the input board to an array
def input_convert(B):
    list_board = [w_pichu if x=='w' else b_pichu if x=='b' else 0 if x=='.' else w_pikachu if x=='W' else b_pikachu if x=='B' else x for x in B]
    array_board = [list_board[i:i+N] for i in range(0, len(list_board), N)]
    return array_board


## MAIN ##

(board_size, player_color, board_input, run_time) = sys.argv[1:]
N = board_size
player = player_color
#initial_board = input_convert(str(board_input))
#print "Evaluation value of current state: ",evaluation(initial_board)
print "Recommended Move:\n - No moves recommended; no SUCCESSOR function found.\n - Forfeit or draw?"

#print final_print_conversion(initial_board)
print board_input
