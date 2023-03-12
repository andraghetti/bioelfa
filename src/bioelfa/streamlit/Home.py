import streamlit as st
from pathlib import Path
import base64

from bioelfa import normalizer, dataloader, geneset_compare

CURRENT_DIRECTORY = Path(__file__).parent
STATIC_DIR = CURRENT_DIRECTORY / "static"

normalize_example_file = STATIC_DIR / "bacteria_family.csv"
compare_example_file = STATIC_DIR / "230311_datacomparison.csv"


def img_to_base64(img_path: Path) -> str:
    img_bytes = img_path.read_bytes()
    return base64.b64encode(img_bytes).decode()


def add_header():
    LOGO_PATH = STATIC_DIR / "logo.png"
    st.sidebar.image(str(LOGO_PATH))


def add_sidebar():
    with st.sidebar:
        add_header()
        st.markdown(
            """
        👉 Need help? [Ask a question](https://github.com/andraghetti/bioelfa/issues/new)
        """
        )


def set_page_config():
    st.set_page_config(
        page_title="Bioelfa", layout="wide", initial_sidebar_state="expanded"
    )


def add_normalize_section():
    st.markdown("## Normalize")
    st.markdown(normalizer.normalize.__doc__)
    with st.expander("Normalize"):
        with open(normalize_example_file.absolute(), "rb") as file:
            st.download_button(
                "Do you need an example file?",
                data=file,
                file_name=normalize_example_file.name,
                mime="text/csv",
            )
        with st.form(key="form_normalize", clear_on_submit=False):
            file = st.file_uploader(
                "Drag and drop a file to process", key="upload_normalize"
            )
            seed = st.number_input(
                label="""
                A seed is a value used to initialize a random number generator,
                allowing for reproducibility of the same sequence of random numbers.
                The seed is set to 0 by default to ensure reproducibility, but it can be
                changed here, to get different results:
                """,
                value=0,
                key=int,
            )
            submitted = st.form_submit_button("Submit")
            if submitted:
                if file:
                    if file.type != "text/csv":
                        st.error("The file should be a CSV.")
                        return
                    dataframe = dataloader.load_csv(file)
                    with st.spinner(text="In progress..."):
                        resulting_dataframe = normalizer.normalize(dataframe, seed)
                else:
                    st.error("You must select a file")
                    return
            else:
                return
        if submitted:
            st.write("This is the resulting dataframe with the occurences:")
            st.dataframe(resulting_dataframe)
            csv_result_bytes = dataframe.to_csv(sep=";")
            st.download_button(
                "Download this dataframe as CSV",
                data=csv_result_bytes,
                file_name=f"normalized_{file.name}",
                mime="text/csv",
            )


def add_compare_section():
    st.markdown("## Compare")
    st.markdown(geneset_compare.compare_datasets.__doc__)
    with st.expander("Compare"):
        with open(compare_example_file.absolute(), "rb") as file:
            st.download_button(
                "Do you need an example file?",
                data=file,
                file_name=compare_example_file.name,
                mime="text/csv",
            )
        with st.form(key="form_compare", clear_on_submit=False):
            file = st.file_uploader(
                "Drag and drop a file to process", key="upload_compare"
            )
            submitted = st.form_submit_button("Submit")
            if submitted:
                if file:
                    if file.type != "text/csv":
                        st.error("The file should be a CSV.")
                        return
                    dataframe = dataloader.load_csv(file)
                    with st.spinner(text="In progress..."):
                        occurences_dataframe = geneset_compare.count_occurences(dataframe)
                else:
                    st.error("You must select a file")
                    return
            else:
                return
        if submitted:
            st.write("This is the normalized resulting dataframe:")
            st.dataframe(occurences_dataframe)
            csv_result_bytes = dataframe.to_csv(sep=";")
            st.download_button(
                "Download this dataframe as CSV",
                data=csv_result_bytes,
                file_name=f"occurences_{file.name}",
                mime="text/csv",
            )


def main():
    set_page_config()
    st.title("BIOELFA")
    add_sidebar()
    add_normalize_section()
    add_compare_section()


if __name__ == "__main__":
    main()
