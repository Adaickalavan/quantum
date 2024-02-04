from IPython.display import display
from qiskit import BasicAer, QuantumCircuit, QuantumRegister, execute
from qiskit.circuit.library import MCMT
from qiskit.visualization import array_to_latex

from util.statevector import get_partial_statevector

# Set up
a = QuantumRegister(2, name="a")
b = QuantumRegister(2, name="b")
scratch = QuantumRegister(1, name="scratch")
qc = QuantumCircuit(scratch, a, b)

# a=|3⟩
qc.x(a[1])
qc.x(a[0])
qc.barrier()

# b=|2⟩
qc.x(b[1])
qc.barrier()

# Verify statevector
print("Statevector after initialization")
get_partial_statevector(qc, [1, 2, 3, 4], "scratch")
get_partial_statevector(qc, [0, 3, 4], "a")
get_partial_statevector(qc, [0, 1, 2], "b")

# Create multi target controlled-x gate
mt2cx = MCMT(gate="x", num_ctrl_qubits=1, num_target_qubits=2)

# Compute abs(a)
qc.cx(a[1], scratch)  # scratch qubit
qc.compose(mt2cx, qubits=[0, 1, 2], inplace=True)
qc.mcx([a[0], scratch], a[1])
qc.cx(scratch, a[0])
qc.barrier()

# Verify statevector
print("Statevector after abs(a)")
get_partial_statevector(qc, [1, 2, 3, 4], "scratch")
get_partial_statevector(qc, [0, 3, 4], "a")
get_partial_statevector(qc, [0, 1, 2], "b")

# b += abs(a)
qc.mcx([b[0], a[0]], b[1])
qc.cx(a[0], b[0])
qc.cx(a[1], b[1])
qc.barrier()

# Verify statevector
print("Statevector after b += abs(a)")
get_partial_statevector(qc, [1, 2, 3, 4], "scratch")
get_partial_statevector(qc, [0, 3, 4], "a")
get_partial_statevector(qc, [0, 1, 2], "b")

# uncompute abs(a)
qc.cx(scratch, a[0])
qc.mcx([a[0], scratch], a[1])
qc.compose(mt2cx, qubits=[0, 1, 2], inplace=True)
qc.cx(a[1], scratch)
qc.barrier()

# Verify statevector
print("Statevector after Uncompute abs(a)")
get_partial_statevector(qc, [1, 2, 3, 4], "scratch")
get_partial_statevector(qc, [0, 3, 4], "a")
get_partial_statevector(qc, [0, 1, 2], "b")

# Run circuit
backend = BasicAer.get_backend("statevector_simulator")
job = execute(qc, backend)
result = job.result()

outputstate = result.get_statevector(qc, decimals=3)

display(array_to_latex(outputstate, prefix="\\text{Statevector}", max_size=32))

for i, amp in enumerate(outputstate):
    if abs(amp) > 0.000001:
        print("|{}> {}".format(i, amp))

# Draw the circuit
qc.draw(
    output="mpl",
    style="iqp",
    cregbundle=False,
    initial_state=True,
    fold=-1,
    filename="./docs/_static/scratch_qubit.png",
)
