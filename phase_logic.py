from qiskit import BasicAer, QuantumCircuit, QuantumRegister, execute
from qiskit.circuit import Gate
from qiskit.circuit.library import MCMT, OR
from qiskit.circuit.library.standard_gates import CZGate

from util.statevector import get_partial_statevector


# Create diffuser circuit
def diffuser(n) -> Gate:
    mtcz = MCMT(gate=CZGate(), num_ctrl_qubits=n - 1, num_target_qubits=1)
    qc = QuantumCircuit(n)
    qc.h(range(n))
    qc.x(range(n))
    qc.compose(mtcz, qubits=range(n), inplace=True)
    qc.x(range(n))
    qc.h(range(n))

    # Return diffuser circuit as a gate
    gate = qc.to_gate()
    gate.name = "diffuser"

    return gate


# Phase-logic circuit to flip the relative phases of all input states for which the statement evaluates to TRUE.
# Statement: `(a OR b) AND ((NOT a) OR c) AND ((NOT b) OR (NOT c)) AND (a OR c)`
def phase_flip() -> QuantumCircuit:
    a = QuantumRegister(1, name="a")
    b = QuantumRegister(1, name="b")
    c = QuantumRegister(1, name="c")
    scratch_length = 4
    scratch = QuantumRegister(scratch_length, name="scratch")
    qc = QuantumCircuit(a, b, c, scratch)

    # Clause 1: (a OR b)
    clause_1 = OR(num_variable_qubits=2, flags=[1, 1], mcx_mode="noancilla").to_gate(
        label="OR"
    )
    qc.append(clause_1, qargs=[a, b, scratch[0]])
    qc.barrier()

    # Clause 2: ((NOT a) OR c)
    clause_2 = OR(num_variable_qubits=2, flags=[-1, 1], mcx_mode="noancilla").to_gate(
        label="OR"
    )
    qc.append(clause_2, qargs=[a, c, scratch[1]])
    qc.barrier()

    # Clause 3: ((NOT b) OR (NOT c))
    clause_3 = OR(num_variable_qubits=2, flags=[-1, -1], mcx_mode="noancilla").to_gate(
        label="OR"
    )
    qc.append(clause_3, qargs=[b, c, scratch[2]])
    qc.barrier()

    # Clause 4: (a OR c)
    clause_4 = OR(num_variable_qubits=2, flags=[1, 1], mcx_mode="noancilla").to_gate(
        label="OR"
    )
    qc.append(clause_4, qargs=[a, c, scratch[3]])
    qc.barrier()

    # Phase AND gate
    mtcz = MCMT(gate=CZGate(), num_ctrl_qubits=scratch_length - 1, num_target_qubits=1)
    qc.compose(mtcz, qubits=scratch[:], inplace=True)
    qc.barrier()

    # Uncompute Clause 4
    qc.append(clause_4.inverse(), qargs=[a, c, scratch[3]])
    qc.barrier()

    # Uncompute Clause 3
    qc.append(clause_3.inverse(), qargs=[b, c, scratch[2]])
    qc.barrier()

    # Uncompute Clause 2
    qc.append(clause_2.inverse(), qargs=[a, c, scratch[1]])
    qc.barrier()

    # Uncompute Clause 1
    qc.append(clause_1.inverse(), qargs=[a, b, scratch[0]])

    return qc


# Set up register and ancilla qubits.
reg_a = QuantumRegister(1, name="a")
reg_b = QuantumRegister(1, name="b")
reg_c = QuantumRegister(1, name="c")
reg_length = len(reg_a) + len(reg_b) + len(reg_c)
ancilla_length = 4
ancilla = QuantumRegister(ancilla_length, name="ancilla")
qc = QuantumCircuit(reg_a, reg_b, reg_c, ancilla)
qc.h([*range(0, reg_length)])
qc.barrier()

# Amplitude amplification cycle
number_of_iterations = 2
for i in range(number_of_iterations):
    # Flip the marked value
    qc_phase_flip = phase_flip()
    qc.compose(qc_phase_flip, qubits=qc.qubits, inplace=True)
    qc.barrier()

    # Apply the diffuser
    qc.append(diffuser(reg_length), range(reg_length))
    qc.barrier()

# Run circuit
backend = BasicAer.get_backend("statevector_simulator")
job = execute(qc, backend)
result = job.result()

# Output statevector
outputstate = get_partial_statevector(
    qc, qargs=[*range(reg_length, qc.num_qubits)], label="register"
)

# Output state probabilities
print("Output state probabilities")
for i, amp in enumerate(outputstate):
    if abs(amp) > 0.000001:
        prob = abs(amp) * abs(amp)
        print(f"|{i}⟩ {amp} probability = {round(prob * 100, 3)}%")

# Draw the circuit
qc.decompose(gates_to_decompose=["OR", "or", "or_dg", "mcmt", "diffuser"], reps=2).draw(
    output="mpl",
    style="iqp",
    cregbundle=False,
    initial_state=True,
    fold=-1,
    filename="./docs/_static/phase_logic.png",
)
