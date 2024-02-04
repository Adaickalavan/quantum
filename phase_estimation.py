import math

import numpy as np
from qiskit import BasicAer, QuantumCircuit, QuantumRegister, execute
from qiskit.circuit import Gate
from qiskit.circuit.library import QFT
from qiskit.circuit.library.standard_gates import HGate, TGate

from util.statevector import get_partial_statevector


def phase_to_frequency(
    qc_count: QuantumCircuit, qc_state: QuantumCircuit, unitary: Gate
) -> QuantumCircuit:
    count_length = qc_count.num_qubits
    state_length = qc_state.num_qubits
    controlled_unitary = unitary.control()
    qc = QuantumCircuit(
        QuantumRegister(count_length, name="count"),
        QuantumRegister(state_length, name="state"),
    )
    qc.compose(
        qc_state, [*range(count_length, count_length + state_length)], inplace=True
    )
    qc.barrier()
    qc.compose(qc_count, [*range(count_length)], inplace=True)
    qc.barrier()

    # Perform U^k operations, where k is repetitions.
    repetitions = 1
    state_qubits = [*range(count_length, count_length + state_length)]
    for i in range(count_length):
        for _ in range(repetitions):
            qc.append(controlled_unitary, [i] + state_qubits)
        repetitions *= 2

    return qc


# Set up eigenstate
which_eigenstate = "C"  # Desired signal
if which_eigenstate == "A":
    # Eigenstate `sqrt(0.15)|0⟩-sqrt(0.85)|1⟩` of Hadamard gate with eigenphase 180°
    qc_state = QuantumCircuit(1, name="state")
    qc_state.ry(math.radians(-135), 0)
    unitary = HGate()
elif which_eigenstate == "B":
    # Eigenstate `sqrt(0.85)|0⟩+sqrt(0.15)|1⟩` of Hadamard gate with eigenphase 0°
    qc_state = QuantumCircuit(1, name="state")
    qc_state.ry(math.radians(45), 0)
    unitary = HGate()
elif which_eigenstate == "C":
    # Eigenstate `sqrt(0)|0⟩+sqrt(1)|1⟩` of T gate with eigenphase 45°
    qc_state = QuantumCircuit(1, name="state")
    qc_state.x(0)
    unitary = TGate()
else:
    raise KeyError("Unkown eigenstate.")

# Set up counting register and apply Hadamard gates to the counting qubits
count_length = 3
qc_count = QuantumCircuit(count_length, name="count")
qc_count.h([*range(0, count_length)])

# Apply controlled unitary operations to kickback eigenphase of `U|Ψ⟩` to counting qubits.
qc = phase_to_frequency(qc_count=qc_count, qc_state=qc_state, unitary=unitary)
qc.barrier()
qc.draw()

# Perform Inverse Quantum Fourier Transform
qft_inv = QFT(num_qubits=count_length, inverse=True).to_gate(label="IQFT")
qc.append(qft_inv, qargs=range(count_length))
qc.barrier()

# Run circuit
backend = BasicAer.get_backend("statevector_simulator")
job = execute(qc, backend)
result = job.result()

# Output statevector
outputstate = get_partial_statevector(
    qc, qargs=[*range(count_length, qc.num_qubits)], label="count\_register"
)
count_value = int(np.argmax(outputstate))
eigenphase = count_value * 360 / 2**count_length
print(f"eigenphase = {eigenphase}\n")

# Output state probabilities
print("Output state probabilities")
for i, amp in enumerate(outputstate):
    if abs(amp) > 0.000001:
        prob = abs(amp) * abs(amp)
        print("|{}⟩ {} probability = {}%".format(i, amp, round(prob * 100, 5)))

# Draw the circuit
qc.decompose(gates_to_decompose="IQFT", reps=2).draw(
    output="mpl",
    style="iqp",
    cregbundle=False,
    initial_state=True,
    fold=-1,
    filename="./util/phase_estimation.png",
)
