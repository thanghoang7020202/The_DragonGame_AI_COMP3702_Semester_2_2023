from game_env import GameEnv
from game_state import GameState
import heapq
"""
solution.py

This file is a template you should use to implement your solution.

You should implement each of the method stubs below. You may add additional methods and/or classes to this file if you 
wish. You may also create additional source files and import to this file if you wish.

COMP3702 Assignment 1 "Dragon Game" Support Code

Last updated by njc 07/08/23
"""

class ContainerEntry:
    def __init__(self, state, path, cost):
        self.state = state
        self.path = path
        self.cost = cost
    
    def __lt__(self, other):
        return self.cost < other.cost

class ContainerEntryAStar:
    def __init__(self, state, path, cost, heuristic_cost):
        self.state = state
        self.path = path
        self.cost = cost
        self.heuristic_cost = heuristic_cost + cost
    
    def __lt__(self, other):
        return self.heuristic_cost + self.cost < other.heuristic_cost + other.cost
        
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
        container = [ContainerEntry(self.game_env.get_init_state(), [], 0)]
        heapq.heapify(container)
        visited = set()
        while container:
            Entry = heapq.heappop(container)
            if Entry.state in visited:
                continue
            visited.add(Entry.state)
            for action in GameEnv.ACTIONS:
                success, persistent_state = self.game_env.perform_action(Entry.state, action)
                if success and persistent_state not in visited and not self.game_env.is_game_over(persistent_state):
                    if self.game_env.is_solved(persistent_state):
                        return Entry.path + [action]
                    node =  ContainerEntry(persistent_state, Entry.path + [action], Entry.cost + self.game_env.ACTION_COST[action])
                    heapq.heappush(container, node)
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

    def gem_distance(self, state):
        gem = state.gem_status.index(0)
        # get position to the gem
        gem_pos = self.game_env.gem_positions[gem]
        if gem_pos[0] > state.row: # target (gem, goal) is below the current state
            # compute Euclidean distance
            return ((state.row - gem_pos[0]) ** 2 + (state.col - gem_pos[1]) ** 2) ** 0.5
        else:
            # compute Manhattan distance
            return (abs(state.row - gem_pos[0]) + abs(state.col - gem_pos[1]))
        
    def compute_heuristic(self, state):
        """
        Compute a heuristic value h(n) for the given state.
        :param state: given state (GameState object)
        :return a real number h(n)
        
        if self.game_env.exit_row > state.row:
            return (((state.row - self.game_env.exit_row) ** 2 + (state.col - self.game_env.exit_col) ** 2) ** 0.5)
        else:
            return (abs(state.row - self.game_env.exit_row) + abs(state.col - self.game_env.exit_col))
        """
        n_gems = state.gem_status.count(0)
        return (n_gems / len(state.gem_status) ) * 0.1
        

    def search_a_star(self):
        """
        Find a path which solves the environment using A* Search.
        :return: path (list of actions, where each action is an element of GameEnv.ACTIONS)
        """
        container = [ContainerEntryAStar(self.game_env.get_init_state(), [], 0, 0)]
        heapq.heapify(container)
        visited = set()
        while container:
            Entry = heapq.heappop(container)
            if Entry.state in visited:
                continue
            visited.add(Entry.state)
            for action in GameEnv.ACTIONS:
                success, persistent_state = self.game_env.perform_action(Entry.state, action)
                if success and persistent_state not in visited and not self.game_env.is_game_over(persistent_state):
                    if self.game_env.is_solved(persistent_state):
                        return Entry.path + [action]
                    if 0 in persistent_state.gem_status:
                        heuristic_cost = self.gem_distance(persistent_state)
                    else:
                        heuristic_cost = self.compute_heuristic(persistent_state)
                    node =  ContainerEntryAStar(persistent_state, Entry.path + [action], \
                                                Entry.cost + self.game_env.ACTION_COST[action], \
                                                heuristic_cost)
                    heapq.heappush(container, node)
        return []
