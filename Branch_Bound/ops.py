import numpy as np 

## Define operations for branch and bound algorithms in action. 

## Define branching algorithm for path problem: 
def branch_path(Node_path):
    '''
    Branch operation for path node. We could imagine that this is more complicated in other settings, here we just call the 
    children method on the node. 
    '''
    return Node_path.children()
## Define bound algorithm for path problem. We define a parametric set of bound algorithms, correspnding to the bound strategy used. 
## At a given node, the parameter k determines a depth for which we recurse fully, after which we employ a greedy selection method over corresponding path choices. 
def bound_path(Node_path,data,k):
    '''
    Bound operation for path node. Our approximate bound calculates to a depth k what the cost of following that path would be, and then finds a greedy path from that starting point. 
    
    Parameters: 
    Node_path: A Node path instance that represents a solution set. 
    data: A set of weights that determine our particular problem. 
    k: the recursion depth we will use for our approximate cost calculation. 
    '''
    ## Problem parameters from the weights: 
    N = np.shape(data)[-1]+1
    d = np.shape(data)[0]
    
    ## First we get the signature of Node path in question: 
    base_sig = Node_path.signature
    
    current_depth = len(base_sig)
    search_depth = current_depth + k
    ## Come up with "effective signatures" of all paths we will check. 
    ### Come up with an effective k: 
    excess_depth = search_depth-N
    k_eff = k-np.max([0,excess_depth])
    ### Check if we will be greedy/we are at the bottom of the tree: 
    if k_eff == 0:
        eff_sigs = [base_sig]
    ### Otherwise we explore paths to depth k:  
    else: 
        recurse_sigs = np.array(np.meshgrid(*[np.arange(d) for ki in range(k_eff)])).T.reshape(-1,k_eff)
        eff_sigs = [base_sig+list(recurse_sig) for recurse_sig in recurse_sigs]
    ### Calculate cost for all elements of explored recursion: 
    all_cost = [calculate_cost_path(sig,data) for sig in eff_sigs]
    min_cost = np.min(all_cost)

    ### Finally, we need a flag to indicate if this represents a real solution: 
    if excess_depth == k:
        solution = 1
    else:
        solution = 0
    return min_cost,solution

## Given a signature, returns the cost of the corresponding solution (full solution if the signature is complete, greedy approximation if not)
def calculate_cost_path(signature,data):
    ## Calculate the cost of the given signature: 
    traversed_len = len(signature)-1
    ## The weights should be of length 1 - depth, as they are links between the nodes. 
    traversed = data[:,:,:traversed_len]
    ### Turn the signature into tuples for indexing:
    tuplesigs = [signature[i:i+2] for i in range(len(signature)-1)]
    ### Pick out chosen path: 
    traversed_cost = [traversed[tuplet[0],tuplet[1],t] for t,tuplet in enumerate(tuplesigs)]
    ## First check if we have to use a greedy strategy at all: 
    N = np.shape(data)[-1]+1
    if len(signature) == N:
        return sum(traversed_cost)
    else:
        untraversed = data[:,:,traversed_len:]
        prev_init = signature[-1]
        min_greedy_sig,min_greedy_cost = min_greedy_path(untraversed,prev_init)
        return sum(traversed_cost)+min_greedy_cost
        

def min_greedy_path(weights,prev_init):
    '''
    Finds the locally shortest path given a set of connective weights. 
    Parameters: 
    weights: A numpy array of shape (dxdxN), where d is the set of states available, and N is the number of iterations to run the path for 
    prev_init: The state to initialize the greedy search from
    Returns:
    path: A list containing the index of the locally best choice of path. 
    '''
    time = np.shape(weights)[-1]
    best_inds = []
    cost = 0
    for t in range(time):
        if t == 0:
            prev = prev_init
        else:
            prev = best_inds[-1]
        woi = weights[prev,:,t]
        ind = np.argmin(woi)
        cost_l = woi[ind]
        cost+= cost_l
        best_inds.append(ind)
    return best_inds,cost
