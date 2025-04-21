import os
import shutil

from PyPDF2                     import PdfReader, PdfWriter
from concurrent.futures         import ProcessPoolExecutor
from unstructured.partition.pdf import partition_pdf

class PDFProcessor:

    def __init__(self, split_dir=None):
        self.split_dir = split_dir

    def process_single_pdf(self, file_path, image_path=None):
        return partition_pdf(
            filename=file_path,
            content_type="application/pdf",
            extract_images_in_pdf=True,
            extract_image_block_types=["Image", "Table"],
            skip_infer_table_types=False,
            infer_table_structure=True,
            include_page_breaks=True,
            extract_image_block_to_payload=False,
            extract_image_block_output_dir=image_path,
            languages=["eng"],
            strategy='hi_res',
            split_pdf_page=True,
            chunking_strategy="by_title",
            max_characters=4000,
            new_after_n_chars=3800,
            combine_text_under_n_chars=2000,
        )

    def split_pdf(self, input_path):
        os.makedirs(self.split_dir, exist_ok=True)
        split_files = []
        for pdf in input_path:
          input_pdf = PdfReader(open(pdf, 'rb'))
          for page_num in range(len(input_pdf.pages)):
              output_pdf = PdfWriter()
              output_pdf.add_page(input_pdf.pages[page_num])
              base_name = os.path.splitext(os.path.basename(pdf))[0]
              output_filename = os.path.join(self.split_dir, f'{base_name}_{page_num + 1}.pdf')
              print(output_filename)
              with open(output_filename, 'wb') as output_file:
                  output_pdf.write(output_file)
              split_files.append(output_filename)
        return split_files

    def process_pdf_in_parallel(self, pdf_files):
        files_pdf   = []
        elements    = []

        if type(pdf_files) == list:
          files_pdf = pdf_files
        elif type(pdf_files) == str:
          files_pdf = [os.path.join(pdf_files, pdf) for pdf in os.listdir(pdf_files) if pdf.endswith('.pdf')]
        
        split_files = self.split_pdf(files_pdf)
        
        with ProcessPoolExecutor() as executor:
            results = executor.map(self.process_single_pdf, split_files)
            for result in results:
                elements.extend(result)
        return elements

    def clean(self):
        if os.path.exists(self.split_dir):
            shutil.rmtree(self.split_dir)