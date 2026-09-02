import fitz  # PyMuPDF
import csv
import os
import glob

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

def clean_text(text):
    cleaned_text = text.replace('\n', ' ').replace('  ', ' ').strip()
    return cleaned_text

def save_text_to_csv(text, csv_path):
    with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        # csv_writer.writerow(['text'])
        csv_writer.writerow([text])

def process_pdfs_in_directory(directory, output_directory):
    pdf_paths = glob.glob(os.path.join(directory, '**', '*.pdf'), recursive=True)
    for pdf_path in pdf_paths:
        try:
            text = extract_text_from_pdf(pdf_path)
            cleaned_text = clean_text(text)
            base_name = os.path.basename(pdf_path).replace('.pdf', '.csv')
            csv_path = os.path.join(output_directory, base_name)
            save_text_to_csv(cleaned_text, csv_path)
            print(f"Text from {pdf_path} has been saved to {csv_path}")
        except Exception as e:
            print(f"Failed to process {pdf_path}: {e}")

if __name__ == "__main__":
    pdf_directory = "/Users/enshanchen/Downloads/for_design_vocabulary_principles"
    output_directory = "/Users/enshanchen/Downloads/for_design_vocabulary_principles/csv"
    process_pdfs_in_directory(pdf_directory, output_directory)






