# import os
#
# from PIL import Image
# from reportlab.lib import colors
# from reportlab.lib.colors import HexColor
# from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm
# from reportlab.lib.utils import ImageReader
# from reportlab.pdfgen import canvas
# from reportlab.platypus import SimpleDocTemplate
#
# from reportlab.platypus.tables import Table, TableStyle, LongTable
from src.pcclass import InventoryDataBase
from fpdf import FPDF, HTMLMixin


db = InventoryDataBase()

L_margin = 0.5 * inch
data = ['No', 'Product', 'Qty', 'Unit Price', 'Amount']
extra = [["", "", "", "", ""]]
details = db.sqldb.get_company_details


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
    pdf = MyFPDF('L', unit='mm', format='A4')
    pdf_w_ = pdf.w / 3
    pdf.set_font_size(6)
    pdf.set_font('helvetica', '', 6)
    pdf.set_margins(30, 30, 30)
    pdf.add_page('L')
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


def nir_header(comp_details, pdf, pdf_w_, row_height, supplier):
    pdf.cell(pdf_w_, row_height, comp_details['comp_name'], border=0, ln=0, align='left')
    pdf.cell(pdf_w_, row_height, supplier[1], border=0, ln=0, align='R')
    pdf.ln(row_height)
    pdf.cell(pdf_w_, row_height, comp_details['comp_add'], border=0, ln=0, align='left')
    pdf.cell(pdf_w_, row_height, supplier[2], border=0, ln=0, align='R')
    pdf.ln(row_height)
    pdf.cell(pdf_w_, row_height, comp_details['comp_phn'], border=0, ln=0, align='left')
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


def build_nir_content_rows(comp_details, i, pdf, row_height, tup_not_for):
    total_w_vat = round((float(tup_not_for[i][2]) *
                         (float(comp_details['cgst']) / 100)), 2)
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
    pdf.cell(10, row_height, str(comp_details['cgst']), border=1)
    pdf.cell(15, row_height, str(total_w_vat), border=1)
    pdf.cell(15, row_height, str(with_vat), border=1)
    pdf.cell(17, row_height, str(fara_tva), border=1)


def invoice_header(pdf, company_name, date, company_add, cus_name, cus_add, row_height, pdf_w_):
    pdf.set_font_size(10)
    pdf.font_style = 'B'
    pdf.cell(pdf_w_, row_height, company_name, border=0, ln=0, align='left')
    pdf.cell(pdf_w_, row_height, cus_name, border=0, ln=0, align='R')
    pdf.ln(row_height*2)
    pdf.cell(pdf_w_, row_height, company_add, border=0, ln=0, align='L')
    pdf.cell(pdf_w_, row_height, cus_add, border=0, ln=0, align='R')
    pdf.ln(row_height*2)
    pdf.cell(pdf_w_, row_height, '', border=0, ln=0, align='L')
    pdf.cell(pdf_w_, row_height, '', border=0, ln=0, align='R')
    pdf.ln(row_height*5)


def build_invoice_content_rows(details, i, pdf, row_height, plist, currency, total_amt, sub_total, grand_total, discount):
    pdf.set_font('arial', '', 10)
    pdf.cell(15, row_height, txt=str(plist[i][0]), border='L', align='C')
    pdf.cell(105, row_height, txt=plist[i][1] + ' ' + plist[i][5], border='L', align='L')
    pdf.cell(22, row_height, txt=str(plist[i][3]), border='L', align='L')
    pdf.cell(25, row_height, txt=str(int(plist[i][2])), border='L', align='C')
    pdf.cell(15, row_height, txt=str(plist[i][4]), border='LR', align='C')


def pdf_document(delegate, pic_add, inv_no, company_name, date, company_add,
                 cus_name, cus_add, plist, currency, total_amt, s_g_s_t,
                 c_g_s_t, sub_total, grand_total, discount, bottom_detail):
    """
    this is only used for invoice generation
    """
    print(plist)
    pdf = MyFPDF()
    pdf_w_ = pdf.w / 3
    pdf.set_font_size(6)
    pdf.set_font('helvetica', '', 6)
    pdf.add_page()
    pdf.set_margins(2, 2, 2)
    row_height = pdf.font_size * 1.2
    invoice_header(pdf, company_name, date, company_add, cus_name, cus_add, row_height, pdf_w_)
    pdf.cell(pdf.w, row_height * 10, txt='Factura #' + str(inv_no), align='C')
    pdf.ln(row_height * 12)
    invoice_table_header(pdf, row_height)
    for i in range(len(plist)):
        build_invoice_content_rows(details, i, pdf, row_height, plist, currency, total_amt, sub_total, grand_total, discount)
        pdf.ln(row_height)

    pdf.output('invoice/INV-' + inv_no +
               '.pdf', 'F')


def invoice_table_header(pdf, row_height):
    pdf.set_font('arial', 'B', 10)
    pdf.cell(15, row_height, txt='Nr.', border='LTB', align='C')
    pdf.cell(105, row_height, txt='Denumire', border='LTB', align='L')
    pdf.cell(22, row_height, txt='Pret', border='LTB', align='L')
    pdf.cell(25, row_height, txt='Cantitate', border='LTB', align='C')
    pdf.cell(15, row_height, txt='3x4', border='LRTB', align='C')
    pdf.ln(row_height)
    pdf.font_style = ''
