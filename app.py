import html
import streamlit as st
import sympy as sp
from PIL import Image

st.set_page_config(
    page_title="Math ↔ LaTeX Converter",
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

.result {
    margin-top: 1.5rem;
    font-weight: 600;
    font-size: 1.1rem;
}
</style>
""", unsafe_allow_html=True)


def copy_button(text, key):
    safe_text = html.escape(text).replace("\\", "\\\\").replace("`", "\\`")

    st.components.v1.html(
        f"""
        <button
            onclick="
                navigator.clipboard.writeText(`{safe_text}`);
                this.innerText='✓ Copied';
                setTimeout(() => this.innerText='📋 Copy LaTeX', 1500);
            "
            style="
                padding: 7px 14px;
                border: 1px solid #ccc;
                border-radius: 6px;
                background: white;
                cursor: pointer;
            "
        >
            📋 Copy LaTeX
        </button>
        """,
        height=45
    )


st.markdown(
    '<div class="title">Math ↔ LaTeX</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Convert equations between LaTeX, mathematical expressions and images.'
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

    latex = st.text_area(
        "Enter LaTeX",
        value=r"\frac{x^2 + 1}{2}",
        height=120,
        placeholder=r"\frac{x^2+1}{2}"
    )

    if st.button(
        "Render Equation",
        type="primary",
        use_container_width=True,
        key="render"
    ):
        if not latex.strip():
            st.warning("Enter some LaTeX first.")
        else:
            st.markdown(
                '<div class="result">Equation</div>',
                unsafe_allow_html=True
            )

            st.latex(latex)

            st.markdown(
                '<div class="result">LaTeX</div>',
                unsafe_allow_html=True
            )

            st.code(latex)

            copy_button(latex, "copy_latex")


with math_tab:
    st.subheader("Math expression → LaTeX")

    st.caption(
        "Examples: (x^2 + 1)/2, sqrt(x), sin(x), x^2 + y^2"
    )

    expression = st.text_input(
        "Enter expression",
        placeholder="(x^2 + 1) / 2"
    )

    if st.button(
        "Convert to LaTeX",
        type="primary",
        use_container_width=True,
        key="convert_math"
    ):
        if not expression.strip():
            st.warning("Enter an expression first.")
        else:
            try:
                result = sp.sympify(expression)
                latex = sp.latex(result)

                st.markdown(
                    '<div class="result">Equation</div>',
                    unsafe_allow_html=True
                )

                st.latex(latex)

                st.markdown(
                    '<div class="result">LaTeX</div>',
                    unsafe_allow_html=True
                )

                st.code(latex)

                copy_button(latex, "copy_math")

            except Exception:
                st.error(
                    "I couldn't understand that expression. "
                    "Try something like (x^2 + 1)/2."
                )


with image_tab:
    st.subheader("Image → LaTeX")

    st.caption(
        "Upload a PNG, JPG or JPEG containing a mathematical equation."
    )

    uploaded = st.file_uploader(
        "Upload equation image",
        type=["png", "jpg", "jpeg"],
        label_visibility="collapsed"
    )

    if uploaded:
        image = Image.open(uploaded)

        st.image(
            image,
            caption="Uploaded image",
            use_container_width=True
        )

        if st.button(
            "Convert Image",
            type="primary",
            use_container_width=True,
            key="convert_image"
        ):
            with st.spinner("Recognizing equation..."):
                try:
                    from pix2text import Pix2Text

                    p2t = Pix2Text()
                    result = p2t.recognize_formula(image)

                    latex = str(result).strip()

                    if not latex:
                        st.error("No equation was detected.")
                    else:
                        st.success("Equation recognized.")

                        st.markdown(
                            '<div class="result">LaTeX</div>',
                            unsafe_allow_html=True
                        )

                        st.code(latex)

                        copy_button(latex, "copy_image")

                        st.markdown(
                            '<div class="result">Equation</div>',
                            unsafe_allow_html=True
                        )

                        try:
                            st.latex(latex)
                        except Exception:
                            st.warning(
                                "The OCR result could not be rendered."
                            )

                except ImportError:
                    st.error(
                        "Pix2Text is not installed. "
                        "Check requirements.txt."
                    )

                except Exception as error:
                    st.error(
                        "The equation could not be recognized."
                    )
                    st.caption(str(error))


st.divider()

st.caption("Free Math ↔ LaTeX Converter")
