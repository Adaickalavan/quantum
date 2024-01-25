import math
from qiskit import QuantumCircuit, QuantumRegister, execute, BasicAer
from qiskit.circuit.library import QFT
from util.statevector import get_partial_statevector

# Set up quantum registers
eigenphase = QuantumRegister(4, name="eigenphase")
eigenstate = QuantumRegister(1, name="eigenstate")
qc = QuantumCircuit(eigenphase, eigenstate)

# Set up eigenstate 
which_eigenstate = "B"  # Desired signal
if which_eigenstate == "A":
    # Eigenstate `sqrt(0.15)|0⟩-sqrt(0.85)|1⟩` of Hadamard gate with corresponding eigenphase 180°
    qc.ry(math.radians(-135), eigenstate)
elif which_eigenstate == "B":
    # Eigenstate `sqrt(0.85)|0⟩+sqrt(0.15)|1⟩` of Hadamard gate with corresponding eigenphase 0°
    qc.ry(math.radians(45), eigenstate)

# Initialize the output qubits to superposition state using Hadamard gate
qc.h(eigenphase)
qc.barrier()

# Set up controlled unitary quantum gate
qc.ch(eigenphase[0], eigenstate)
qc.barrier()

# Perform Inverse Quantum Fourier Transform
qft_inv = QFT(num_qubits=len(eigenphase), inverse=True).to_gate(label="IQFT")
qc.append(qft_inv, qargs=range(len(eigenphase)))
qc.barrier()

# Run circuit
backend = BasicAer.get_backend("statevector_simulator")
job = execute(qc, backend)
result = job.result()

outputstate = get_partial_statevector(qc, qargs=[4], label="eigenphase")
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
    filename="phase_estimation.png",
)
