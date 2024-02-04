import math

from qiskit import BasicAer, QuantumCircuit, QuantumRegister, execute
from qiskit.circuit.library import QFT

# Set up
signal = QuantumRegister(4, name="signal")
qc = QuantumCircuit(signal)

# Prepare the signal
which_signal = "B"  # Desired signal
qc.h(signal)
if which_signal == "A":
    qc.rz(math.radians(180), signal[0])
elif which_signal == "B":
    qc.rz(math.radians(90), signal[0])
    qc.rz(math.radians(180), signal[1])
elif which_signal == "C":
    qc.rz(math.radians(45), signal[0])
    qc.rz(math.radians(90), signal[1])
    qc.rz(math.radians(180), signal[2])
elif which_signal == "D":  # Square-wave signal
    qc.rz(math.radians(180), signal[2])

# Perform Quantum Fourier Transform
qc.barrier()
qft = QFT(num_qubits=len(signal)).to_gate(label="QFT")
qc.append(qft, qargs=range(len(signal)))
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
qc.decompose(gates_to_decompose="QFT", reps=2).draw(
    output="mpl",
    style="iqp",
    cregbundle=False,
    initial_state=True,
    fold=-1,
    filename="./util/quantum_fourier_transform.png",
)
