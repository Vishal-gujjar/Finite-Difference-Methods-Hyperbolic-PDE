# Finite Difference Methods for Hyperbolic PDEs

Implementation of finite difference schemes to solve a coupled system of one-dimensional hyperbolic partial differential equations. This project compares the performance of the **Lax–Friedrichs** and **Central Difference** schemes, highlighting their numerical stability and accuracy.

**Project completed under:**  
**Prof. Kirit Makwana**  
Department of Physics, IIT Hyderabad

---

## Problem Statement

Solve the following initial value problem:

\[
\frac{\partial \rho}{\partial t}+\frac{\partial u}{\partial x}=0
\]

\[
\frac{\partial u}{\partial t}+\frac{\partial \rho}{\partial x}=0
\]

Domain:

\[
x \in [-1,1]
\]

with zero-gradient boundary conditions and discontinuous initial conditions.

---

## Numerical Methods

Two finite difference schemes were implemented:

- Lax–Friedrichs Scheme
- Central Difference Scheme

The numerical solutions obtained from both methods were compared to study their behavior for hyperbolic PDEs.

---

## Features

- Python implementation of finite difference methods
- Zero-gradient (Neumann) boundary conditions
- Wave propagation simulation
- Numerical stability comparison
- Animated visualization of density and velocity evolution
- Comparison between stable and unstable numerical schemes

---

## Repository Structure

```text
Finite-Difference-Methods-Hyperbolic-PDE/
│
├── lax_friedrichs_solver.py
├── central_difference_solver.py
├── requirements.txt
├── LICENSE
└── README.md
```

---

## Technologies Used

- Python
- NumPy
- Matplotlib

---

## Results

### Lax–Friedrichs Scheme

- Stable numerical solution
- Handles discontinuities effectively
- Produces physically meaningful wave propagation

### Central Difference Scheme

- Demonstrates numerical instability for this hyperbolic system
- Solution diverges with time
- Illustrates why stable numerical schemes are essential

---

## How to Run

### Clone the repository

```bash
git clone https://github.com/<your-username>/Finite-Difference-Methods-Hyperbolic-PDE.git
cd Finite-Difference-Methods-Hyperbolic-PDE
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run Lax–Friedrichs simulation

```bash
python lax_friedrichs_solver.py
```

### Run Central Difference simulation

```bash
python central_difference_solver.py
```

---

## Learning Outcomes

- Numerical solution of hyperbolic PDEs
- Finite Difference Methods
- CFL stability condition
- Boundary condition implementation
- Numerical stability analysis
- Scientific computing using Python

---

## Future Improvements

- Lax–Wendroff Scheme
- Upwind Method
- Exact Riemann Solver comparison
- Higher-order finite volume methods
- Error and convergence analysis

---

## License

This project is released under the MIT License.
