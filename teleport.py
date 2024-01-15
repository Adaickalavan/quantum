import math
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, BasicAer
from qiskit.visualization import array_to_latex
from IPython.display import display

alice = QuantumRegister(1, name="alice")
ep = QuantumRegister(1, name="entangled_pair")
bob = QuantumRegister(1, name="bob")
alice_c = ClassicalRegister(1, name="alice_c")
ep_c = ClassicalRegister(1, name="entangled_pair_c")
bob_c = ClassicalRegister(1, name="bob_c")
qc = QuantumCircuit(alice, ep, bob, alice_c, ep_c, bob_c)

# Entangle
qc.h(ep)
qc.cx(ep, bob)
qc.barrier()

# Prep payload
qc.reset(alice)
qc.h(alice)
qc.rz(math.radians(45), alice)
qc.h(alice)
qc.barrier()

# Send
qc.cx(alice, ep)
qc.h(alice)
qc.measure(alice, alice_c)
qc.measure(ep, ep_c)
qc.barrier()

# Receive
qc.x(bob).c_if(ep_c, 1)
qc.z(bob).c_if(alice_c, 1)
qc.barrier()

# Verify
qc.h(bob)
qc.rz(math.radians(-45), bob)
qc.h(bob)
qc.measure(bob, bob_c)

# Run circuit
backend = BasicAer.get_backend("statevector_simulator")
job = execute(qc, backend)
result = job.result()

counts = result.get_counts(qc)
print("counts:", counts)

# Display statevector
outputstate = result.get_statevector(qc, decimals=3)
display(array_to_latex(outputstate, prefix="\\text{Statevector} = "))

# Draw the circuit
qc.draw(
    output="mpl",
    style="iqp",
    cregbundle=False,
    initial_state=True,
    fold=-1,
    filename="teleport.png",
)
