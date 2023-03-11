import streamlit as st
from pathlib import Path
import base64

from bioelfa import normalizer, dataloader

CURRENT_DIRECTORY = Path(__file__).parent
STATIC_DIR = CURRENT_DIRECTORY / "static"


def img_to_base64(img_path: Path) -> str:
    img_bytes = img_path.read_bytes()
    return base64.b64encode(img_bytes).decode()

def add_header():
    LOGO_PATH = STATIC_DIR / "logo.png"
    st.sidebar.image(str(LOGO_PATH))

def add_sidebar():
    with st.sidebar:
        add_header()
        st.markdown("""
        👉 Need help? [Ask a question](https://github.com/andraghetti/bioelfa/issues/new)
        """)

def set_page_config():
    st.set_page_config(
        page_title="Bioelfa",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def add_normalize_section():
    st.markdown('## Normalize')
    st.markdown(normalizer.normalize.__doc__)
    with st.expander("Normalize"):
        with st.form(key='form_normalize', clear_on_submit=False):
            file = st.file_uploader("Drag and drop a file to process", key='upload_normalize')
            seed = st.number_input(
                label="""
                A seed is a value used to initialize a random number generator, 
                allowing for reproducibility of the same sequence of random numbers.
                The seed is set to 0 by default to ensure reproducibility, but it can be
                changed here, to get different results:
                """,
                value=0,
                key=int
            )
            submitted = st.form_submit_button("Submit")
            if submitted:
                if file:
                    if file.type != 'text/csv':
                        st.error("The file should be a CSV.")
                        st.stop()
                    dataframe = dataloader.load_csv(file)
                    with st.spinner(text="In progress..."):
                        resulting_dataframe = normalizer.normalize(dataframe, seed)
                else:
                    st.error("You must select a file")
                    st.stop()
            else:
                st.stop()
        if submitted:
            st.write("This is the normalized resulting dataframe:")
            st.dataframe(resulting_dataframe)
            csv_result_bytes = dataframe.to_csv(sep=';')
            st.download_button(
                "Download this dataframe as CSV",
                data=csv_result_bytes,
                file_name=f"normalized_{file.name}",
                mime='text/csv'
            )

def main():
    set_page_config()
    st.title("BIOELFA")
    add_sidebar()
    add_normalize_section()        

if __name__ == "__main__":
    main()