# 🎓 Academic-AI-Copilot

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-green)
![LLM Agents](https://img.shields.io/badge/AI-Agents%20%26%20MCP-orange)

An open-source toolkit designed to completely automate the academic writing, reviewing, and formatting lifecycle using Python and AI Agents. This project acts as an autonomous **AI Copilot for Researchers**, drastically reducing the time spent on formatting, context extraction, and literature review.

## 🚀 Key Features

### 1. 📄 `pdf2md.py` (Zero-Hallucination PDF Extraction)
Converts complex academic PDFs (with multi-column layouts, mathematical equations, and booktabs tables) directly into highly optimized Markdown format. 
- **Why?** Perfect for loading research papers into LLM context windows (like Claude or GPT-4) without losing structural integrity or burning excess tokens.
- **Tech:** Built on top of `PyMuPDF4LLM`.

### 2. 📝 `word_formatter.py` (Programmatic IEEE/APA Typesetting)
Automatically generates perfectly formatted Microsoft Word (`.docx`) files from plain text or markdown inputs. 
- Implements strict IEEE and APA 7th edition formatting rules.
- Manages dynamic tables, OMML math equation rendering, and structural headings automatically.
- Completely removes the need to manually battle Word formatting for journal submissions.

### 3. 🔬 SciWrite Agent (Automated Peer-Review Simulation)
A multi-stage prompt engineering framework and pipeline that reviews academic texts using Dr. Kristin Sainani's 'Writing in the Sciences' methodology.
- Extracts clutter, improves voice vitality, checks keyword consistency, and verifies citation integrity before submission.

## ⚙️ Quick Start

```bash
git clone https://github.com/Marco9249/Academic-AI-Copilot.git
cd Academic-AI-Copilot
pip install -r requirements.txt
```

### Convert a Paper for LLM Analysis:
```bash
python tools/pdf2md.py my_research_paper.pdf --output context_ready.md
```

## 🏗️ Architecture
This project is built using:
- **PyMuPDF / PyMuPDF4LLM:** High-fidelity data extraction.
- **python-docx:** Headless Word document generation.
- **Prompt Engineering / MCP:** Bridging the gap between raw Python outputs and AI reasoning engines.

## 🤝 Contributing
As researchers, we spend too much time formatting and not enough time discovering. Contributions to add more journal templates (Nature, Science, Elsevier) or better agentic review hooks are welcome!

## 📬 Contact
- **Email:** izzeldeenm@gmail.com
- **GitHub:** [Marco9249](https://github.com/Marco9249)

---
*Maintained by [Marco9249](https://github.com/Marco9249) - Bridging Deep Learning and Practical Automation.*
