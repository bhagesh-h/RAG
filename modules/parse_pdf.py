import os
import glob
from langchain_unstructured import UnstructuredLoader

class ParsePDF:
    """
    Parse PDF files using UnstructuredLoader and save the extracted text, tables and images.
    """
    def __init__(self, path, output):
        self.path = path
        self.output = output
    
    def UnstructuredPDFLoader(self):
        pdfs_list       = glob.glob(os.path.join(self.path,"*.pdf"))
        images_path     = os.path.join(self.output, "images")
        text_path       = os.path.join(self.output, "text")
        loader_object   = {}

        os.makedirs(images_path, exist_ok=True)
        os.makedirs(text_path, exist_ok=True)
        
        if not pdfs_list:
            raise ValueError("No PDF files found in the specified directory.")
        
        for file_path in pdfs_list :
            extracted_content   = ""
            txt_file_path       = os.path.join(text_path, os.path.basename(file_path).replace(".pdf", ".txt"))
            loader              = UnstructuredLoader(
                strategy="hi_res",
                file_path=file_path,
                extract_images_in_pdf=True,
                extract_image_block_to_payload=False,
                extract_image_block_output_dir=images_path,
                extract_image_block_types=["Image", "Table"]
                )
            
            try:
                docs = loader.load()
            except:
                docs = []
                for doc in loader.lazy_load():
                    docs.append(doc)
                for doc in docs:
                    extracted_content += doc.page_content + "\n"
            
            with open(txt_file_path, 'w') as file:
                file.write(extracted_content)
            
            loader_object[file_path] = docs
        
        return loader_object