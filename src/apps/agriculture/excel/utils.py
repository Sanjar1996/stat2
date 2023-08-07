from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment, Font

align = Alignment(wrapText=True, horizontal='center', vertical='center')


def write_header_title(sheet, row, col, size, is_bold, is_italic, value):
    cell = sheet.cell(row=row, column=col, value=value)
    cell.alignment = align
    cell.font = Font(name='Times New Roman', bold=is_bold, italic=is_italic, size=size)
