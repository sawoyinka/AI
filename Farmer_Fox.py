'''Farmer_Fox.py
[STUDENTS: REPLACE THE FOLLOWING INFORMATION WITH YOUR
OWN:]
by Sophia Awoyinka
UWNetIDs: sawoyink
Student numbers: 2379502

Assignment 2, in CSE 415, Winter 2025
 
This file contains my problem formulation for the problem of
the Farmer, Fox, Chicken, and Grain.
'''

# Put your formulation of the Farmer-Fox-Chicken-and-Grain problem here.
# Be sure your name(s), uwnetid(s), and 7-digit student number(s) are given above in 
# the format shown.

# You should model your code closely after the given example problem
# formulation in HumansRobotsFerry.py

#<METADATA>
PROBLEM_NAME = "Farmer, Fox, Chicken, Grain "
PROBLEM_VERSION = "1.1"
PROBLEM_AUTHORS = ['S. Awoyinka']
PROBLEM_CREATION_DATE = "26-JAN-2025"

PROBLEM_DESC=\
 ''' In the Farmer, Fox, Chicken, Grain problem, the player starts off with 
a farmer with a fox, chicken, and some grain on the left bank of a creek.  
The object is to execute a sequence of legal moves that transfers them all to the 
right bank of the creek.  In this puzzle, there is a ferry that the farmer can use to
transfer one item across the creek at a time.  It is forbidden to ever have 
the fox left alone with the chicken or the chicken left alone with the grain. 
The computer will not let you make a move to such a forbidden situation, and it will only 
show you moves that could be executed "safely."
'''
#</METADATA>

#<COMMON_CODE>
LEFT=0 
RIGHT=1 

class State:

    def __init__(self, old=None):
        if old is None: 
            self.farmer = LEFT
            self.fox = LEFT
            self.chicken = LEFT
            self.grain = LEFT
        else:
            self.farmer = old.farmer
            self.fox = old.fox
            self.chicken = old.chicken
            self.grain = old.grain

    def __eq__(self,s2):
        if self.farmer != s2.farmer: return False
        if self.fox != s2.fox: return False
        if self.chicken != s2.chicken: return False
        if self.grain != s2.grain: return False       
        return True

    def __str__(self):
        # Produces a textual description of a state.
        txt = ""

        if self.farmer == LEFT:
            txt += " farmer is on the left.\n"
        else:
            txt += " farmer is on the right.\n"

        if self.fox == LEFT:
            txt += " fox is on the left.\n"
        else:
            txt += " fox is on the right.\n"

        if self.chicken == LEFT:
            txt += " chicken is on the left.\n"
        else:
            txt += " chicken is on the right.\n"

        if self.grain == LEFT:
            txt += " grain is on the left.\n"
        else:
            txt += " grain is on the right.\n"
        return txt

    def __hash__(self):
        return (self.__str__()).__hash__()

    def copy(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        return State(old=self)

    def can_move(self, item):
        '''Tests whether it's legal for the farmer to move with given animal/grain.'''
        side = self.farmer
        if item == 'alone':
            return True
        if item == 'fox' and self.fox != side:
            return False
        elif item == 'chicken' and self.chicken != side:
            return False
        elif item == 'grain' and self.grain != side:
            return False
        if item == 'fox' and self.chicken == self.grain:
            return False
        if item == 'grain' and self.fox == self.chicken:
            return False
        return True

    def move(self, item):
        '''Assumes it's legal to make the move. Computes the new state.'''
        news = self.copy()
        if item == 'alone':
            news.farmer = RIGHT if self.farmer == LEFT else LEFT
        else:
            setattr(news, item, RIGHT if getattr(self, item) == LEFT else LEFT)
            news.farmer = RIGHT if self.farmer == LEFT else LEFT
        return news

    def is_goal(self):
        '''If farmer, chicken, fox, and grain are on the right then it's a 
        goal state.'''
        if self.farmer == RIGHT and self.fox == RIGHT and self.chicken == RIGHT and self.grain == RIGHT: 
            return True
        else: return False

def goal_message(s):
    return "Congratulations on getting the fox, chicken, and grain across!"


class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)
#</COMMON_CODE>

#<INITIAL_STATE>
CREATE_INITIAL_STATE = lambda : State()
#</INITIAL_STATE>

#<OPERATORS>
items = ['fox', 'chicken', 'grain', 'alone']

OPERATORS = [Operator(
  "Farmer crosses the creek with " + str(item),
  lambda s, thing=item: s.can_move(thing),
  lambda s, thing=item: s.move(thing))
  for item in items]

GOAL_TEST = lambda s: s.is_goal()
GOAL_MESSAGE_FUNCTION = lambda s: s.goal_message()
#<OPERATORS>

PROBLEM = type("Problem", (), {
    "CREATE_INITIAL_STATE": CREATE_INITIAL_STATE,
    "OPERATORS": OPERATORS,
    "GOAL_TEST": GOAL_TEST,
    "GOAL_MESSAGE_FUNCTION": GOAL_MESSAGE_FUNCTION
})


