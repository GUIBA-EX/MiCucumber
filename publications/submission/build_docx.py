from pathlib import Path
from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Mm, Pt, RGBColor

work=Path(__file__).parent
out=work
import subprocess,tempfile
raw=Path(tempfile.mkdtemp(prefix='micucumber-docx-'))
for key,name in [('manuscript','MiCucumber_revision.md'),('letter','Cover_letter.md'),('esm','Supplementary.md')]:
    subprocess.run(['pandoc','-f','markdown-implicit_figures','-t','docx','--resource-path='+str(work),str(work/name),'-o',str(raw/f'{key}_raw.docx')],check=True)
for key,filename in [('manuscript','MiCucumber_revision.docx'),('letter','Cover_letter.docx'),('esm','Supplementary.docx')]:
    doc=Document(raw/f'{key}_raw.docx')
    doc.core_properties.author='Fei Xia'
    doc.core_properties.title=next(p.text for p in doc.paragraphs if p.style.name=='Heading 1')
    for s in doc.styles:
        if s.type not in (WD_STYLE_TYPE.PARAGRAPH,WD_STYLE_TYPE.CHARACTER):
            continue
        s.font.name='Times New Roman'
        s.font.size=Pt(10)
        s.font.color.rgb=RGBColor(0,0,0)
        prop=s.element.get_or_add_rPr()
        fonts=prop.find(qn('w:rFonts'))
        if fonts is not None:
            for k in list(fonts.attrib):
                if 'Theme' in k: del fonts.attrib[k]
            for k in ('ascii','hAnsi','eastAsia','cs'):
                fonts.set(qn('w:'+k),'Times New Roman')
    normal=doc.styles['Normal']
    normal.paragraph_format.line_spacing=1.2
    normal.paragraph_format.space_after=Pt(6)
    for level in range(1,4):
        s=doc.styles[f'Heading {level}']
        s.font.bold=True
        s.paragraph_format.space_before=Pt(12 if level<=2 else 7)
        s.paragraph_format.space_after=Pt(4)
    title=doc.styles['Title']
    title.font.size=Pt(14)
    title.font.bold=True
    title.paragraph_format.space_after=Pt(8)
    first=next(p for p in doc.paragraphs if p.style.name=='Heading 1')
    first.style=title
    for section in doc.sections:
        section.page_width=Mm(210)
        section.page_height=Mm(297)
        section.left_margin=Mm(18)
        section.right_margin=Mm(18)
        section.top_margin=Mm(20)
        section.bottom_margin=Mm(20)
        section.footer_distance=Mm(10)
        if key!='letter':
            p=section.footer.paragraphs[0]
            p.alignment=WD_ALIGN_PARAGRAPH.RIGHT
            field_start=OxmlElement('w:fldChar')
            field_start.set(qn('w:fldCharType'),'begin')
            p.add_run()._r.append(field_start)
            page_instruction=OxmlElement('w:instrText')
            page_instruction.text=' PAGE '
            page_instruction.set(qn('xml:space'),'preserve')
            p.add_run()._r.append(page_instruction)
            field_separator=OxmlElement('w:fldChar')
            field_separator.set(qn('w:fldCharType'),'separate')
            p.add_run()._r.append(field_separator)
            p.add_run('1')
            field_end=OxmlElement('w:fldChar')
            field_end.set(qn('w:fldCharType'),'end')
            p.add_run()._r.append(field_end)
        if key=='manuscript':
            n=OxmlElement('w:lnNumType')
            for a,b in [('countBy','1'),('distance','165'),('restart','continuous')]:
                n.set(qn('w:'+a),b)
            section._sectPr.insert_element_before(n,'w:pgNumType','w:cols')
    for p in doc.paragraphs:
        if p._p.xpath('.//w:drawing'):
            p.alignment=WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.keep_with_next=True
        elif p.text.startswith(('Table 1.','Table 2.','Table 3.')):
            p.paragraph_format.keep_with_next=True
        if p.text.startswith('Fig. '):
            p.paragraph_format.keep_together=True
        if p.style.name=='Heading 3':
            # Pandoc maps level-3 headings under level-2 sections.
            p.paragraph_format.keep_with_next=True
    if key=='manuscript':
        first_shape=doc.inline_shapes[0]
        first_shape.width=Mm(174)
        first_shape.height=Mm(174*297/210)
        image_paragraph=next(p for p in doc.paragraphs if p._p.xpath('.//w:drawing'))
        image_paragraph.paragraph_format.page_break_before=True
        image_paragraph.paragraph_format.keep_with_next=False
        image_paragraph.paragraph_format.space_before=Pt(0)
        image_paragraph.paragraph_format.space_after=Pt(0)
        caption=next(p for p in doc.paragraphs if p.text.startswith('Fig. 1'))
        caption.paragraph_format.page_break_before=True
    for table_index, (table, widths) in enumerate(zip(doc.tables, ([20,26,67,18,19,24],[38,15,25,25,27,15,29],[22,24,34,37,57]))):
        table.autofit=False
        for col, width in zip(table.columns,widths):
            col.width=Mm(width)
            for cell in col.cells:
                cell.width=Mm(width)
        header=OxmlElement('w:tblHeader')
        table.rows[0]._tr.get_or_add_trPr().append(header)
        for i,row in enumerate(table.rows):
            cant_split=OxmlElement('w:cantSplit')
            row._tr.get_or_add_trPr().append(cant_split)
            for column_index, cell in enumerate(row.cells):
                if table_index == 0 and column_index == 2:
                    cell._tc.get_or_add_tcPr().append(OxmlElement('w:noWrap'))
                for p in cell.paragraphs:
                    p.paragraph_format.space_before=Pt(1)
                    p.paragraph_format.space_after=Pt(2)
                    p.paragraph_format.line_spacing=1.0
                    p.paragraph_format.keep_with_next=i < len(table.rows)-1
    dest=(work if key=='esm' else out)/filename
    doc.save(dest)

import shutil
shutil.rmtree(raw)
