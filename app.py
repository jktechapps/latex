import streamlit as st
import streamlit.components.v1 as components
import sympy as sp
from PIL import Image
from pix2text import Pix2Text
import html
import uuid


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
# Helpers
# -----------------------------

def clean_latex(latex):
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


def copy_buttons(latex):
    """
    Display buttons for:
    - Copy as Equation
    - Copy as LaTeX
    """

    latex = clean_latex(latex)

    # Safely put LaTeX inside JavaScript
    latex_js = (
        latex
        .replace("\\", "\\\\")
        .replace("`", "\\`")
        .replace("${", "\\${")
    )

    component_id = uuid.uuid4().hex

    html_code = f"""
<!DOCTYPE html>
<html>
<head>

<script>
window.MathJax = {{
    tex: {{
        inlineMath: [['\\\\(', '\\\\)']],
        displayMath: [['\\\\[', '\\\\]']]
    }},
    svg: {{
        fontCache: 'none'
    }}
}};
</script>

<script
    src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js">
</script>

<style>

body {{
    margin: 0;
    background: transparent;
    font-family: sans-serif;
}}

.buttons {{
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin: 4px 0 10px 0;
}}

button {{
    padding: 8px 14px;
    border-radius: 6px;
    border: 1px solid #555;
    background: transparent;
    color: #f5f5f5;
    cursor: pointer;
    font-size: 14px;
}}

button:hover {{
    background: rgba(255,255,255,0.08);
}}

button:active {{
    background: rgba(255,255,255,0.15);
}}

</style>

</head>

<body>

<div class="buttons">

<button id="equationButton">
📋 Copy as Equation
</button>

<button id="latexButton">
📋 Copy as LaTeX
</button>

</div>

<script>

const latex = `{latex_js}`;

const equationButton =
    document.getElementById("equationButton");

const latexButton =
    document.getElementById("latexButton");


function copied(button, original) {{

    button.innerText = "✓ Copied";

    setTimeout(() => {{
        button.innerText = original;
    }}, 1500);

}}


// -----------------------------
// Copy LaTeX
// -----------------------------

latexButton.addEventListener("click", async () => {{

    try {{

        await navigator.clipboard.writeText(latex);

        copied(
            latexButton,
            "📋 Copy as LaTeX"
        );

    }} catch (error) {{

        const textarea =
            document.createElement("textarea");

        textarea.value = latex;

        document.body.appendChild(textarea);

        textarea.select();

        document.execCommand("copy");

        textarea.remove();

        copied(
            latexButton,
            "📋 Copy as LaTeX"
        );

    }}

}});


// -----------------------------
// Copy Equation
// -----------------------------

equationButton.addEventListener("click", async () => {{

    try {{

        await MathJax.typesetPromise();

        const math =
            document.createElement("div");

        math.style.position = "fixed";
        math.style.left = "-10000px";
        math.style.top = "0";
        math.style.background = "white";
        math.style.padding = "20px";
        math.style.fontSize = "30px";
        math.style.color = "black";

        math.innerHTML =
            "\\\\[" + latex + "\\\\]";

        document.body.appendChild(math);

        await MathJax.typesetPromise([math]);

        const svg =
            math.querySelector("svg");

        if (!svg) {{
            throw new Error(
                "Could not render equation."
            );
        }}

        const svgCopy =
            svg.cloneNode(true);

        svgCopy.setAttribute(
            "xmlns",
            "http://www.w3.org/2000/svg"
        );

        const svgData =
            new XMLSerializer()
                .serializeToString(svgCopy);

        const svgBlob =
            new Blob(
                [svgData],
                {{
                    type: "image/svg+xml"
                }}
            );

        if (
            navigator.clipboard &&
            window.ClipboardItem
        ) {{

            const item =
                new ClipboardItem({{
                    "image/svg+xml": svgBlob
                }});

            await navigator.clipboard.write([item]);

        }} else {{

            throw new Error(
                "Image clipboard is not supported by this browser."
            );

        }}

        math.remove();

        copied(
            equationButton,
            "📋 Copy as Equation"
        );

    }} catch (error) {{

        console.error(error);

        equationButton.innerText =
            "⚠ Copy failed";

        setTimeout(() => {{

            equationButton.innerText =
                "📋 Copy as Equation";

        }}, 2000);

    }}

}});

</script>

</body>
</html>
"""

    components.html(
        html_code,
        height=55,
        scrolling=False
    )


def show_latex_result(latex):

    latex = clean_latex(latex)

    if not latex:
        st.error("No equation was generated.")
        return

    st.subheader("Generated Equation")

    # Render equation
    st.latex(latex)

    # Copy buttons
    copy_buttons(latex)


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
# LaTeX → Math
# -----------------------------

with tab1:

    st.subheader("Enter LaTeX")

    latex_input = st.text_area(
        "LaTeX",
        placeholder=r"\frac{x^2 + 1}{2}",
        height=120,
        label_visibility="collapsed"
    )

    if st.button(
        "Render Equation",
        key="render_button"
    ):

        if latex_input.strip():

            show_latex_result(
                latex_input
            )

        else:

            st.warning(
                "Please enter a LaTeX equation."
            )


# -----------------------------
# Math → LaTeX
# -----------------------------

with tab2:

    st.subheader(
        "Enter a Mathematical Expression"
    )

    math_input = st.text_area(
        "Math expression",
        placeholder="(x^2 + 1)/2",
        height=120,
        label_visibility="collapsed"
    )

    st.caption(
        "Examples: (x^2 + 1)/2, sqrt(x), "
        "sin(x), x^2 + y^2"
    )

    if st.button(
        "Convert to LaTeX",
        key="math_button"
    ):

        if math_input.strip():

            try:

                expression = sp.sympify(
                    math_input
                )

                latex = sp.latex(
                    expression
                )

                show_latex_result(
                    latex
                )

            except Exception:

                st.error(
                    "I couldn't understand "
                    "that mathematical expression."
                )

        else:

            st.warning(
                "Please enter a mathematical expression."
            )


# -----------------------------
# Image → LaTeX
# -----------------------------

with tab3:

    st.subheader(
        "Upload a Mathematical Image"
    )

    uploaded_file = st.file_uploader(
        "Upload image",
        type=[
            "png",
            "jpg",
            "jpeg",
            "webp"
        ],
        label_visibility="collapsed"
    )

    if uploaded_file:

        image = Image.open(
            uploaded_file
        )

        st.image(
            image,
            caption="Uploaded image",
            use_container_width=True
        )

        if st.button(
            "Convert Image to LaTeX",
            key="image_button"
        ):

            with st.spinner(
                "Reading equation..."
            ):

                try:

                    p2t = Pix2Text()

                    result = (
                        p2t.recognize_formula(
                            image
                        )
                    )

                    latex = clean_latex(
                        result
                    )

                    show_latex_result(
                        latex
                    )

                except Exception as e:

                    st.error(
                        "Couldn't read the equation "
                        "from the image."
                    )

                    st.exception(e)
