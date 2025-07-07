import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from .number2text import format_number, convert_to_words


def Generate_Salary_Certificate(employee_data):
    buffer = io.BytesIO()
    flowables = []

    ref_style = ParagraphStyle(
        name="RefStyle",
        fontName="Times-Roman",
        fontSize=12,
        leading=20,
        textColor=colors.black,
        alignment=TA_LEFT,
    )

    body_style = ParagraphStyle(
        name="bodyStyle",
        fontName="Times-Roman",
        fontSize=12,
        leading=20,
        textColor=colors.black,
        alignment=TA_JUSTIFY,
    )

    signature_style = ParagraphStyle(
        name="bodyStyle",
        fontName="Times-Roman",
        fontSize=12,
        leading=14,
        textColor=colors.black,
        alignment=TA_JUSTIFY,
    )

    title_style = ParagraphStyle(
        name="TitleStyle",
        fontName="Times-Bold",
        fontSize=14,
        leading=16,
        textColor=colors.black,
        alignment=TA_CENTER,
    )

    if employee_data["company"] == "Prime Pusti Limited":
        company = f"in {employee_data['company']} a concern of Samuda Group || House of T.K. Group"
        ref = f"T.K./PPL & PCL/HR/SALCER/{int(employee_data['reference']):02d}/{employee_data['issue_date'].strftime('%m-%Y')}"

    elif employee_data["company"] == "Prime Cosmetics Limited":
        company = f"in {employee_data['company']} a concern of Samuda Group || House of T.K. Group"
        ref = f"T.K./PPL & PCL/HR/SALCER/{int(employee_data['reference']):02d}/{employee_data['issue_date'].strftime('%m-%Y')}"

    elif employee_data["company"] == "T.K. Food Products Distribution Limited":
        company = f"in {employee_data['company']}"
        ref = f"T.K./TKFPDL/HR/SALCER/{int(employee_data['reference']):02d}/{employee_data['issue_date'].strftime('%m-%Y')}"
    else:
        company = f"at {employee_data['company']} in Super Oil Refinery Limited (a concern of T.K. Group)"
        ref = f'T.K./Cons/HR/SALCER/{int(employee_data["reference"]):02d}/{employee_data["issue_date"].strftime("%m-%Y")}'

    flowables.append(Spacer(1, 15))
    flowables.append(
        Paragraph(
            f"<br/>{ref} <br/> {employee_data['issue_date'].strftime("%d-%b-%Y")} <br/>",
            ref_style,
        )
    )
    flowables.append(Spacer(1, 15))

    header = "<u><br/>TO WHOM IT MAY CONCERN</u>"
    flowables.append(Paragraph(header, title_style))
    flowables.append(Spacer(1, 15))

    introduce_text = f""" 
    <br/>This is to certify that Mr. {employee_data['name']}, 
    Employee ID: {employee_data['emp_id']}, has been working {company}, as {employee_data['designation']}, 
    under the department of {employee_data['department']} since {employee_data['joining_date'].strftime("%d-%b-%Y")}. He is a 
    permanent employee of the company. His monthly salary is as follows: 
    """
    flowables.append(Paragraph(introduce_text, body_style))
    flowables.append(Spacer(1, 15))

    salary_table_info = [
        ["Basic Salary", "Tk.", "{:,.2f}".format(employee_data["Basic Salary"])],
        ["House Rent", "Tk.", "{:,.2f}".format(employee_data["House Rent"])],
        [
            "Conveyance Allowance",
            "Tk.",
            "{:,.2f}".format(employee_data["Conveyance Allowance"]),
        ],
        [
            "Medical Allowance",
            "Tk.",
            "{:,.2f}".format(employee_data["Medical Allowance"]),
        ],
        [
            "Entertainment Allowance",
            "Tk.",
            "{:,.2f}".format(employee_data["Entertainment Allowance"]),
        ],
        ["Gross Salary", "Tk.", f"{employee_data['gross_salary']}.00"],
        [f"Amount in Word: {employee_data['salary_in_words']}", "", " "],
    ]

    if employee_data["cash"] != None:
        salary_table_info.insert(
            6,
            [
                "Cash Salary",
                "Tk.",
                f"{format_number(int(employee_data['cash']))}.00",
            ],
        )

    if employee_data["Car Allowance"] != 0.00:
        salary_table_info.insert(
            7,
            [
                "Car Allowance",
                "Tk.",
                f"{format_number(int(employee_data['Car Allowance']))}.00",
            ],
        )

        salary_table_info.insert(
            8,
            [
                "Total Salary",
                "Tk.",
                f"{format_number(int(employee_data['Car Allowance']) + int(employee_data['total_salary']) + int(employee_data['cash']))}.00",
            ],
        )

        salary_table_info[9] = [
            f"Amount in Word: {convert_to_words(int(employee_data['Car Allowance']) + int(employee_data['total_salary']) + int(employee_data['cash']))} only",
            "",
            " ",
        ]

    col_widths = [3.5 * inch, 0.5 * inch, 2 * inch]
    emp_info_row_heights = [0.4 * inch] * len(salary_table_info)

    table = Table(
        salary_table_info, colWidths=col_widths, rowHeights=emp_info_row_heights
    )

    LIST_STYLE = TableStyle(
        [
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("LINEBEFORE", (2, 0), (2, -1), 0, colors.white),
            ("ALIGN", (1, 0), (-1, -1), "LEFT"),
            ("ALIGN", (-1, 0), (-1, -1), "RIGHT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("FONT", (0, 0), (-1, -1), "Times-Roman"),
            ("FONTSIZE", (0, 0), (-1, -1), 12),
            ("SPAN", (0, -1), (-1, -1)),
            ("FONT", (0, -2), (-1, -2), "Times-Bold"),
            ("FONT", (0, -1), (-1, -1), "Times-Bold"),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.black),
        ]
    )

    table.setStyle(LIST_STYLE)
    flowables.append(table)
    flowables.append(Spacer(1, 15))

    last_para = """
    <b><i>This certificate has been issued as per the request of the aforesaid employee. 
    The Company is in no way responsible for his personal liabilities. </i></b>
    """
    flowables.append(Paragraph(last_para, body_style))
    flowables.append(Spacer(1, 15))

    signature = """<br/><br/><br/>
                <b>
                _________________________<br/>
                Abdullah -Al- Momen Mollah <br/>
                Manager, HR & Admin<br/>
                T.K. Group </b>
                """

    flowables.append(Paragraph(signature, signature_style))
    # Create PDF
    doc = SimpleDocTemplate(buffer, pagesize=A4, bottomMargin=0 * inch)
    doc.build(flowables)

    # Return PDF data
    buffer.seek(0)
    return buffer.getvalue()


