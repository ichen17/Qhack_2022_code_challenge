import sys
import pennylane as qml
from pennylane import numpy as np
from pennylane import hf


def ground_state_VQE(H):
    """Perform VQE to find the ground state of the H2 Hamiltonian.
    Args:
        - H (qml.Hamiltonian): The Hydrogen (H2) Hamiltonian
    Returns:
        - (float): The ground state energy
        - (np.ndarray): The ground state calculated through your optimization routine
    """

    # QHACK #
    dev = qml.device("default.qubit", wires=4)

    @qml.qnode(dev)
    def circuit(param, wires):
        qml.BasisState(np.array([1, 1, 0, 0]), wires=wires)
        qml.DoubleExcitation(param[0], wires=[0, 1, 2, 3])
        return qml.expval(H)

    opt = qml.AdamOptimizer()
    theta = np.ones(1, requires_grad = True)
    for n in range(100):
        theta, energy = opt.step_and_cost(circuit, theta, wires=[0, 1, 2, 3])
        
    #@qml.qnode(dev)
    #def circuit(param):
    #    qml.BasisState(np.array([1, 1, 0, 0]), wires=[0, 1, 2, 3])
    #    qml.DoubleExcitation(param[0], wires=[0, 1, 2, 3])
    #    return qml.state()
    #print(theta)
        
    return energy, theta[0]


    # QHACK #


def create_H1(ground_state, beta, H):
    """Create the H1 matrix, then use `qml.Hermitian(matrix)` to return an observable-form of H1.
    Args:
        - ground_state (np.ndarray): from the ground state VQE calculation
        - beta (float): the prefactor for the ground state projector term
        - H (qml.Hamiltonian): the result of hf.generate_hamiltonian(mol)()
    Returns:
        - (qml.Observable): The result of qml.Hermitian(H1_matrix)
    """

    # QHACK #
    dev = qml.device("default.qubit", wires=4)
    @qml.qnode(dev)
    def circuit(ground_state):
        qml.BasisState(np.array([1, 1, 0, 0]), wires=[0, 1, 2, 3])
        qml.DoubleExcitation(ground_state, wires=[0, 1, 2, 3])
        return qml.density_matrix(wires=[0, 1, 2, 3])
   
    
    #coeffs, obs_list=qml.utils.decompose_hamiltonian((np.outer(ground_state,np.conj(ground_state))))
    
    #HH = np.outer(ground_state,np.conj(ground_state))
    
    #H1=H
    
    #for ith, ob in enumerate(obs_list):
    #print(coeffs)
    #QubitDensityMatrix()
    #qml.QubitUnitary(HH, wires=[0,1,2,3])
    dm=circuit(ground_state)
    
    coeffs, obs_list=qml.utils.decompose_hamiltonian(dm)
    
    H1=H+beta*qml.Hamiltonian(coeffs,obs_list) 
    
    return H1
    
    

    # QHACK #


def excited_state_VQE(H1):
    """Perform VQE using the "excited state" Hamiltonian.
    Args:
        - H1 (qml.Observable): result of create_H1
    Returns:
        - (float): The excited state energy
    """

    # QHACK #
    
    dev = qml.device("default.qubit", wires=4)

    @qml.qnode(dev)
    def circuit(param, wires):
        qml.BasisState(np.array([0, 1, 0, 1]), wires=wires)
        qml.DoubleExcitation(param[0], wires=[0, 1, 2, 3])
        return qml.expval(H1)

    opt = qml.NesterovMomentumOptimizer(0.1,0.5)
    #opt =qml.GradientDescentOptimizer(stepsize=0.3)
    theta = np.zeros(1, requires_grad = True)
    for n in range(100):
        theta, energy = opt.step_and_cost(circuit, theta, wires=[0, 1, 2, 3])
        
    opt = qml.AdamOptimizer(0.03,0.9)
    for n in range(50):
        theta, energy = opt.step_and_cost(circuit, theta, wires=[0, 1, 2, 3])
        
    return energy

    # QHACK #


if __name__ == "__main__":
    coord = float(sys.stdin.read())
    symbols = ["H", "H"]
    geometry = np.array([[0.0, 0.0, -coord], [0.0, 0.0, coord]], requires_grad=False)
    mol = hf.Molecule(symbols, geometry)

    H = hf.generate_hamiltonian(mol)()
    E0, ground_state = ground_state_VQE(H)

    beta = 15.0
    H1 = create_H1(ground_state, beta, H)
    E1 = excited_state_VQE(H1)

    answer = [np.real(E0), E1]
    print(*answer, sep=",")