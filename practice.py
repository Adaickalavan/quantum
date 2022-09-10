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