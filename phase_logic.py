from qiskit import BasicAer, QuantumCircuit, QuantumRegister, execute
from qiskit.circuit.library import MCMT, OR
from qiskit.circuit.library.standard_gates import CZGate

from util.statevector import get_partial_statevector

# Create diffuser circuit
def diffuser(n):
    qc = QuantumCircuit(n)
    qc.h(range(n))
    qc.x(range(n))
    qc.compose(mtcx, qubits=range(n), inplace=True)
    qc.x(range(n))
    qc.h(range(n))

    # Return diffuser circuit as a gate
    gate = qc.to_gate()
    gate.name = "diffuser"

    return gate

# Set up register and ancilla qubits.
reg_a = QuantumRegister(1, name="a")
reg_b = QuantumRegister(1, name="b")
reg_c = QuantumRegister(1, name="c")
reg_length = len(reg_a) + len(reg_b) + len(reg_c)
ancilla_length = 4
ancilla = QuantumRegister(ancilla_length, name="ancilla")
qc = QuantumCircuit(reg_a, reg_b, reg_c, ancilla)
qc.h([*range(0, reg_length)])


# Amplitude amplification cycle
number_of_iterations = 1
for i in range(number_of_iterations):
    # Flip the marked value

    # Apply the diffuser
    qc.barrier()
    qc.append(diffuser(reg_length), range(reg_length))

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
        print("|{}⟩ {} probability = {}%".format(i, amp, round(prob * 100, 5)))

# Draw the circuit
qc.draw(
    output="mpl",
    style="iqp",
    cregbundle=False,
    initial_state=True,
    fold=-1,
    filename="phase_logic.png",
)
