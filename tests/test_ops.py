import numpy as np 
import time
from Branch_Bound.dataformat import Node_path
from Branch_Bound.ops import branch_path,bound_path,calculate_cost_path,min_greedy_path

def construct_toy_weights(to_node1,to_node2):
    '''
    A function to construct a matrix of weights from two lists specifying the "to" weights from a node to its successor.  
    
    This function returns a 2x2xlen(to_node1) matrix, that specifies the cost of traversing the graph for which the weights represent edges. Useful to check the performance of our algorithm on path-length problems.  

    Parameters:
    to_node1 (list): a list of weights that specify the cost to travel to the "left" node. 
    to_node2 (list): the same as to_node1, but with the cost to travel to the "right" node. 

    Returns: 
    array: the numpy array constructed by the function. 
    '''

    length_lists = len(to_node1)
    assert len(to_node1) == len(to_node2), " The two lists must be of equal length "
    lists_stacked = np.array([to_node1,to_node2]) # should be 2x len
    lists_repeated = np.repeat(lists_stacked,2,axis = 1) # necessary to replicate for each node
    lists_reshaped = lists_repeated.reshape(2,2,length_lists,order = 'F')
    lists_rotated = np.swapaxes(lists_reshaped,0,1)

    return lists_rotated


def construct_trap_weights():
    '''
    A function to contruct a matrix of weights that "traps" greedy algorithms in a suboptimal solution.
    
    Parameters:
    to_node1 (list): a list of weights that specify the cost to travel to the "left" node. 
    to_node2 (list): the same as to_node1, but with the cost to travel to the "right" node. 

    Returns: 
    array: the numpy array constructed by the function. 
    list: the greedy and true optimal cost.   
    '''
    weights_0 = [10,1000,0,0,0]
    weights_1 = [100,1,1,1,1]
    weights = construct_toy_weights(weights_0,weights_1)
    weights[:,:,1] = weights[:,:,1].T ## this makes going to node 0 on the first move a trap. 
    weights[:,1,1] += 1 ## break the tie just so we get stereotyped behavior. 
    return weights,[1010,101]

def extend_trap(n):
    '''
    To test BB_k, we will extend our trap example to include n steps where the greedy solution will be optimal. 

    Parameters: 
    n (int): the number of non-challenging steps (at optimally 0 additional cost) to insert before the trap weights. 

    Returns: 
    array: the numpy array of weights constructed by the function. 
    list: the costs for choosing a greedy or optimal path through the sequence. 
    '''
    preweights = np.zeros((2,2,n))
    preweights[:,1,:] += 1
    harder_weights,costs = construct_trap_weights() 
    all_weights = np.concatenate((preweights,harder_weights),axis = -1)
    all_weights+=1
    added_costs=n+5
    full_costs=added_costs+np.array(costs)
    return all_weights,full_costs

def test_min_greedy_path(): 
    ## Check to see if you can truly find a minimum greedy path should it exist. 
    ## Initialize an array of ones: 
    dummy_weights = np.ones((4,4,50))
    ## Set a subset to zeros: 
    dummy_weights[0,0,:] = 0 
    ## Choose a slightly less obvious example: 
    harder_weights = construct_trap_weights()[0]
    assert np.all(min_greedy_path(dummy_weights,0)[0] == np.zeros(50,))
    assert np.all(min_greedy_path(harder_weights,0)[0] == np.zeros(5,))

def test_min_greedy_path_trap(): 
    ## Check to see if you can truly find a minimum greedy path should it exist. 
    
    ## Choose a slightly less obvious example: 
    harder_weights = construct_trap_weights()[0]
    assert np.all(min_greedy_path(harder_weights,0)[0] == np.zeros(5,))

def test_calculate_cost_path_0():
    '''
    To check that the greedy method is still working when we have no signature: 
    '''
    ## Check that this returns the correct behavior for signatures of variable size relative to the weights. 
    signature = [0]
    data,costs = extend_trap(10)
    greedycost = calculate_cost_path(signature,data)
    assert greedycost == costs[0]
    
def test_calculate_cost_path_1():
    '''
    To check that the greedy method is still working when we have a partial signature, but does not specify non-greedy behavior:
    '''
    ## Check that this returns the correct behavior for signatures of variable size relative to the weights. 
    signature = [0 for i in range(12)]
    data,costs = extend_trap(10)
    greedycost = calculate_cost_path(signature,data)
    assert greedycost == costs[0]

def test_calculate_cost_path_2():
    '''
    To check that the greedy method is still working when we have a partial signature, and the difficult decision has already been made: 
    '''
    ## Check that this returns the correct behavior for signatures of variable size relative to the weights. 
    signature = [0 for i in range(16)]
    data,costs = extend_trap(10)
    greedycost = calculate_cost_path(signature,data)
    assert greedycost == costs[0]

def test_calculate_cost_path_3():
    '''
    To check that the greedy method is still working when we have a partial signature, and a non-greedy decision has been made:
    '''
    ## Check that this returns the correct behavior for signatures of variable size relative to the weights. 
    signature = [0,1]
    data,costs = construct_trap_weights()
    greedycost = calculate_cost_path(signature,data)
    assert greedycost == costs[1]

def test_bound_path_accuracy():
    '''
    To check that BB_k returns expected behavior across a large collection of k- more specifically, asserts that BB_k performs as expected as a function of k (expected transition from apparent greedy behavior to apparent optimal behavior on a small dataset). 
    '''
    test_weights,costs = extend_trap(10) # generates a graph of length 20 
    test_node = Node_path([0],2,15)
    for k in range(15):
        cost,solution = bound_path(test_node,test_weights,k)
        if k < 11:
            assert cost == costs[0]
        else:
            assert cost == costs[1]

def test_bound_path_halt():
    '''
    To check that BB_k returns expected behavior w.r.t recognizing that it has found a solution. 
    '''
    test_weights,costs = extend_trap(10) # generates a graph of length 15 
    for N in range(17):
        test_node = Node_path([0 for n in range(N)],2,15)
        cost,solution = bound_path(test_node,test_weights,5)
        if N < 16:
            assert solution == 0
        else:
            assert solution == 1 

def test_bound_path_time():
    '''
    To check that longer expansions are taking more time, as we would expect. 
    '''
    test_weights,costs = extend_trap(10) # generates a graph of length 20 
    test_node = Node_path([0],2,15)
    durations = []
    for k in range(15):
        start = time.time()
        cost,solution = bound_path(test_node,test_weights,k)
        end = time.time()
        durations.append(end-start)

    for i in range(len(durations)-1):
        assert durations[i+1]>durations[i]
