import copy
import random
import time

class Stack:
    "A container with a last-in-first-out (LIFO) queuing policy."
    def __init__(self):
        self.list = []

    def __repr__(self):
        return str(self.list)+'@'
    
    def __len__(self):
        return len(self.list)

    def push(self,item):
        "Push 'item' onto the stack"
        self.list.append(item)

    def pop(self):
        "Pop the most recently pushed item from the stack"
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the stack is empty"
        return len(self.list) == 0

    def Copy(self):
        #to make a deep copy of the stack
        s = Stack()
        s.list = copy.deepcopy(self.list)
        return s

    def __eq__(self, __o):
        #to check the equality of the two stacks.
        return len(self.list)==len(__o.list) and sum([self.list[i] == __o.list[i] for i in range(len(self.list))]) == len(self.list)

class State:
    def __init__(self,stacka,stackb,stackc):
        self.stacka = stacka
        self.stackb = stackb
        self.stackc = stackc

    def __repr__(self):
        #prints the state elements.
        return '<state>['+str(self.stacka)+' '+str(self.stackb)+' '+str(self.stackc)+']\n'

    def __eq__(self, __o: object) -> bool:
        #to check the equality of two states
        if self.stacka == __o.stacka and self.stackb == __o.stackb and self.stackc == __o.stackc:
            return True
        else:
            return False

def successors(state):
    
    states = {0 : state.stacka.Copy(),1 : state.stackb.Copy(),2 : state.stackc.Copy()}
    allstates = []

    for i in range(3):
        if not states[i].isEmpty():
            for j in range(3):
                if i!=j:
                    s = copy.deepcopy(states)
                    po = s[i].pop() #pop an element from the stack
                    s[j].push(po)   #push that element in any other stack
                    allstates.append(State(*s.values()))    
    return allstates

def compareStacks(stack1,stack2):
    check = True

    if len(stack1)!=len(stack2):
        #checking the length is equal or not
        check = False
        return check

    while(len(stack1)):
        # comparing last element of stack and poping that element
        if stack1.list[-1]==stack2.list[-1]:
            stack1.pop()
            stack2.pop()
        else:
            check = False
            break

    return check

def isGoalState(state,goalstate):
    state1 = {0 : state.stacka.Copy(),1 : state.stackb.Copy(),2 : state.stackc.Copy()}
    state2 = {0 : goalstate.stacka.Copy(),1 : goalstate.stackb.Copy(),2 : goalstate.stackc.Copy()}

    check = True
    for i in range(3):
        if not compareStacks(state1[i] ,state2[i]):
            check = False
            break
    return check

def getPositionOfBlock(block,state):
    idx = {0:state.stacka.list, 1 : state.stackb.list, 2:state.stackc.list}

    for k in range(3):
        for i in range(len(idx[k])):
                if idx[k][i]==block:    #checking by element at the index is equal to the block or not.
                    return (k,i)

def heuristic1(curr_state,final_state):
    #+1 if block is at the correct position of final state else -1.
    dic1 = {0:curr_state.stacka.list, 1:curr_state.stackb.list, 2:curr_state.stackc.list}
    sum = 0
    for i in range(3):
        for j in range(len(dic1[i])):
            if (i,j) == getPositionOfBlock(dic1[i][j],final_state):
                sum+=1
            else:
                sum-=1
    return sum

def heuristic2(curr_state,final_state):
    #+h if block is at the correct position of final state else -h.
    dic1 = {0:curr_state.stacka.list, 1:curr_state.stackb.list, 2:curr_state.stackc.list}
    # dic2 = {0:final_state.stacka.list, 1:final_state.stackb.list, 2:final_state.stackc.list}

    value = 0
    for i in range(3):
        for h in range(len(dic1[i])):
            if(i,h) == getPositionOfBlock(dic1[i][h],final_state):
                value+=(h+1)
            else:
                value-=(h+1)
    return value

def heuristic3(curr_state,final_state):
    #manhattan distance
    dic1 = {0:curr_state.stacka.list, 1:curr_state.stackb.list, 2:curr_state.stackc.list}
    distance = 0
    for i in range(3):
        for j in range(len(dic1[i])):
            distance += abs((getPositionOfBlock(dic1[i][j],final_state)[0]-i))+ abs((getPositionOfBlock(dic1[i][j],final_state)[1]-j)) 
    return 100-distance     #to make it a maximization problem

def hillClimbing(initial_state,final_state,h_number):

    explored = []
    curr_state = initial_state
    path = []
    path.append(curr_state)
    # func = lambda x,y: random.randint(0,100)

    while not isGoalState(curr_state,final_state):
        heuristics = {1:heuristic1,2:heuristic2,3:heuristic3}
        if curr_state not in explored:
            explored.append(curr_state)
            succ = successors(curr_state)
            nextstate = max(succ,key=lambda x:heuristics[h_number](x,final_state)) #next state is the successor given by the max value of heuristic
            # print(nextstate)
            # print(type(nextstate))
            path.append(nextstate)
            curr_state = nextstate
        else:
            print("Goal state is not reachable")
            break
    else:
        print('Goal state is reachable')

    print("No. of states explored is : ", len(explored))
    return path


def convertToState(IS):
    s = []
    for i in IS:
        k = Stack()
        for j in i:
            k.push(j)
        s.append(k.Copy())
    for i in range(3-len(IS)):
        s.append(Stack())
    return State(*s)

# print(initialstate)
# print(successors(initialstate))
# print(isGoalState(initialstate,goalstate))
# print(hillClimbing(initialstate,goalstate))

f = open("input.txt","r")


h_number = int(input("Enter heuristic number you want to test b/w [1,2,3]: "))
p = f.readline()
for i in range(int(p)):
    IS = []
    FS = [] 
    for p in f:
        if p[0] != '\n':
            IS.append(p[:-1].split(","))
        else:
            break
    for p in f:
        if p[0]!= '-':
            FS.append(p[:-1].split(","))
        else:
            break
    initial_state = convertToState(IS)
    final_state = convertToState(FS)
    print("Initial State is :",initial_state)
    print("Goal State is :",final_state)
# print(heuristic1(final_state,final_state))
    stamp_0 = time.time()
    print(*hillClimbing(initial_state,final_state,h_number))
    stamp_1 = time.time()
    print("Time taken : ", stamp_1 - stamp_0)
    print("----------------------------")

    # print(heuristic3(initial_state,final_state))
    # print(heuristic3(final_state,final_state))