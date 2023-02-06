from qiskit import QuantumCircuit

qc = QuantumCircuit(3, 3)
# measure qubits 0, 1 & 2 to classical bits 0, 1 & 2 respectively
qc.measure([0,1,2], [0,1,2])
qc.draw()


from qiskit.providers.aer import AerSimulator

sim = AerSimulator()  # make new simulator object

job = sim.run(qc)      # run the experiment
result = job.result()  # get the results
result.get_counts()    # interpret the results as a "counts" dictionary

# Create quantum circuit with 3 qubits and 3 classical bits:
qc = QuantumCircuit(3, 3)
qc.x([0,1])  # Perform X-gates on qubits 0 & 1
qc.measure([0,1,2], [0,1,2])
qc.draw()    # returns a drawing of the circuit


from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

# Let's create a fresh quantum circuit
qc = QuantumCircuit(2)


qc = QuantumCircuit(2)
qc.h(0)
qc.h(1)
qc.cx(1,0)
qc.z(0)
qc.barrier
qc.draw()
ket = Statevector(qc)
ket.draw()
qc.cx(1,0)
qc.draw()
ket = Statevector(qc)
ket.draw()



MESSAGE = '00'

qc_alice = QuantumCircuit(2,2)

# Alice encodes the message
if MESSAGE[-1]=='1':
    qc_alice.x(0)
if MESSAGE[-2]=='1':
    qc_alice.x(1)

# then she creates entangled states
qc_alice.h(1)
ket = Statevector(qc_alice)
ket.draw()
qc_alice.cx(1,0)
qc_alice.draw()
ket = Statevector(qc_alice)
ket.draw()

qc_bob = QuantumCircuit(2,2)
# Bob disentangles
d = qc_bob.compose(qc_alice)
d.cx(1,0)
d.h(1)
# Then measures
d.measure([0,1],[0,1])
d.draw()
sim.run(d).result().get_counts()


MESSAGE = '00'

qc_alice = QuantumCircuit(2,2)
qc_alice.h(1)
qc_alice.cx(1,0)

if MESSAGE[-2]=='1':
    qc_alice.z(1)
if MESSAGE[-1]=='1':
    qc_alice.x(1)

ket = Statevector(qc_alice)
ket.draw()
qc_alice.draw()
qc_bob = QuantumCircuit(2,2)
# Bob disentangles
qc_bob.cx(1,0)
qc_bob.h(1)
# Then measures
qc_bob.measure([0,1],[0,1])
qc_bob.draw()
d = qc_alice.compose(qc_bob)
d.draw()
sim.run(d).result().get_counts()

from qiskit import Aer, QuantumCircuit
from qiskit.quantum_info import Statevector

backend = Aer.get_backend('aer_simulator')
meas_x = QuantumCircuit(1,1)
meas_x.h(0)
# meas_x.measure(0,0)
meas_x.draw()
meas_z = QuantumCircuit(1,1)
# meas_z.measure(0,0)
meas_z.draw()
qc = QuantumCircuit(1,1)
qc.x(0)
for basis,circ in [('z', meas_z), ('x', meas_x)]:
    print('Results from ' + basis + ' measurement:',
        backend.run(qc.compose(circ)).result().get_counts())
qc = QuantumCircuit(1,1)
qc.x(0)
qc.h(0)
ket = Statevector(qc)
ket.draw()
qcc = qc.compose(meas_x)
qcc.draw()
ket = Statevector(qcc)
ket.draw()


from math import pi

qc = QuantumCircuit(1, 1)
qc.ry(2*pi, 0)
qc.draw()
ket = Statevector(qc)
ket.draw()


qc_charlie = QuantumCircuit(2,2)
qc_charlie.ry(1.911,1)
qc_charlie.cx(1,0)
qc_charlie.ry(0.785,0)
qc_charlie.cx(1,0)
qc_charlie.ry(2.356,0)

qc_charlie.draw()


ket = Statevector(qc_charlie)
ket.draw()

meas_zz = QuantumCircuit(2,2)
meas_zz.measure([0,1],[0,1])
meas_zz.draw()

