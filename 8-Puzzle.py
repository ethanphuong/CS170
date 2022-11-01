from copy import deepcopy
import numpy as np
import math

trivial = [[1, 2, 3], 
           [4, 5, 6], 
           [7, 8, 0]]

veryEasy = [[1, 2, 3], 
            [4, 5, 6], 
            [7, 0, 8]]

easy = [[1, 2, 0], 
        [4, 5, 3], 
        [7, 8, 6]]

doable = [[0, 1, 2], 
          [4, 5, 3], 
          [7, 8, 6]]

oh_boy = [[8, 7, 1], 
          [6, 0, 2], 
          [5, 4, 3]]

impossible = [[1, 1, 1], 
              [1, 1, 1], 
              [1, 1, 0]]

eight_goal_state = [[1, 2, 3], 
                    [4, 5, 6], 
                    [7, 8, 0]]
                    
#node class to set up the tree
class node:
    #constructor for nodes
    def __init__(self, state, depth, cost):
        #current state
        self.state = state
        #depth
        self.depth = depth
        #cost of moves
        self.cost = cost
    
    #function to make the children for nodes
    def children(self):
        #list for children
        successors = []
        temp = 0
        #finding where the 0 is in the 2d array
        for i, j in enumerate(self.state):
            #if 0 is in the current row
            if 0 in j:
                #iterate through the current row
                for x, y in enumerate(j):
                    #if the current element is 0
                    if y == 0:
                        #record the index
                        zero_index = [i, x]
                #separate row and column
                row = zero_index[0]
                col = zero_index[1]

        #check to see if it can move left by making sure the 0 is not in the first column
        if col != 0  and (row != 0 or row != 1 or row != 2):
            #left shift by adding -1 to the index
            l_r_shift = -1
            #not moving up or down
            u_d_shift = 0
            #new list with the shifts included
            next_state = self.copy_list(row, col, l_r_shift, u_d_shift)
            cost = abs(l_r_shift + u_d_shift)
            #add the new list to the list of states
            if temp > 0:
                successors.append(node(next_state, self.depth + 1, self.cost + cost))
            else:
                temp += 1
                successors.append(node(next_state, self.depth, self.cost + cost))
        
        #check to see if it can move right by making sure the 0 is not in the last column
        if col != 2 and (row != 0 or row != 1 or row != 2):
            #right shift by adding 1 to the index
            l_r_shift = 1
            #not moving up or down
            u_d_shift = 0
            #new list with the shifts included
            next_state = self.copy_list(row, col, l_r_shift, u_d_shift)
            cost = abs(l_r_shift + u_d_shift)
            #add the new list to the list of states
            if temp > 0:
                successors.append(node(next_state, self.depth + 1, self.cost + cost))
            else:
                temp += 1
                successors.append(node(next_state, self.depth, self.cost + cost))

        #check to see if it can move up by making sure the 0 is not in the first row
        if row != 0 and (col != 0 or col != 1 or col != 2):
            #not moving left or right
            l_r_shift = 0
            #shift up by adding -1 to the index
            u_d_shift = -1
            #new list with the shifts included
            next_state = self.copy_list(row, col, l_r_shift, u_d_shift)
            cost = abs(l_r_shift + u_d_shift)
            #add the new list to the list of states
            if temp > 0:
                successors.append(node(next_state, self.depth + 1, self.cost + cost))
            else:
                temp += 1
                successors.append(node(next_state, self.depth, self.cost + cost))
        
        #check to see if it can move down by making sure the 0 is not in the last row
        if row != 2 and (col != 0 or col != 1 or col != 2):
            #not moving left or right
            l_r_shift = 0
            #shift up by adding 1 to the index
            u_d_shift =  1
            #new list with shifts included
            next_state = self.copy_list(row, col, l_r_shift, u_d_shift)
            cost = abs(l_r_shift + u_d_shift)
            #add the new list to the list of states
            if temp > 0:
                successors.append(node(next_state, self.depth + 1, self.cost + cost))
            else:
                temp += 1
                successors.append(node(next_state, self.depth, self.cost + cost))

        #return the list of new states
        return successors

    #function to create a new list with shifts
    def copy_list(self, zero_row, zero_col, horizontal_shift, vertical_shift):
        #make a temporary copy of the current state
        new_list = []
        new_list = deepcopy(self.state)
        #keep track of what number is where the new 0 is supposed to be
        temp_place = new_list[zero_row + vertical_shift][zero_col + horizontal_shift]
        #set the new placement for the 0 as 0 in the new list
        new_list[zero_row + vertical_shift][zero_col + horizontal_shift] = 0
        #set the place where 0 was as the new number
        new_list[zero_row][zero_col] = temp_place
        #return the new list
        return new_list
    
    def misplaced_tile(self):
        #converting working state to NumPy arrays
        working_array = np.array(self.state)
        goal_array = np.array(eight_goal_state)
        #total misplaced tiles
        total = 0
        #iterate through the 2d array
        for i in range(0, len(self.state)):
            for j in range(0, len(self.state)):
                element = working_array[i][j]
                #if the current element in our working array doesn't match the index of the goal array
                if np.where(element == working_array) != np.where(element == goal_array):
                    #add a misplaced tile
                    total += 1
        #return total misplaced tiles
        return total
    
    def manhattan_distance(self):
        #converting working state to NumPy arrays
        working_array = np.array(self.state)
        goal_array = np.array(eight_goal_state)
        #total manhattan cost
        total_cost = 0
        #iterate through the 2d array
        for i in range(0, len(self.state)):
            for j in range(0, len(self.state)):
                element = self.state[i][j]
                #if the current element in our working array doesn't match the index of the goal array
                if np.where(element == working_array) != np.where(element == goal_array):
                    index1 = np.where(working_array == element)
                    index2 = np.where(goal_array == element)
                    #calculate the total distance between the mismatched indexes
                    total_cost += abs(index1[0] - index2[0])
                    total_cost += abs(index1[1] - index2[1])
        #return total manhattan cost
        return total_cost

