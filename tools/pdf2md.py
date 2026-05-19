import fitz  # PyMuPDF
import pymupdf4llm
import argparse
import os

def pdf_to_markdown(pdf_path, output_md_path=None):
    """
    Converts an academic PDF to a Markdown file optimized for LLM Context Windows.
    Preserves tables, figures (as descriptions or extracted), and hierarchical structure.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
        
    print(f"[*] Extracting highly accurate Markdown from {pdf_path}...")
    md_text = pymupdf4llm.to_markdown(pdf_path)
    
    if output_md_path is None:
        output_md_path = pdf_path.replace('.pdf', '.md')
        
    with open(output_md_path, 'w', encoding='utf-8') as f:
        f.write(md_text)
        
    print(f"[+] Successfully saved Markdown to {output_md_path}")
    print(f"[i] Context size (chars): {len(md_text)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Academic PDF to LLM-Optimized Markdown")
    parser.add_argument("pdf", help="Path to the PDF file")
    parser.add_argument("-o", "--output", help="Output Markdown path", default=None)
    args = parser.parse_args()
    
    pdf_to_markdown(args.pdf, args.output)
