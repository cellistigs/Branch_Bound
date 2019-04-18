## Define structure in which we store data on which to implement branch and bound. We define an abstract class called Node, which carries around a signature (indicating the solution set that it corresponds to), as well as the signature of its children and parents. 

## We think of this algorithm as traversing a tree, where each node represents a subset of problem solutions. Each node is identified by a signature that gives the subset of problem solutions that it represents, as well as the signatures of its parents and children.

class Node(object):
    '''
    Abstract class object that defines a subset of solutions to our problem. 
    Parameters: 
    signature: the tag that uniquely identifies the subset of solutions to which this node corresponds.   
    '''
    def __init__(self,signature):
        self.signature = signature 

    def children(self):
        '''
        Abstract method that returns the Node instances corresponding to the children of this particular node. 
        Parameters: 
        self
        Returns: 
        Children of this node
        '''
        child_sigs = self.childsig()

        return [Node(child_sig) for child_sig in child_sigs]

    def childsig(self):
        '''
        Method to get the signature of children from current node. 
        Parameters: 
        self
        Returns:
        signatures of children for this node
        '''
        raise NotImplementedError('PLEASE IMPLEMENT ME')

    def parent(self):
        '''
        Abstract method that returns the Node instance corresponding to the parent of this particular node. 
        Should be only one! 
        Parameters: 
        self
        Returns:
        Parent node of this node 
        '''
        parent_sig = self.parentsig()
        
        return Node(parent_sig)

    def parentsig(self):
        '''
        Method that returns the signature of parent of the current node. 
        Parameters:
        self
        Returns: 
        signature of parent node
        '''
        raise NotImplementedError('PLEASE IMPLEMENT ME')

class Node_path(Node):
    '''
    Toy model class to use Branch and Bound to find the shortest path for a walk on d nodes with N steps and time varying weights (imitates Viterbi inference)
    Parameters: 
    self
    signature: the signature of the node for the viterbi path is given by a list of length M specifying which of the d possible choices is specified by this Node. 
    d: the number of possible states available at every time point
    N: the number of time points available. 
    ''' 
    def __init__(self,signature,d,N):
        self.signature = signature
        self.d = d
        self.N = N

    def children(self):
        '''
        Method that returns the Node instances corresponding to the children of this particular node. 
        Parameters: 
        self
        Returns: 
        Children of this node
        '''
        child_sigs = self.childsig()

        return [Node_path(child_sig,self.d,self.N) for child_sig in child_sigs]


    def childsig(self):
        '''
        Method to define signatures of child Nodes from that of parent node. 
        Parameters: 
        self
        Returns:
        signatures of children for this node, as a list of lists. 
        '''
        if len(self.signature) == self.N:
            childsigs = []
        else:
            childsigs = [self.signature+[i] for i in range(self.d)]
        return childsigs

    def parent(self):
        '''
        Method that returns the Node instance corresponding to the parent of this particular node. 
        Should be only one! 
        Parameters: 
        self
        Returns:
        Parent node of this node 
        '''
        parent_sig = self.parentsig()
        
        if parent_sig is None:
            return None
        else:
            return Node_path(parent_sig,self.d,self.N) 

    def parentsig(self):
        '''
        Method that returns the signature of parent of the current node. 
        Parameters:
        self
        Returns: 
        signature of parent node
        '''
        if len(self.signature) == 0:
            return None 
        else: 
            parentsigs = self.signature[:-1]
            return parentsigs


