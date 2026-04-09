import streamlit as st
import random
import sympy as sp
from sympy.core.sympify import SympifyError
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
from streamlit_drawable_canvas import st_canvas

st.set_page_config(page_title="Solving Limits", initial_sidebar_state="expanded")

transformations = (standard_transformations + (implicit_multiplication_application,))

css = f"""
    <style>
    div.stButton > button[kind="primary"] {{
        background-color: #028384; color: white; border-radius: 8px; border: none; font-weight: 600; transition: all 0.3s ease;
    }}
    div.stButton > button[kind="primary"]:hover {{
        background-color: #026666; color: white; box-shadow: 0 4px 10px rgba(2, 131, 132, 0.3); transform: translateY(-1px);
    }}
    div.stButton > button[kind="secondary"] {{
        background-color: #4A81A8; color: white; border-radius: 8px; border: none; font-weight: 600; transition: all 0.3s ease;
    }}
    div.stButton > button[kind="secondary"]:hover {{
        background-color: #224C5E; color: white; box-shadow: 0 4px 10px rgba(74, 129, 168, 0.3); transform: translateY(-1px);
    }}
    div.element-container:has(#generate-btn-anchor) + div.element-container button {{
        background-color: #4F4F4F !important; color: white !important; border-color: #4F4F4F !important;
    }}
    div.element-container:has(#generate-btn-anchor) + div.element-container button:hover {{
        background-color: #333333 !important; box-shadow: 0 4px 10px rgba(79, 79, 79, 0.3) !important;
    }}
    div.element-container:has(.stuck-anchor) {{
        height: 0px; margin-bottom: -1rem;
    }}
    div.element-container:has(.stuck-anchor) + div.element-container button {{
        background-color: #C14729 !important; color: white !important; border-color: #C14729 !important;
    }}
    div.element-container:has(.stuck-anchor) + div.element-container button:hover {{
        background-color: #922f17 !important; box-shadow: 0 4px 10px rgba(193, 71, 41, 0.3) !important;
    }}
    
    /* Anchor Trick to format Streamlit's Native Markdown (Fixes LaTeX rendering) */
    div.element-container:has(.custom-hint-anchor),
    div.element-container:has(.custom-success-anchor),
    div.element-container:has(.custom-error-anchor) {{
        height: 0px; margin-bottom: -1rem;
    }}
    
    /* Custom Hint Boxes */
    div.element-container:has(.custom-hint-anchor) + div.element-container {{
        background-color: #eaeff3 !important; 
        padding: 15px !important; 
        border-radius: 8px !important; 
        border-left: 5px solid #4A81A8 !important; 
        margin-bottom: 15px !important;
    }}
    div.element-container:has(.custom-hint-anchor) + div.element-container p {{
        color: #4f4f4f !important; margin-bottom: 0 !important;
    }}
    
    /* Custom Success Boxes */
    div.element-container:has(.custom-success-anchor) + div.element-container {{
        background-color: #e5f2f2 !important; 
        padding: 15px !important; 
        border-radius: 8px !important; 
        border-left: 5px solid #028384 !important; 
        margin-bottom: 15px !important;
    }}
    div.element-container:has(.custom-success-anchor) + div.element-container p {{
        color: #014d4d !important; margin-bottom: 0 !important;
    }}

    /* Custom Error Boxes */
    div.element-container:has(.custom-error-anchor) + div.element-container {{
        background-color: #fcece8 !important; 
        padding: 15px !important; 
        border-radius: 8px !important; 
        border-left: 5px solid #c14729 !important; 
        margin-bottom: 15px !important;
    }}
    div.element-container:has(.custom-error-anchor) + div.element-container p {{
        color: #7a2b18 !important; margin-bottom: 0 !important;
    }}

    /* Explanation Expander Styling */
    div.element-container:has(.explanation-anchor) {{
        height: 0px; margin-bottom: -1rem;
    }}
    div.element-container:has(.explanation-anchor) + div.element-container details {{
        background-color: #e5f2f2 !important; 
        border: 1px solid #cce8e8 !important; 
        border-left: 5px solid #028384 !important; 
        border-radius: 8px !important;
        margin-bottom: 15px !important;
    }}
    div.element-container:has(.explanation-anchor) + div.element-container summary {{
        background-color: #e5f2f2 !important;
        border-radius: 8px !important;
    }}
    div.element-container:has(.explanation-anchor) + div.element-container summary p {{
        color: #014d4d !important; 
        font-weight: 700 !important;
    }}
    div.element-container:has(.explanation-anchor) + div.element-container summary svg {{
        fill: #014d4d !important; 
        color: #014d4d !important;
    }}
    div.element-container:has(.explanation-anchor) + div.element-container [data-testid="stExpanderDetails"] p,
    div.element-container:has(.explanation-anchor) + div.element-container [data-testid="stExpanderDetails"] span {{
        color: #014d4d !important;
    }}
    </style>
"""
st.markdown(css, unsafe_allow_html=True)