def init_default_puzzle_mode():
    #input for difficulty for testing
    selected_difficulty = input("You wish to use a default puzzle. Please enter a desired difficulty on a scale from 0 to 5" + "\n")

    if selected_difficulty == "0":
        print("Difficulty of 'Trivial' selected.")
        return trivial
    if selected_difficulty == "1":
        print("Difficulty of 'Very Easy' selected.")
        return veryEasy
    if selected_difficulty == "2":
        print("Difficulty of 'Easy' selected.")
        return easy
    if selected_difficulty == "3":
        print("Difficulty of 'Doable' selected.")
        return doable
    if selected_difficulty == "4":
        print("Difficulty of 'Oh Boy' selected.")
        return oh_boy
    if selected_difficulty == "5":
        print("Difficulty of 'Impossible' selected.")
        return impossible

def print_puzzle(puzzle):
    #print puzzle
    for i in range(0, 3):
        print(puzzle[i])
    print("\n")

def select_and_init_algorithm(puzzle):
    #determine which heuristic we want to use
    algorithm = input("Select algorithm. (1) for Uniform Cost Search, (2) for the Misplaced Tile Heuristic, or (3) for the Manhattan Distance Heuristic." + "\n")

    if algorithm == "1":
        uniform_cost_search(puzzle, 0)
    if algorithm == "2":
        uniform_cost_search(puzzle, 1)
    if algorithm == "3":
        uniform_cost_search(puzzle, 2)

def uniform_cost_search(puzzle, heuristic):
    
    #current node that we want to work with in a queue
    working_queue = [node(puzzle, 0, 0)]
    #keep track of repeated states
    repeated_states = dict()
    #tracker for number of nodes expanded
    num_nodes_expanded = 0
    #keep track of the max queue size
    max_queue_size = 0
    #adding current node to the repeated states
    repeated_states = puzzle

    #keep track of puzzles to print
    stack_to_print = []
    
    #make sure theres still something in the queue
    while len(working_queue) > 0:
        #calculate max queue size
        max_queue_size = max(len(working_queue), max_queue_size)
        #pop off queue
        node_from_queue = working_queue.pop()
        #add one to number of nodes expanded because we popped off the queue
        num_nodes_expanded += 1
        
        #if the current state is the goal
        if node_from_queue.state == eight_goal_state:
            while len(stack_to_print) > 0:
                print_puzzle(stack_to_print.pop())
            print("Solution depth was:", int((math.sqrt(i.depth) // 1)))
            print("Number of nodes expanded:", num_nodes_expanded)
            print("Max queue size:", max_queue_size)
            return node_from_queue
        
        #else generate new children for the node
        successor_state = node_from_queue.children()
        #iterate through the child
        for i in successor_state:
            #check if it is the goal
            if i.state == eight_goal_state:
                stack_to_print.append(node_from_queue.state)
                while len(stack_to_print) > 0:
                    print_puzzle(stack_to_print.pop())
                print("Solution depth was:", int((math.sqrt(i.depth) // 1)))
                print("Number of nodes expanded:", num_nodes_expanded)
                print("Max queue size:", max_queue_size)
                return node_from_queue

            #else add it to the queue
            elif i.state not in repeated_states:
                repeated_states.append(i.state)
                working_queue.append(i)

        #check heuristics and then sort the queue by the heuristic
        if heuristic == 1:
            working_queue.sort(key = lambda node: node.cost, reverse = True)
        elif heuristic == 2:
            working_queue.sort(key = lambda node: node.misplaced_tile(), reverse = True)
        elif heuristic == 3:
            working_queue.sort(key = lambda node: node.manhattan_distance(), reverse = True)

        #add new node to the stack to print
        stack_to_print.append(node_from_queue.state)

def main():
    #interface
    puzzle_mode = input("Welcome to an 8-Puzzle Solver. Type '1 to use a default puzzle, or '2' to create your own." + "\n")

    if puzzle_mode == "1":
        select_and_init_algorithm(init_default_puzzle_mode())

    if puzzle_mode == "2":
        print("Enter your puzzle, using a zero to represent the blank. " + "Please only enter valid 8-puzzles. Enter the puzzle demilimiting " + "the numbers with a space. RET only when finished." + "\n")
        puzzle_row_one = input("Enter the first row: ")
        puzzle_row_two = input("Enter the second row: ")
        puzzle_row_three = input("Enter the third row: ")

        puzzle_row_one = puzzle_row_one.split()
        puzzle_row_two = puzzle_row_two.split()
        puzzle_row_three = puzzle_row_three.split()

        for i in range(0, 3):
            puzzle_row_one[i] = int(puzzle_row_one[i])
            puzzle_row_two[i] = int(puzzle_row_two[i])
            puzzle_row_three[i] = int(puzzle_row_three[i])

        user_puzzle = [puzzle_row_one, puzzle_row_two, puzzle_row_three]
        select_and_init_algorithm(user_puzzle)
    
    return

main()  