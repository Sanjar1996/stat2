# from datetime import datetime
# from django.db import connection
# from django.http import HttpResponse
# from openpyxl import Workbook
# from openpyxl.styles import Font, Alignment, Border, Side
# from openpyxl.utils import get_column_letter, column_index_from_string
# from ..models import Chorvachilik
# from ...accounts.models import Department
#
#
# class ChorvaByTypeSheet:
#     def __init__(self, obj=None, start=None, end=None):
#         self.start_date = start
#         self.end_date = end
#         self.type_name = obj
#
#     def generate_chorva_by_type_report(self):
#         now = datetime.now()
#         response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#         response['Content-Disposition'] = f"attachment; filename=chorva-topsh-amal-{now.strftime('%d-%m-%Y')}.xlsx"
#         wb = Workbook()
#         sheet = wb.active
#
#         align = Alignment(wrapText=True, horizontal='center', vertical='center')
#         sheet.merge_cells('A1:T1')
#         sheet.column_dimensions['A'].width = 5
#         sheet.column_dimensions['B'].width = 35
#         sheet.column_dimensions['C'].width = 14
#         sheet.row_dimensions[1].height = 45  # height size in the first row
#         year = f'{self.end_date[:4]} йил'
#         title = sheet['A1']
#         title.value = f"Ўрмон хўжалиги давлат қўмитаси тизимидаги-давлат ўрмон хўжалигида " \
#                       f"{self.type_name.name} бўйича {year} йил ҳолатига МАЬЛУМОТ"
#         title.alignment = align
#         title.font = Font(name='Times New Roman', bold=True, size=15)
#         sheet.merge_cells('A2:A4')
#         sheet.merge_cells('B2:B4')
#         sheet.row_dimensions[2].height = 40
#         sheet.row_dimensions[3].height = 60
#         sheet.row_dimensions[4].height = 35
#
#         number = sheet.cell(column=1, row=2, value='№')
#         number.alignment = align
#         number.font = Font(name='Times New Roman', bold=True, size=12)
#
#         department_name = sheet.cell(column=2, row=2, value='Хўжалик номи')
#         department_name.alignment = align
#         department_name.font = Font(name='Times New Roman', bold=True, size=15)
#
#         sheet.merge_cells('C2:E3')
#         cereals_title = sheet.cell(column=3, row=2, value=self.type_name.name)
#         cereals_title.alignment = align
#         cereals_title.font = Font(name='Times New Roman', bold=True, italic=True, size=12)
#
#         to_title = sheet.cell(column=3, row=4, value='Топшириқ')
#         to_title.alignment = align
#         to_title.font = Font(name='Times New Roman', bold=True, italic=True, size=10)
#
#         to_centner_title = sheet.cell(column=4, row=4, value='Амалда')
#         to_centner_title.alignment = align
#         to_centner_title.font = Font(name='Times New Roman', italic=True, bold=True, size=10)
#
#         ton_title = sheet.cell(column=5, row=4, value='%')
#         ton_title.alignment = align
#         ton_title.font = Font(name='Times New Roman', italic=True, bold=True, size=10)
#
#         categories = Chorvachilik.objects.filter(type__pk=self.type_name.pk, parent=None)
#         print("C..........", categories)
#         end_column = categories.count() * 4 + 5
#         header_title_coordinate = f'F2:{get_column_letter(end_column)}2'
#         sheet.merge_cells(header_title_coordinate)
#         total_ton_title = sheet.cell(column=6, row=2, value='Шу жумладан')
#         total_ton_title.alignment = align
#         total_ton_title.font = Font(name='Times New Roman', italic=True, bold=True, size=13)
#         col_index = 6
#         for index, product in enumerate(categories):
#             if product.profit:
#                 start_letter = get_column_letter(col_index)
#                 end_letter = get_column_letter(col_index + 3)
#                 distance = f'{start_letter}3:{end_letter}3'
#                 sheet.merge_cells(distance)
#                 col = sheet.cell(row=3, column=col_index, value=product.name)
#                 col.alignment = align
#                 col.font = Font(name='Times New Roman', bold=True, italic=True, size=13)
#                 units_1 = sheet.cell(row=4, column=col_index, value='Топшириқ')
#                 units_1.font = Font(name='Times New Roman', bold=True, italic=True, size=10)
#                 units_1.alignment = align
#                 units_2 = sheet.cell(row=4, column=col_index + 1, value='Амалда')
#                 units_2.font = Font(name='Times New Roman', bold=True, italic=True, size=10)
#                 units_2.alignment = align
#                 units_3 = sheet.cell(row=4, column=col_index + 2, value='%')
#                 units_3.font = Font(name='Times New Roman', bold=True, italic=True, size=10)
#                 units_3.alignment = align
#                 units_4 = sheet.cell(row=4, column=col_index + 3, value='даромад')
#                 units_4.font = Font(name='Times New Roman', bold=True, italic=True, size=10)
#                 units_4.alignment = align
#                 col_index += 4
#             else:
#                 start_letter = get_column_letter(col_index)
#                 end_letter = get_column_letter(col_index + 2)
#                 distance = f'{start_letter}3:{end_letter}3'
#                 sheet.merge_cells(distance)
#                 col = sheet.cell(row=3, column=col_index, value=product.name)
#                 col.alignment = align
#                 col.font = Font(name='Times New Roman', bold=True, italic=True, size=13)
#                 units_1 = sheet.cell(row=4, column=col_index, value='Топшириқ')
#                 units_1.font = Font(name='Times New Roman', bold=True, italic=True, size=10)
#                 units_1.alignment = align
#                 units_2 = sheet.cell(row=4, column=col_index + 1, value='Амалда')
#                 units_2.font = Font(name='Times New Roman', bold=True, italic=True, size=10)
#                 units_2.alignment = align
#                 units_3 = sheet.cell(row=4, column=col_index + 2, value='%')
#                 units_3.font = Font(name='Times New Roman', bold=True, italic=True, size=10)
#                 units_3.alignment = align
#                 col_index += 3
#
#         departments = Department.objects.filter(status=1).order_by('sort')
#         row_index = 5
#         region = 0
#         region_id = 0
#         region_row = []
#         republic_task_formula = []
#         republic_act_formula = []
#         republic_percent_formula = []
#         republic_profit_formula = []
#         region_tree_index = 0
#         task_each_letter_row = '='
#         act_each_letter_row = '='
#         article_id = 0
#         for index, department_value in enumerate(departments):
#             article_id += 1
#             region = department_value.region
#             department_id = sheet.cell(column=1, row=row_index, value=article_id)
#             department_id.font = Font(name='Times New Roman', size=11)
#             department_id.alignment = align
#             if len(department_value.name) > 32:
#                 name = f' {department_value.name[:29]}...'
#             else:
#                 name = f' {department_value.name}'
#             department_name = sheet.cell(column=2, row=row_index, value=name)
#             # department_name.alignment = align
#             department_name.font = Font(name='Times New Roman', size=11)
#
#             # for c_index, category in enumerate(categories):
#             #     if category.profit:
#             #         pass
#             col_index = 6
#             for cat in categories:
#                 if cat.profit:
#                     """4 column"""
#                     chorva_is_profit = self.chorva_plan_act_is_profit_raw_sql(department=department_value.pk)
#                     for ch_index, ch_value in enumerate(chorva_is_profit):
#                         sheet.cell(column=col_index, row=row_index, value=1)
#                         sheet.cell(column=col_index + 1, row=row_index, value=2)
#                         sheet.cell(column=col_index + 2, row=row_index, value=3)
#                         sheet.cell(column=col_index + 3, row=row_index, value=4)
#                         col_index += 4
#                 else:
#                     """3 column"""
#                     chorva_in_profit = self.chorva_plan_act_in_profit_raw_sql(department=department_value.pk)
#                     for ch_index, ch_value in enumerate(chorva_in_profit):
#                         sheet.cell(column=col_index, row=row_index, value=1)
#                         sheet.cell(column=col_index + 1, row=row_index, value=2)
#                         sheet.cell(column=col_index + 2, row=row_index, value=3)
#                         col_index += 3
#
#                 # for ch_index, ch_value in enumerate(chorvachilik_list):
#         #             task_cell = sheet.cell(column=col_index, row=row_index, value=ch_value[0])
#         #             task_cell.alignment = align
#         #             if task_cell.column_letter not in task_each_letter_row:
#         #                 task_each_letter_row += f'+{task_cell.column_letter}{row_index}'
#         #
#         #             act_cell = sheet.cell(column=col_index + 1, row=row_index, value=ch_value[1])
#         #             act_cell.alignment = align
#         #             if act_cell.column_letter not in act_each_letter_row:
#         #                 act_each_letter_row += f'+{act_cell.column_letter}{row_index}'
#         #
#         #             percent_cell = sheet.cell(column=col_index + 2, row=row_index, value=ch_value[2])
#         #             percent_cell.number_format = '0.0'
#         #             percent_cell.alignment = align
#         #
#         #             profit_cell = sheet.cell(column=col_index + 3, row=row_index, value=ch_value[3])
#         #             profit_cell.alignment = align
#         #
#         #             col_index += 4
#         #
#         #     department_task = sheet.cell(column=3, row=row_index, value=task_each_letter_row)
#         #     department_task.alignment = align
#         #     department_task.font = Font(name='Times New Roman', size=11)
#         #
#         #     department_progress = sheet.cell(column=4, row=row_index, value=act_each_letter_row)
#         #     department_progress.alignment = align
#         #     department_progress.font = Font(name='Times New Roman', size=11)
#         #     percent_formula = f'=IF(D{row_index}={0},{0},D{row_index}/C{row_index}*{100})'
#         #     department_percent = sheet.cell(column=5, row=row_index, value=percent_formula)
#         #     department_percent.alignment = align
#         #     department_percent.number_format = '0.0'
#         #     department_percent.font = Font(name='Times New Roman', size=11)
#         #
#         #     task_each_letter_row = '='
#         #     act_each_letter_row = '='
#         #     if index == departments.count() - 1 or region.pk != departments[index + 1].region.pk:
#         #         article_id = 0
#         #         row_index += 1
#         #         region_row.append(row_index)
#         #         if region_tree_index == 0:
#         #             begin_row = row_index - index - 1
#         #             end_row = row_index - 1
#         #         else:
#         #             begin_row = row_index - (index - region_tree_index)
#         #             end_row = row_index - 1
#         #         region_tree_index = index
#         #         region_name = sheet.cell(column=2, row=row_index, value=region.name)
#         #         region_name.alignment = align
#         #         region_name.font = Font(name='Times New Roman', bold=True, size=12)
#         #
#         #         task_formula = '='
#         #         act_formula = '='
#         #         profit_formula = '='
#         #
#         #         region_task_each_letter_row = '='
#         #         region_act_each_letter_row = '='
#         #         for x in range(0, len(chorvachilik_list)):
#         #             col_index = 6
#         #             for _, _ in enumerate(chorvachilik_list):
#         #                 task_letter = get_column_letter(col_index)
#         #                 if task_letter not in region_task_each_letter_row:
#         #                     region_task_each_letter_row += f'+{task_letter}{row_index}'
#         #                 task_formula += f'SUM({task_letter}{begin_row}:{task_letter}{end_row})'
#         #                 task_region_cell = sheet.cell(column=col_index, row=row_index, value=task_formula)
#         #                 task_region_cell.alignment = align
#         #                 task_region_cell.font = Font(name='Times New Roman', bold=True, size=11)
#         #                 if task_letter not in republic_task_formula:
#         #                     republic_task_formula.append(task_letter)
#         #
#         #                 act_letter = get_column_letter(col_index + 1)
#         #                 if act_letter not in region_act_each_letter_row:
#         #                     region_act_each_letter_row += f'+{act_letter}{row_index}'
#         #                 act_formula += f'SUM({act_letter}{begin_row}:{act_letter}{end_row})'
#         #                 act_region_cell = sheet.cell(column=col_index + 1, row=row_index, value=act_formula)
#         #                 act_region_cell.alignment = align
#         #                 act_region_cell.font = Font(name='Times New Roman', bold=True, size=11)
#         #                 if act_letter not in republic_act_formula:
#         #                     republic_act_formula.append(act_letter)
#         #
#         #                 percent_formula = f'=IF({act_letter}{row_index}={0},{0},{act_letter}{row_index}/{task_letter}{row_index}*{100})'
#         #                 percent_region_cell = sheet.cell(column=col_index + 2, row=row_index, value=percent_formula)
#         #                 percent_region_cell.alignment = align
#         #                 percent_region_cell.number_format = '0.0'
#         #                 percent_region_cell.font = Font(name='Times New Roman', bold=True, size=11)
#         #                 if percent_region_cell.column_letter not in republic_percent_formula:
#         #                     republic_percent_formula.append(percent_region_cell.column_letter)
#         #
#         #                 profit_letter = get_column_letter(col_index + 3)
#         #                 profit_formula += f'SUM({profit_letter}{begin_row}:{profit_letter}{end_row})'
#         #                 profit_region_cell = sheet.cell(column=col_index + 3, row=row_index, value=profit_formula)
#         #                 profit_region_cell.alignment = align
#         #                 profit_region_cell.font = Font(name='Times New Roman', bold=True, size=11)
#         #                 if profit_letter not in republic_profit_formula:
#         #                     republic_profit_formula.append(profit_letter)
#         #
#         #                 col_index += 4
#         #                 task_formula = '='
#         #                 act_formula = '='
#         #                 profit_formula = '='
#         #
#         #         region_task = sheet.cell(column=3, row=row_index, value=region_task_each_letter_row)
#         #         region_task.alignment = align
#         #         region_task.font = Font(name='Times New Roman', bold=True, size=11)
#         #
#         #         region_progress = sheet.cell(column=4, row=row_index, value=region_act_each_letter_row)
#         #         region_progress.alignment = align
#         #         region_progress.font = Font(name='Times New Roman', bold=True, size=11)
#         #
#         #         percent_formula = f'=IF(D{row_index}={0},{0},D{row_index}/C{row_index}*{100})'
#         #         region_percent = sheet.cell(column=5, row=row_index, value=percent_formula)
#         #         region_percent.alignment = align
#         #         region_percent.number_format = '0.0'
#         #         region_percent.font = Font(name='Times New Roman', bold=True, size=11)
#         #
#         #     row_index += 1
#
#         cell_finish_total_title = sheet.cell(row=row_index, column=2, value='Республика бўйича жами')
#         cell_finish_total_title.font = Font(name='Times New Roman', bold=True, size=13)
#         cell_finish_total_title.alignment = align
#
#         total_task_formula = '='
#         for row in region_row:
#             total_task_formula += f'+C{row}'
#         total_act_formula = '='
#         for row in region_row:
#             total_act_formula += f'+D{row}'
#
#         cell_total_task = sheet.cell(row=row_index, column=3, value=total_task_formula)
#         cell_total_task.alignment = align
#         cell_total_task.font = Font(name='Times New Roman', bold=True, size=13)
#
#         cell_total_act = sheet.cell(row=row_index, column=4, value=total_act_formula)
#         cell_total_act.alignment = align
#         cell_total_act.font = Font(name='Times New Roman', bold=True, size=13)
#
#         republic_centner = f'=IF(D{row_index}={0},{0},D{row_index}/C{row_index}*{100})'
#         cell_total_percent = sheet.cell(row=row_index, column=5, value=republic_centner)
#         cell_total_percent.alignment = align
#         cell_total_percent.number_format = '0.0'
#         cell_total_percent.font = Font(name='Times New Roman', bold=True, size=13)
#
#         formula_1 = '='
#         for item in republic_task_formula:
#             for row in region_row:
#                 formula_1 += f'+{item}{row}'
#                 _idx = column_index_from_string(item)
#                 cell_republic_task_formula = sheet.cell(row=row_index, column=_idx, value=formula_1)
#                 cell_republic_task_formula.alignment = align
#                 cell_republic_task_formula.font = Font(name='Times New Roman', bold=True, size=13)
#             formula_1 = '='
#
#         formula_2 = '='
#         for item in republic_act_formula:
#             for row in region_row:
#                 formula_2 += f'+{item}{row}'
#                 _idx = column_index_from_string(item)
#                 cell_republic_act_formula = sheet.cell(row=row_index, column=_idx, value=formula_2)
#                 cell_republic_act_formula.alignment = align
#                 cell_republic_act_formula.font = Font(name='Times New Roman', bold=True, size=13)
#             formula_2 = '='
#
#         formula_3 = '='
#         for item in republic_profit_formula:
#             for row in region_row:
#                 formula_3 += f'+{item}{row}'
#                 _idx = column_index_from_string(item)
#                 cell_republic_profit_formula = sheet.cell(row=row_index, column=_idx, value=formula_3)
#                 cell_republic_profit_formula.alignment = align
#                 cell_republic_profit_formula.font = Font(name='Times New Roman', bold=True, size=13)
#             formula_3 = '='
#
#         formula_4 = '='
#         for item in republic_percent_formula:
#             for row in region_row:
#                 formula_4 += f'+{item}{row}'
#                 col_idx = column_index_from_string(item)
#                 begin = sheet.cell(row=row_index, column=col_idx - 2).column_letter
#                 end = sheet.cell(row=row_index, column=col_idx - 1).column_letter
#                 end_row_formula = f'=IF({end}{row_index}={0},{0},{end}{row_index}/{begin}{row_index}*{100})'
#                 cell_republic_percent_formula = sheet.cell(row=row_index, column=col_idx, value=end_row_formula)
#                 cell_republic_percent_formula.alignment = align
#                 cell_republic_percent_formula.number_format = '0.0'
#                 cell_republic_percent_formula.font = Font(name='Times New Roman', bold=True, size=13)
#             formula_4 = '='
#
#         def set_border(ws, cell_range):
#             thin = Side(border_style="thin", color="000000")
#             for row in ws[cell_range]:
#                 for cell in row:
#                     cell.border = Border(top=thin, left=thin, right=thin, bottom=thin)
#
#         set_border(sheet, f'A1:{get_column_letter(sheet.max_column)}{row_index}')
#         sheet.freeze_panes = 'A5'
#         wb.save(response)
#         return response
#
#     def chorva_plan_act_is_profit_raw_sql(self, department):
#         start = self.start_date  # date format '2021-01-01'
#         end = self.end_date
#         with connection.cursor() as cursor:
#             query = f"""
#             SELECT
#             sum(chp.amount) topshiriq,
#             sum(cha.amount) amalda,
#             sum(cha.amount)*100/sum(chp.amount) foiz,
#             sum(cha.profit) foyda
#             FROM chorvachilik ch
#             LEFT JOIN chorvachilik_plan chp ON chp.chorvachilik_id = ch.id AND chp.department_id = {department} AND chp.date BETWEEN '{start}' AND '{end}'
#             LEFT JOIN chorvachilik_actual cha ON cha.chorvachilik_id = ch.id AND cha.department_id = {department} AND cha.date BETWEEN '{start}' AND '{end}'
#             LEFT JOIN chorvachilik_type cht ON cht.chorvachilik_id = ch.id
#             where cht.chorvachiliktypes_id = {self.type_name.pk}
#             GROUP BY ch.id ORDER BY ch.id
#             """
#             cursor.execute(query)
#             row = cursor.fetchall()
#             return row
#
#     def chorva_plan_act_in_profit_raw_sql(self, department):
#         start = self.start_date  # date format '2021-01-01'
#         end = self.end_date
#         with connection.cursor() as cursor:
#             query = f"""
#             select
#             sum(chp.amount) topshiriq,
#             sum(cha.amount) amalda,
#             sum(cha.amount)*100/sum(chp.amount) foiz
#             from chorvachilik ch
#             left join chorvachilik_plan chp on chp.chorvachilik_id = ch.id
#             and chp.department_id = {department} and chp.date between '{start}' and '{end}'
#             left join chorvachilik_actual cha on cha.chorvachilik_id = ch.id
#             and cha.department_id = {department} and cha.date between '{start}' and '{end}'
#             left join chorvachilik_type cht on cht.chorvachilik_id = ch.id
#             where cht.chorvachiliktypes_id = {self.type_name.pk}
#             group by ch.id order by ch.id
#             """
#             cursor.execute(query)
#             row = cursor.fetchall()
#             return row