def clear_error(step):
    """Clears the error message when a user modifies their input to try again."""
    st.session_state[f'error_{step}'] = None

def generate_math_vars():
    """Generates the mathematically constrained coefficients."""
    a = random.randint(2, 15)
    b = (a ** 2) + 1
    c = b + 1
    return a, b, c

def clear_inputs():
    """Clears text inputs to prevent state retention on new problems."""
    keys_to_clear = ['l2_input', 'l3_input', 'l4_input']
    for key in keys_to_clear:
        if key in st.session_state:
            st.session_state[key] = ""

def initialize_state(target_level=1):
    a, b, c = generate_math_vars()
    clear_inputs()
    st.session_state.update({
        'a': a, 'b': b, 'c': c,
        'level': target_level,
        'level_1_solved': False,
        'level_2_solved': False,
        'level_3_solved': False,
        'level_4_solved': False,
        'hint_level': 0,
        'error_1': None, 'error_2': None, 'error_3': None, 'error_4': None
    })

def refresh_mastery_problem(target_level=4):
    """Generates a new problem, ensuring it is different from the current one."""
    current_a = st.session_state.get('a')
    a, b, c = generate_math_vars()
    
    # Loop until we get a set of variables that differ from the current problem
    while a == current_a:
        a, b, c = generate_math_vars()
        
    clear_inputs()
    st.session_state.update({
        'a': a, 'b': b, 'c': c,
        'level': target_level,
        'level_4_solved': False,
        'error_4': None
    })

def advance_level(target_level):
    st.session_state.level = target_level
    st.session_state.hint_level = 0

def increment_hint():
    # If both hints are showing, loop back to 0. Otherwise, increment.
    if st.session_state.hint_level >= 2:
        st.session_state.hint_level = 0
    else:
        st.session_state.hint_level += 1

if 'level' not in st.session_state:
    initialize_state()

levels_solved = [
    st.session_state.level_1_solved,
    st.session_state.level_2_solved,
    st.session_state.level_3_solved,
    st.session_state.level_4_solved,
]

st.progress(sum(levels_solved) / 4.0, text=f"Solving Limits: {sum(levels_solved)}/4 Completed")
st.markdown("<h1 style='color: #028384'>Interactive Practice</h1>", unsafe_allow_html=True)
st.divider()
st.subheader("Solve the Limit:")

