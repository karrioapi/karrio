import io
import base64
from pathlib import Path
from barcode import Code128
from lxml.etree import fromstring
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw, ImageFont
from karrio.core.utils import DP, request

FONTS_DIR = Path(__file__).resolve().parent / "fonts"
LINE_SEPARATOR = """
"""


def generate_pdf_from_svg_label(content: str, **kwargs):
    template = fromstring(content)
    label = Image.new("L", (1200, 1800), "white")
    draw = ImageDraw.Draw(label)

    font = lambda size=10, bold=False: ImageFont.truetype(
        f"{FONTS_DIR}/Oswald-{'SemiBold' if bold else 'Regular'}.ttf", size
    )

    for element in template:
        tag = element.tag if isinstance(element.tag, str) else ""

        if "g" in tag and element.get("data-type") == "barcode":
            x = int(element.get("x") or 0)
            y = int(element.get("y") or 0)
            width = int(element.get("width") or 0)
            height = int(element.get("height") or 0)
            value = element.get("data-value")
            style_text = element.get("style")
            style = dict(
                [
                    [k.strip() for k in s.split(":")]
                    for s in style_text.split(";")
                    if s != ""
                ]
            )
            bold = "bold" in style_text
            font_size = int(style.get("font-size", "40").replace("px", ""))

            barcode = Code128(value, writer=ImageWriter()).render(
                writer_options=dict(
                    quiet_zone=1.0,
                    module_width=0.5,
                    module_height=30.0,
                    font_size=1,
                    text_distance=0.0,
                    dpi=300,
                ),
                text="",
            )
            barcode.thumbnail((width, height))

            label.paste(barcode, (x, y))

        if "line" in tag:
            fill = element.get("fill")
            width = int(element.get("stroke-width") or 3)
            x1 = int(element.get("x1") or 0)
            y1 = int(element.get("y1") or 0) + 20
            x2 = int(element.get("x2") or 0)
            y2 = int(element.get("y2") or 0) + 20

            draw.line((x1, y1, x2, y2), fill=fill, width=width)

        if "text" in tag:
            x = int(element.get("x") or 0)
            y = int(element.get("y") or 0) - 20
            text = element.text or ""
            fill = element.get("fill")
            style_text = element.get("style")
            style = dict(
                [
                    [k.strip() for k in s.split(":")]
                    for s in style_text.split(";")
                    if s != ""
                ]
            )
            bold = "bold" in style_text
            font_size = int(style.get("font-size", "10").replace("px", ""))

            if element.get("data-type") == "barcode-text":
                for i, char in enumerate(text, 0):
                    draw.text(
                        (x + ((font_size * 0.66) * i), y),
                        char,
                        fill="black",
                        font=font(font_size, False),
                    )
            else:
                draw.text((x, y), text, fill=fill, font=font(font_size, bold))

    return label


def generate_zpl_from_svg_label(content: str, **kwargs) -> str:
    template = fromstring(content)
    concat = lambda *args: LINE_SEPARATOR.join(args)
    doc = "^XA"

    for element in template:
        tag = element.tag if isinstance(element.tag, str) else ""

        if "g" in tag and element.get("data-type") == "barcode":
            x = int(element.get("x") or 0)
            y = int(element.get("y") or 0)
            width = int(element.get("width") or 0)
            height = int(element.get("height") or 0)
            module_width = int(element.get("data-module-width") or 3)
            width_ratio = int(element.get("data-width-ratio") or 2)
            value = element.get("data-value")
            style_text = element.get("style")
            style = dict(
                [
                    [k.strip() for k in s.split(":")]
                    for s in style_text.split(";")
                    if s != ""
                ]
            )
            bold = "bold" in style_text
            font_size = int(style.get("font-size", "40").replace("px", ""))

            doc = concat(
                doc,
                "",
                f"^BY{module_width},{width_ratio},{height}",
                f"^FO{x},{y}^BCN,{height},N,Y,Y,D^FD{value}^FS",
            )

        if "line" in tag:
            stroke = int(element.get("stroke-width") or 3) + 1
            x1 = int(element.get("x1") or 0)
            y1 = int(element.get("y1") or 0) + 20
            x2 = int(element.get("x2") or 0)
            y2 = int(element.get("y2") or 0) + 20

            width = x2 - x1 if x2 != x1 else stroke
            height = y2 - y1 if y2 != y1 else stroke

            doc = concat(
                doc,
                "",
                f"^FO{x1},{y1}^GB{width},{height},{stroke}^FS",
            )

        if "text" in tag:
            x = int(element.get("x") or 0)
            y = int(element.get("y") or 0)
            text = element.text
            style_text = element.get("style")
            style = dict(
                [
                    [k.strip() for k in s.split(":")]
                    for s in style_text.split(";")
                    if s != ""
                ]
            )
            bold = "bold" in style_text
            font_size = int(style.get("font-size", "10").replace("px", ""))

            doc = concat(
                doc,
                "",
                f"^CF{'0' if bold else 'A'},{font_size}",
                f"^FO{x},{y}^FD{text}^FS",
            )

    doc = concat(
        doc,
        "",
        "^XZ",
    )

    return doc


def render_label(label: str, label_type: str, template_type: str, **kwargs) -> str:
    """Return a base64 string from a label."""
    result = io.BytesIO()

    if template_type == "SVG" and label_type == "PDF":
        pdf = generate_pdf_from_svg_label(label, **kwargs)
        pdf.save(result, label_type, resolution=300)

    elif template_type == "ZPL" and label_type == "PDF":
        width, height = kwargs.get("width"), kwargs.get("height")
        data = DP.jsonify(dict(file=label))
        pdf = request(
            url=f"http://api.labelary.com/v1/printers/12dpmm/labels/{width}x{height}/0/",
            data=data,
            headers={"Accept": "application/pdf"},
            decoder=lambda b: base64.encodebytes(b).decode("utf-8"),
        )

        # return it as is because it's already a base64 string.
        return pdf

    elif template_type == "SVG" and label_type == "ZPL":
        doc = generate_zpl_from_svg_label(label, **kwargs)
        result.write(doc.encode("utf-8"))

    else:
        result.write(label.encode("utf-8"))

    return base64.b64encode(result.getvalue()).decode("utf-8")
