import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from .number2text import format_number, convert_to_words


def Generate_PaySlip(employee_data, pdf_path):
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

    # Header Section
    Header = f"""
    {employee_data['company']} <br/>		
    T.K. Bhaban (2nd Floor), 13, Kawran Bazar, Dhaka-1215. <br/>		
    <u>Salary Slip</u>			
  
    """
    flowables.append(Paragraph(Header, title_style))
    flowables.append(Spacer(1, 15))

    # Employee Name Section

    Employee_Details = f"""
    <br/>	<br/>	Date: {employee_data['issue_date'].strftime('%d-%b-%Y')} <br/>			
    Head of Accounts: Salary & Allowance <br/>			
    Month: {employee_data['salary_month'].strftime('%B %Y')}	<br/>		
    Employee Name: {employee_data['name']} <br/>			
    Designation: {employee_data['designation']} <br/>			
    """
    flowables.append(Paragraph(Employee_Details, body_style))
    flowables.append(Spacer(1, 15))

    # Salary Table Section
    salary_table_info = [
        [
            "Earning",
            "BDT.",
            "Deductions",
            "BDT.",
        ],
        [
            "Basic Salary",
            f"{employee_data['Basic Salary']}.00",
            "Less: Tax",
            "{:,.2f}".format(employee_data["tax"]),
        ],
        [
            "House Rent",
            f"{employee_data['House Rent']}.00",
            "Provident fund",
            "{:,.2f}".format(employee_data["pf"]),
        ],
        [
            "Conveyance Allowance",
            f"{employee_data['Conveyance Allowance']}.00",
            "Food Consumption",
            "{:,.2f}".format(employee_data["food"]),
        ],
        [
            "Medical Allowance",
            f"{employee_data['Medical Allowance']}.00",
            "Benevolent Fund",
            "{:,.2f}".format(employee_data["bf"]),
        ],
        [
            "Entertainment Allowance",
            f"{employee_data['Entertainment Allowance']}.00",
            "Loan",
            "{:,.2f}".format(employee_data["loan"]),
        ],
        [
            "-",
            "-",
            "Excess Mobile Bill",
            "{:,.2f}".format(employee_data["exceed_mobile"]),
        ],
        [
            "-",
            "-",
            "Others",
            "{:,.2f}".format(employee_data["other_deduction"]),
        ],
        [
            "Gross Salary",
            f"{employee_data['gross_salary']}.00",
            "Total deduction",
            "{:,.2f}".format(employee_data["total_deduction"]),
        ],
        [
            "-",
            "-",
            "Net Salary",
            "{:,.2f}".format(round(employee_data["net_salary"])),
        ],
    ]

    # if Statement

    if employee_data["cash_salary"] != None and employee_data["Car Allowance"] != 0.00:
        salary_table_info.insert(
            11,
            [
                "-",
                "-",
                "Cash Salary",
                f"{format_number(int(employee_data['cash_salary']))}.00",
            ],
        )

        salary_table_info.insert(
            12,
            [
                "-",
                "-",
                "Car Allowance",
                f"{format_number(int(employee_data['Car Allowance']))}.00",
            ],
        )

        salary_table_info.insert(
            13,
            [
                "-",
                "-",
                "Total Salary",
                f"{format_number(round(employee_data['Car Allowance']) + round(employee_data['net_salary'])+int(employee_data['cash_salary']))}.00",
            ],
        )

    elif employee_data["cash_salary"] != None:
        salary_table_info.insert(
            11,
            [
                "-",
                "-",
                "Cash_Salary",
                f"{format_number(int(employee_data['cash_salary']))}.00",
            ],
        )

        salary_table_info.insert(
            12,
            [
                "-",
                "-",
                "Total Salary",
                f"{format_number(round(employee_data['cash_salary']) + round(employee_data['net_salary']))}.00",
            ],
        )

    elif employee_data["Car Allowance"] != 0.00:
        salary_table_info.insert(
            11,
            [
                "-",
                "-",
                "Car Allowance",
                f"{format_number(int(employee_data['Car Allowance']))}.00",
            ],
        )

        salary_table_info.insert(
            12,
            [
                "-",
                "-",
                "Total Salary",
                f"{format_number(round(employee_data['Car Allowance']) + round(employee_data['net_salary']))}.00",
            ],
        )

    col_widths = [
        2 * inch,
        1 * inch,
        2 * inch,
        1 * inch,
    ]
    emp_info_row_heights = [0.4 * inch] * len(salary_table_info)

    table = Table(
        salary_table_info, colWidths=col_widths, rowHeights=emp_info_row_heights
    )

    LIST_STYLE = TableStyle(
        [
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("ALIGN", (1, 0), (-1, -1), "LEFT"),  # salary BDT column
            ("ALIGN", (-1, 0), (-1, -1), "RIGHT"),  # deduction BDT column
            ("ALIGN", (1, 0), (1, -1), "RIGHT"),  # deduction text column
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("FONT", (0, 0), (-1, -1), "Times-Roman"),
            ("FONTSIZE", (0, 0), (-1, -1), 12),
            ("FONT", (0, -1), (-1, -1), "Times-Bold"),
            ("FONT", (0, 8), (-1, 8), "Times-Bold"),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.black),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            ("FONT", (0, 0), (-1, 0), "Times-Bold"),
        ]
    )

    table.setStyle(LIST_STYLE)
    flowables.append(table)
    flowables.append(Spacer(1, 15))

    signature = """<br/> <br/>	<br/> <br/>	
    <b>______________ &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
    &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
    &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp____________<br/>
    Prepared by&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
    &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
    &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp Received by</b>
    
    
    """

    flowables.append(Paragraph(signature, signature_style))

    # Create PDF
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, bottomMargin=0 * inch)
    doc.build(flowables)

    # Return PDF data
    return pdf_path