with st.sidebar:
    st.title("Module: Solving Limits")
    st.header("⭐ Objective")
    st.write("Students will be able to evaluate limits involving square roots and rational expressions.")
    st.divider()
    st.header("🧠 Guided Practice")
    st.button("✅ Step 1: Substitution" if st.session_state.level_1_solved else "Step 1: Substitution", on_click=advance_level, args=(1,), use_container_width=True, type="secondary")
    st.button("✅ Step 2: Factorization" if st.session_state.level_2_solved else "Step 2: Factorization", on_click=advance_level, args=(2,), use_container_width=True, type="secondary")
    st.button("✅ Step 3: Evaluation" if st.session_state.level_3_solved else "Step 3: Evaluation", on_click=advance_level, args=(3,), use_container_width=True, type="secondary")
    st.divider()
    st.header("🏆 Show Mastery")
    st.button("✅ Final Challenge: Solo Mode" if st.session_state.level_4_solved else "Final Challenge: Solo Mode", on_click=refresh_mastery_problem, args=(4,), use_container_width=True, type="primary")
    st.divider()
    st.markdown('<div id="generate-btn-anchor"></div>', unsafe_allow_html=True)
    st.button("🔄 Reset Activity", on_click=initialize_state, args=(1,), use_container_width=True)

# ------------------------------------------
# STEP 1: Substitution
# ------------------------------------------
if st.session_state.level == 1:
    st.latex(r"\lim_{x \to -1} \sqrt{\frac{x + 1}{x^2 + %dx + %d}}" % (st.session_state.c, st.session_state.b))
    
    st.markdown("**Step 1:** Use substitution to evaluate the radicand at $x = -1$. What is the result?")
    step1_ans = st.radio("s1", ["Choose...", "A real number", "0/0 (Indeterminate Form)", "Undefined"], label_visibility="collapsed", on_change=clear_error, args=(1,))
    
    col_submit, col_hint = st.columns(2)
    with col_submit:
        submit_btn_1 = st.button("Check Answer", use_container_width=True, type="primary")
    with col_hint:
        st.markdown('<div class="stuck-anchor"></div>', unsafe_allow_html=True)
        hint_label = "💡 Stuck?" if st.session_state.hint_level == 0 else ("💡 Need another hint?" if st.session_state.hint_level == 1 else "Hide hints")
        st.button(hint_label, on_click=increment_hint, key="hint_btn_1", use_container_width=True)

    if st.session_state.hint_level >= 1:
        st.markdown('<div class="custom-hint-anchor"></div>', unsafe_allow_html=True)
        st.markdown("💡 **Hint 1:** Apply **direct substitution** by evaluating the numerator and denominator at $x = -1$.")
    if st.session_state.hint_level >= 2:
        st.markdown('<div class="custom-hint-anchor"></div>', unsafe_allow_html=True)
        st.markdown("🚨 **Hint 2:** Both evaluate to zero, yielding the **indeterminate form** $0/0$. This indicates a removable discontinuity (a hole) and requires algebraic manipulation.")
    
    if submit_btn_1:
        if step1_ans == "0/0 (Indeterminate Form)":
            st.session_state.level_1_solved = True
            st.session_state.error_1 = None
        elif step1_ans != "Choose...":
            st.session_state.error_1 = "✗ Not quite. Apply direct substitution to the numerator and denominator separately."
            
    if st.session_state.error_1 and not st.session_state.level_1_solved:
        st.markdown('<div class="custom-error-anchor"></div>', unsafe_allow_html=True)
        st.markdown(st.session_state.error_1)

    if st.session_state.level_1_solved:
        st.markdown('<div class="custom-success-anchor"></div>', unsafe_allow_html=True)
        st.markdown("✓ Correct! The indeterminate form indicates a removable discontinuity — factoring is required to evaluate the limit.")
        
        st.markdown('<div class="explanation-anchor"></div>', unsafe_allow_html=True)
        with st.expander("📝 Explanation", expanded=True):
            st.markdown(f"**Numerator:** $\\sqrt{{-1 + 1}} = \\sqrt{{0}} = 0$  \n**Denominator:** $(-1)^2 + {st.session_state.c}(-1) + {st.session_state.b} = 1 - {st.session_state.c} + {st.session_state.b} = 0$  \nBoth expressions evaluate to zero, yielding the indeterminate form $\\frac{{0}}{{0}}$. This indicates a **removable discontinuity** (a 'hole') in the graph. Because division by zero is undefined, algebraic manipulation is required to evaluate the limit.")
        st.button("Proceed to Step 2 ➔", on_click=advance_level, args=(2,), use_container_width=True)

