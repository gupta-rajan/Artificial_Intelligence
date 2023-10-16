# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        #value iteration code 
        for i in range(iterations):
            v = self.values.copy()
            states_list = self.mdp.getStates()
            
            for s in states_list:
                act_list = self.mdp.getPossibleActions(s)
                Q_new = -1*float("inf")
                for a in act_list:
                    Q_val = self.computeQValueFromValues(s,a)
                    if Q_val>Q_new:
                        v[s] = Q_val
                        Q_new = Q_val

            self.values = v

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        state_list = self.mdp.getTransitionStatesAndProbs(state,action)   #Returns list of (nextState, prob)
        qvalue = 0
        for (s,p) in state_list:
            reward = self.mdp.getReward(state,action,s)
            val = self.getValue(s)
            qvalue += p*(reward + self.discount*val)

        return qvalue
        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        actions_list = self.mdp.getPossibleActions(state)

        if len(actions_list)==0:
            return None
        action_best = actions_list[0]
        q_best = self.computeQValueFromValues(state,action_best)

        for a in actions_list[1:]:
            q = self.computeQValueFromValues(state,a)
            if q > q_best:
                q_best = q
                action_best = a
        
        return action_best
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
