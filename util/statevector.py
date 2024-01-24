import numpy as np
from qiskit.quantum_info import Statevector, partial_trace
from qiskit.visualization import array_to_latex
from IPython.display import display


def get_partial_statevector(qc, qargs, label="\\psi"):
    # Get density matrix for desired qubits
    full_statevector = Statevector(qc)
    partial_density_matrix = partial_trace(full_statevector, qargs)

    # Extract statevector out of the density matrix
    partial_statevector = np.diagonal(partial_density_matrix)

    display(
        array_to_latex(
            partial_statevector,
            precision=3,
            prefix=f"{label} =",
            max_size=2**qc.num_qubits,
        )
    )

    return partial_statevector
