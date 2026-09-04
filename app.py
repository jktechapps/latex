import streamlit as st
import sympy as sp
from PIL import Image
import re

st.set_page_config(
    page_title="Math ↔ LaTeX",
    page_icon="∑",
    layout="centered"
)

st.markdown("""
<style>
.block-container {
    max-width: 850px;
    padding-top: 2rem;
}

.title {
    text-align: center;
    font-size: 2.5rem;
    font-weight: 700;
}

.subtitle {
    text-align: center;
    color: #666;
    margin-bottom: 2rem;
}

.result-title {
    font-weight: 600;
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)


def clean_latex(text):
    text = str(text).strip()

    text = re.sub(r"^\s*\$\$(.*?)\$\$\s*$", r"\1", text, flags=re.S)
    text = re.sub(r"^\s*\$(.*?)\$\s*$", r"\1", text, flags=re.S)
    text = re.sub(r"^\s*\\\[(.*?)\\\]\s*$", r"\1", text, flags=re.S)
    text = re.sub(r"^\s*\\\((.*?)\\\)\s*$", r"\1", text, flags=re.S)

    return text.strip()


def show_latex_result(latex, key):
    latex = clean_latex(latex)

    if not latex:
        st.error("No LaTeX was produced.")
        return

    st.markdown(
        '<div class="result-title">Equation</div>',
        unsafe_allow_html=True
    )

    try:
        st.latex(latex)
    except Exception:
        st.warning("The result could not be rendered as an equation.")

    st.markdown(
        '<div class="result-title">LaTeX</div>',
        unsafe_allow_html=True
    )

    st.code(latex, language="latex")

    st.download_button(
        "Download LaTeX",
        data=latex,
        file_name="equation.tex",
        mime="text/plain",
        key=f"download_{key}",
        width="content"
    )

    st.caption("Select the LaTeX above and copy it with Ctrl+C.")


st.markdown(
    '<div class="title">Math ↔ LaTeX</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Convert equations between LaTeX, expressions and images.'
    '</div>',
    unsafe_allow_html=True
)


latex_tab, math_tab, image_tab = st.tabs([
    "LaTeX → Math",
    "Math → LaTeX",
    "Image → LaTeX"
])


with latex_tab:
    st.subheader("LaTeX → Math")

    latex_input = st.text_area(
        "Enter LaTeX",
        value=r"\frac{x^2 + 1}{2}",
        height=120,
        placeholder=r"\frac{x^2+1}{2}"
    )

    if st.button(
        "Render Equation",
        type="primary",
        width="stretch",
        key="render_latex"
    ):
        if not latex_input.strip():
            st.warning("Please enter some LaTeX.")
        else:
            show_latex_result(
                latex_input,
                "latex"
            )


with math_tab:
    st.subheader("Math expression → LaTeX")

    st.caption(
        "Type expressions such as: (x^2 + 1)/2, sqrt(x), sin(x), x^2 + y^2"
    )

    math_input = st.text_input(
        "Enter expression",
        placeholder="(x^2 + 1) / 2"
    )

    if st.button(
        "Convert to LaTeX",
        type="primary",
        width="stretch",
        key="convert_math"
    ):
        if not math_input.strip():
            st.warning("Please enter an expression.")
        else:
            try:
                expression = sp.sympify(math_input)
                latex_output = sp.latex(expression)

                show_latex_result(
                    latex_output,
                    "math"
                )

            except Exception:
                st.error(
                    "I couldn't understand that expression."
                )

                st.info(
                    "Try something like: (x^2 + 1) / 2"
                )


with image_tab:
    st.subheader("Image → LaTeX")

    st.caption(
        "Upload a PNG, JPG or JPEG containing a mathematical equation."
    )

    uploaded_file = st.file_uploader(
        "Choose an image",
        type=["png", "jpg", "jpeg"],
        label_visibility="collapsed"
    )

    if uploaded_file:

        try:
            image = Image.open(uploaded_file)

            st.image(
                image,
                caption="Uploaded equation",
                width="stretch"
            )

        except Exception:
            st.error("The uploaded image could not be opened.")
            st.stop()

        if st.button(
            "Convert Image",
            type="primary",
            width="stretch",
            key="convert_image"
        ):

            with st.spinner("Recognizing equation..."):

                try:
                    from pix2text import Pix2Text

                    p2t = Pix2Text()

                    result = p2t.recognize_formula(image)

                    latex_output = clean_latex(result)

                    if not latex_output:
                        st.error(
                            "No mathematical equation was detected."
                        )
                    else:
                        st.success("Equation recognized.")

                        show_latex_result(
                            latex_output,
                            "image"
                        )

                except Exception as error:
                    st.error(
                        "Image recognition failed."
                    )

                    st.warning(
                        "Pix2Text is installed, but the recognition "
                        "process returned an error."
                    )

                    with st.expander("Technical details"):
                        st.code(str(error))


st.divider()

st.caption("Math ↔ LaTeX Converter")
