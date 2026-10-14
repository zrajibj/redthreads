"""Build a Red Threads host offer letter as a PDF.

Usage: python3 make_offer_letter.py "Full Name" "First name" out.pdf
"""
import sys
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (KeepTogether, ListFlowable, ListItem, Paragraph,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("Serif", FONT_DIR + "DejaVuSerif.ttf"))
pdfmetrics.registerFont(TTFont("Serif-Bold", FONT_DIR + "DejaVuSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sans", FONT_DIR + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Bold", FONT_DIR + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-Bold",
                              italic="Serif", boldItalic="Serif-Bold")

RED = HexColor("#C8102E")
INK = HexColor("#1E1E24")
SLATE = HexColor("#6B6B73")

body = ParagraphStyle("body", fontName="Serif", fontSize=9.6, leading=13.6,
                      textColor=INK, spaceAfter=6, alignment=TA_LEFT)
small = ParagraphStyle("small", parent=body, fontName="Sans", fontSize=8,
                       leading=11, textColor=SLATE, spaceAfter=0)
term_head = ParagraphStyle("termhead", parent=body, fontName="Sans-Bold",
                           fontSize=9, leading=12, spaceAfter=1, textColor=INK,
                           keepWithNext=1)
title = ParagraphStyle("title", parent=body, fontName="Serif-Bold", fontSize=15,
                       leading=19, spaceBefore=4, spaceAfter=8)

BLANK = "____________"


def build(full_name, first_name, out_path):
    doc = SimpleDocTemplate(out_path, pagesize=A4, leftMargin=22 * mm,
                            rightMargin=22 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title=f"Red Threads: Offer to {full_name}",
                            author="Zakaria, Red Threads")
    s = []

    s.append(Paragraph('<font name="Sans-Bold" color="#C8102E" size="13">RED THREADS</font>'
                       '<font name="Sans" color="#6B6B73" size="8">&nbsp;&nbsp;·&nbsp;&nbsp;The base, not the face.</font>',
                       body))
    s.append(Table([[""]], colWidths=[doc.width - 12], rowHeights=[2],
                   style=TableStyle([("LINEABOVE", (0, 0), (-1, 0), 1.2, RED)])))
    s.append(Spacer(1, 8))
    s.append(Paragraph(f"Date: {BLANK}", body))
    s.append(Paragraph(f"To: <b>{full_name}</b><br/>Address: {BLANK}{BLANK}", body))
    s.append(Paragraph("Offer to host Red Threads", title))
    s.append(Paragraph(f"Dear {first_name},", body))
    s.append(Paragraph(
        "Following our proposal, I am pleased to offer you the role of host of Red Threads, "
        "an educational channel on YouTube, Facebook and Instagram that asks why changing the "
        "government changes so little. The lessons stay animated; as host, you are the real "
        "person viewers see behind them. The terms of this offer are set out below.", body))

    terms = [
        ("Role.", "You will appear as host in a short intro after each lesson's opening hook "
         "(about 10 to 15 seconds), an outro setting up the next lesson (about 15 to 20 seconds), "
         "and occasional on-camera pieces such as a channel trailer or replies to viewers, "
         "at most two a month."),
        ("Format.", "Your appearances will be made with a HeyGen avatar of you, with video you "
         "record yourself, or a mix of both. We will choose together after one test recording."),
        ("Start date.", f"{BLANK}, beginning with the test recording for lesson 1."),
        ("Time commitment.", "About 2 hours once to set up (avatar footage, HeyGen's on-camera "
         "consent video and voice), then 15 to 30 minutes per lesson to review the script and "
         "the finished video, about every two weeks. Recording yourself adds 30 to 60 minutes per lesson."),
        ("Compensation.", f"{BLANK}{BLANK} (amount, and whether per lesson or per month), "
         f"payable {BLANK}. Revenue share once the channel is monetized: {BLANK}. "
         f"HeyGen and equipment costs are paid by {BLANK}."),
        ("Use of your likeness and voice.", "Your face, voice and avatar will be used only on "
         "Red Threads channels, only to say scripts you have approved in writing, and in clips cut "
         "from approved videos without changing what you said. They will never be used in ads or "
         "endorsements, to support or attack any party, government or named person, or in any "
         "other project, and will never be sold, lent or given to anyone else."),
        ("Approval rights.", "You see every script before it is recorded or generated and every "
         "finished video before it is published, and you may refuse any line or video without "
         "giving a reason."),
        ("Disclosure.", "Every video that uses your avatar will be labelled as AI-generated, on the "
         "platform and in the description."),
        ("Credit.", f"Each lesson credits you as host on the end card and in the description "
         f"(\"Hosted by {full_name}\"), and the channel's About page names you as host."),
        ("Your right to withdraw.", "You may stop at any time, for any reason, by telling me. "
         "No new videos with your likeness will be made from that day. Your avatar and voice clone "
         f"will be deleted from HeyGen within {BLANK} days, with written confirmation. Videos "
         f"already published will (tick one): <font name='Sans'>&#9744;</font> stay up as they are &nbsp; <font name='Sans'>&#9744;</font> have your "
         f"segments replaced within {BLANK} days."),
        ("Safety.", "The channel never attacks any government or party. A lawyer familiar with "
         "Bangladesh's speech laws will review the channel's approach before the first upload. "
         f"You will appear as (tick one): <font name='Sans'>&#9744;</font> full name &nbsp; <font name='Sans'>&#9744;</font> first name only "
         f"&nbsp; <font name='Sans'>&#9744;</font> no name."),
    ]
    items = [ListItem(Paragraph(f'<font name="Sans-Bold" size="9">{h}</font><br/>{t}', body), leftIndent=16)
             for h, t in terms]
    s.append(ListFlowable(items, bulletType="1", bulletFontName="Sans-Bold",
                          bulletFontSize=9, bulletColor=RED, leftIndent=16))

    s.append(Paragraph(
        f"To accept, please sign below and return a copy to me by {BLANK}. "
        "If anything here doesn't work for you, tell me and we will change it before signing.",
        body))
    s.append(Paragraph("I look forward to working with you.", body))

    sig = [
        [Paragraph("<b>Offered by</b>", body), Paragraph("<b>Accepted by</b>", body)],
        [Paragraph(f"Signature: {BLANK}{BLANK}", body), Paragraph(f"Signature: {BLANK}{BLANK}", body)],
        [Paragraph("Name: Zakaria, for Red Threads", body), Paragraph(f"Name: {full_name}", body)],
        [Paragraph(f"Date: {BLANK}", body), Paragraph(f"Date: {BLANK}", body)],
    ]
    s.append(Spacer(1, 6))
    s.append(KeepTogether(Table(sig, colWidths=[(doc.width - 12) / 2] * 2, style=TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 1), (-1, 1), 12),
    ]))))

    def footer(canvas, d):
        canvas.saveState()
        canvas.setFont("Sans", 7.5)
        canvas.setFillColor(SLATE)
        canvas.drawString(d.leftMargin, 10 * mm, f"Red Threads · Offer to {full_name}")
        canvas.drawRightString(A4[0] - d.rightMargin, 10 * mm, f"Page {d.page}")
        canvas.restoreState()

    doc.build(s, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    build(*sys.argv[1:4])
