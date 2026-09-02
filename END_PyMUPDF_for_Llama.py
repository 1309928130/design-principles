# import fitz  # PyMuPDF
# import json
# import os
#
# def extract_text_from_pdf(pdf_path):
#     """
#     Extracts text from a PDF file.
#
#     Parameters:
#     pdf_path (str): The path to the PDF file.
#
#     Returns:
#     str: The extracted text from the PDF.
#     """
#     doc = fitz.open(pdf_path)
#     text = ""
#     for page_num in range(len(doc)):
#         page = doc.load_page(page_num)
#         text += page.get_text()
#     return text
#
# def clean_text(text):
#     """
#     Cleans the extracted text by replacing newline characters with spaces
#     and ensuring proper formatting.
#
#     Parameters:
#     text (str): The extracted text.
#
#     Returns:
#     str: The cleaned text.
#     """
#     # Replace multiple newlines with a single newline
#     cleaned_text = text.replace('\n', ' ').replace('  ', ' ').strip()
#     return cleaned_text
#
# def save_text_to_json(text, json_path):
#     """
#     Saves the extracted text to a JSON file.
#
#     Parameters:
#     text (str): The extracted text.
#     json_path (str): The path to the JSON file where the text will be saved.
#     """
#     data = {"text": text}
#     with open(json_path, 'w', encoding='utf-8') as json_file:
#         json.dump(data, json_file, ensure_ascii=False, indent=4)
#
# def main(pdf_path, json_path):
#     """
#     Main function to extract text from a PDF and save it to a JSON file.
#
#     Parameters:
#     pdf_path (str): The path to the PDF file.
#     json_path (str): The path to the JSON file where the text will be saved.
#     """
#     text = extract_text_from_pdf(pdf_path)
#     cleaned_text = clean_text(text)
#     save_text_to_json(cleaned_text, json_path)
#     print(f"Text from {pdf_path} has been saved to {json_path}")
#
# if __name__ == "__main__":
#     # Specify the path to the PDF file
#     pdf_path = "/Users/enshanchen/Downloads/for_github_0720/Hoogendoorn and Daamen - 2004 - Design assessment of Lisbon transfer stations usin.pdf"
#
#     # Specify the path where the JSON file will be saved
#     json_path = "/Users/enshanchen/Downloads/for_github_0720/Hoogendoorn and Daamen - 2004 - Design assessment of Lisbon transfer stations usin_text.json"
#
#     # Create the directory if it doesn't exist
#     os.makedirs(os.path.dirname(json_path), exist_ok=True)
#
#     # Run the main function
#     main(pdf_path, json_path)


import fitz  # PyMuPDF
import json
import os
import glob


def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.

    Parameters:
    pdf_path (str): The path to the PDF file.

    Returns:
    str: The extracted text from the PDF.
    """
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text


def clean_text(text):
    """
    Cleans the extracted text by replacing newline characters with spaces
    and ensuring proper formatting.

    Parameters:
    text (str): The extracted text.

    Returns:
    str: The cleaned text.
    """
    cleaned_text = text.replace('\n', ' ').replace('  ', ' ').strip()
    return cleaned_text


def save_text_to_json(text, json_path):
    """
    Saves the extracted text to a JSON file.

    Parameters:
    text (str): The extracted text.
    json_path (str): The path to the JSON file where the text will be saved.
    """
    data = {"text": text}
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


def process_pdfs_in_directory(directory, output_directory):
    """
    Processes all PDFs in a directory and its subdirectories, extracting text and saving it to JSON files.

    Parameters:
    directory (str): The path to the directory containing PDFs.
    output_directory (str): The path to the directory where JSON files will be saved.
    """
    pdf_paths = glob.glob(os.path.join(directory, '**', '*.pdf'), recursive=True)

    for pdf_path in pdf_paths:
        try:
            text = extract_text_from_pdf(pdf_path)
            cleaned_text = clean_text(text)
            base_name = os.path.basename(pdf_path).replace('.pdf', '.json')
            json_path = os.path.join(output_directory, base_name)
            save_text_to_json(cleaned_text, json_path)
            print(f"Text from {pdf_path} has been saved to {json_path}")
        except Exception as e:
            print(f"Failed to process {pdf_path}: {e}")


if __name__ == "__main__":
    # Specify the path to the directory containing the PDFs
    pdf_directory = "/Users/enshanchen/Downloads/for_design_vocabulary_principles/generated_json_files"

    # Specify the output directory where the JSON files will be saved
    output_directory = pdf_directory

    # Process the PDFs
    process_pdfs_in_directory(pdf_directory, output_directory)
