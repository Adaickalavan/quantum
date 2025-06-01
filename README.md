# Quantum Computing

See [website](https://adaickalavan.github.io/portfolio/quantum/) for more information.

Here, we explore quantum computing and quantum error correction. Each file is a standalone example.

## Installation
First, perform generic setup as follows.  
```bash
$ cd <path>/quantum
$ python3.10 -m venv ./.venv
$ source ./.venv/bin/activate
$ pip install --upgrade pip
$ pip install qiskit[visualization]
$ pip install qiskit-ibm-runtime
$ pip install matplotlib pylatexenc ipykernel
```

Users are recommended to run each of this repository's code files inside the interactive window in VSCode.

Alternatively, users may run the code inside JupyterLab. Follow the additional steps below to install and launch JupyterLab.
```bash
$ cd <path>/quantum
$ pip install jupyterlab
# Once installed, launch JupyterLab with:
$ jupyter lab
```

Optional libraries for code formatting.
```bash
$ cd <path>/quantum
$ pip install black[jupyter] isort
# Execute to format code.
$ make format
```

## Code

1. [Swap test](swap_test.py)

    ![swap test](https://github.com/Adaickalavan/quantum/blob/main/docs/_static/swap_test.png)

    Compare the states of two single-qubit registers. If the two input states are equal, the output register results in $|1⟩$ state. An useful interpretation is to see that the probability of a $|1⟩$ outcome is a measure of just how identical the two inputs are.

1. [Teleport](teleport.py)

    ![teleport](https://github.com/Adaickalavan/quantum/blob/main/docs/_static/teleport.png)

    Alice teleports the quantum state of her payload qubit using an entangled pair of qubits shared with Bob. Only two classical bits are needed to transmit Alice’s qubit state (i.e., magnitudes and relative phase) and Bob's retrieved qubit state will be correct to a potentially infinite number of classical bits of precision. Because a traditional channel is needed to convey the two classical bits from Alice to Bob, the speed of teleportation can be no faster than the speed of light. <br>

    To verify successful teleportation, Bob applies the gates, which Alice applied on $|0⟩$ to prepare her payload, to his retrieved qubit in reverse. If Bob's retrieved qubit matches that sent by Alice, the final measurement result after verification gates should always be `0` in a perfect quantum circuit.

1. [Arithmetic](arithmetic.py)

    ![arithmetic](https://github.com/Adaickalavan/quantum/blob/main/docs/_static/arithmetic.png)

    Create two quantum registers and initialize them to $a=\sqrt{0.5}|1⟩+\sqrt{0.5}|5⟩$ and $b=\sqrt{0.5}|1⟩+e^{i\pi/4}\sqrt{0.5}|3⟩$. Decrement register $a$ by 3. Then, increment register $b$ conditional on register $a<0$. Here, register $a$ is assumed to be in two’s-complement, where the highest-order bit indicates the sign. Finally, increment register $a$ by 3.

1. [Scratch qubit](scratch_qubit.py)

    ![scratch qubit](https://github.com/Adaickalavan/quantum/blob/main/docs/_static/scratch_qubit.png)

    Scratch qubits play a temporary role in enabling quantum operations. A specific example of an otherwise irreversible operation that can be made reversible with a scratch qubit is `abs(a)`. The `abs()` function computes the absolute value of a signed integer. We assume two’s-complement notation here. <br>

    In this example, `abs` of a quantum register `a` is computed. Then, add `abs(a)` to another quantum register `b`. Finally, uncompute (i.e., reverse the operations on) the scratch qubit and quantum register `a` to return them to their initial states.

1. [Amplitude amplification](amplitude_amplification.py) <a id="amplitude-amplification"></a>

    ![amplitude amplification](https://github.com/Adaickalavan/quantum/blob/main/docs/_static/amplitude_amplification.png)

    Amplitude amplification converts inaccessible phase differences inside a quantum processor into measurable magnitude differences. Amplitue amplification consists of iterative `flip` followed by `mirror` subroutines. Subroutine `flip` marks the desired state by a phase-flip. Subroutine `mirror` reflects each state about the average overall state. This results in the marked state having a larger read probability than nonmarked states. In Grover search algorithm, the `flip` and `mirror` are known as the `oracle` and `diffuser`, respectively.

1. [Quantum Fourier Transform](quantum_fourier_transform.py)

    ![QFT](https://github.com/Adaickalavan/quantum/blob/main/docs/_static/quantum_fourier_transform.png)

    Use Quantum Fourier Transform to deduce the frequencies present in a quantum register.

1. [Phase estimation](phase_estimation.py)

    ![phase estimation](https://github.com/Adaickalavan/quantum/blob/main/docs/_static/phase_estimation.png)

    We build a phase estimation circuit to compute the eigenphase $\theta$, given a unitary quantum operation $U$ and its eigenstate. Acting an $U$ on its eigenstate produces the same eigenstate but with the eigenphase applied to its global phase. That is to say $U|\psi⟩=e^{i2\pi\theta}|\psi⟩$. These eigenphase rotations are kicked-back into the $m$ qubits in the counting register, creating a frequency modulation. Inverse QFT is applied to the counting register to decode the frequency present and to obtain its count value $v$. Then, $\theta = v2\pi / 2^m$.<br>

    A superposition of eigenstates as an input to the phase estimation results in a superposition of the associated eigenphases in the output. The magnitude for each eigenphase in the output superposition will be precisely the magnitude that its corresponding eigenstate had in the input register.

1. [Phase logic](phase_logic.py)

    ![phase logic](https://github.com/Adaickalavan/quantum/blob/main/docs/_static/phase_logic.png)

    Phase-logic circuits flip the relative phases of all input states for which the circuit operation evaluate to true. Note that phase-logic circuits take in magnitude values such as $|1⟩$ or $|2⟩$, but not phase values, as inputs and encode output values in the relative phases.<br>

    Here, we solve a satisfiable 3-SAT problem by finding the combination of boolean inputs `a`, `b`, `c` which  produce a 1 output from the boolean statement `(a OR b) AND ((NOT a) OR c) AND ((NOT b) OR (NOT c)) AND (a OR c)`.<br>

    General recipe to solve satisfiability problems using phase logic is as follows.
    + Initialize the quantum register in a uniform superposition.
    + Transform the boolean statement into a number of clauses that have to be satisfied simultaneously, such that the final statement is the `AND` of a number of independent clauses.
    + Represent each individual clause using magnitude logic, storing the output in scratch qubits.
    + Perform a phase-logic `AND` between all the scratch qubits to combine the different clauses.
    + Uncompute all of the magnitude-logic operations, returning the scratch qubits to their initial states.
    + Finally, perform `mirror` subroutine, from the [amplitude amplification](#amplitude-amplification) algorithm.

    Perform the above phase `flip` (i.e., magnitude-logic and phase-logic operations) and `mirror` subroutines, as many times as necessary before reading out the quantum register.

1. [Transpile](transpile.py)

    ![transpile](https://github.com/Adaickalavan/quantum/blob/main/docs/_static/transpile.png)

    Quantum circuit must be transpiled for it to run on real devices. Qiskit's transpiler converts circuit operations to those supported by the device, maps qubits according to the device's coupling map, and performs some optimization of circuit’s gate count.

    Here, we transpile a quantum circuit containing `[cx, y]` gates onto a `GenericBackendV2` device which only supports `[id, rz, sx, x, cx]` gates. Circuit before (left) and after (right) transpiling is shown above. We may select `optimization_level`$\in [0,1,2,3]$ as input argument to the transpiler. Level 0 does the aboslute minimum necessary, level 1 is the default setting, level 2 tries to avoid qubit swaps, and level 3 is the highest which  uses smarter algorithms to cancel out gates.
