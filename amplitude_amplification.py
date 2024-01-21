from qiskit import QuantumCircuit, QuantumRegister, execute, BasicAer
from qiskit.visualization import array_to_latex
from IPython.display import display
from qiskit.circuit.library import MCMT
from qiskit.quantum_info import Statevector

# Set up the program
n_qubits = 4
number_to_flip = 3
number_of_iterations = 2
reg = QuantumRegister(n_qubits, name="reg")
qc = QuantumCircuit(reg)
qc.h(reg)
x_bits = ~number_to_flip  # Perform bit flip. Here, `~x` is equivalent to `(-x) - 1`.
x_list = [reg[x] for x in range(n_qubits) if x_bits & (1 << x)]

# Create multi controlled-z gate
mtcx = MCMT(gate="cz", num_ctrl_qubits=n_qubits - 1, num_target_qubits=1)

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

# Verify statevector
print(f"Statevector after 0 amplitude amplification iteration")
ket = Statevector(qc)
display(array_to_latex(ket, precision=3, prefix="\\psi =", max_size=2**n_qubits))

# Amplitude amplification cycle
for i in range(number_of_iterations):
    # Flip the marked value
    qc.barrier()
    qc.x(x_list)
    qc.compose(mtcx, qubits=range(n_qubits), inplace=True)
    qc.x(x_list)

    # Apply the diffuser
    qc.barrier()
    qc.append(diffuser(n_qubits), range(n_qubits))

    # Verify statevector
    print(f"Statevector after {i+1} amplitude amplification iteration")
    ket = Statevector(qc)
    display(array_to_latex(ket, precision=3, prefix="\\psi =", max_size=2**n_qubits))

# Run circuit
backend = BasicAer.get_backend("statevector_simulator")
job = execute(qc, backend)
result = job.result()

print("Final state probabilities")
outputstate = result.get_statevector(qc, decimals=3)
total_prob = 0
for i, amp in enumerate(outputstate):
    if abs(amp) > 0.000001:
        prob = abs(amp) * abs(amp)
        total_prob += prob
        print("|{}⟩ {} probability = {}%".format(i, amp, round(prob * 100, 5)))
print("Total probability: {}%".format(int(round(total_prob * 100))))

# Draw the circuit
qc.draw(
    output="mpl",
    style="iqp",
    cregbundle=False,
    initial_state=True,
    fold=-1,
    filename="amplitude_amplification.png",
)
