from qiskit import BasicAer, QuantumCircuit, QuantumRegister, execute
from qiskit.circuit import Gate
from qiskit.circuit.library import MCMT, OR
from qiskit.circuit.library.standard_gates import CZGate

from util.statevector import get_partial_statevector


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
