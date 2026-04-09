# Interactive Limit Evaluator: EdTech Practice Module

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://solving-limits.streamlit.app/)

An interactive educational web application built with Python, Streamlit, and SymPy. This module is designed to help students master the algebraic evaluation of limits involving indeterminate forms, rational expressions, and square roots.

## 🚀 Overview & Features

This project moves beyond a static calculator to function as a fully realized EdTech learning tool. It guarantees unique practice opportunities by procedurally generating math problems that adhere to specific evaluation constraints.

* **Algorithmic Problem Generation:** Dynamically generates unique calculus problems where the denominator coefficients ($b$ and $c$) are constrained so that $c = b+1$ and $b = a^2+1$. This ensures the limit always evaluates to an indeterminate form ($0/0$) at $x = -1$ and simplifies cleanly to exactly $\\frac{1}{a}$ for an integer $a$.
* **Robust Mathematical Parsing:** Utilizes the `SymPy` library to validate student inputs natively. The application gracefully handles fractions (e.g., `1/2`), decimals (e.g., `0.5`), and algebraically equivalent expressions. 
* **Scaffolded Learning Flow:** Breaks complex limits down into a Guided Practice mode featuring three cognitive steps, followed by the chance for the student to show mastery or endlessly practice.
  1. **Substitution:** Identifying the $0/0$ indeterminate form.
  2. **Factorization:** Performing algebraic manipulation to remove the discontinuity.
  3. **Evaluation:** Solving the simplified limit.
* **Progressive Hint System & Intelligent Error Catching:** Features a looping "Stuck?" mechanic and specific error handlers. For instance, if a student evaluates the fraction but forgets to compute the final square root, the application provides targeted feedback rather than a generic "Incorrect" alert. After 2 incorrect attempts, the student receives the correct answer and explanation, and the chance to try again with a new problem.
* **Integrated Digital Scratchpad:** Embeds a responsive canvas element directly into the UI so students can map out their factorization steps without needing external tools.

## 💻 Tech Stack

* **Frontend & State Management:** [Streamlit](https://streamlit.io/)
* **Algebraic Validation Engine:** [SymPy](https://www.sympy.org/)
* **Interactive Canvas:** `streamlit-drawable-canvas`

## ⚙️ Installation & Setup

1. **Clone the repository** to your local machine.
2. **Install the required dependencies** using pip:
   ```bash
   pip install streamlit sympy streamlit-drawable-canvas