def Generate_Salary_Certificate_without_deduction(employee_data):
    buffer = io.BytesIO()
    flowables = []

    ref_style = ParagraphStyle(
        name="RefStyle",
        fontName="Times-Roman",
        fontSize=12,
        leading=20,
        textColor=colors.black,
        alignment=TA_LEFT,
    )

    body_style = ParagraphStyle(
        name="bodyStyle",
        fontName="Times-Roman",
        fontSize=12,
        leading=20,
        textColor=colors.black,
        alignment=TA_JUSTIFY,
    )

    signature_style = ParagraphStyle(
        name="bodyStyle",
        fontName="Times-Roman",
        fontSize=12,
        leading=14,
        textColor=colors.black,
        alignment=TA_JUSTIFY,
    )

    title_style = ParagraphStyle(
        name="TitleStyle",
        fontName="Times-Bold",
        fontSize=14,
        leading=16,
        textColor=colors.black,
        alignment=TA_CENTER,
    )

    if employee_data["company"] == "Prime Pusti Limited":
        company = f"in {employee_data['company']} a concern of Samuda Group || House of T.K. Group"
        ref = f"T.K./PPL & PCL/HR/SALCER/{int(employee_data['reference']):02d}/{employee_data['issue_date'].strftime('%m-%Y')}"

    elif employee_data["company"] == "Prime Cosmetics Limited":
        company = f"in {employee_data['company']} a concern of Samuda Group || House of T.K. Group"
        ref = f"T.K./PPL & PCL/HR/SALCER/{int(employee_data['reference']):02d}/{employee_data['issue_date'].strftime('%m-%Y')}"

    elif employee_data["company"] == "T.K. Food Products Distribution Limited":
        company = f"in {employee_data['company']}"
        ref = f"T.K./TKFPDL/HR/SALCER/{int(employee_data['reference']):02d}/{employee_data['issue_date'].strftime('%m-%Y')}"
    else:
        company = f"at {employee_data['company']} in Super Oil Refinery Limited (a concern of T.K. Group)"
        ref = f'T.K./Cons/HR/SALCER/{int(employee_data["reference"]):02d}/{employee_data["issue_date"].strftime("%m-%Y")}'

    flowables.append(Spacer(1, 15))
    flowables.append(
        Paragraph(
            f"<br/>{ref} <br/> {employee_data['issue_date'].strftime("%d-%b-%Y")} <br/>",
            ref_style,
        )
    )
    flowables.append(Spacer(1, 15))

    header = "<u><br/>TO WHOM IT MAY CONCERN</u>"
    flowables.append(Paragraph(header, title_style))
    flowables.append(Spacer(1, 15))

    introduce_text = f""" 
    <br/>This is to certify that Mr. {employee_data['name']}, 
    Employee ID: {employee_data['emp_id']}, has been working {company}, as {employee_data['designation']}, 
    under the department of {employee_data['department']} since {employee_data['joining_date'].strftime("%d-%b-%Y")}. He is a 
    permanent employee of the company. His monthly salary is as follows: 
    """
    flowables.append(Paragraph(introduce_text, body_style))
    flowables.append(Spacer(1, 15))

    salary_table_info = [
        [
            "Less: Tax",
            "Tk.",
            f"{format_number(int(employee_data['tax']))}.00",
            "Basic Salary",
            "Tk.",
            "{:,.2f}".format(employee_data["Basic Salary"]),
        ],
        [
            "Provident fund",
            "Tk.",
            f"{format_number(int(employee_data['pf']))}.00",
            "House Rent",
            "Tk.",
            "{:,.2f}".format(employee_data["House Rent"]),
        ],
        [
            "Food Consumption",
            "Tk.",
            f"{format_number(int(employee_data['food']))}.00",
            "Conveyance Allowance",
            "Tk.",
            "{:,.2f}".format(employee_data["Conveyance Allowance"]),
        ],
        [
            "Benevolent Fund",
            "Tk.",
            f"{format_number(int(employee_data['bf']))}.00",
            "Medical Allowance",
            "Tk.",
            "{:,.2f}".format(employee_data["Medical Allowance"]),
        ],
        [
            "Loan",
            "Tk.",
            f"{format_number(int(employee_data['loan']))}.00",
            "Entertainment Allowance",
            "Tk.",
            "{:,.2f}".format(employee_data["Entertainment Allowance"]),
        ],
        [
            "Excess Mobile Bill",
            "Tk.",
            f"{format_number(int(employee_data['exceed_mobile']))}.00",
            "",
            "",
            "",
        ],
        [
            "Others",
            "Tk.",
            f"{format_number(int(employee_data['other_deduction']))}.00",
            "",
            "",
            "",
        ],
        [
            "Total deduction",
            "Tk.",
            f"{format_number(int(employee_data['total_deduction']))}.00",
            "Gross Salary",
            "Tk.",
            f"{employee_data['gross_salary']}.00",
        ],
        [f"Amount in Word: {employee_data['salary_in_words']}", "", " "],
    ]

    if employee_data["Car Allowance"] != 0.00:
        salary_table_info.insert(
            8,
            [
                "",
                "",
                "",
                "Car Allowance",
                "Tk.",
                f"{format_number(int(employee_data['Car Allowance']))}.00",
            ],
        )

        salary_table_info.insert(
            9,
            [
                "",
                "",
                "",
                "Total Salary",
                "Tk.",
                f"{format_number(int(employee_data['Car Allowance']) + int(employee_data['total_salary']))}.00",
            ],
        )

        salary_table_info[10] = [
            f"Amount in Word: {convert_to_words(int(employee_data['Car Allowance']) + int(employee_data['total_salary']))} only",
            "",
            " ",
        ]

    col_widths = [
        1.4 * inch,
        0.3 * inch,
        0.9 * inch,
        2 * inch,
        0.3 * inch,
        1 * inch,
    ]
    emp_info_row_heights = [0.4 * inch] * len(salary_table_info)

    table = Table(
        salary_table_info, colWidths=col_widths, rowHeights=emp_info_row_heights
    )

    LIST_STYLE = TableStyle(
        [
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("LINEBEFORE", (2, 0), (2, -1), 0, colors.white),
            ("LINEBEFORE", (5, 0), (5, -1), 0, colors.white),
            ("ALIGN", (1, 0), (-1, -1), "LEFT"),
            ("ALIGN", (-1, 0), (-1, -1), "RIGHT"),
            ("ALIGN", (2, 0), (2, -1), "RIGHT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("FONT", (0, 0), (-1, -1), "Times-Roman"),
            ("FONTSIZE", (0, 0), (-1, -1), 12),
            ("SPAN", (0, -1), (-1, -1)),
            ("FONT", (0, -2), (-1, -2), "Times-Bold"),
            ("FONT", (0, -1), (-1, -1), "Times-Bold"),
            ("FONT", (0, 7), (-1, 7), "Times-Bold"),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.black),
        ]
    )

    table.setStyle(LIST_STYLE)
    flowables.append(table)
    flowables.append(Spacer(1, 15))

    last_para = """
    <b><i>This certificate has been issued as per the request of the aforesaid employee. 
    The Company is in no way responsible for his personal liabilities. </i></b>
    """
    flowables.append(Paragraph(last_para, body_style))
    flowables.append(Spacer(1, 15))

    signature = """<br/><br/><br/>
                <b>
                _________________________<br/>
                Abdullah -Al- Momen Mollah <br/>
                Manager, HR & Admin<br/>
                T.K. Group </b>
                """

    flowables.append(Paragraph(signature, signature_style))
    # Create PDF
    doc = SimpleDocTemplate(buffer, pagesize=A4, bottomMargin=0 * inch)
    doc.build(flowables)

    # Return PDF data
    buffer.seek(0)
    return buffer.getvalue()
