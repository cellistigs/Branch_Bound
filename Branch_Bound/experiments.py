## Where we will actually implement BB_k for different models. 
import numpy as np 
from Branch_Bound.dataformat import Node_path
from Branch_Bound.ops import branch_path,bound_path,min_greedy_path
from collections import deque
from heapq import heappush,heappop
# Implement BB_k with different kinds of data structures on the nodes: 

## With FIFO queue (upper bound by arbitrary solution/negative inf to start): 
def BB_FIFO(weights,k):
    ## First recover problem parameters from the weights:
    transitions_nb = np.shape(weights)[-1]
    states_nb = np.shape(weights)[0]
    N = transitions_nb+1
    d = states_nb
    ## Now come up with a heuristic solution: 
    minpath,mincost = min_greedy_path(weights,0)
    ## Initialize the root node:
    root = Node_path([],d,N)
    ## Initialize problem parameters: 
    B = mincost # Upper bound on solutions
    ## Now we will search the tree using BB_k: 
    node_list = deque([root])
    node_solution = []
    while len(node_list):
        ## Get the active node 
        node_active = node_list.popleft()
        ## Branch on that node
        nodes_eval = branch_path(node_active)
        ## Evaluate each child node
        bounds = [bound_path(node_eval,weights,k) for node_eval in nodes_eval]
        ## Evaluate if a solution was reached, and add those child nodes that satisfy the bound. 
        for child_nb,bound in enumerate(bounds):
            if bound[0] <= B:
                node_list.append(nodes_eval[child_nb])
                ## If the solution is as good as a previously found one, add it, if it is better replace the other. 
                if bound[1] == 1:
                    if B == bound[0]:
                        node_solution.append((nodes_eval[child_nb],bound))
                    else:
                        B = bound[0]
                        node_solution = [(nodes_eval[child_nb],bound)]
    return node_solution


## With LIFO stack (upper bound by negative inf to start): 
def BB_LIFO(weights,k):
    ## First recover problem parameters from the weights:
    transitions_nb = np.shape(weights)[-1]
    states_nb = np.shape(weights)[0]
    N = transitions_nb+1
    d = states_nb
    ## Now come up with a heuristic solution: 
    minpath,mincost = min_greedy_path(weights,0)
    ## Initialize the root node:
    root = Node_path([],d,N)
    ## Initialize problem parameters: 
    B = mincost # Upper bound on solutions
    ## Now we will search the tree using BB_k: 
    node_list = [root]
    node_solution = []
    while len(node_list):
        ## Get the active node 
        node_active = node_list.pop()
        ## Branch on that node
        nodes_eval = branch_path(node_active)
        ## Evaluate each child node
        bounds = [bound_path(node_eval,weights,k) for node_eval in nodes_eval]
        ## Evaluate if a solution was reached, and add those child nodes that satisfy the bound. 
        for child_nb,bound in enumerate(bounds):
            if bound[0] <= B:
                node_list.append(nodes_eval[child_nb])
                ## If the solution is as good as a previously found one, add it, if it is better replace the other. 
                if bound[1] == 1:
                    if B == bound[0]:
                        node_solution.append((nodes_eval[child_nb],bound))
                    else:
                        B = bound[0]
                        node_solution = [(nodes_eval[child_nb],bound)]
    return node_solution

## With priority queue (no upper bound)
def BB_Q(weights,k):
    ## First recover problem parameters from the weights:
    transitions_nb = np.shape(weights)[-1]
    states_nb = np.shape(weights)[0]
    N = transitions_nb+1
    d = states_nb
    ## Now come up with a heuristic solution: 
    minpath,mincost = min_greedy_path(weights,0)
    ## Initialize the root node:
    root = Node_path([],d,N)
    ## Initialize problem parameters: 
    B = mincost # Upper bound on solutions
    ## Now we will search the tree using BB_k: 
    node_list = []
    heappush(node_list,(B,0,root)) 
    node_solutions = []
    entry_count = 0
    while len(node_list):
        ## Get the active node 
        parent_bound,parent_sol,node_active = heappop(node_list)
        # In this case reaching a solution should be good enough (?)
        if parent_sol == 1:
            B = parent_bound
            node_solution = (node_active,[parent_bound,parent_sol])
            return node_solution

        ## Branch on that node
        nodes_eval = branch_path(node_active)
        ## Evaluate each child node
        bounds = [bound_path(node_eval,weights,k) for node_eval in nodes_eval]
        ## Evaluate if a solution was reached, and add those child nodes that satisfy the bound. 
        for child_nb,bound in enumerate(bounds):
            entry_count+=1
            if bound[1] == 1:
                solution_penalty = d**N 
            else:
                solution_penalty = 0 
            heappush(node_list,(bound[0],entry_count+solution_penalty,nodes_eval[child_nb]))


# Function to calculate feasible k for a given N and d: 

# Function to calculate true solution for a problem instance using viterbi: 

# Function to calculate time and performance relative to viterbi as a function of k. 


