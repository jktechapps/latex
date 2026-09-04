import streamlit as st
import sympy as sp
from PIL import Image
from io import BytesIO

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="Math ↔ LaTeX Converter",
    page_icon="∑",
    layout="centered"
)

# ---------------------------------------------------------
# CSS
# ---------------------------------------------------------

st.markdown(
    """
    <style>
        .block-container {
            max-width: 900px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        .title {
            text-align: center;
            font-size: 2.4rem;
            font-weight: 700;
        }

        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 2rem;
        }

        .result-box {
            padding: 1.5rem;
            border: 1px solid #ddd;
            border-radius: 10px;
            margin-top: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    '<div class="title">Math ↔ LaTeX</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Convert mathematical equations between LaTeX, text and images.'
    '</div>',
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# TABS
# ---------------------------------------------------------

tab1, tab2, tab3 = st.tabs(
    [
        "LaTeX → Math",
        "Math → LaTeX",
        "Image → LaTeX"
    ]
)

# =========================================================
# TAB 1
# LATEX → MATH
# =========================================================

with tab1:

    st.subheader("Enter LaTeX")

    latex_input = st.text_area(
        "LaTeX",
        value=r"\frac{x^2 + 1}{2}",
        height=120,
        placeholder=r"Example: \frac{x^2+1}{2}"
    )

    if st.button(
        "Render Equation",
        key="render_latex",
        use_container_width=True
    ):

        if latex_input.strip():

            st.markdown("### Equation")

            try:
                st.latex(latex_input)

                st.markdown("### LaTeX")

                st.code(latex_input, language="text")

            except Exception as e:
                st.error(f"Could not render the equation: {e}")

# =========================================================
# TAB 2
# MATH → LATEX
# =========================================================

with tab2:

    st.subheader("Enter a mathematical expression")

    st.info(
        "For V1, enter the expression as normal mathematical text. "
        "For example: (x^2 + 1) / 2"
    )

    math_input = st.text_input(
        "Expression",
        placeholder="Example: (x^2 + 1) / 2"
    )

    if st.button(
        "Convert to LaTeX",
        key="math_to_latex",
        use_container_width=True
    ):

        if math_input.strip():

            try:

                expression = sp.sympify(math_input)

                latex_output = sp.latex(expression)

                st.markdown("### Equation")

                st.latex(latex_output)

                st.markdown("### LaTeX")

                st.code(latex_output, language="text")

                st.success("Converted successfully.")

            except Exception:
                st.error(
                    "I couldn't understand that expression. "
                    "Try something like: (x^2 + 1) / 2"
                )

# =========================================================
# TAB 3
# IMAGE → LATEX
# =========================================================

with tab3:

    st.subheader("Upload an equation image")

    st.write(
        "Upload a screenshot, photo or image containing a mathematical equation."
    )

    uploaded_file = st.file_uploader(
        "Choose an image",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file:

        image = Image.open(uploaded_file)

        st.image(
            image,
            caption="Uploaded image",
            use_container_width=True
        )

        if st.button(
            "Convert Image",
            key="image_to_latex",
            use_container_width=True
        ):

            with st.spinner("Recognizing equation..."):

                try:

                    from pix2text import Pix2Text

                    p2t = Pix2Text()

                    result = p2t.recognize_formula(
                        image
                    )

                    latex_output = str(result)

                    st.markdown("### LaTeX")

                    st.code(
                        latex_output,
                        language="text"
                    )

                    st.markdown("### Equation")

                    st.latex(latex_output)

                    st.success(
                        "Equation converted successfully."
                    )

                except ImportError:

                    st.error(
                        "Image recognition is not installed yet."
                    )

                    st.info(
                        "Add pix2text to requirements.txt "
                        "and redeploy the application."
                    )

                except Exception as e:

                    st.error(
                        f"Could not recognize the equation: {e}"
                    )

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown("---")

st.caption(
    "Free Math ↔ LaTeX Converter"
)
