"""
Builds Smart_Parking_Project_Explanation_and_Viva_Guide.docx and converts to PDF.
Full comprehensive guide structured into Part A (Spoken project explanation) and
Part B (Viva question bank with 80+ categorized Q&As, cheat sheets, and strategies).
"""

import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK_DIR = os.path.join(BASE_DIR, "final_report", "work")
FIG_DIR = os.path.join(WORK_DIR, "figures")
TAB_DIR = os.path.join(WORK_DIR, "tables")
FINAL_DIR = os.path.join(BASE_DIR, "final_report")

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=130, right=130):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def add_footer(doc):
    for section in doc.sections:
        footer = section.footer
        p = footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p.text = "Student: Abhishek Jagam | Course: Machine Learning Laboratory | Academic Year: 2026-2027"
        p.runs[0].font.name = "Times New Roman"
        p.runs[0].font.size = Pt(8.5)
        p.runs[0].font.color.rgb = RGBColor(100, 116, 139)

def style_heading(p, text, level=1):
    p.paragraph_format.space_before = Pt(14 if level == 1 else 11)
    p.paragraph_format.space_after = Pt(4 if level == 1 else 3)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.bold = True
    if level == 1:
        run.font.size = Pt(15)
        run.font.color.rgb = RGBColor(15, 23, 42)
    elif level == 2:
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(30, 41, 59)
    else:
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(51, 65, 85)

def add_body_p(doc, text="", space_after=6, bold_prefix=""):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(space_after)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    if bold_prefix:
        r_b = p.add_run(bold_prefix)
        r_b.font.name = "Times New Roman"
        r_b.font.size = Pt(12)
        r_b.font.bold = True
        
    if text:
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(15, 23, 42)
    return p

def add_qa_p(doc, q_num, question, answer):
    """Adds a structured viva question and answer pair."""
    p_q = doc.add_paragraph()
    p_q.paragraph_format.line_spacing = 1.15
    p_q.paragraph_format.space_before = Pt(8)
    p_q.paragraph_format.space_after = Pt(2)
    p_q.paragraph_format.keep_with_next = True
    
    rq_num = p_q.add_run(f"Q{q_num}: ")
    rq_num.font.name = "Times New Roman"
    rq_num.font.size = Pt(11.5)
    rq_num.font.bold = True
    rq_num.font.color.rgb = RGBColor(14, 165, 233)
    
    rq = p_q.add_run(question)
    rq.font.name = "Times New Roman"
    rq.font.size = Pt(11.5)
    rq.font.bold = True
    rq.font.color.rgb = RGBColor(15, 23, 42)
    
    p_a = doc.add_paragraph()
    p_a.paragraph_format.line_spacing = 1.15
    p_a.paragraph_format.space_after = Pt(6)
    p_a.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    ra_lbl = p_a.add_run("Answer: ")
    ra_lbl.font.name = "Times New Roman"
    ra_lbl.font.size = Pt(11)
    ra_lbl.font.bold = True
    ra_lbl.font.color.rgb = RGBColor(5, 150, 105)
    
    ra = p_a.add_run(answer)
    ra.font.name = "Times New Roman"
    ra.font.size = Pt(11)
    ra.font.color.rgb = RGBColor(15, 23, 42)

def add_table_custom(doc, headers, data, caption=""):
    if caption:
        p_cap = doc.add_paragraph()
        p_cap.paragraph_format.space_before = Pt(8)
        p_cap.paragraph_format.space_after = Pt(3)
        p_cap.paragraph_format.keep_with_next = True
        r = p_cap.add_run(caption)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(15, 23, 42)

    table = doc.add_table(rows=len(data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True
    
    hdr_cells = table.rows[0].cells
    for i, h_text in enumerate(headers):
        hdr_cells[i].text = str(h_text)
        set_cell_background(hdr_cells[i], "0F172A")
        set_cell_margins(hdr_cells[i], top=90, bottom=90, left=120, right=120)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.0)
            r.font.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)
            
    for r_idx, row_data in enumerate(data):
        row_cells = table.rows[r_idx + 1].cells
        bg_col = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            row_cells[c_idx].text = str(val)
            set_cell_background(row_cells[c_idx], bg_col)
            set_cell_margins(row_cells[c_idx], top=60, bottom=60, left=120, right=120)
            p = row_cells[c_idx].paragraphs[0]
            val_str = str(val).strip()
            if any(char.isdigit() for char in val_str) and not any(w in val_str.lower() for w in ["oct", "nov", "dec", "http", "doi", "model", "l2", "svm", "bhm", "linear", "tree", "kernel", "neural", "ensemble", "boosting", "baseline"]):
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(8.5)
                r.font.color.rgb = RGBColor(15, 23, 42)

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(4)

def add_figure_custom(doc, img_path, caption="", width=Inches(5.4)):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(2)
        run = p_img.add_run()
        run.add_picture(img_path, width=width)
        
        if caption:
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(6)
            r = p_cap.add_run(caption)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)
            r.font.italic = True
            r.font.color.rgb = RGBColor(51, 65, 85)

print("Helper functions ready for viva guide build.")

