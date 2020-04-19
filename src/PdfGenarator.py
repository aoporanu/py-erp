import os

from PIL import Image
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import inch, mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from src.Table import Table, N, S, E, W
from src.pcclass import InventoryDataBase
from fpdf import FPDF, HTMLMixin


db = InventoryDataBase()

L_margin = 0.5 * inch
data = ['No', 'Product', 'Qty', 'Unit Price', 'Amount']
extra = [["", "", "", "", ""]]


class MyFPDF(FPDF, HTMLMixin):
    """ cannot parse table unless I override the FPDF and HTMLMixin classes """

    def footer(self):
        self.set_y(-10)
        self.set_font('Arial', 'I', 8)

        # Add a page number
        page = 'Pagina: ' + str(self.page_no()) + '/{nb}'
        self.cell(0, 10, page, 0, 0, 'C')


def calculate_y(y, lines, offset):
    lines = lines.split('\n')
    multiplier = len(lines)
    new_y = y + (multiplier * offset)
    return new_y


def draw_string(string, canvas_instance, x, y, lead):
    """ draws string on canvas """
    text_object = canvas_instance.beginText()
    text_object.setTextOrigin(x, y)
    text_object.setLeading(lead)
    for i in string.split('\n'):
        if len(i) > 90:
            i = i.split(" ")
            s = len(i) / 4
            wrd = ""
            for w in range(int(3 * s)):
                wrd = wrd + i[w] + " "
            text_object.textLine(wrd)
            wrd = ""
            for w in range(int(3 * s), len(i)):
                wrd = wrd + i[w] + " "
            text_object.textLine(wrd)
        else:
            text_object.textLine(i)
    return canvas_instance.drawText(text_object)


def nir_document(tup_not_for, pur_id, supplier):
    """ called when new products are purchased """
    pdf = MyFPDF('L')
    pdf_w_ = pdf.w / 2
    pdf.set_font_size(6)
    pdf.set_font('helvetica', '', 6)
    pdf.add_page('L')
    details = db.sqldb.get_company_details
    row_height = pdf.font_size + 1
    nir_header(details, pdf, pdf_w_, row_height, supplier)
    pdf.ln(row_height * 6)
    build_nir_header(pdf, row_height)
    pdf.ln(row_height)
    for i in range(len(tup_not_for)):
        build_nir_content_rows(details, i, pdf, row_height, tup_not_for)
        pdf.ln(row_height)
    pdf.output('niruri/NIR-' + pur_id +
               '.pdf', 'F')


def nir_header(details, pdf, pdf_w_, row_height, supplier):
    pdf.cell(pdf_w_, row_height, details['comp_name'], border=0, ln=0, align='left')
    pdf.cell(pdf_w_, row_height, supplier[1], border=0, ln=0, align='R')
    pdf.ln(row_height)
    pdf.cell(pdf_w_, row_height, details['comp_add'], border=0, ln=0, align='left')
    pdf.cell(pdf_w_, row_height, supplier[2], border=0, ln=0, align='R')
    pdf.ln(row_height)
    pdf.cell(pdf_w_, row_height, details['comp_phn'], border=0, ln=0, align='left')
    pdf.cell(pdf_w_, row_height, supplier[3], border=0, ln=0, align='R')


def build_nir_header(pdf, row_height):
    pdf.cell(10, row_height, '#', border=1)
    pdf.cell(25, row_height, 'Denumire', border=1, ln=0, align='C')
    pdf.cell(15, row_height, 'Cantitate', border=1, ln=0, align='C')
    pdf.cell(7, row_height, 'UM', border=1, ln=0, align='C')
    pdf.cell(15, row_height, 'Pret pe UM', border=1, ln=0, align='C')
    pdf.cell(10, row_height, 'Cota TVA', border=1, ln=0, align="C")
    pdf.cell(15, row_height, 'TVA Per UM', border=1, ln=0, align='C')
    pdf.cell(15, row_height, 'Pret cu TVA', border=1, ln=0, align='C')
    pdf.cell(17, row_height, 'Subtotal cu TVA', border=1, ln=0, align='C')


def build_nir_content_rows(details, i, pdf, row_height, tup_not_for):
    total_w_vat = round((float(tup_not_for[i][2]) *
                         (float(details['cgst']) / 100)), 2)
    total_w_vat = str(total_w_vat)
    fara_tva = float(tup_not_for[i][4]) * float(tup_not_for[i][2])
    # total_wo_vat prints only the vat for one UM
    total_wo_vat = (float(tup_not_for[i][2]) * float(tup_not_for[i][4]))
    with_vat = round(float(total_w_vat) * float(total_wo_vat), 2)
    pdf.cell(10, row_height, str(i), border=1)
    pdf.cell(25, row_height, tup_not_for[i][0], border=1)
    pdf.cell(15, row_height, tup_not_for[i][4], border=1)
    pdf.cell(7, row_height, tup_not_for[i][1], border=1)
    pdf.cell(15, row_height, tup_not_for[i][2], border=1)
    pdf.cell(10, row_height, str(details['cgst']), border=1)
    pdf.cell(15, row_height, str(total_w_vat), border=1)
    pdf.cell(15, row_height, str(with_vat), border=1)
    pdf.cell(17, row_height, str(fara_tva), border=1)


