import streamlit as st
import sympy as sp
from PIL import Image
from pix2text import Pix2Text


# -----------------------------
# Page setup
# -----------------------------

st.set_page_config(
    page_title="Maths → LaTeX",
    page_icon="∑",
    layout="centered"
)

st.title("Maths → LaTeX")
st.write("Convert mathematical expressions and images into editable LaTeX.")


# -----------------------------
# Helper functions
# -----------------------------

def clean_latex(latex):
    """Remove common LaTeX display wrappers."""
    if not latex:
        return ""

    latex = str(latex).strip()

    if latex.startswith("$$") and latex.endswith("$$"):
        latex = latex[2:-2].strip()

    elif latex.startswith("\\[") and latex.endswith("\\]"):
        latex = latex[2:-2].strip()

    elif latex.startswith("\\(") and latex.endswith("\\)"):
        latex = latex[2:-2].strip()

    elif latex.startswith("$") and latex.endswith("$"):
        latex = latex[1:-1].strip()

    return latex


def show_latex_result(latex):
    """Display the generated equation and copyable LaTeX."""
    latex = clean_latex(latex)

    if not latex:
        st.error("No equation was generated.")
        return

    st.subheader("Generated Equation")

    # Render the equation
    st.latex(latex)

    st.subheader("Copy Equation")

    # Streamlit provides a built-in copy button
    st.code(latex, language="latex")

    st.caption("Click the 📋 button to copy the equation.")

    st.subheader("Use in Microsoft Word")

    st.code(latex, language="latex")

    st.caption(
        "In Word, press Alt + =, paste the equation, "
        "then choose Convert → Professional."
    )

    st.download_button(
        label="Download LaTeX",
        data=latex,
        file_name="equation.tex",
        mime="text/plain"
    )


# -----------------------------
# Tabs
# -----------------------------

tab1, tab2, tab3 = st.tabs(
    [
        "LaTeX → Math",
        "Math → LaTeX",
        "Image → LaTeX"
    ]
)


# -----------------------------
# Tab 1: LaTeX → Math
# -----------------------------

with tab1:

    st.subheader("Enter LaTeX")

    latex_input = st.text_area(
        "LaTeX",
        placeholder=r"\frac{x^2 + 1}{2}",
        height=120,
        label_visibility="collapsed"
    )

    if st.button("Render Equation", key="render_button"):

        if latex_input.strip():
            latex = clean_latex(latex_input)

            st.subheader("Generated Equation")

            st.latex(latex)

            st.subheader("Copy Equation")

            st.code(latex, language="latex")

            st.caption("Click the 📋 button to copy the equation.")

            st.download_button(
                "Download LaTeX",
                latex,
                file_name="equation.tex",
                mime="text/plain",
                key="download_latex_tab1"
            )

        else:
            st.warning("Please enter a LaTeX equation.")


# -----------------------------
# Tab 2: Math → LaTeX
# -----------------------------

with tab2:

    st.subheader("Enter a Mathematical Expression")

    math_input = st.text_area(
        "Math expression",
        placeholder="(x^2 + 1)/2",
        height=120,
        label_visibility="collapsed"
    )

    st.caption(
        "Examples: (x^2 + 1)/2, sqrt(x), sin(x), x^2 + y^2"
    )

    if st.button("Convert to LaTeX", key="math_button"):

        if math_input.strip():

            try:
                expression = sp.sympify(math_input)
                latex = sp.latex(expression)

                show_latex_result(latex)

            except Exception:
                st.error(
                    "I couldn't understand that mathematical expression."
                )

        else:
            st.warning("Please enter a mathematical expression.")


# -----------------------------
# Tab 3: Image → LaTeX
# -----------------------------

with tab3:

    st.subheader("Upload a Mathematical Image")

    uploaded_file = st.file_uploader(
        "Upload image",
        type=["png", "jpg", "jpeg", "webp"],
        label_visibility="collapsed"
    )

    if uploaded_file:

        image = Image.open(uploaded_file)

        st.image(
            image,
            caption="Uploaded image",
            use_container_width=True
        )

        if st.button("Convert Image to LaTeX", key="image_button"):

            with st.spinner("Reading equation..."):

                try:

                    p2t = Pix2Text()

                    result = p2t.recognize_formula(image)

                    latex = clean_latex(result)

                    show_latex_result(latex)

                except Exception as e:

                    st.error(
                        "Couldn't read the equation from the image."
                    )

                    st.exception(e)
