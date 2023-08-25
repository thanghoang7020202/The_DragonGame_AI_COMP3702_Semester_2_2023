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

class GemDistance:
    def __init__(self, distance, gem_pos):
        self.gem_pos = gem_pos
        self.distance = distance
    
    def __lt__(self, other):
        return self.distance < other.distance   
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

    def distance(self, pre_pos, row, col):
        # target (gem, goal) is right below the current state
        if row > pre_pos[0]:
            glide_costs = [
                self.game_env.ACTION_COST[GameEnv.GLIDE_LEFT_1],
                self.game_env.ACTION_COST[GameEnv.GLIDE_LEFT_2],
                self.game_env.ACTION_COST[GameEnv.GLIDE_LEFT_3]
            ]
            if col == pre_pos[1]:
                row_diff = row - pre_pos[0]
                third, remainder = divmod(row_diff, 3)
                second, first = divmod(remainder, 2)
                return  self.game_env.ACTION_COST[GameEnv.DROP_3] * third \
                    + self.game_env.ACTION_COST[GameEnv.DROP_2] * second \
                        + self.game_env.ACTION_COST[GameEnv.DROP_1] * first 
            else:   
                row_diff = row - pre_pos[0]
                col_diff = abs(pre_pos[1] - col)
                col_third, col_remainder = divmod(col_diff, 3)
                row_diff -= col_third
                if row_diff == 0:
                    return col_diff * self.game_env.ACTION_COST[GameEnv.WALK_LEFT] + col_third * glide_costs[2]
                
                col_second, col_first = divmod(col_remainder, 2)
                row_diff -= col_second
                if row_diff == 0:
                    return col_diff * self.game_env.ACTION_COST[GameEnv.WALK_LEFT] + col_third * glide_costs[2] \
                        + col_second * glide_costs[1] 
                
                row_diff -= col_first
                if row_diff == 0:
                    return col_third * glide_costs[2] \
                        + col_second * glide_costs[1] + col_first * glide_costs[0]
                
                row_third, row_remainder = divmod(row_diff, 3)
                row_second, row_first = divmod(row_remainder, 2)
                return (col_third * glide_costs[2] + col_second * glide_costs[1] + col_first * glide_costs[0] 
                        + row_third * self.game_env.ACTION_COST[GameEnv.DROP_3] + row_second * self.game_env.ACTION_COST[GameEnv.DROP_2] \
                              + row_first * self.game_env.ACTION_COST[GameEnv.DROP_1])  
        else: # target (gem, goal) is above the current state
            row_diff = abs(pre_pos[0] - row)
            col_diff = abs(pre_pos[1] - col)
            return row_diff * self.game_env.ACTION_COST[GameEnv.JUMP] \
                + col_diff * self.game_env.ACTION_COST[GameEnv.WALK_LEFT] # both walk left and right have the same cost

    def compute_heuristic(self, state):
        cost = 0
        pre_pos = (state.row, state.col)
        if 0 in state.gem_status:
            # list of distance to each gem
            gem_distance = []
            heapq.heapify(gem_distance)
            n = len(state.gem_status)
            for gem in range (n):
                if state.gem_status[gem] == 0:
                    gem_pos = self.game_env.gem_positions[gem]
                    heapq.heappush(gem_distance,GemDistance(abs(state.row - gem_pos[0]) + abs(state.col - gem_pos[1]), gem_pos))
            while(gem_distance):
                node = heapq.heappop(gem_distance)
                cost += self.distance(pre_pos, node.gem_pos[0], node.gem_pos[1])
                pre_pos = node.gem_pos
            cost += self.distance(pre_pos, self.game_env.exit_row, self.game_env.exit_col)
        else: # no gem left
            cost = self.distance(pre_pos, self.game_env.exit_row, self.game_env.exit_col)
        return cost



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
                    heuristic_cost = self.compute_heuristic(persistent_state)
                    node =  ContainerEntryAStar(persistent_state, Entry.path + [action], \
                                                Entry.cost + self.game_env.ACTION_COST[action], \
                                                heuristic_cost)
                    heapq.heappush(container, node)
        return []
