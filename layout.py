from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from styles import (
    PAGE_TITLE,
    BLACK,
    WHITE,
    HEADER_GREEN,
    ROW_GREEN,
    BCG_BLUE,
    TITLE_FONT,
    HEADER_FONT,
    BODY_FONT,
    TITLE_SIZE,
    HEADER_SIZE,
    BODY_SIZE,
)


from components import PDFForm


def create_hardware_request(pdf):

    pdf.title("Hardware Request Form")

    pdf.row(
        ("Requestor", "requestor", 2),
        ("Date", "date", 1),
        ("Job #", "job_number", 1)
    )

    pdf.row(
        ("Job Name", "job_name", 2),
        ("Phone", "phone", 1),
        ("Email", "email", 1)
    )