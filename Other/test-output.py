#!/usr/bin/env python2
#author: Zehua Zhang
import subprocess
import sys


def check_board(board, n):
    for piece in board:
        if not (piece == 'w' or piece == 'b' or piece == 'W' or piece == 'B' or piece == '.'):
                return 'Incorrect output format. Usually it is because there are symbols other than w, b or . in the last line.'
    if len(board) != n**2:
        return 'Incorrect output format. Usually it is because the last line of your output is not a n*n board, where n is the length of the square board given by the first argument.'
    return 'Congratulations! Your output format looks great! :)'


def getboard(arg):
    proc = subprocess.Popen(arg, stdout=subprocess.PIPE)
    board =[]
    for line in proc.stdout:
        row = line.strip()
        board.append(row)
    try:
        if board[-1] == ['']:
            return board[-2]
        else:
            return board[-1]
    except IndexError:
        print('No board solution got after running your code. Usually it is because your code encountered some error when executed. Please debug it and try again.')
        return False

        
def checkinput(arg):
    correctIn = 1
    if not arg[1].isdigit(): 
        print('Incorrect input format. The first input argument should be the length of the board, which should be an integer.\n')
        correctIn = 0
    if not (arg[2] == 'w' or arg[2] == 'b'): 
        print('Incorrect input format. The second input argument should be either "w" or "b" to indicate whose turn it is now.\n')
        correctIn = 0
    if not all([piece == 'w' or piece == 'b' or piece == 'W' or piece == 'B' or piece == '.' for piece in arg[3]]): 
        print('Incorrect input format. The third input argument should be a string describe the board, which only contains "w", "W", "b", "B" or ".".\n')
        correctIn = 0
    if not arg[4].isdigit(): 
        print('Incorrect input format. The fourth input argument should be an integer to specify the time limit.\n')
        correctIn = 0
    return correctIn

def main():
    arg = sys.argv[1:]
    correctIn = checkinput(arg)
    if correctIn:
        if 'pikachu.py' in arg[0]:
            if len(arg) == 5:
                n = int(arg[1])
                board = getboard(arg)
                if board:
                    print(check_board(board, n))
            else:
                print('Incorrect way to execute the code. Usually it is because the number of arguments you passed through commandline is too few or too many.')
        else:
            print('Your code name is not what we required.')

if __name__ == "__main__":
    main()