
#! /usr/bin/python3

import sys
from pennylane import numpy as np
import pennylane as qml


def deutsch_jozsa(fs):
    """Function that determines whether four given functions are all of the same type or not.
    Args:
        - fs (list(function)): A list of 4 quantum functions. Each of them will accept a 'wires' parameter.
        The first two wires refer to the input and the third to the output of the function.
    Returns:
        - (str) : "4 same" or "2 and 2"
    """

    # QHACK #
    
    dev = qml.device("default.qubit", wires=range(7), shots=1)
    
    @qml.qnode(dev)
    def circuit(funs):
        """Implements the Deutsch Jozsa algorithm."""

        # QHACK #
        wires=range(7)
        
        qml.PauliX(wires=2)
        
        qml.Hadamard(wires=2)
        
        for num,fun in enumerate(funs):
            
            qml.Hadamard(wires=1)
            
            qml.Hadamard(wires=0)
            
            fun(wires)
                
            qml.Hadamard(wires=1)
            
            qml.Hadamard(wires=0)
            
            qml.Toffoli(wires=[0,1,num+3])
            
            
        return qml.sample(wires=[3,4,5,6])
    
    ans=circuit(fs)
    
    if list(ans) == [1,0,1,0] or list(ans) == [0,0,0,0]: 
        
        return "4 same"
    
    else:
        
        return "2 and 2"
    

    # QHACK #


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = sys.stdin.read().split(",")
    numbers = [int(i) for i in inputs]

    # Definition of the four oracles we will work with.

    def f1(wires):
        qml.CNOT(wires=[wires[numbers[0]], wires[2]])
        qml.CNOT(wires=[wires[numbers[1]], wires[2]])

    def f2(wires):
        qml.CNOT(wires=[wires[numbers[2]], wires[2]])
        qml.CNOT(wires=[wires[numbers[3]], wires[2]])

    def f3(wires):
        qml.CNOT(wires=[wires[numbers[4]], wires[2]])
        qml.CNOT(wires=[wires[numbers[5]], wires[2]])
        qml.PauliX(wires=wires[2])

    def f4(wires):
        qml.CNOT(wires=[wires[numbers[6]], wires[2]])
        qml.CNOT(wires=[wires[numbers[7]], wires[2]])
        qml.PauliX(wires=wires[2])

    output = deutsch_jozsa([f1, f2, f3, f4])
    print(f"{output}")