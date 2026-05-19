import docx
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

class IEEEFormatter:
    """
    Automates the formatting of an academic research paper strictly to IEEE/APA standards.
    """
    def __init__(self, output_path="Formatted_Paper.docx"):
        self.doc = docx.Document()
        self.output_path = output_path
        self._setup_styles()

    def _setup_styles(self):
        # Set normal text to Times New Roman 10pt
        style = self.doc.styles['Normal']
        font = style.font
        font.name = 'Times New Roman'
        font.size = Pt(10)

    def add_title(self, title_text):
        p = self.doc.add_paragraph(title_text)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.runs[0].font.size = Pt(24)
        p.runs[0].bold = True

    def add_abstract(self, abstract_text):
        self.doc.add_heading('Abstract', level=1)
        p = self.doc.add_paragraph(abstract_text)
        p.runs[0].bold = True
        p.runs[0].italic = True

    def add_section(self, heading, content):
        self.doc.add_heading(heading, level=1)
        self.doc.add_paragraph(content)

    def save(self):
        self.doc.save(self.output_path)
        print(f"[+] Paper automatically compiled and saved to {self.output_path}")

if __name__ == "__main__":
    formatter = IEEEFormatter("Sample_IEEE_Paper.docx")
    formatter.add_title("Autonomous Microgrid Optimization using Physics-Informed Neural Networks")
    formatter.add_abstract("This paper presents a novel approach to solar forecasting using PINNs...")
    formatter.add_section("1. Introduction", "Energy forecasting is critical for microgrids...")
    formatter.save()
