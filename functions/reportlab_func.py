import random

from PIL import Image as img
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.doctemplate import SimpleDocTemplate, Spacer
from reportlab.platypus.flowables import Image
from reportlab.platypus.paragraph import Paragraph, ParagraphStyle
from reportlab.platypus.tables import Table, TableStyle


def _addPageNumber(canvas, doc):
    page_num = canvas.getPageNumber()
    text = str(page_num)
    canvas.drawCentredString(300, 30, text)
    canvas.saveState()


def wish_list_func(data_list: list, path):
    file_path = f"wish_list_from_{data_list[0][0]}.pdf"
    font = f"{random.randrange(1, 6)}.ttf"
    color = random.choice(
        [
            colors.palevioletred,
            colors.blue,
            colors.green,
            colors.goldenrod,
            colors.blueviolet,
            colors.royalblue,
            colors.blueviolet,
            colors.darkslategray,
            colors.darkgreen,
        ]
    )
    pdfmetrics.registerFont(TTFont("MyFont", font))
    doc = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        topMargin=50,
        BottomMargin=20,
        leftMargin=20,
        rightMargin=20,
    )
    story = []
    data = []
    if path:
        story.append(Image(path, width=100, height=100))
    story.append(Spacer(20, 20))
    story.append(
        Paragraph(
            f"ХОТЕЛКИ на новый год от {data_list[0][0]}",
            ParagraphStyle(
                name="name",
                fontName="MyFont",
                alignment=TA_CENTER,
                fontSize=22,
                spaceAfter=50,
                textColor=color,
            ),
        )
    )
    for el in data_list:
        im = img.open(el[1])
        im_new = im.crop(
            (
                0,
                ((im.size[1] - 900) // 2),
                im.size[0],
                im.size[1] - ((im.size[1] - 900) // 2),
            )
        )
        im_new.save(el[1], quality=95)
        I = Image(el[1], width=110, height=150)
        des = Paragraph(
            el[2],
            ParagraphStyle(
                name="name",
                fontName="MyFont",
                alignment=TA_CENTER,
                fontSize=18,
                textColor=color,
            ),
        )
        if "нет" in el[3].lower():
            link = Paragraph(
                "Ссылки нет(",
                ParagraphStyle(
                    name="name",
                    fontName="MyFont",
                    alignment=TA_CENTER,
                    fontSize=16,
                    textColor=color,
                ),
            )
        else:
            link = Paragraph(
                f'<link href="{el[3]}">Можно купить здесь</link>',
                ParagraphStyle(
                    name="name",
                    fontName="MyFont",
                    alignment=TA_CENTER,
                    fontSize=16,
                    textColor=color,
                ),
            )
        data.append([[I], des, link])
    tblstyle = TableStyle(
        [
            ("FONT", (0, 0), (2, -1), "MyFont"),
            ("ALIGNMENT", (0, 0), (2, -1), "CENTRE"),
            ("VALIGN", (0, 0), (2, -1), "MIDDLE"),
            ("BOTTOMPADDING", (0, 0), (2, -1), 15),
        ]
    )
    tbl = Table(data)
    tbl.setStyle(tblstyle)
    story.append(tbl)
    doc.build(story, onFirstPage=_addPageNumber, onLaterPages=_addPageNumber)

    return file_path