def pdf_document(delegate, pic_add, inv_no, company_name, date, company_add,
                 cus_name, cus_add, plist, currency, total_amt, s_g_s_t,
                 c_g_s_t, sub_total, grand_total, discount, bottom_detail):
    """
    this is only used for invoice generation
    """
    try:
        pil = Image.open(pic_add).resize(
            (250, 43), Image.ANTIALIAS).transpose(Image.FLIP_TOP_BOTTOM)
    except IOError:
        pil = Image.new('RGB', (250, 43))
    p = ImageReader(pil)
    c = canvas.Canvas("invoice" + os.sep + "Invoice_" + inv_no + ".pdf", pagesize=A4, bottomup=0)
    c.setViewerPreference("FitWindow", "true")
    c.setFont("Times-Bold", 24)
    c.drawImage(p, 2.5 * inch, 0.5 * inch)
    heading = 2 * inch
    c.drawString(L_margin, heading, company_name)
    c.setFillColor(HexColor('#9558fb'))
    c.setLineWidth(0.1)
    c.rect(5.65 * inch - 15, heading - 20,
           (7.8500000000000005 * inch - 5.65 * inch) + 15, 0.34 * inch, 1, 1)
    c.setFillColor(colors.white)
    c.setFont("Times-Bold", 20)
    c.drawString(5.65 * inch, heading, "Invoice")
    for i in range(4 - len(inv_no)):
        inv_no = "0" + inv_no
    inv_no = "#" + inv_no
    c.drawRightString(7.8500000000000005 * inch - 15, heading, inv_no)
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 11)
    c.drawString(5.65 * inch - 15, (heading + 0.35 * inch), "Invoice Date")
    c.drawRightString(7.8500000000000005 * inch, (heading + 0.35 * inch), date)
    c.setFont("Helvetica", 11)
    c.drawRightString(7.8500000000000005 * inch, (heading + 0.55 * inch),
                      "Delegate name: " + delegate[1])
    c.drawRightString(7.8500000000000005 * inch, (heading + 0.75 * inch),
                      "Delegate #" + delegate[4])
    c.drawRightString(7.8500000000000005 * inch, (heading + 0.95 * inch),
                      "CNP Delegate" + delegate[3])
    draw_string(company_add, c, L_margin, (heading + 0.5 * inch), 15)
    c.setFont("Times-Bold", 15)
    c.drawString(L_margin,
                 calculate_y((heading + 0.5 * inch), company_add, 0.23 * inch),
                 "Bill To :")
    c.setFont("Times-Bold", 16)
    c.drawString(
        L_margin,
        calculate_y(
            (heading + 0.5 * inch), company_add, 0.23 * inch) + 0.3 * inch,
        cus_name)
    hei = calculate_y(
        (heading + 0.5 * inch), company_add, 0.23 * inch) + 0.3 * inch
    c.setFont("Helvetica", 11)
    draw_string(cus_add, c, L_margin, hei + 0.25 * inch, 15)
    ori = (hei + inch, L_margin)
    rowheight = [0.25 * inch]
    columnwidth = [0.35 * inch, 3.5 * inch, 1.1 * inch, 0.9 * inch, 1.5 * inch]
    item = plist
    if len(item) < 11:
        itemmultiply = 10 - len(item)
        item = item + extra * itemmultiply
    s = Table(c,
              ori,
              no_of_rows=len(item) + 1,
              no_of_column=len(item[0]),
              rowheight=rowheight,
              columnwidth=columnwidth)
    for i in range(5):
        if i == 0:
            lining = N + W + S
        elif i == 4:
            lining = N + E + S
        else:
            lining = N + S
        s.modify(0,
                 i,
                 text=data[i],
                 fontcolour=colors.white,
                 bg=HexColor('#9558fb'),
                 bpad=2 * mm,
                 font=("Helvetica", 11),
                 justify='center',
                 lining=lining)
    for i in range(len(item)):
        las = len(item) - 1
        if i == 0:
            lining = N + E + W
        elif i == las:
            lining = S + E + W
        else:
            lining = E + W
        if i % 2 == 0:
            bg = HexColor('#f2ecfd')
        else:
            bg = HexColor('#e8dcff')
        for t in range(len(item[i])):
            if t == 1:
                justify = 'left'
            elif t == 4 or t == 3:
                justify = 'right'
            else:
                justify = 'center'
            s.modify(i + 1,
                     t,
                     text=item[i][t],
                     fontcolour=colors.black,
                     bpad=2 * mm,
                     font=("Helvetica", 11),
                     justify=justify,
                     lining=lining,
                     bg=bg)
    s.Draw()
    tab2_ori = s.Get_Cor(-1, -2)
    x2, y2 = tab2_ori[0][0]
    w2, h2 = tab2_ori[0][1]
    tab2_ori = [x2, y2 + h2 + 0.2 * inch]
    tab2_ori.reverse()
    cw = [0.9 * inch, 0.5 * inch, 1 * inch]
    rh = [0.25 * inch, 0.25 * inch, 0.25 * inch, 0.25 * inch, 0.25 * inch]
    tab = Table(c,
                tab2_ori,
                rowheight=rh,
                columnwidth=cw,
                no_of_rows=5,
                no_of_column=3)
    tab.modify(0,
               0,
               text="Total Amt",
               justify='right',
               bpad=2 * mm,
               font=("Helvetica", 11),
               fontcolour=colors.black)
    tab.modify(1,
               0,
               text="SGST",
               justify='right',
               bpad=2 * mm,
               font=("Helvetica", 11),
               fontcolour=colors.black)
    tab.modify(2,
               0,
               text="CGST",
               justify='right',
               bpad=2 * mm,
               font=("Helvetica", 11),
               fontcolour=colors.black)
    tab.modify(3,
               0,
               text="SubTotal",
               justify='right',
               bpad=2 * mm,
               font=("Helvetica", 11),
               fontcolour=colors.black)
    tab.modify(4,
               0,
               text="Discount",
               justify='right',
               bpad=2 * mm,
               font=("Helvetica", 11),
               fontcolour=colors.black)

    tab.modify(0,
               1,
               text=currency,
               justify='right',
               bpad=2 * mm,
               font=("Helvetica", 11),
               fontcolour=colors.black,
               lining=N + S + W)
    tab.modify(1,
               1,
               text=currency,
               justify='right',
               bpad=2 * mm,
               font=("Helvetica", 11),
               fontcolour=colors.black,
               lining=N + S + W)
    tab.modify(2,
               1,
               text=currency,
               justify='right',
               bpad=2 * mm,
               font=("Helvetica", 11),
               fontcolour=colors.black,
               lining=N + S + W)
    tab.modify(3,
               1,
               text=currency,
               justify='right',
               bpad=2 * mm,
               font=("Helvetica", 11),
               fontcolour=colors.black,
               lining=N + S + W)
    tab.modify(4,
               1,
               text=currency,
               justify='right',
               bpad=2 * mm,
               font=("Helvetica", 11),
               fontcolour=colors.black,
               lining=N + S + W)

    tab.modify(0,
               2,
               text=str(total_amt),
               justify='right',
               bpad=2 * mm,
               font=("Helvetica", 11),
               fontcolour=colors.black,
               rightpadding=5.5 * mm,
               lining=N + S + E)
    tab.modify(1,
               2,
               text=str(s_g_s_t),
               justify='right',
               bpad=2 * mm,
               font=("Helvetica", 11),
               fontcolour=colors.black,
               rightpadding=5.5 * mm,
               lining=N + S + E)
    tab.modify(2,
               2,
               text=str(c_g_s_t),
               justify='right',
               bpad=2 * mm,
               font=("Helvetica", 11),
               fontcolour=colors.black,
               rightpadding=5.5 * mm,
               lining=N + S + E)
    tab.modify(3,
               2,
               text=str(sub_total),
               justify='right',
               bpad=2 * mm,
               font=("Helvetica", 11),
               fontcolour=colors.black,
               rightpadding=5.5 * mm,
               lining=N + S + E)
    tab.modify(4,
               2,
               text=str(discount),
               justify='right',
               bpad=2 * mm,
               font=("Helvetica", 11),
               fontcolour=colors.black,
               rightpadding=5.5 * mm,
               lining=N + S + E)
    tab.Draw()
    c.setFont("Helvetica", 11)
    draw_string(bottom_detail, c, L_margin, y2 + h2 + 0.40909 * inch, 15)
    b = sum(columnwidth) + L_margin
    tab2_ori = tab.Get_Cor(-1, -1)
    x2, y2 = tab2_ori[0][0]
    w2, h2 = tab2_ori[0][1]
    c.setFont('Times-Bold', 19)
    c.setFillColor(HexColor('#9558fb'))
    ju = c.stringWidth("GrandTotal  - " + currency + " " + str(grand_total),
                       'Times-Bold', 19)
    c.rect((x2 + w2 - 15) - ju - 15, y2 + 0.9 * inch, ju + 30, 0.4 * inch, 1,
           1)
    c.setFillColor(colors.white)
    c.drawRightString(x2 + w2 - 15, y2 + 1.2 * inch,
                      "GrandTotal  - " + currency + "  " + str(grand_total))
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 11)
    if len(item) >= 10:
        sign = 11 * inch
    else:
        sign = 9.5 * inch
    c.drawString(L_margin, sign, "Customer Signature")
    c.drawRightString(b - 0.12 * inch, sign, "Signature")
    c.showPage()
    try:
        c.save()
        return True
    except IOError:
        return False
