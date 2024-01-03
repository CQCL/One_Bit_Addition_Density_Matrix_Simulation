import functools as ft
import itertools as it
import numpy as np
import operator as op
import qutip as qt
from qutip.qip.qasm import read_qasm
from qutip.qip.operations import cnot, hadamard_transform
from qutip.qip.circuit import QubitCircuit

qc = read_qasm("destructive-x-fault-tolerant-circuit.qasm")
# sim = qt.CircuitSimulator(qc, mode="density_matrix_simulator")
noiseless_qc = read_qasm("noiseless-x-fault-tolerant-circuit.qasm")
def tensor_index(operator_1, operator_2, i, j):
    eye_2 = qt.qeye(2)
    operator_list = []
    for index in range(10):
        if index == i:
            operator_list.append(operator_1)
        elif index == j:
            operator_list.append(operator_2)
        else:
            operator_list.append(eye_2)
    
    return qt.tensor(operator_list)

def kraus_operators(i, j):
    """
    As the noise model propagates off of ZZ() as opposed to CNOT, the
    Pauli noise bias must be changed.
    CNOT = (1 S^dag) (1 sqrt(X)^dag) (S^dag 1) ZZ (1 sqrt(Y)^dag),
    so any Pauli propagated off of the ZZ becomes equivalent to the
    same Pauli conjugated by (1 sqrt(Y)^dag) propagating off of the
    CNOT.
    As sqrt(Y)^dag is Pauli-equivalent to Hadamard, we need only switch
    X and Z in the targets, which we do just below.
    """

    ai, x, y, z = qt.qeye(2), qt.sigmax(), qt.sigmay(), qt.sigmaz()

    # Probability of a two qubit error
    p = 0.002048

    rate_paulis = [
                    (0.0786, ai, z), (0.0786, ai, y),(0.171, ai, x),
                    (0.0786, x, ai), (0.0002, x, z), (0.0002, x, y),
                    (0.0786, x, x), (0.0786, y, ai), (0.0002, y, z),
                    (0.0002, y, y), (0.0786, y, x),(0.171, z, ai),
                    (0.0786, z, z), (0.0786, z, y), (0.0284, z, x)
                    ]

    prob_paulis = [(1 - p, ai, ai)] + \
                    [(rp[0] * p, rp[1], rp[2]) for rp in rate_paulis]
    
    return [np.sqrt(prob) * tensor_index(p_1, p_2, i, j)
                    for prob, p_1, p_2 in prob_paulis]

def apply_kraus_operators(density_matrix, kraus_list):
    kraus_conj = [k * density_matrix * k.dag() for k in kraus_list]
    return sum(kraus_conj)

def postselect(state):
    ai = qt.qeye(2)
    pi_0 = qt.basis(2,0) * (qt.basis(2,0).dag())
    pi_1 = ai - pi_0
    ai_8 = qt.tensor(ai, ai, ai, ai, ai, ai, ai, ai)
    data_qubits = list(range(8))
    # Probability of a bit flip if 0 is measured
    p0 = 0.0017
    # Probability of a bit flip if 1 is measured
    p1 = 0.0045

    operator = qt.tensor(ai_8, pi_0, pi_0)
    state00 = (operator * state * operator).ptrace(data_qubits)

    operator = qt.tensor(ai_8, pi_0, pi_1)
    state01 = (operator * state * operator).ptrace(data_qubits)

    operator = qt.tensor(ai_8, pi_1, pi_0)
    state10 = (operator * state * operator).ptrace(data_qubits)

    operator = qt.tensor(ai_8, pi_1, pi_1)
    state11 = (operator * state * operator).ptrace(data_qubits)

    final_state = (1 - p0) * (1 - p0) * state00 + \
                    p1 * (1 - p0) * state10 + \
                    (1 - p0) * p1 * state01 * \
                    p1 * p1 * state11

    return final_state / final_state.tr()


def postselect_ideal(state):
    ai = qt.qeye(2)
    pi_0 = qt.basis(2,0) * (qt.basis(2,0).dag())
    pi_1 = ai - pi_0
    ai_8 = qt.tensor(ai, ai, ai, ai, ai, ai, ai, ai)
    data_qubits = list(range(8))
    # Probability of a bit flip if 0 is measured
    p0 = 0.0
    # Probability of a bit flip if 1 is measured
    p1 = 0.0

    operator = qt.tensor(ai_8, pi_0, pi_0)
    state00 = (operator * state * operator).ptrace(data_qubits)
    final_state =  state00

    return final_state / final_state.tr()

def propagate_circuit():
    psi0 = qt.basis(2, 0)
    state = qt.tensor(*[psi0 for _ in range(10)])
    
    state = state * state.dag()
    
    for (gate, prop) in zip(qc.gates, qc.propagators()):
        state = (prop) * state * (prop.dag())
        if gate.name == 'CNOT':
            # If the gate is a CNOT, apply the biased Pauli noise model
            # on target and control registers
            state = apply_kraus_operators(state, kraus_operators(gate.targets[0], gate.controls[0]))
            
    return postselect(state)

def ideal_state():
    # The computation from before, but with no noise applied
    psi_0 = qt.basis(2, 0)
    state = qt.tensor(psi_0, psi_0, psi_0, psi_0, psi_0, psi_0, psi_0,
                    psi_0, psi_0, psi_0)
    state = state * state.dag()
    
    for (gate, prop) in zip(noiseless_qc.gates, noiseless_qc.propagators()):
        state = (prop) * state * (prop.dag())
    
    return postselect_ideal(state)