# ------------------------------------------
# STEP 2: Factorization
# ------------------------------------------
elif st.session_state.level == 2:
    st.latex(r"\lim_{x \to -1} \sqrt{\frac{x + 1}{x^2 + %dx + %d}}" % (st.session_state.c, st.session_state.b))
    
    st.markdown(f"**Step 2:** Factor the quadratic denominator $x^2 + {st.session_state.c}x + {st.session_state.b}$:")
    factor_input = st.text_input("s2", key="l2_input", label_visibility="collapsed", on_change=clear_error, args=(2,))
    
    col_submit, col_hint = st.columns(2)
    with col_submit:
        submit_btn_2 = st.button("Check Answer", use_container_width=True, type="primary")
    with col_hint:
        st.markdown('<div class="stuck-anchor"></div>', unsafe_allow_html=True)
        hint_label = "💡 Stuck?" if st.session_state.hint_level == 0 else ("💡 Need another hint?" if st.session_state.hint_level == 1 else "Hide hints")
        st.button(hint_label, on_click=increment_hint, key="hint_btn_2", use_container_width=True)

    if st.session_state.hint_level >= 1:
        st.markdown('<div class="custom-hint-anchor"></div>', unsafe_allow_html=True)
        st.markdown(f"💡 **Hint 1:** To remove the discontinuity, factor the quadratic in the denominator. Find two integers that multiply to ${st.session_state.b}$ and add to ${st.session_state.c}$.")
    if st.session_state.hint_level >= 2:
        st.markdown('<div class="custom-hint-anchor"></div>', unsafe_allow_html=True)
        st.markdown(f"🚨 **Hint 2 (Solution):** The integers are $1$ and ${st.session_state.b}$. The fully factored denominator is:\n\n$(x + 1)(x + {st.session_state.b})$")
    
    if submit_btn_2:
        if factor_input:
            x = sp.Symbol('x')
            expected_expr = (x + 1) * (x + st.session_state.b)
            try:
                user_expr = parse_expr(factor_input, local_dict={'x': x}, transformations=transformations)
                if sp.simplify(user_expr - expected_expr) == 0:
                    st.session_state.level_2_solved = True
                    st.session_state.error_2 = None
                else:
                    st.session_state.error_2 = f"✗ Incorrect. Find two integers that multiply to {st.session_state.b} and add to {st.session_state.c}."
            except SympifyError:
                st.session_state.error_2 = "⚠️ Please enter a valid algebraic expression (e.g., (x+1)(x+2))."
            except Exception:
                 st.session_state.error_2 = "⚠️ An unexpected error occurred while parsing your expression."
        else:
            st.session_state.error_2 = "⚠️ Please enter an answer before checking."
    
    if st.session_state.error_2 and not st.session_state.level_2_solved:
        st.markdown('<div class="custom-error-anchor"></div>', unsafe_allow_html=True)
        st.markdown(st.session_state.error_2)

    if st.session_state.level_2_solved:
        st.markdown('<div class="custom-success-anchor"></div>', unsafe_allow_html=True)
        st.markdown(f"✓ Perfect! The denominator factors to $(x + 1)(x + {st.session_state.b})$.")
        
        st.markdown('<div class="explanation-anchor"></div>', unsafe_allow_html=True)
        with st.expander("📝 Explanation", expanded=True):
            st.markdown(
                f"With the denominator factored, the limit becomes:\n\n$\\sqrt{{\\frac{{x + 1}}{{(x + 1)(x + {st.session_state.b})}}}}$" +
                "\n\nThe $(x+1)$ factors in the numerator and denominator cancel, resolving the removable discontinuity."
                "\n\nThis cancellation yields the simplified expression:"
            )
            st.latex(r"\lim_{x \to -1} \sqrt{\frac{1}{x + %d}}" % st.session_state.b)
        st.button("Proceed to Step 3 ➔", on_click=advance_level, args=(3,), use_container_width=True)

