import os
import fitz
import arabic_reshaper
from bidi.algorithm import get_display
from app.file_naming import generate_filename

MARGIN = 50
PAGE_WIDTH = 595
PAGE_HEIGHT = 842
CONTENT_WIDTH = PAGE_WIDTH - MARGIN * 2

COLOR_HEADER_BG = (0.18, 0.35, 0.60)
COLOR_HEADER_TEXT = (1, 1, 1)
COLOR_ROW_ALT = (0.95, 0.97, 1.0)
COLOR_ROW_NORMAL = (1, 1, 1)
COLOR_BORDER = (0.80, 0.80, 0.80)
COLOR_SECTION_TITLE = (0.18, 0.35, 0.60)
COLOR_LABEL = (0.4, 0.4, 0.4)
COLOR_VALUE = (0.1, 0.1, 0.1)
COLOR_TITLE_BAR = (0.12, 0.25, 0.45)

FONT_PATH = os.path.join(os.path.dirname(
    __file__), "..", "fonts", "Amiri-Regular.ttf")
FONT_NAME = "amiri"


def _is_arabic(text: str) -> bool:
    return any("\u0600" <= c <= "\u06FF" for c in str(text))


def _fix_arabic(text: str) -> str:
    """Reshape and apply BiDi algorithm to fix Arabic display."""
    reshaped = arabic_reshaper.reshape(str(text))
    return get_display(reshaped)


def _new_page(doc):
    page = doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)
    return page, MARGIN, 50


def _check_space(doc, pages, page, y, needed=25):
    if y + needed > PAGE_HEIGHT - 40:
        page, _, y = _new_page(doc)
        pages.append(page)
        y = 50
    return page, y


def _draw_rect(page, x, y, w, h, fill, border=None):
    rect = fitz.Rect(x, y, x + w, y + h)
    page.draw_rect(rect, color=border, fill=fill, width=0.5 if border else 0)


def _insert_text_in_rect(page, rect, text, size=9, color=(0, 0, 0),
                         bold=False, is_arab=False):
    """Insert text in a rect, with Arabic reshaping if needed."""
    if is_arab:
        display_text = _fix_arabic(text)
        page.insert_textbox(
            rect, display_text,
            fontsize=size,
            fontfile=FONT_PATH,
            fontname=FONT_NAME,
            color=color,
            align=2  # right align for Arabic
        )
    else:
        font = "hebo" if bold else "helv"
        page.insert_textbox(
            rect, text,
            fontsize=size,
            fontname=font,
            color=color,
            align=0
        )


def _draw_kv(page, y, label, value):
    label_str = str(label)
    value_str = str(value or "")

    label_is_arab = _is_arabic(label_str)
    value_is_arab = _is_arabic(value_str)

    if label_is_arab or value_is_arab:
        # Full width RTL layout: value on left, label on right
        label_rect = fitz.Rect(MARGIN + 160, y, PAGE_WIDTH - MARGIN, y + 16)
        value_rect = fitz.Rect(MARGIN, y, MARGIN + 155, y + 16)
        _insert_text_in_rect(page, label_rect, label_str + ":",
                             size=9, color=COLOR_LABEL,
                             is_arab=label_is_arab)
        _insert_text_in_rect(page, value_rect, value_str,
                             size=9, color=COLOR_VALUE,
                             is_arab=value_is_arab)
    else:
        label_rect = fitz.Rect(MARGIN, y, MARGIN + 155, y + 16)
        value_rect = fitz.Rect(MARGIN + 160, y, PAGE_WIDTH - MARGIN, y + 16)
        _insert_text_in_rect(page, label_rect, label_str + ":",
                             size=9, color=COLOR_LABEL, bold=True)
        _insert_text_in_rect(page, value_rect, value_str,
                             size=9, color=COLOR_VALUE)
    return y + 16


def _draw_section_title(page, y, title):
    _draw_rect(page, MARGIN, y, CONTENT_WIDTH, 20, fill=COLOR_SECTION_TITLE)
    title_is_arab = _is_arabic(title)
    rect = fitz.Rect(MARGIN + 4, y + 2, PAGE_WIDTH - MARGIN - 4, y + 20)
    _insert_text_in_rect(page, rect, title.upper(),
                         size=9, color=(1, 1, 1),
                         bold=True, is_arab=title_is_arab)
    return y + 26


