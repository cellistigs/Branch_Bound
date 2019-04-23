import numpy as np
import time
from Branch_Bound.experiments import BB_FIFO,BB_LIFO,BB_Q
from scipy.sparse.csgraph import csgraph_from_dense,dijkstra
from test_ops import extend_trap 

def for_viterbi(weights):
    '''
    Converts weights for this problem to a csgraph representation that can be used to check arbitrary graphs against a ground truth dijkstra solver. 

    Given a representation that gives transition cost at every point of our solution space tree, embedding the solution space tree into a directed graph representation. Invalid nodes are represented by having infinity cost, self transitions have no cost, and the actual transition matrix is represented in the upper off diagonal band. 

    Parameters:
    weights (array): input representation of weights for solution via BB. 

    Returns:
    array: csgraph representation of weights for solution via Dijkstra. 
    '''
    ## Discover the right dimensions to work from. 
    d,N = np.shape(weights)[0],np.shape(weights)[-1]+3 # for nodes, not transition (+1), for initialization and end state (+2)
    ## Some weight-agnostic blocks: 
    diag = np.ones((d,d))*np.inf
    for i in range(np.shape(diag)[0]):
        diag[i,i] = 0 
    off = np.ones((d,d))*np.inf
    ## Initialize the block matrix as a list of lists
    block = [[off for n in range(N)] for n in range(N)]
    ## Replace the diagonals
    for i in range(len(block)):
        block[i][i] = diag 

    ## Replace the first and lastupper off diagonal with an array of zeros to find the right initialization and end state: 
    block[0][1] = np.zeros((d,d))
    block[N-2][N-1] = np.zeros((d,d))
    ## Now we replace the upper off diagonals with the actual data: 
    for n in range(N-3):
        block[n+1][n+2] = weights[:,:,n]

    block_matrix = np.block(block)
    return block_matrix

def recover_viterbipath(weights):
    ''' 
    Function to recover the shortest path through the set of weights we find as according to the viterbi algorithm. 
    '''
    matreformed_raw = for_viterbi(weights)
    matreformed = csgraph_from_dense(matreformed_raw,null_value = np.inf)
    costs,pred = dijkstra(matreformed,indices=0,return_predecessors=True)
    mincost = costs[-1]
    d = weights.shape[0] 
    i = len(costs)-1
    path = []
    while i != 0:
        path.append(i%d)
        i = pred[i]
    return mincost,path[:0:-1]


def test_BB_FIFO_path():
    '''
    Constructs an array to test the solutions that expected solutions are found.
    '''

    ## First construct weights: 
    weights,costs = extend_trap(15)
    ## Gives an array of size 20 as the transition weights, with k_critical (switch from greedy to optimal strategy being 1.) 
    greedy_solution_nodes = BB_FIFO(weights,0)
    greedyout = [node[0].signature for node in greedy_solution_nodes]
    greedycost = [node[1][0] for node in greedy_solution_nodes]
    print(greedycost,costs)
    optans0 = np.zeros(21,)
    optans0[16] = 1
    optans0[0] = 1
    optans1 = np.zeros(21,)
    optans1[16] = 1
    all_ans = [list(optans0),list(optans1)]
    for solution in greedyout:
        assert solution in all_ans        
def test_BB_FIFO_cost():
    '''
    Constructs an array to test the solutions that expected solutions are found.
    '''

    ## First construct weights: 
    weights,costs = extend_trap(15)
    ## Gives an array of size 20 as the transition weights, with k_critical (switch from greedy to optimal strategy being 1.) 
    greedy_solution_nodes = BB_FIFO(weights,0)
    greedyout = [node[0].signature for node in greedy_solution_nodes]
    greedycost = [node[1][0] for node in greedy_solution_nodes]
    print(greedycost,costs)
    optans0 = np.zeros(21,)
    optans0[16] = 1
    optans0[0] = 1
    for solution in greedycost:
        assert costs[1] == solution
        
def test_BB_LIFO_path():
    '''
    Constructs an array to test the solutions that expected solutions are found.
    '''

    ## First construct weights: 
    weights,costs = extend_trap(15)
    ## Gives an array of size 20 as the transition weights, with k_critical (switch from greedy to optimal strategy being 1.) 
    greedy_solution_nodes = BB_LIFO(weights,0)
    greedyout = [node[0].signature for node in greedy_solution_nodes]
    optans0 = np.zeros(21,)
    optans0[16] = 1
    optans0[0] = 1
    for solution in greedyout:
        assert np.all(solution == optans0)

def test_BB_LIFO_cost():
    '''
    Constructs an array to test the solutions that expected solutions are found.
    '''

    ## First construct weights: 
    weights,costs = extend_trap(15)
    ## Gives an array of size 20 as the transition weights, with k_critical (switch from greedy to optimal strategy being 1.) 
    greedy_solution_nodes = BB_LIFO(weights,0)
    greedyout = [node[0].signature for node in greedy_solution_nodes]
    greedycost = [node[1][0] for node in greedy_solution_nodes]
    optans0 = np.zeros(21,)
    optans0[16] = 1
    optans0[0] = 1
    for solution in greedycost:
        print(greedycost,costs)
        assert solution in costs


