# Quantum Computing

We present several quantum computing algorithms. Each file is a standalone example. 

First perform generic setup as follows.  

```bash
cd <path>/quantum
python3.8 -m venv ./.venv
source ./.venv/bin/activate
pip install qiskit
pip install qiskit-ibm-runtime
```

Users are recommended to run each of this repository's code files inside the interactive window in VSCode.

Alternatively, you may run the code inside JupyterLab. Follow the additional steps below to install and launch JupyterLab. 
```bash
pip install jupyterlab
# Once installed, launch JupyterLab with:
jupyter lab
```

## Code

1. [Swap test](swap_test.py)
   
    ![](docs/_static/swap_test.png)

    Compare the states of two single-qubit registers. If the two input states are equal, the output register results in `∣1⟩` state. An useful interpretation is to see that the probability of a `|1⟩` outcome is a measure of just how identical the two inputs are.

1.  