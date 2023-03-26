import re
import json
import typer
import PyPDF2
from pathlib import Path

app = typer.Typer()


def get_output_filename(input_filename: str) -> str:
    """Return the output filename for the given input filename."""
    input_path = Path(input_filename)
    return f"{input_path.stem}_extracted.json"


@app.command()
def extract_data_from_pdf(pdf_file_path: str):
    """
    Extract data from a PDF file and print it as a dictionary.
    """
    # Open the PDF file in read-binary mode
    with open(pdf_file_path, "rb") as pdf_file:
        # Create a new PDF reader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        # Get the number of pages in the PDF
        num_pages = len(pdf_reader.pages)
        # Initialize an empty dictionary to store the data
        data = {}
        # Loop through each page in the PDF
        for page_num in range(num_pages):
            # Get the text content of the page
            page = pdf_reader.pages[page_num]
            text = page.extract_text().replace("  \n", "").replace(" \xad", "")
            data[page_num] = text
        # Print the dictionary of data
        typer.echo(data)
        # Export the dictionary of data as JSON
        output_filename = get_output_filename(pdf_file_path)
        output_path = Path(output_filename)
        with output_path.open("w") as output_file:
            json.dump(data, output_file, indent=2)
        typer.echo(
            f"Data extracted from {pdf_file_path} and saved to {output_path.absolute()}."
        )


if __name__ == "__main__":
    app()
