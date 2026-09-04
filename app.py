import streamlit as st
import sympy as sp
from PIL import Image
from pix2text import Pix2Text


# --------------------------------------------------
# Page setup
# --------------------------------------------------

st.set_page_config(
    page_title="Maths → LaTeX",
    page_icon="∑",
    layout="centered"
)

st.title("Maths → LaTeX")
st.write("Convert mathematical expressions and images into editable LaTeX.")


# --------------------------------------------------
# Helpers
# --------------------------------------------------

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


# --------------------------------------------------
# Copy component
# --------------------------------------------------

COPY_HTML = """
<div class="copy-container">
    <button id="copy-equation">
        📋 Copy as Equation
    </button>

    <button id="copy-latex">
        📋 Copy as LaTeX
    </button>
</div>
"""


COPY_CSS = """
.copy-container {
    display: flex;
    gap: 10px;
    margin-top: 6px;
    margin-bottom: 10px;
}

button {
    border: 1px solid var(--st-border-color);
    border-radius: 6px;
    padding: 8px 14px;
    background: var(--st-secondary-background-color);
    color: var(--st-text-color);
    cursor: pointer;
    font-size: 14px;
}

button:hover {
    border-color: var(--st-primary-color);
}

button:active {
    transform: translateY(1px);
}
"""


COPY_JS = """
export default function(component) {

    const { data, parentElement } = component;

    const equationButton =
        parentElement.querySelector("#copy-equation");

    const latexButton =
        parentElement.querySelector("#copy-latex");


    function copied(button, originalText) {

        button.innerText = "✓ Copied";

        setTimeout(() => {
            button.innerText = originalText;
        }, 1500);
    }


    // ----------------------------------------
    // Copy LaTeX
    // ----------------------------------------

    latexButton.onclick = async () => {

        try {

            await navigator.clipboard.writeText(data.latex);

            copied(
                latexButton,
                "📋 Copy as LaTeX"
            );

        } catch (error) {

            const textarea =
                document.createElement("textarea");

            textarea.value = data.latex;

            textarea.style.position = "fixed";
            textarea.style.opacity = "0";

            document.body.appendChild(textarea);

            textarea.focus();
            textarea.select();

            document.execCommand("copy");

            textarea.remove();

            copied(
                latexButton,
                "📋 Copy as LaTeX"
            );
        }
    };


    // ----------------------------------------
    // Render equation and copy as PNG
    // ----------------------------------------

    equationButton.onclick = async () => {

        try {

            equationButton.innerText =
                "⏳ Copying...";


            // Load MathJax once
            if (!window.MathJax) {

                window.MathJax = {
                    tex: {
                        inlineMath: [
                            ["\\\\(", "\\\\)"]
                        ],
                        displayMath: [
                            ["\\\\[", "\\\\]"]
                        ]
                    },

                    svg: {
                        fontCache: "none"
                    }
                };


                await new Promise((resolve, reject) => {

                    const script =
                        document.createElement("script");

                    script.src =
                        "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js";

                    script.onload = resolve;
                    script.onerror = reject;

                    document.head.appendChild(script);
                });
            }


            // Create temporary math element
            const math =
                document.createElement("div");

            math.style.position = "fixed";
            math.style.left = "-10000px";
            math.style.top = "0";

            math.style.background = "white";
            math.style.color = "black";

            math.style.padding = "20px";

            math.style.fontSize = "32px";

            math.innerHTML =
                "\\\\[" +
                data.latex +
                "\\\\]";


            document.body.appendChild(math);


            // Render LaTeX
            await MathJax.typesetPromise([math]);


            const svg =
                math.querySelector("svg");


            if (!svg) {

                throw new Error(
                    "Equation rendering failed."
                );
            }


            // Clone SVG
            const svgClone =
                svg.cloneNode(true);


            svgClone.setAttribute(
                "xmlns",
                "http://www.w3.org/2000/svg"
            );


            // Convert SVG to string
            const svgString =
                new XMLSerializer()
                    .serializeToString(svgClone);


            // Create SVG blob
            const svgBlob =
                new Blob(
                    [svgString],
                    {
                        type: "image/svg+xml"
                    }
                );


            const svgUrl =
                URL.createObjectURL(svgBlob);


            // Load SVG into an image
            const img =
                new Image();


            await new Promise((resolve, reject) => {

                img.onload = resolve;
                img.onerror = reject;

                img.src = svgUrl;
            });


            // Create canvas
            const canvas =
                document.createElement("canvas");


            const scale = 2;


            canvas.width =
                img.width * scale;

            canvas.height =
                img.height * scale;


            const ctx =
                canvas.getContext("2d");


            ctx.fillStyle = "white";

            ctx.fillRect(
                0,
                0,
                canvas.width,
                canvas.height
            );


            ctx.scale(
                scale,
                scale
            );


            ctx.drawImage(
                img,
                0,
                0
            );


            // Convert canvas to PNG
            const pngBlob =
                await new Promise(resolve => {

                    canvas.toBlob(
                        resolve,
                        "image/png"
                    );
                });


            if (!pngBlob) {

                throw new Error(
                    "PNG conversion failed."
                );
            }


            // Copy PNG to clipboard
            const clipboardItem =
                new ClipboardItem({
                    "image/png": pngBlob
                });


            await navigator.clipboard.write([
                clipboardItem
            ]);


            // Cleanup
            URL.revokeObjectURL(svgUrl);

            math.remove();


            copied(
                equationButton,
                "📋 Copy as Equation"
            );


        } catch (error) {

            console.error(
                "Copy equation error:",
                error
            );


            equationButton.innerText =
                "⚠ Copy failed";


            setTimeout(() => {

                equationButton.innerText =
                    "📋 Copy as Equation";

            }, 2000);
        }
    };
}
"""


# Register component once
copy_component = st.components.v2.component(
    name="equation_copy_component",
    html=COPY_HTML,
    css=COPY_CSS,
    js=COPY_JS
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
    copy_component(
        data={
            "latex": latex
        }
    )


# --------------------------------------------------
# Tabs
# --------------------------------------------------

tab1, tab2, tab3 = st.tabs(
    [
        "LaTeX → Math",
        "Math → LaTeX",
        "Image → LaTeX"
    ]
)


# --------------------------------------------------
# LaTeX → Math
# --------------------------------------------------

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


# --------------------------------------------------
# Math → LaTeX
# --------------------------------------------------

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

                expression =
                    sp.sympify(math_input)

                latex =
                    sp.latex(expression)

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


# --------------------------------------------------
# Image → LaTeX
# --------------------------------------------------

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

                    result =
                        p2t.recognize_formula(
                            image
                        )

                    latex =
                        clean_latex(result)

                    show_latex_result(
                        latex
                    )

                except Exception as e:

                    st.error(
                        "Couldn't read the equation "
                        "from the image."
                    )

                    st.exception(e)