# ------------------------------------------
# STEP 3: Evaluation
# ------------------------------------------
elif st.session_state.level == 3:
    st.latex(r"\lim_{x \to -1} \sqrt{\frac{1}{x + %d}}" % st.session_state.b)
    
    st.markdown("**Step 3:** Enter the final limit value:")
    final_input = st.text_input("s3", key="l3_input", label_visibility="collapsed", on_change=clear_error, args=(3,))
    
    col_submit, col_hint = st.columns(2)
    with col_submit:
        submit_btn_3 = st.button("Check Answer", use_container_width=True, type="primary")
    with col_hint:
        st.markdown('<div class="stuck-anchor"></div>', unsafe_allow_html=True)
        hint_label = "💡 Stuck?" if st.session_state.hint_level == 0 else ("💡 Need another hint?" if st.session_state.hint_level == 1 else "Hide hints")
        st.button(hint_label, on_click=increment_hint, key="hint_btn_3", use_container_width=True)

    if st.session_state.hint_level >= 1:
        st.markdown('<div class="custom-hint-anchor"></div>', unsafe_allow_html=True)
        st.markdown("💡 **Hint 1:** Apply **direct substitution** again by evaluating the simplified expression at $x = -1$.")
    if st.session_state.hint_level >= 2:
        st.markdown('<div class="custom-hint-anchor"></div>', unsafe_allow_html=True)
        st.markdown(f"🚨 **Hint 2:** The fraction evaluates to $1/{st.session_state.b - 1}$. Do not forget to compute the square root of that result!")
    
    if submit_btn_3:
        if final_input:
            expected_val = 1 / st.session_state.a
            try:
                user_val = float(sp.sympify(final_input).evalf())
                if abs(user_val - expected_val) < 1e-4:
                    st.session_state.level_3_solved = True
                    st.session_state.error_3 = None
                elif abs(user_val - st.session_state.a) < 1e-4:
                    st.session_state.error_3 = "✗ Almost! You evaluated the denominator correctly, but your fraction is missing the numerator."
                elif abs(user_val - (1 / (st.session_state.b - 1))) < 1e-4:
                    st.session_state.error_3 = "✗ Almost! You evaluated the fraction inside the square root. Now, calculate the root itself."
                else:
                    st.session_state.error_3 = "✗ Incorrect. Apply direct substitution at $x = -1$ into the simplified expression and evaluate."
            except (SympifyError, ValueError, TypeError):
                st.session_state.error_3 = "⚠️ Please enter a valid number or fraction (e.g., 1/2 or 0.5)."
        else:
            st.session_state.error_3 = "⚠️ Please enter an answer before checking."

    if st.session_state.error_3 and not st.session_state.level_3_solved:
        st.markdown('<div class="custom-error-anchor"></div>', unsafe_allow_html=True)
        st.markdown(st.session_state.error_3)

    if st.session_state.level_3_solved:
        st.markdown('<div class="custom-success-anchor"></div>', unsafe_allow_html=True)
        st.markdown(f"🎉 Correct! The answer is $1/{st.session_state.a}$.")
        
        st.markdown('<div class="explanation-anchor"></div>', unsafe_allow_html=True)
        with st.expander("📝 Explanation", expanded=True):
            st.markdown(f"Evaluate the limit using direct substitution at $x = -1$:\n\n$\\sqrt{{\\frac{{1}}{{-1 + {st.session_state.b}}}}} = \\sqrt{{\\frac{{1}}{{{st.session_state.b - 1}}}}} = \\frac{{1}}{{{st.session_state.a}}}$")
        st.button("🚀 Proceed to Final Challenge", on_click=refresh_mastery_problem, args=(4,), use_container_width=True, type="primary")