#def test_BB_Q():
#    '''
#    Constructs an array to test the solutions that expected solutions are found.
#    '''
#
#    ## First construct weights: 
#    weights,costs = extend_trap(15)
#    ## Gives an array of size 20 as the transition weights, with k_critical (switch from greedy to optimal strategy being 1.) 
#    greedy_solution_node = BB_Q(weights,1)
#    print(greedy_solution_node)
#    greedyout = greedy_solution_node[0].signature
#    optans0 = np.zeros(20,)
#    optans0[16] = 1
#    all_ans = [optans0]
#    print(greedyout==all_ans[0])
#    assert np.all(greedyout == all_ans[s])

def test_BB_FIFO_dijkstra_cost():
    '''
    compares the optimal solution to one found by dijkstra's algorithm. 
    '''

    ## First randomly sample weights: 
    weights = np.random.poisson(15,size = (6,6,5))
    cost,path = recover_viterbipath(weights)
    for k in range(6):
        greedy_solution_nodes = BB_FIFO(weights,k)
        greedyout = [node[0].signature for node in greedy_solution_nodes]
        print([node[0].signature for node in greedy_solution_nodes],path)
        interim_solution = np.inf
        if k < 5:
            assert np.all([cost<=node[1][0] for node in greedy_solution_nodes])
            assert np.all([interim_solution>=node[1][0] for node in greedy_solution_nodes])
            interim_solution = greedy_solution_nodes[0][1][0]
        else:
            assert np.all([cost==node[1][0] for node in greedy_solution_nodes])
            

def test_BB_FIFO_dijkstra_path():
    '''
    compares the optimal solution to one found by dijkstra's algorithm. 
    '''

    ## First randomly sample weights: 
    weights = np.random.poisson(15,size = (6,6,5))
    cost,path = recover_viterbipath(weights)
    for k in range(6):
        greedy_solution_nodes = BB_FIFO(weights,k)
        greedyout = [node[0].signature for node in greedy_solution_nodes]
        interim_solution = np.inf
        if k < 5:
            assert np.all([cost<=node[1][0] for node in greedy_solution_nodes])
            assert np.all([interim_solution>=node[1][0] for node in greedy_solution_nodes])
            interim_solution = greedy_solution_nodes[0][1][0]
        else:
            assert path in [node[0].signature for node in greedy_solution_nodes]
            
def test_BB_LIFO_dijkstra_cost():
    '''
    compares the optimal solution to one found by dijkstra's algorithm. 
    '''

    ## First randomly sample weights: 
    weights = np.random.poisson(15,size = (6,6,5))
    cost,path = recover_viterbipath(weights)
    for k in range(6):
        greedy_solution_nodes = BB_LIFO(weights,k)
        greedyout = [node[0].signature for node in greedy_solution_nodes]
        print([node[0].signature for node in greedy_solution_nodes],path)
        interim_solution = np.inf
        if k < 5:
            assert np.all([cost<=node[1][0] for node in greedy_solution_nodes])
            assert np.all([interim_solution>=node[1][0] for node in greedy_solution_nodes])
            interim_solution = greedy_solution_nodes[0][1][0]
        else:
            assert np.all([cost==node[1][0] for node in greedy_solution_nodes])
            

def test_BB_LIFO_dijkstra_path():
    '''
    compares the optimal solution to one found by dijkstra's algorithm. 
    '''

    ## First randomly sample weights: 
    weights = np.random.poisson(15,size = (6,6,5))
    cost,path = recover_viterbipath(weights)
    for k in range(6):
        greedy_solution_nodes = BB_LIFO(weights,k)
        greedyout = [node[0].signature for node in greedy_solution_nodes]
        interim_solution = np.inf
        if k < 5:
            assert np.all([cost<=node[1][0] for node in greedy_solution_nodes])
            assert np.all([interim_solution>=node[1][0] for node in greedy_solution_nodes])
            interim_solution = greedy_solution_nodes[0][1][0]
        else:
            assert path in [node[0].signature for node in greedy_solution_nodes]
            
#def test_BB_Q_dijkstra():
#    '''
#    compares the optimal solution to one found by dijkstra's algorithm. 
#    '''
#
#    ## First randomly sample weights: 
#    weights = np.random.poisson(15,size = (6,6,5))
#    cost,path = recover_viterbipath(weights)
#    for k in range(7):
#        greedy_solution_nodes = [BB_Q(weights,k)]
#        print([node for node in greedy_solution_nodes],cost,'here')
#        greedyout = [node[0].signature for node in greedy_solution_nodes]
#        if k < 6:
#            assert np.all([cost<=node[1][0] for node in greedy_solution_nodes])
#        else:
#            assert np.all([cost==node[1][0] for node in greedy_solution_nodes])
            