from qiskit.visualization import plot_histogram

print('Results for z measurements:')
counts = backend.run(qc_charlie.compose(meas_zz)).result().get_counts()
plot_histogram(counts)

from qiskit_textbook.games.hello_quantum import run_game

puzzle = run_game(0)


qc = QuantumCircuit(1,1)
qc.h(0)
qc.draw()
ket = Statevector(qc)
ket.draw()




from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit import QuantumCircuit, assemble, Aer
from math import pi, sqrt
from qiskit.visualization import plot_bloch_multivector, plot_histogram
sim = Aer.get_backend('aer_simulator')

def x_measurement(qc, qubit, cbit):
    """Measure 'qubit' in the X-basis, and store the result in 'cbit'"""
    qc.h(qubit)
    qc.measure(qubit, cbit)
    return qc

initial_state = [1/sqrt(2), -1/sqrt(2)]
# Initialize our qubit and measure it
qc = QuantumCircuit(1,1)
qc.initialize(initial_state, 0)
x_measurement(qc, 0, 0)  # measure qubit 0 to classical bit 0
qc.draw()

qobj = assemble(qc)  # Assemble circuit into a Qobj that can be run
counts = sim.run(qobj).result().get_counts()  # Do the simulation, returning the state vector
plot_histogram(counts)  # Display the output on measurement of state vector


from qiskit import QuantumCircuit, Aer, assemble
import numpy as np
from qiskit.visualization import plot_histogram, plot_bloch_multivector

qc = QuantumCircuit(3)
# Apply H-gate to each qubit:
for qubit in range(3):
    qc.h(qubit)
# See the circuit:
qc.draw()

svsim = Aer.get_backend('aer_simulator')
qc.save_statevector()
qobj = assemble(qc)
final_state = svsim.run(qobj).result().get_statevector()

# In Jupyter Notebooks we can display this nicely using Latex.
# If not using Jupyter Notebooks you may need to remove the 
# array_to_latex function and use print(final_state) instead.
from qiskit.visualization import array_to_latex
array_to_latex(final_state, prefix="\\text{Statevector} = ")



qc = QuantumCircuit(2)
qc.h(0)
qc.h(1)

# Apply H-gate to the first:
qc.h(0)
# Apply a CNOT:
qc.cx(0,1)
qc.draw()

# Apply H-gate to the first:
qc.h(0)
# Apply a CNOT:
qc.cx(0,1)
qc.draw()

ket = Statevector(qc)
ket.draw()





# Do the necessary imports
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import IBMQ, Aer, transpile
from qiskit.visualization import plot_histogram, plot_bloch_multivector, array_to_latex
from qiskit.extensions import Initialize
from qiskit.result import marginal_counts
from qiskit.quantum_info import random_statevector

def new_bob_gates(qc, a, b, c):
    qc.cx(b, c)
    qc.cz(a, c)

def measure_and_send(qc, a, b):
    """Measures qubits a & b and 'sends' the results to Bob"""
    qc.barrier()
    first = qc.measure(a,0)
    second = qc.measure(b,1)
    print(f"first={first}, second={second}")

def alice_gates(qc, psi, a):
    qc.cx(psi, a)
    qc.h(psi)

def create_bell_pair(qc, a, b):
    """Creates a bell pair in qc using qubits a & b"""
    qc.h(a) # Put qubit a into state |+>
    qc.cx(a,b) # CNOT with a as control and b as target

qc = QuantumCircuit(3,1)

# First, let's initialize Alice's q0

qc.x(0)
qc.barrier()

# Now begins the teleportation protocol
create_bell_pair(qc, 1, 2)
qc.barrier()
# Send q1 to Alice and q2 to Bob
alice_gates(qc, 0, 1)
qc.barrier()
# Alice sends classical bits to Bob
new_bob_gates(qc, 0, 1, 2)

# We undo the initialization process

# See the results, we only care about the state of qubit 2
# qc.measure(2,0)

# View the results:
qc.draw()

ket = Statevector(qc)
ket.draw()
display(array_to_latex(ket, prefix="|\\psi\\rangle ="))
