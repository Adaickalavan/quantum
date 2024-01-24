from qiskit import QuantumCircuit, QuantumRegister, execute, BasicAer
from qiskit.circuit.library import QFT
import math

# Set up quantum registers
eigenphase = QuantumRegister(4, name="eigenphase")
eigenstate = QuantumRegister(1, name="eigenstate")
qc = QuantumCircuit(eigenphase, eigenstate)

# Set up eigenstate and initialize the output qubits to superposition state using Hadamard gate
qc.ry(math.radians(-135),eigenstate)
qc.h(eigenphase)
qc.barrier()

# Set up unitary quantum gate
qc.ch(eigenphase[0], eigenstate);
qc.barrier()


# Perform Inverse Quantum Fourier Transform
qft_inv = QFT.inverse(num_qubits=len(eigenphase)).to_gate(label="QFT_Inv")
qc.append(qft_inv, qargs=range(len(eigenphase)))
qc.barrier()

# Run circuit
backend = BasicAer.get_backend("statevector_simulator")
job = execute(qc, backend)
result = job.result()

outputstate = result.get_statevector(qc, decimals=3)
for i, amp in enumerate(outputstate):
    if abs(amp) > 0.000001:
        prob = abs(amp) * abs(amp)
        print("|{}⟩ {} probability = {}%".format(i, amp, round(prob * 100, 5)))

# Draw the circuit
qc.decompose(gates_to_decompose="QFT_Inv", reps=2).draw(
    output="mpl",
    style="iqp",
    cregbundle=False,
    initial_state=True,
    fold=-1,
    filename="phase_estimation.png",
)
