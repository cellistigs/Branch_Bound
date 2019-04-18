import numpy as np
import time
from Branch_Bound.dataformat import Node,Node_path

## Test that the child classes of the parent class are of the correct class:
def test_children():
    node_ex = Node_path([],4,10)
    children = node_ex.children()
    for child in children:
        assert type(node_ex) == type(child)
    return None

def test_parent():
    node_ex = Node_path([],4,10)
    children = node_ex.children()
    for child in children:
        assert type(child) == type(child.parent())
    return None

## Find an easy way to extend this to Node_path
def test_childsigs_path():
    node_ex = Node_path([0,1,2,0],4,10)
    children = node_ex.children()
    for child in children:
        assert node_ex.signature == child.signature[:-1]

def test_parentsigs_path():
    node_ex = Node_path([0,1,2,0],4,10)
    parent = node_ex.parent()
    assert node_ex.signature[:-1] == parent.signature
        
if __name__ == '__main__':
    test_children()
    test_parent()
    test_childsigs_path()
    test_parentsigs_path()
