# Hardware Request PDF Generator

A Python application that generates a structured, fillable hardware request form in PDF format. The project uses ReportLab and reusable layout components to create interactive fields, styled sections, and an editable parts table.

## Demo

[View the generated fillable PDF](examples/hardware_request_form.pdf)

> For the best experience with interactive form fields, download the PDF and open it in a compatible PDF reader.

## Features

- Fillable PDF form fields
- Reusable form and layout components
- Customizable colors, fonts, and dimensions
- Weighted row layout for flexible field sizing
- Alternating table row colors
- Interactive parts table
- Signature and completion fields
- Clean separation between layout, styles, and PDF components

## Project Structure

```text
hardware-request-pdf/
├── examples/
│   └── hardware_request_form.pdf
├── components.py
├── layout.py
├── main.py
├── styles.py
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.9 or newer
- ReportLab

## Installation

Clone the repository:

```bash
git clone https://github.com/maitekenupp/hardware-request-pdf.git
cd hardware-request-pdf
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install the dependency:

```bash
python -m pip install -r requirements.txt
```

## Usage

Run the PDF generator:

```bash
python main.py
```

The generated form will be saved as:

```text
output/hardware_request.pdf
```

## Customization

Visual settings such as colors, fonts, field sizes, and table styles can be changed in `styles.py`. Form fields and document sections can be adjusted in `main.py`, while reusable PDF components are defined in `components.py`.

## License

This project is licensed under the [MIT License](LICENSE).