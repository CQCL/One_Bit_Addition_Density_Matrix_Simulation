import itertools as it
import numpy as np
import qutip as qt

import ccz_state_prep as csp

def commuting(op_0, op_1):
    return np.allclose(op_0 * op_1 - op_1 * op_0, 0.)

def anticommuting(op_0, op_1):
    return np.allclose(op_0 * op_1 + op_1 * op_0, 0.)

def pairwise_anticommuting(z_outs, x_outs):
    n_ops = len(z_outs)
    ops = z_outs + x_outs

    for dx in range(0, n_ops):
        acom_dx = n_ops + dx
        op = ops[dx]
        for other_dx in it.chain(range(dx + 1, acom_dx), range(acom_dx + 1, 2*n_ops)):
            if not(commuting(op, ops[other_dx])):
                return False

        if not(anticommuting(op, ops[acom_dx])):
            return False

    for dx in range(n_ops, 2 * n_ops):
        op = ops[dx]
        for other_dx in range(dx + 1, 2 * n_ops):
            if not(commuting(op, ops[other_dx])):
                return False

    return True

def conjugates_as_clifford(u, z_outs, x_outs):
    ai, x, z = qt.qeye(2), qt.sigmax(), qt.sigmaz()   
    nq = len(z_outs)
    for q in range(nq):
        x_lst = [ai for _ in range(q)] + [x] + [ai for _ in range(q + 1, nq)]
        z_lst = [ai for _ in range(q)] + [z] + [ai for _ in range(q + 1, nq)]
        x_in = qt.tensor(*x_lst)
        z_in = qt.tensor(*z_lst)

        if not(np.allclose(u * x_in * u.dag(), x_outs[q])):
            return False

        if not(np.allclose(u * z_in * u.dag(), z_outs[q])):
            return False

    return True

def test_clifford_outputs_commute_correctly():
	assert pairwise_anticommuting(*csp.clifford_outputs())

def test_unitary_encoder_conjugates_paulis_correctly():
	z_outs, x_outs = csp.clifford_outputs()
	u = csp.encoder_unitary()
	assert u.isunitary
	assert conjugates_as_clifford(u, z_outs, x_outs)

def test_kraus_sum():
	kraus_ops = csp.kraus_operators(0, 1)
	i2 = qt.qeye(2)
	eye_10 = qt.tensor(*[i2 for _ in range(10)])
	assert np.allclose(sum([k.dag() * k for k in kraus_ops]), eye_10)