def _draw_table(doc, pages, page, y, rows, col_widths=None):
    if not rows or not isinstance(rows[0], dict):
        return page, y

    headers = list(rows[0].keys())

    if col_widths is None:
        wide_keys = {"description", "service_description",
                     "item_description", "details", "notes"}
        total = CONTENT_WIDTH - 10
        wide_count = sum(1 for h in headers if h.lower() in wide_keys)
        narrow_w = total / (len(headers) + wide_count)
        col_widths = []
        for h in headers:
            if h.lower() in wide_keys:
                col_widths.append(narrow_w * 2)
            else:
                col_widths.append(narrow_w)

    header_h = 18

    # Header row
    page, y = _check_space(doc, pages, page, y, header_h + 5)
    cx = MARGIN
    for h, w in zip(headers, col_widths):
        _draw_rect(page, cx, y, w, header_h,
                   fill=COLOR_HEADER_BG, border=COLOR_BORDER)
        rect = fitz.Rect(cx + 2, y + 2, cx + w - 2, y + header_h - 2)
        header_label = h.replace("_", " ").title()
        page.insert_textbox(
            rect, header_label,
            fontsize=8,
            fontname="hebo",
            color=COLOR_HEADER_TEXT,
            align=1  # center
        )
        cx += w
    y += header_h

    # Data rows
    for i, r in enumerate(rows):
        row_h = 18
        for h, w in zip(headers, col_widths):
            cell_val = str(r.get(h, "") or "")
            chars_per_line = max(1, int((w - 8) / 5.5))
            lines = max(1, -(-len(cell_val) // chars_per_line))
            cell_h = max(18, lines * 13 + 6)
            row_h = max(row_h, cell_h)

        page, y = _check_space(doc, pages, page, y, row_h)
        fill = COLOR_ROW_ALT if i % 2 == 0 else COLOR_ROW_NORMAL
        cx = MARGIN

        for h, w in zip(headers, col_widths):
            _draw_rect(page, cx, y, w, row_h, fill=fill, border=COLOR_BORDER)
            cell_val = str(r.get(h, "") or "")
            rect = fitz.Rect(cx + 4, y + 3, cx + w - 4, y + row_h - 3)
            cell_is_arab = _is_arabic(cell_val)

            if cell_is_arab:
                display_val = _fix_arabic(cell_val)
                page.insert_textbox(
                    rect, display_val,
                    fontsize=8,
                    fontfile=FONT_PATH,
                    fontname=FONT_NAME,
                    color=COLOR_VALUE,
                    align=2  # right align
                )
            else:
                page.insert_textbox(
                    rect, cell_val,
                    fontsize=8,
                    fontname="helv",
                    color=COLOR_VALUE,
                    align=0
                )
            cx += w
        y += row_h

    return page, y + 10


def export_to_pdf(data: dict, output_dir: str) -> None:
    for page_data in data.get("pages", [data]):
        doc = fitz.open()
        page = doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)
        pages = [page]
        y = MARGIN

        # Title bar
        doc_type = page_data.get("document_type", "Document")
        _draw_rect(page, 0, 0, PAGE_WIDTH, 45, fill=COLOR_TITLE_BAR)
        title_rect = fitz.Rect(MARGIN, 10, PAGE_WIDTH - MARGIN, 44)
        title_is_arab = _is_arabic(doc_type)
        _insert_text_in_rect(page, title_rect, doc_type.upper(),
                             size=18, color=(1, 1, 1),
                             bold=True, is_arab=title_is_arab)
        y = 65

        for key, value in page_data.items():
            if key == "document_type":
                continue

            label = key.replace("_", " ").title()
            page, y = _check_space(doc, pages, page, y, 30)

            if isinstance(value, list) and value and isinstance(value[0], dict):
                y = _draw_section_title(page, y, label)
                page, y = _draw_table(doc, pages, page, y, value)

            elif isinstance(value, dict):
                y = _draw_section_title(page, y, label)
                for k, v in value.items():
                    page, y = _check_space(doc, pages, page, y, 16)
                    y = _draw_kv(page, y, k.replace("_", " ").title(), v)
                y += 6

            else:
                page, y = _check_space(doc, pages, page, y, 16)
                y = _draw_kv(page, y, label, value)

        path = os.path.join(output_dir, generate_filename(page_data, "pdf"))
        doc.save(path)
        doc.close()
        print(f"PDF exported: {path}")
