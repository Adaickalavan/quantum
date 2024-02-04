import math

from IPython.display import display
from qiskit import BasicAer, QuantumCircuit, QuantumRegister, execute
from qiskit.visualization import array_to_latex

# Set up
a = QuantumRegister(3, name="a")
b = QuantumRegister(2, name="b")
qc = QuantumCircuit(a, b)

# a=sqrt(0.5)|1⟩+sqrt(0.5)|5⟩
qc.x(a[0])
qc.h(a[2])
qc.barrier()

# b=sqrt(0.5)|1⟩+45°sqrt(0.5)|3⟩
qc.x(b[0])
qc.h(b[1])
qc.rz(math.radians(90), b[1])
qc.barrier()

# a -= 3
qc.x(a[1])
qc.cx(a[1], a[2])
qc.x(a[0])
qc.cx(a[0], a[1])
qc.mcx([a[0], a[1]], a[2])
qc.barrier()

# if (a<0) then b++
qc.mcx([a[2], b[0]], b[1])
qc.cx(a[2], b[0])
qc.barrier()

# a += 3
qc.mcx([a[0], a[1]], a[2])
qc.cx(a[0], a[1])
qc.x(a[0])
qc.cx(a[1], a[2])
qc.x(a[1])
qc.barrier()

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
    filename="./docs/_static/arithmetic.png",
)
