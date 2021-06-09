import numpy as np
board_cols = 10
board_rows = 10

board = [[0 for i in range(board_cols)] for j in range(board_rows)]
d = {(0, 0): -50.94, (0, 1): -73.69, (0, 2): -78.56, (0, 3): -82.83, (0, 4): -86.84, (0, 5): -88.23, (0, 6): -89.94, (0, 7): -91.52, (0, 8): -92.96, (0, 9): -93.97, (1, 0): -15.5, (1, 1): -29.16, (1, 2): -49.02, (1, 3): -68.1, (1, 4): -74.62, (1, 5): -79.85, (1, 6): -88.65, (1, 7): -92.93, (1, 8): -95.08, (1, 9): -96.01, (2, 0): -0.03, (2, 1): -1.84, (2, 2): -14.37, (2, 3): -36.08, (2, 4): -100.0, (2, 5): -100.0, (2, 6): -100.0, (2, 7): -100.0, (2, 8): -79.04, (2, 9): -100.0, (3, 0): -0.05, (3, 1): -0.69, (3, 2): -3.41, (3, 3): -0.72, (3, 4): 0, (3, 5): 0, (3, 6): 0, (3, 7): 0, (3, 8): -0.07, (3, 9): 0, (4, 0): -0.08, (4, 1): -0.56, (4, 2): -2.69, (4, 3): -0.91, (4, 4): -0.01, (4, 5): 0, (4, 6): 0, (4, 7): -0.8, (4, 8): -0.09, (4, 9): 0, (5, 0): -0.05, (5, 1): -0.16, (5, 2): -16.8, (5, 3): -7.2, (5, 4): -0.03, (5, 5): 0, (5, 6): 0, (5, 7): -4.0, (5, 8): -0.01, (5, 9): 0, (6, 0): -0.27, (6, 1): -0.8, (6, 2): -100.0, (6, 3): -20.0, (6, 4): -0.16, (6, 5): 0, (6, 6): 0, (6, 7): -20.0, (6, 8): -0.03, (6, 9): -0.16, (7, 0): -0.49, (7, 1): -4.0, (7, 2): 0, (7, 3): -100.0, (7, 4): -0.8, (7, 5): 0, (7, 6): 0, (7, 7): -100.0, (7, 8): 0, (7, 9): -0.8, (8, 0): -3.36, (8, 1): -20.0, (8, 2): -100.0, (8, 3): -20.0, (8, 4): -4.0, (8, 5): 0, (8, 6): 0, (8, 7): 0, (8, 8): -20.0, (8, 9): -4.0, (9, 0): -0.8, (9, 1): -20.0, (9, 2): -100.0, (9, 3): -100.0, (9, 4): 0, (9, 5): 0, (9, 6): 0, (9, 7): 0, (9, 8): -100.0, (9, 9): 0}
for k,v in d.items():
    board[k[0]][k[1]] = v
print(board)

def mapper(board):
    reflection = [[0 for i in range(board_cols)] for j in range(board_rows)]
    
    boundary = [-100 for i in range(board_cols+2)]
    board.insert(0,boundary)
    board.append(boundary)
    for i in range(board_rows+1):
        if i != 0 and i != len(board)-1:
            board[i].insert(0,-100)
            board[i].append(-100)
    #for i in board:
     #   print(i,len(i))
        
        
        
    for i in range(1,len(board)-1):
        #print(board[i])
        for j in range(1,len(board[i])-1):
            #print(i,j)
            if board[i][j] != -100:
                bigOne = max([board[i-1][j],board[i+1][j],board[i][j-1],board[i][j+1]])
                if board[i-1][j] == bigOne and board[i-1][j] >= board[i][j]:
                    reflection[i-1][j-1] = 'U'
                elif board[i+1][j] == bigOne and board[i+1][j] >= board[i][j]:
                    reflection[i-1][j-1] = 'D'
                elif board[i][j-1] == bigOne and board[i][j-1] >= board[i][j]:
                    reflection[i-1][j-1] = 'L'
                elif board[i][j+1] == bigOne and board[i][j+1] >= board[i][j]:
                    reflection[i-1][j-1] = 'R'
    for i in reflection:
        print(i)

mapper(board)         
