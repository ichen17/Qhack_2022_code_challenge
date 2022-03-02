#! /usr/bin/python3

import sys
import pennylane as qml
from pennylane import numpy as np


def compare_circuits(angles):
    """Given two angles, compare two circuit outputs that have their order of operations flipped: RX then RY VERSUS RY then RX.
    Args:
        - angles (np.ndarray): Two angles
    Returns:
        - (float): | < \sigma^x >_1 - < \sigma^x >_2 |
    """

    # QHACK #

    # define a device and quantum functions/circuits here

    dev = qml.device("default.qubit", wires=2)

    @qml.qnode(dev)
    def circuit__rotation(angles):
        qml.RX(angles[0],wires=0)
        qml.RY(angles[1],wires=0)
        qml.RY(angles[1],wires=1)
        qml.RX(angles[0],wires=1)
        H = np.zeros((4, 4))
        H[1,0] = 1.0
        H[0,1] = 1.0
        H[2,3] = 1.0
        H[3,2] = 1.0
        H[0,2] = -1.0
        H[2,0] = -1.0
        H[1,3] = -1.0
        H[3,1] = -1.0
        return qml.expval(qml.Hermitian(H, [0,1]))

    y=circuit__rotation(angles)

    return np.abs(float(y))

if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    angles = np.array(sys.stdin.read().split(","), dtype=float)
    output = compare_circuits(angles)
    print(f"{output:.6f}")