import numpy as np

board_rows = 5
board_cols = 5

win_state = (5,5)
losing_states = [(9,2),(9,3),(9,4),(9,5),(9,6),(9,7),
                 (9,8),(8,2),(7,2),(7,3),(7,6),(7,7),
                 (7,8),(6,2),(2,4),(2,5),(2,6),(2,7),(2,9)]
start = (0,0)
deterministic = True

class Grid:
    def __init__(self, board_rows,board_cols,win_state,losing_state,start,deterministic):
        self.board_rows = board_rows
        self.board_cols = board_cols
        self.win_state = win_state
        self.losing_state = losing_state
        self.start = start
        self.deterministic = deterministic
        self.state = start
        self.isEnd = False

        self.board = np.zeros([board_rows,board_cols])
        for states in self.losing_state:
            self.board[states[0],states[1]] = -100
        self.board[win_state] = 100
        #Grid.showBoard(self)
        #print(self.board)

    def giveReward(self):
        print(self.state in self.losing_state)
        if self.state == self.win_state:
            return 100
        elif self.state in self.losing_state:
            return -100
        else:
            return 0

    def nxtPosition(self, action):
        if self.deterministic:
            if action == "up":
                nxtState = (self.state[0] - 1, self.state[1])
            elif action == "down":
                nxtState = (self.state[0] + 1, self.state[1])
            elif action == "left":
                nxtState = (self.state[0], self.state[1] - 1)
            else:
                nxtState = (self.state[0], self.state[1] + 1) # right
            # if next state legal
            if (nxtState[0] >= 0) and (nxtState[0] <= self.board_rows-1):
                if (nxtState[1] >= 0) and (nxtState[1] <= self.board_cols-1):
                    #if nxtState not in self.losing_state:
                    return nxtState
            return self.state

    def showBoard(self):
        self.board[self.state] = "@"
        for i in range(0, self.board_rows):
            print('----' * self.board_rows +"-")
            out = '| '
            for j in range(0, self.board_cols):
                if self.board[i, j] == 100:
                    token = '*'
                if self.board[i, j] == -100:
                    token = '#'
                if self.board[i, j] == 0:
                    token = '0'
                out += token + ' | '
            print('| ')
        print('----' * self.board_rows +"-")

    def isEndFunc(self):
        if (self.state == self.win_state) or (self.state in self.losing_state):
            self.isEnd = True

class Agent:
    def __init__(self,board_rows,board_cols,win_state,losing_state,start,deterministic):
        self.board_rows = board_rows
        self.board_cols = board_cols
        self.win_state = win_state
        self.losing_state = losing_state
        self.start = start
        self.deterministic = deterministic
        
        self.states = []
        self.State = Grid( board_rows,board_cols,win_state,losing_state,start,deterministic)
        self.board = self.State.board
        self.actions = ["right","left","up","down"]
        self.lr = 0.8
        self.exp_rate = 1

        self.state_values = {}
        for i in range(board_rows):
            for j in range(board_cols):
                self.state_values[(i, j)] = 0

    def chooseAction(self):
        # choose action with most expected value
        mx_nxt_reward = 0
        action = ""

        if np.random.uniform(0, 1) <= self.exp_rate:
            action = np.random.choice(self.actions)
        else:
            # greedy action
            for a in self.actions:
                # if the action is deterministic
                nxt_reward = self.state_values[self.State.nxtPosition(a)]
                if nxt_reward >= mx_nxt_reward:
                    action = a
                    mx_nxt_reward = nxt_reward
        return action

    def takeAction(self, action):
        position = self.State.nxtPosition(action)
        return Grid(self.board_rows,self.board_cols,self.win_state,self.losing_state,position,deterministic)

    def reset(self):
        self.states = []
        self.State =  Grid(self.board_rows,self.board_cols,self.win_state,self.losing_state,self.start,deterministic)

    def play(self, rounds=10):
        i = 0
        ac = {"down":8, "up":7 , "right":5 , "left":4}
        while i < rounds:
            # to the end of game back propagate reward
            if self.State.isEnd:
                # back propagate
                reward = self.State.giveReward()
                print(self.State.state,reward)
                # explicitly assign end state to reward values
                self.state_values[self.State.state] = reward  # this is optional
                print("Game End Reward", reward)
                for s in reversed(self.states):
                    reward = self.state_values[s] + self.lr * (reward - self.state_values[s])
                    self.state_values[s] = round(reward, 2)
                self.reset()
                i += 1
            else:
                action = self.chooseAction()
                # append trace
                self.states.append(self.State.nxtPosition(action))
                print("current position {} action {}".format(self.State.state, action))
                # by taking the action, it reaches the next state
                if action in ac.keys():
                    self.board[self.State.state] = ac[action]
                self.State = self.takeAction(action)
                # mark is end
                self.State.isEndFunc()
                print("nxt state", self.State.state)
                print("---------------------")

    def showValues(self):
        for i in range(0, self.board_rows):
            print('----------------------------------')
            out = '| '
            for j in range(0, self.board_cols):
                out += str(self.state_values[(i, j)]).ljust(6) + ' | '
            print(out)
        print('----------------------------------')

        
    def showBoard(self):
        self.board[self.start] = 1
        for i in range(0, len(self.board)):
            print('----' * self.board_rows +"-")
            out = '| '
            for j in range(0, len(self.board[i])):
                if self.board[i, j] == 100:
                    token = ' * '
                elif self.board[i, j] == -100:
                    token = ' Z '
                elif self.board[i, j] == 0:
                    token = ' 0 '
                elif self.board[i, j] == 8:
                    token = ' D '
                elif self.board[i, j] == 7:
                    token = ' U '
                elif self.board[i, j] == 5:
                    token = ' R '
                elif self.board[i, j] == 4:
                    token = ' L '
                elif self.board[i, j] == 1:
                    token = ' @ '
                out += token + ' | '
            print(out)
        print('----' * self.board_rows +"-")


if __name__ == "__main__":
    ag = Agent(board_rows,board_cols,win_state,losing_states,start,deterministic)
    ag.play(50)
    print(ag.state_values)
    ag.showValues()
    ag.showBoard()
    
#g = Grid(board_rows,board_cols,win_state,losing_states,start,deterministic)
#g.showBoard()
