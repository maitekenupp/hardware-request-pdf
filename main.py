from components import PDFForm
from reportlab.lib import colors

from pathlib import Path

output_file = Path("output/hardware_request.pdf")
output_file.parent.mkdir(parents=True, exist_ok=True)

pdf = PDFForm(str(output_file))

pdf.title("Hardware Request Form")

pdf.row(
    ("Requestor:", "requestor",2),
    ("Date:", "date",1),
    ("Date Needed:", "date_needed", 1, colors.red)
)

pdf.row(
    ("Email:", "email",2),
    ("Job#:", "job_number",1),
    None
)

pdf.row(
    ("Phone:", "phone",0.91),
    ("Job Name:", "job_name")
    
)

pdf.section("FOR INTERNAL USE ONLY")
pdf.parts_table(rows=29)
pdf.pulled_by_section()

pdf.save()

print("PDF created!")