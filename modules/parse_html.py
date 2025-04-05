import os
import glob
from langchain_community.document_loaders import UnstructuredHTMLLoader

class ParseHtml:
    """
    Parse HTML files using UnstructuredHTMLLoader and save the extracted text, tables and images.
    """
    def __init__(self, path, output):
        self.path = path
        self.output = output
    
    def UnstructuredHtmlLoader(self):
        html_list       = glob.glob(os.path.join(self.path,"*.html"))
        images_path     = os.path.join(self.output, "images")
        text_path       = os.path.join(self.output, "text")
        loader_object   = {}
        
        os.makedirs(images_path, exist_ok=True)
        os.makedirs(text_path, exist_ok=True)
        
        if not html_list: 
            raise ValueError("No HTML files found in the specified directory.")
        
        for file_path in html_list:
            extracted_content   = ""
            txt_file_path       = os.path.join(text_path, os.path.basename(file_path).replace(".html", ".txt"))
            loader              = UnstructuredHTMLLoader(
                file_path=file_path,
                extract_images_in_html=True,
                extract_image_block_to_payload=False,
                extract_image_block_output_dir=images_path,
                extract_image_block_types=["Image", "Table"]
                )
            
            try:
                htmls = loader.load()
            except:
                htmls = []
                for html in loader.lazy_load():
                    htmls.append(html)
                for html in htmls:
                    extracted_content += html.page_content + "\n"
            
            with open(txt_file_path, 'w') as file:
                file.write(extracted_content)
            
            loader_object[file_path] = htmls
        
        return loader_object