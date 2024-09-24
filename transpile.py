from qiskit import QuantumCircuit, transpile
from qiskit.providers.fake_provider import GenericBackendV2

qc = QuantumCircuit(3)
qc.y(0)
for t in range(2):
    qc.cx(0, t + 1)

print(qc.draw())

backend = GenericBackendV2(num_qubits=3)
t_qc = transpile(qc, backend, optimization_level=1)

# Draw the circuit
t_qc.draw(
    output="mpl",
    style="iqp",
    cregbundle=False,
    initial_state=True,
    fold=-1,
    filename="./docs/_static/transpile.png",
)
