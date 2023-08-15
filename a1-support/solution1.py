from game_env import GameEnv
from game_state import GameState

"""
solution.py

This file is a template you should use to implement your solution.

You should implement each of the method stubs below. You may add additional methods and/or classes to this file if you 
wish. You may also create additional source files and import to this file if you wish.

COMP3702 Assignment 1 "Dragon Game" Support Code

Last updated by njc 07/08/23
"""

class ContainerEntry:
    def __init__(self, state, parent, action_from_parent, cost):
        self.state = state
        self.parent = parent
        self.action_from_parent = action_from_parent
        self.cost = cost

    def get_successors(self, game_env,state):
        successors = []
        for action in GameEnv.ACTIONS:
            success, persistent_state = game_env.perform_action(state, action)
            if success:
                successors.append(ContainerEntry(persistent_state, self, action, self.cost + game_env.ACTION_COST[action]))
        #return list of successors in form of ContainerEntry
        return successors

class Solver:

    def __init__(self, game_env):
        self.game_env = game_env

        #
        #
        # TODO: Define any class instance variables you require here (avoid performing any computationally expensive
        #  heuristic preprocessing operations here - use the preprocess_heuristic method below for this purpose).
        #
        #
        pass

    # === Uniform Cost Search ==========================================================================================
    def search_ucs(self):
        """
        Find a path which solves the environment using Uniform Cost Search (UCS).
        :return: path (list of actions, where each action is an element of GameEnv.ACTIONS)
        """
        container = [ContainerEntry(self.game_env.get_init_state(), None, None, 0)]
        visited = set([])
        while container:
            Entry = container.pop(0)
            #print(Entry.state)
            # check if it is the goal state
            if self.game_env.is_solved(Entry.state):
                actions = []
                while Entry.parent is not None:
                    actions.append(Entry.action_from_parent)
                    Entry = Entry.parent
                    #print(actions)
                return actions[::-1]
            
            if Entry.state not in visited:
                visited.add(Entry.state)
            EntrySucs = Entry.get_successors(self.game_env,Entry.state)
            #interate through successors (ContainerEntries) and add to container (Priority Queue)
            for Suc in EntrySucs:
                if Suc.state not in visited and not self.game_env.is_game_over(Suc.state):
                    container.append(ContainerEntry(Suc.state, Entry, Suc.action_from_parent, Entry.cost + self.game_env.ACTION_COST[Suc.action_from_parent]))
                    visited.add(Suc.state)
            container = sorted(container, key=lambda x: x.cost)
        return []

    # === A* Search ====================================================================================================
    def preprocess_heuristic(self):
        """
        Perform pre-processing (e.g. pre-computing repeatedly used values) necessary for your heuristic,
        """

        #
        #
        # TODO: (Optional) Implement code for any preprocessing required by your heuristic here (if your heuristic
        #  requires preprocessing).
        #
        # If you choose to implement code here, you should call this method from your search_a_star method (e.g. once at
        # the beginning of your search).
        #
        #


        pass

    def compute_heuristic(self, state):
        """
        Compute a heuristic value h(n) for the given state.
        :param state: given state (GameState object)
        :return a real number h(n)
        """
        
        return abs(self.game_env.exit_row - state.row) + abs(self.game_env.exit_col - state.col)
        #
        #
        # TODO: Implement your heuristic function for A* search here. Note that your heuristic can be tested on
        #  gradescope even if you have not yet implemented search_a_star.
        #
        # You should call this method from your search_a_star method (e.g. every time you need to compute a heuristic
        # value for a state).
        #

        pass

    def search_a_star(self):
        """
        Find a path which solves the environment using A* Search.
        :return: path (list of actions, where each action is an element of GameEnv.ACTIONS)
        """
        container = [ContainerEntry(self.game_env.get_init_state(), None, None, 0)]
        visited = set()
        while len(container) > 0:
            Entry = container.pop(0)
            #print(Entry.state)
            # check if it is the goal state
            if self.game_env.is_solved(Entry.state):
                actions = []
                while Entry.parent is not None:
                    actions.append(Entry.action_from_parent)
                    Entry = Entry.parent
                    #print(actions)
                return actions[::-1]
            if Entry.state not in visited:
                visited.add(Entry.state)
            EntrySucs = Entry.get_successors(self.game_env,Entry.state)
            #interate through successors (ContainerEntries) and add to container (Priority Queue)
            for Suc in EntrySucs:
                if Suc.state not in visited:
                    container.append(ContainerEntry(Suc.state, Entry, Suc.action_from_parent, Entry.cost + self.game_env.ACTION_COST[Suc.action_from_parent]))
                    visited.add(Suc.state)
            container = sorted(container, key=lambda x: x.cost + self.compute_heuristic(x.state))
        pass