def plus_one_projector(pauli_qobjs):
    big_I = qt.qeye(pauli_qobjs[0].dims[0])
    return ft.reduce(op.mul, [0.5 * (big_I + p) for p in pauli_qobjs])

def principal_eigenvector(matrix_qobj):
    return matrix_qobj.eigenstates(sort='high', eigvals=1)[1][0]

def clifford_outputs():
    ai, x, z = qt.qeye(2), qt.sigmax(), qt.sigmaz()

    s_x = [qt.tensor(x,  x,  x,  x,  x,  x,  x,  x)]

    s_z = [
            qt.tensor(z,  z,  z,  z,  ai, ai, ai, ai),
            qt.tensor(ai, ai, ai, ai, z,  z,  z,  z),
            qt.tensor(z,  z,  ai, ai, z,  z,  ai, ai),
            qt.tensor(z,  ai, z,  ai, z,  ai, z,  ai)]

    l_z = [qt.tensor(z, z, ai, ai, ai, ai, ai, ai),
            qt.tensor(z, ai, z, ai, ai, ai, ai, ai),
            qt.tensor(z, ai, ai, ai, z, ai, ai, ai)]

    l_x = [qt.tensor(x,  ai, x,  ai, x,  ai, x,  ai),
            qt.tensor(x,  x,  ai, ai, x,  x,  ai, ai),
            qt.tensor(x,  x,  x,  x,  ai, ai, ai, ai)
            ]

    # pure errors for X stabilizer are Zs
    t_x = [qt.tensor(ai, ai, ai, ai, ai, ai, ai, z)]

    # pure errors for Z stabilizers are Xs 
    t_z = [qt.tensor(ai, ai, ai, x, ai, ai, ai, ai),
            qt.tensor(x,  x,  x,  x,  x,  x,  x,  ai),
            qt.tensor(x,  x,  x,  x,  x,  ai, x, ai),
            qt.tensor(x,  x,  x,  x,  x,  x,  ai, ai)]

    z_outs = l_z + s_x + s_z
    x_outs = l_x + t_x + t_z

    return z_outs, x_outs

def encoder_unitary():
    z_outs, x_outs = clifford_outputs()

    all_zero_projector = plus_one_projector(z_outs)
    zero_state = principal_eigenvector(all_zero_projector)

    ai = qt.qeye(2)
    output = qt.tensor(ai, ai, ai, ai, ai, ai, ai, ai)
    output.data[:, 0] = zero_state.data
    for col_dx in range(1, output.shape[1]):
        new_col = zero_state.copy()
        for bit_dx in range(8):
            if (col_dx & (1 << (bit_dx))) != 0:
                new_col = x_outs[7 - bit_dx] * new_col

        output.data[:, col_dx] = new_col.data

    return output

def postselect_errors(state):
    """
    Post select on the last five qubits being 0. This is applied after the decoder unitary
    """
    identity = qt.qeye(2)
    projector = qt.basis(2, 0) * (qt.basis(2, 0).dag())
    operator = qt.tensor(identity, identity, identity, projector, projector, projector, projector, projector)
    post_selected_state = (operator * state * operator).ptrace([0, 1, 2])
    return post_selected_state / post_selected_state.tr()


def decoded_state():
    s = encoder_unitary()
    # Apply the decoder unitary to the result of propagating the
    # circuit, and then postselect on no errors having occurred
    # need to apply the inverse; actually an encoder unitary
    return postselect_errors(s.dag() * propagate_circuit() * s)

def ideal_decoded_state():
    s = encoder_unitary()
    return postselect_errors(s.dag() * ideal_state() * s)

def second_half_logical_circuit():
    return qt.tensor(cnot(2, 0, 1), hadamard_transform())

def arithmetic_failure_rate():
    # Calculates the arithmetic failure rate of the circuit.
    diag = (second_half_logical_circuit() * decoded_state() * second_half_logical_circuit()).diag()
    return diag[0b001] + diag[0b011] + diag[0b100] + diag[0b111]

def postselection_fraction():
    """
    Probability that a state preparation experiment will succeed.
    """
    s = encoder_unitary()
    state = s.dag() * propagate_circuit() * s
    identity = qt.qeye(2)
    projector = qt.basis(2, 0) * (qt.basis(2, 0).dag())
    operator = qt.tensor(identity, identity, identity, projector, projector, projector, projector, projector)
    post_selected_state = (operator * state * operator).ptrace([0, 1, 2])
    return post_selected_state.tr()

if __name__ == '__main__':
    frac = postselection_fraction()
    arith_rate = arithmetic_failure_rate()
    print("\n")
    print(f"The acceptance rate predicted by QuTiP simulation is {frac}")
    print(f"The arithmetic failure rate predicted by QuTiP simulation is {arith_rate}")
    
    noisy = ((second_half_logical_circuit() * decoded_state() * second_half_logical_circuit()))
    noiseless = ((second_half_logical_circuit() * ideal_decoded_state() * second_half_logical_circuit()))

    print(f"The fidelity between the noisy and ideal output predicted by QuTiP simulation is {qt.fidelity(noiseless, noisy)}")
    
    """
    uncomment to examine error rates wrt different observables
    """
    # pauli_list=[(qt.qeye(2),"I"),(qt.sigmax(),"X"),(qt.sigmay(),"Y"),(qt.sigmaz(),"Z")]
    # for p,pn in pauli_list:
    #     for q,qn in pauli_list:
    #         for r,rn in pauli_list:
    #             pauli = qt.tensor(p,q,r)
    #             print(f'|{pn}{qn}{rn}| {qt.fidelity(pauli*noiseless*pauli,noisy)}|')