# ------------------------------------------
# STEP 4: Challenge Mode
# ------------------------------------------
elif st.session_state.level == 4:
    st.latex(r"\lim_{x \to -1} \sqrt{\frac{x + 1}{x^2 + %dx + %d}}" % (st.session_state.c, st.session_state.b))

    st.markdown("**Your answer:**")
    answer_field = st.text_input("s4", key="l4_input", label_visibility="collapsed", on_change=clear_error, args=(4,))
    
    col1, col2, col3 = st.columns(3)
    with col1:
        submit_btn_4 = st.button("Check Answer", use_container_width=True, type="primary")
    with col2:
        st.markdown('<div class="stuck-anchor"></div>', unsafe_allow_html=True)
        st.button("New Problem", on_click=refresh_mastery_problem, use_container_width=True)
    with col3:
        st.button("Back to Practice", on_click=advance_level, args=(1,), use_container_width=True)

    if submit_btn_4:
        if answer_field:
            expected_val = 1 / st.session_state.a
            try:
                user_val = float(sp.sympify(answer_field).evalf())
                if abs(user_val - expected_val) < 1e-4:
                    st.session_state.level_4_solved = True
                    st.session_state.error_4 = None
                    st.balloons()
                else:
                    st.session_state.error_4 = "✗ Incorrect. Try mapping out your factorization steps on the scratchpad!"
            except (SympifyError, ValueError, TypeError):
                 st.session_state.error_4 = "⚠️ Please enter a valid number or fraction."

    if st.session_state.error_4 and not st.session_state.level_4_solved:
        st.markdown('<div class="custom-error-anchor"></div>', unsafe_allow_html=True)
        st.markdown(st.session_state.error_4)

    if st.session_state.level_4_solved:
        st.markdown('<div class="custom-success-anchor"></div>', unsafe_allow_html=True)
        st.markdown("⭐ Mastered! You evaluated the limit completely independently.")
        
        st.markdown('<div class="explanation-anchor"></div>', unsafe_allow_html=True)
        with st.expander("📝 Explanation", expanded=True):
            st.markdown("### Let's Review!")
            
            st.markdown("**Step 1: Substitution**")
            st.markdown("Substituting $x = -1$ yields the indeterminate form $\\frac{0}{0}$. This indicates a removable discontinuity, requiring algebraic manipulation to evaluate the limit.")
            
            st.markdown("**Step 2: Factorization**")
            st.markdown(f"Factor the quadratic denominator $x^2 + {st.session_state.c}x + {st.session_state.b}$ by identifying two integers that multiply to ${st.session_state.b}$ and sum to ${st.session_state.c}$. Those integers are $1$ and ${st.session_state.b}$.")
            st.markdown(f"The expression becomes:\n\n$\\sqrt{{\\frac{{x + 1}}{{(x + 1)(x + {st.session_state.b})}}}}$")
            st.markdown(f"The $(x+1)$ factors in the numerator and denominator cancel, resolving the removable discontinuity and leaving the simplified expression:\n\n$\\sqrt{{\\frac{{1}}{{x + {st.session_state.b}}}}}$")
            
            st.markdown("**Step 3: Evaluation**")
            st.markdown(f"Applying direct substitution at $x = -1$ to the simplified expression gives the final limit:\n\n$\\sqrt{{\\frac{{1}}{{-1 + {st.session_state.b}}}}} = \\sqrt{{\\frac{{1}}{{{st.session_state.b - 1}}}}} = \\frac{{1}}{{{st.session_state.a}}}$")

st.subheader("✏️ Scratchpad")
st_canvas(stroke_width=2, stroke_color="#000000", background_color="#FFFFFF", drawing_mode="freedraw", width=670, update_streamlit=False)
