from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from styles import (FIELD_BORDER, FIELD_BACKGROUND, FIELD_TEXT, FIELD_HEIGHT, 
                    LABEL_FONT_SIZE, FIELD_FONT_SIZE, TABLE_HEADER_BACKGROUND, TABLE_HEADER_TEXT, TABLE_ROW_ODD, TABLE_ROW_EVEN,)


class PDFForm:

    def __init__(self, output_path):

        self.canvas = canvas.Canvas(output_path, pagesize=letter)

        self.page_width, self.page_height = letter

        self.margin = 40

        self.content_width = self.page_width - (self.margin * 2)

        # Layout

        self.column_gap = 25

        self.column_width = (self.content_width - self.column_gap) / 2

        self.label_width = 70

        self.field_height = 18

        self.y = self.page_height - self.margin

    def title(self, text):

        c = self.canvas

        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 22)

        title_y = self.y - 35

        c.drawCentredString(
            self.page_width / 2,
            title_y,
            text
        )

        line_y = title_y - 8

        c.setLineWidth(1.5)
        c.line(
            self.margin,
            line_y,
            self.page_width - self.margin,
            line_y
        )

        self.y = line_y - 25
  
    def space(self, amount=15):
        """
        Moves the cursor down by the specified amount.
        """

        self.y -= amount

    def label(self, text, x, y):

        self.canvas.setFont("Helvetica-Bold", LABEL_FONT_SIZE)

        self.canvas.drawString(x, y, text)

    def textbox(self, name, x, y, width=150, height=None, border_color=None,multiline=False):
        flags = "multiline" if multiline else ""

        if height is None:
            height = FIELD_HEIGHT

        if border_color is None:
            border_color = FIELD_BORDER

        self.canvas.acroForm.textfield(
            name=name,
            x=x,
            y=y,
            width=width,
            height=height,

            fontName="Helvetica",
            fontSize=FIELD_FONT_SIZE,
            fieldFlags=flags,

            borderStyle="underlined",
            borderColor=border_color,
            fillColor=FIELD_BACKGROUND,
            textColor=FIELD_TEXT,

            forceBorder=True
        )
    
    def signature_line(self, x, y, width):

        self.canvas.setStrokeColor(FIELD_BORDER)
        self.canvas.setLineWidth(1)

        self.canvas.line(
            x,
            y - 2,
            x + width,
            y - 2
        )

    def row(self, *fields):

        if len(fields) == 0:
            return

        normalized_fields = []

        for field_info in fields:

            border_color = None

            if field_info is None:
                normalized_fields.append((None, None, 1, None))
                continue

            if len(field_info) == 2:
                label, field_name = field_info
                weight = 1
                border_color = None

            elif len(field_info) == 3:
                label, field_name, weight = field_info
                border_color = None

            else:
                label, field_name, weight, border_color = field_info

            normalized_fields.append((label, field_name, weight, border_color))

        total_weight = sum(weight for _, _, weight, _ in normalized_fields)

        total_gap = self.column_gap * (len(normalized_fields) - 1)

        available_width = self.content_width - total_gap

        current_x = self.margin

        for label, field_name, weight, border_color in normalized_fields:

            column_width = available_width * (weight / total_weight)

            if label is not None:
                self.label(label, current_x, self.y)

                self.textbox(
                    field_name,
                    current_x + self.label_width,
                    self.y - 5,
                    width=column_width - self.label_width,
                    border_color=border_color
                )

            current_x += column_width + self.column_gap

        self.space(20)

    def section(self, title):

        self.space(5)

        self.canvas.setFont("Helvetica-Bold", 11)

        self.canvas.drawCentredString(
            self.page_width / 2,
            self.y,
            f"** {title.upper()} **"
        )

        self.space(10)

    def parts_table(self, rows=30):

        headers = ["QTY", "DESCRIPTION", "PART #", "FINISH", "NOTES"]

        column_weights = [0.4, 2.7, 1.8, 0.8, 2.5]

        row_height = 18
        header_height = 18

        table_width = self.content_width
        total_weight = sum(column_weights)

        column_widths = [
            table_width * (weight / total_weight)
            for weight in column_weights
        ]

        x = self.margin
        y = self.y

        self.canvas.setLineWidth(0.5)

        # Header row
        self.canvas.setFont("Helvetica-Bold", 8)

        current_x = x

        for header, col_width in zip(headers, column_widths):

            self.canvas.setFillColor(TABLE_HEADER_BACKGROUND)

            self.canvas.rect(
                current_x,
                y - header_height,
                col_width,
                header_height,
                fill=1
            )

            self.canvas.setFillColor(TABLE_HEADER_TEXT)

            self.canvas.drawCentredString(
                current_x + (col_width / 2),
                y - 13,
                header
            )

            current_x += col_width

        # Body rows
        y -= header_height

        for row in range(rows):

            current_x = x

            # Alternate row colors
            if row % 2 == 0:
                self.canvas.setFillColor(TABLE_ROW_ODD)
            else:
                self.canvas.setFillColor(TABLE_ROW_EVEN)

            for col_index, col_width in enumerate(column_widths):

                self.canvas.rect(
                    current_x,
                    y - row_height,
                    col_width,
                    row_height,
                    fill=1
                )

                field_name = f"table_r{row + 1}_c{col_index + 1}"

                self.canvas.acroForm.textfield(
                    name=field_name,
                    x=current_x + 1,
                    y=y - row_height + 1,
                    width=col_width - 2,
                    height=row_height - 2,
                    borderWidth=0,
                    fillColor=colors.transparent,
                    textColor=colors.black,
                    fontName="Helvetica",
                    fieldFlags="multiline",
                    fontSize=0,
                    forceBorder=False
                )

                current_x += col_width

            y -= row_height
            self.y = y - 10


    def pulled_by_section(self):

        self.space(15)

        # Title
        self.canvas.setFillColor(colors.black)
        self.canvas.setFont("Helvetica-Bold", 10)

        self.canvas.drawString(
            self.margin + 120,
            self.y,
            "Pulled By:"
        )

        # ----- Name -----
        name_x = self.margin + 185

        self.label("Name:", name_x, self.y)

        self.textbox(
            "pulled_by_name",
            name_x + 35,
            self.y - 5,
            width=180
        )

        # ----- Date -----
        date_x = self.page_width - 145

        self.label("Date:", date_x, self.y)

        self.textbox(
            "pulled_by_date",
            date_x + 35,
            self.y - 5,
            width=70
        )

        self.space(25)

        # ----- Signature -----

        self.label("Signature:", self.margin + 120, self.y)

        signature_x = self.margin + 120

        signature_width = self.page_width - self.margin - signature_x

        self.signature_line(
            signature_x,
            self.y - 5,
            signature_width
        )

        self.space(20)


    def save(self):
        self.canvas.save()