# from datetime import datetime
# from django.db import connection
# from django.http import HttpResponse
# from openpyxl import Workbook
# from openpyxl.styles import Font, Alignment, Border, Side
# from openpyxl.utils import get_column_letter, column_index_from_string
# from ..models import TreePlant
# from ...accounts.models import Department
#
#
# class AgriculturalWithProfitSheet:
#     def __init__(self, obj=None,  start=None, end=None):
#         self.start_date = start
#         self.end_date = end
#         self.tree_type = obj
#
#     def generate_agricultural_wit_profit_report(self):
#         now = datetime.now()
#         response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#         response['Content-Disposition'] = f"attachment; filename=report-{now.strftime('%d-%m-%Y')}.xlsx"
#         wb = Workbook()
#         sheet = wb.active
#
#         align = Alignment(wrapText=True, horizontal='center', vertical='center')
#         sheet.merge_cells('A1:U1')
#         sheet.column_dimensions['A'].width = 5
#         sheet.column_dimensions['B'].width = 35
#         sheet.column_dimensions['C'].width = 14
#         sheet.column_dimensions['G'].width = 12
#         sheet.row_dimensions[1].height = 45  # height size in the first row
#
#         if self.start_date[:4] == self.end_date[:4]:
#             year = f'{self.start_date[:4]}'
#         else:
#             year = f'{self.start_date[:4]}-{self.end_date[:4]}'
#
#         title = sheet['A1']
#         title.value = f"Ўрмон хўжалиги давлат қўмитаси тизимидаги ўрмон хўжаликларида " \
#                       f"{year} йилда экиладиган қишлоқ хўжалиги " \
#                       f"экинларидан {self.tree_type.name} экинларини экиш ва махсулотларини " \
#                       f"етиштириш тўғрисида тезкор маълумот"
#         title.alignment = align
#         title.font = Font(name='Times New Roman', bold=True, size=15)
#         sheet.merge_cells('A2:A4')
#         sheet.merge_cells('B2:B4')
#         sheet.merge_cells('C2:C4')
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
#         indicator_name = sheet.cell(column=3, row=2, value='Курсаткич-лар')
#         indicator_name.alignment = align
#         indicator_name.font = Font(name='Times New Roman', bold=True, size=12)
#
#         sheet.merge_cells('D2:F3')
#         cereals_title = sheet.cell(column=4, row=2, value=self.tree_type.name)
#         cereals_title.alignment = align
#         cereals_title.font = Font(name='Times New Roman', bold=True, italic=True, size=12)
#
#         to_title = sheet.cell(column=4, row=4, value='га')
#         to_title.alignment = align
#         to_title.font = Font(name='Times New Roman', bold=True, italic=True, size=11)
#
#         to_centner_title = sheet.cell(column=5, row=4, value='ц/га')
#         to_centner_title.alignment = align
#         to_centner_title.font = Font(name='Times New Roman', italic=True, bold=True, size=11)
#
#         ton_title = sheet.cell(column=6, row=4, value='тн')
#         ton_title.alignment = align
#         ton_title.font = Font(name='Times New Roman', italic=True, bold=True, size=11)
#
#         products = TreePlant.objects.filter(types__pk=self.tree_type.pk)
#         end_column = products.count() * 5 + 6
#         header_title_coordinate = f'G2:{get_column_letter(end_column)}2'
#         sheet.merge_cells(header_title_coordinate)
#         total_ton_title = sheet.cell(column=7, row=2, value='Шу жумладан')
#         total_ton_title.alignment = align
#         total_ton_title.font = Font(name='Times New Roman', italic=True, bold=True, size=13)
#         col_index = 7
#         for index, product in enumerate(products):
#             start_letter = get_column_letter(col_index)
#             end_letter = get_column_letter(col_index + 4)
#             distance = f'{start_letter}3:{end_letter}3'
#             sheet.merge_cells(distance)
#             col = sheet.cell(row=3, column=col_index, value=product.name)
#             col.alignment = align
#             col.font = Font(name='Times New Roman', bold=True, italic=True, size=13)
#
#             units_1 = sheet.cell(row=4, column=col_index, value='Жами майдон, га')
#             units_1.font = Font(name='Times New Roman', bold=True, italic=True, size=11)
#             sheet.column_dimensions[f'{units_1.column_letter}'].width = 12
#             units_1.alignment = align
#
#             units_2 = sheet.cell(row=4, column=col_index + 1, value='ц/га')
#             units_2.font = Font(name='Times New Roman', bold=True, italic=True, size=12)
#             units_2.alignment = align
#
#             units_3 = sheet.cell(row=4, column=col_index + 2, value='тн')
#             units_3.font = Font(name='Times New Roman', bold=True, italic=True, size=12)
#             units_3.alignment = align
#
#             units_4 = sheet.cell(row=4, column=col_index + 3, value='Хосилга киргани')
#             units_4.font = Font(name='Times New Roman', bold=True, italic=True, size=11)
#             sheet.column_dimensions[f'{units_4.column_letter}'].width = 13
#             units_4.alignment = align
#
#             units_5 = sheet.cell(row=4, column=col_index + 4, value='Даромад, млн сўм')
#             units_5.font = Font(name='Times New Roman', bold=True, italic=True, size=11)
#             sheet.column_dimensions[f'{units_5.column_letter}'].width = 12
#             units_5.alignment = align
#             col_index += 5
#
#         departments = Department.objects.filter(status=1).order_by('sort')
#         row_index = 5
#         current_region = 0
#         task_total_each_hectare_row = []
#         task_total_each_ton_row = []
#         task_region_row = []
#         act_region_row = []
#         act_profit_row = []
#         act_total_each_area_row = []
#         task_region_row_letters = []
#         act_region_row_letters = []
#         act_area_row_letters = []
#         act_profit_row_letters = []
#         article_id = 0
#         for index, department_value in enumerate(departments):
#             article_id += 1
#             current_region = department_value.region
#             merge_department_id_row = f'A{row_index}:A{row_index + 2}'
#             sheet.merge_cells(merge_department_id_row)
#
#             merge_department_name_row = f'B{row_index}:B{row_index + 2}'
#             sheet.merge_cells(merge_department_name_row)
#
#             department_id = sheet.cell(column=1, row=row_index, value=article_id)
#             department_id.font = Font(name='Times New Roman', size=12)
#             department_id.alignment = align
#
#             department_name = sheet.cell(column=2, row=row_index, value=department_value.name)
#             department_name.alignment = align
#             department_name.font = Font(name='Times New Roman', size=13)
#
#             department_task = sheet.cell(column=3, row=row_index, value='Топшириқ')
#             department_task.alignment = align
#             department_task.font = Font(name='Times New Roman', italic=True, size=12)
#
#             department_progress = sheet.cell(column=3, row=row_index + 1, value='Амалда')
#             department_progress.alignment = align
#             department_progress.font = Font(name='Times New Roman', italic=True, size=12)
#
#             department_percent = sheet.cell(column=3, row=row_index + 2, value='Фоиз')
#             department_percent.alignment = align
#             department_percent.font = Font(name='Times New Roman', italic=True, size=12)
#
#             agricultural_product = self.agricultural_product_prepare_raw_sql(department=department_value.pk)
#             height_col = 4
#             start_col = 7
#             task_total_hectare_row = '='
#             task_total_ton_row = '='
#             act_total_hectare_row = '='
#             act_total_ton_row = '='
#             for village_index, village_value in enumerate(agricultural_product):
#                 # ---------------------- task -------------------------
#                 task_hectare = sheet.cell(column=start_col, row=row_index, value=village_value[0])
#                 if row_index not in task_total_each_hectare_row:
#                     task_total_each_hectare_row.append(row_index)
#                 task_hectare.alignment = align
#                 task_ton = sheet.cell(column=start_col + 2, row=row_index, value=village_value[1])
#                 task_ton.alignment = align
#                 task_centner_formula_1 = f'=IF({task_ton.column_letter}{row_index}={0},{0},{task_ton.column_letter}{row_index}*10/{task_hectare.column_letter}{row_index})'
#                 task_centner = sheet.cell(column=start_col + 1, row=row_index, value=task_centner_formula_1)
#                 task_centner.alignment = align
#                 task_centner.number_format = '0.0'
#                 sheet.cell(column=start_col + 3, row=row_index)
#                 sheet.cell(column=start_col + 4, row=row_index)
#                 # ---------------------- actual -------------------------
#                 act_hectare = sheet.cell(column=start_col, row=row_index + 1, value=village_value[2])
#                 if row_index + 1 not in task_total_each_ton_row:
#                     task_total_each_ton_row.append(row_index + 1)
#                 if row_index + 1 not in act_total_each_area_row:
#                     act_total_each_area_row.append(row_index + 1)
#                 act_hectare.alignment = align
#                 act_ton = sheet.cell(column=start_col + 2, row=row_index + 1, value=village_value[3])
#                 act_ton.alignment = align
#                 task_centner_formula_2 = f'=IF({act_ton.column_letter}{row_index + 1}={0},{0},{act_ton.column_letter}{row_index + 1}*10/{act_hectare.column_letter}{row_index + 1})'
#                 act_centner = sheet.cell(column=start_col + 1, row=row_index + 1, value=task_centner_formula_2)
#                 act_centner.alignment = align
#                 act_centner.number_format = '0.0'
#                 act_area = sheet.cell(column=start_col + 3, row=row_index + 1, value=village_value[4])
#                 act_area.alignment = align
#                 act_profit = sheet.cell(column=start_col + 4, row=row_index + 1, value=village_value[5])
#                 act_profit.alignment = align
#                 # ---------------------- percent -------------------------
#                 ltr_1 = sheet.cell(column=start_col, row=row_index).column_letter
#                 task_total_hectare_row += f'+{ltr_1}{row_index}'
#                 act_total_hectare_row += f'+{ltr_1}{row_index + 1}'
#                 hectare_percent = f'=IF({ltr_1}{row_index}={0},{0},{ltr_1}{row_index}/{ltr_1}{row_index + 1}*{100})'
#                 percent_hectare = sheet.cell(column=start_col, row=row_index + 2, value=hectare_percent)
#                 percent_hectare.alignment = align
#                 percent_hectare.number_format = '0.0'
#
#                 ltr_2 = sheet.cell(column=start_col + 1, row=row_index).column_letter
#                 centner_percent = f'=IF({ltr_2}{row_index}={0},{0},{ltr_2}{row_index}/{ltr_2}{row_index + 1}*{100})'
#                 task_centner = sheet.cell(column=start_col + 1, row=row_index + 2, value=centner_percent)
#                 task_centner.alignment = align
#                 task_centner.number_format = '0.0'
#
#                 ltr_3 = sheet.cell(column=start_col + 2, row=row_index).column_letter
#                 task_total_ton_row += f'+{ltr_3}{row_index}'
#                 act_total_ton_row += f'+{ltr_3}{row_index + 1}'
#                 ton_percent = f'=IF({ltr_3}{row_index}={0},{0},{ltr_3}{row_index}/{ltr_3}{row_index + 1}*{100})'
#                 percent_ton = sheet.cell(column=start_col + 2, row=row_index + 2, value=ton_percent)
#                 percent_ton.alignment = align
#                 percent_ton.number_format = '0.0'
#
#                 sheet.cell(column=start_col + 3, row=row_index + 2)
#                 sheet.cell(column=start_col + 4, row=row_index + 2)
#                 start_col += 5
#
#             # ----------------------------------- Column 4 TASK hectare ------------------------------
#             task_total_hectare = sheet.cell(column=4, row=row_index, value=task_total_hectare_row)
#             task_total_hectare.alignment = align
#             task_total_hectare.font = Font(name='Times New Roman', size=12)
#             # ----------------------------------- Column 6 TASK ton ------------------------------
#             task_total_ton = sheet.cell(column=6, row=row_index, value=task_total_ton_row)
#             task_total_ton.alignment = align
#             task_total_ton.font = Font(name='Times New Roman', size=12)
#             # ----------------------------------- Column 5 TASK percent ------------------------------
#             task_total_centner_formula = f'=IF({task_total_ton.column_letter}{row_index}={0},{0},{task_total_ton.column_letter}{row_index}*10/{task_total_hectare.column_letter}{row_index})'
#             task_total_centner = sheet.cell(column=5, row=row_index, value=task_total_centner_formula)
#             task_total_centner.alignment = align
#             task_total_centner.font = Font(name='Times New Roman', size=12)
#             task_total_centner.number_format = '0.0'
#
#             # ----------------------------------- Column 4 ACT hectare ------------------------------
#             act_total_hectare = sheet.cell(column=4, row=row_index + 1, value=act_total_hectare_row)
#             act_total_hectare.alignment = align
#             act_total_hectare.font = Font(name='Times New Roman', size=12)
#             # ----------------------------------- Column 6 ACT ton ------------------------------
#             act_total_ton = sheet.cell(column=6, row=row_index + 1, value=act_total_ton_row)
#             act_total_ton.alignment = align
#             act_total_ton.font = Font(name='Times New Roman', size=12)
#             # ----------------------------------- Column 5 ACT percent ------------------------------
#             act_total_centner_formula = f'=IF({act_total_ton.column_letter}{row_index + 1}={0},{0},{act_total_ton.column_letter}{row_index + 1}*10/{act_total_hectare.column_letter}{row_index + 1})'
#             act_total_centner = sheet.cell(column=5, row=row_index + 1, value=act_total_centner_formula)
#             act_total_centner.alignment = align
#             act_total_centner.font = Font(name='Times New Roman', size=12)
#             act_total_centner.number_format = '0.0'
#
#             # ----------------------------------- Column 4 PERCENT hectare ------------------------------
#             letter_1 = sheet.cell(column=4, row=row_index).column_letter
#             percent_hectare_formula = f'=IF({letter_1}{row_index}={0},{0},{letter_1}{row_index + 1}/{letter_1}{row_index}*{100})'
#             percent_total_hectare = sheet.cell(column=4, row=row_index + 2, value=percent_hectare_formula)
#             percent_total_hectare.font = Font(name='Times New Roman', size=12)
#             percent_total_hectare.alignment = align
#             percent_total_hectare.number_format = '0.0'
#             # ----------------------------------- Column 5 PERCENT percent ------------------------------
#             letter_2 = sheet.cell(column=5, row=row_index).column_letter
#             percent_centner_formula = f'=IF({letter_2}{row_index}={0},{0},{letter_2}{row_index + 1}/{letter_2}{row_index}*{100})'
#             percent_total_hectare = sheet.cell(column=5, row=row_index + 2, value=percent_centner_formula)
#             percent_total_hectare.font = Font(name='Times New Roman', size=12)
#             percent_total_hectare.alignment = align
#             percent_total_hectare.number_format = '0.0'
#             # ----------------------------------- Column 6 PERCENT ton ------------------------------
#             letter_3 = sheet.cell(column=6, row=row_index).column_letter
#             percent_ton_formula = f'=IF({letter_3}{row_index}={0},{0},{letter_3}{row_index + 1}/{letter_3}{row_index}*{100})'
#             percent_total_hectare = sheet.cell(column=6, row=row_index + 2, value=percent_ton_formula)
#             percent_total_hectare.font = Font(name='Times New Roman', size=12)
#             percent_total_hectare.alignment = align
#             percent_total_hectare.number_format = '0.0'
#             # ---------------------------------------------------------------------------------------------------
#
#             if index == departments.count() - 1 or current_region.pk != departments[index + 1].region.pk:
#                 article_id = 0
#                 row_index += 3
#                 task_region_row.append(row_index)
#                 act_region_row.append(row_index + 1)
#                 act_profit_row.append(row_index + 1)
#                 # --------------- merge Column A ----------------
#                 merge_department_id_row = f'A{row_index}:A{row_index + 2}'
#                 sheet.merge_cells(merge_department_id_row)
#                 # --------------- merge Column B ----------------
#                 merge_department_name_row = f'B{row_index}:B{row_index + 2}'
#                 sheet.merge_cells(merge_department_name_row)
#                 # --------------- write each Regions ----------------
#                 region_name = sheet.cell(column=2, row=row_index, value=current_region.name)
#                 region_name.alignment = align
#                 region_name.font = Font(name='Times New Roman', bold=True, size=13)
#
#                 region_task = sheet.cell(column=3, row=row_index, value='Топшириқ')
#                 region_task.alignment = align
#                 region_task.font = Font(name='Times New Roman', bold=True, italic=True, size=12)
#
#                 region_progress = sheet.cell(column=3, row=row_index + 1, value='Амалда')
#                 region_progress.alignment = align
#                 region_progress.font = Font(name='Times New Roman', bold=True, italic=True, size=12)
#
#                 region_percent = sheet.cell(column=3, row=row_index + 2, value='Фоиз')
#                 region_percent.alignment = align
#                 region_percent.font = Font(name='Times New Roman', bold=True, italic=True, size=12)
#
#                 column = 7
#                 task_region_row_hectare = '='
#                 task_region_row_ton = '='
#                 act_region_row_hectare = '='
#                 act_region_row_ton = '='
#                 for _, _ in enumerate(agricultural_product):
#                     if get_column_letter(column) not in task_region_row_letters:
#                         task_region_row_letters.append(get_column_letter(column))
#
#                     if get_column_letter(column + 2) not in act_region_row_letters:
#                         act_region_row_letters.append(get_column_letter(column + 2))
#
#                     if get_column_letter(column + 3) not in act_area_row_letters:
#                         act_area_row_letters.append(get_column_letter(column + 3))
#
#                     if get_column_letter(column + 4) not in act_profit_row_letters:
#                         act_profit_row_letters.append(get_column_letter(column + 4))
#
#                     task_hectare_variable_formula = '='
#                     for item in task_total_each_hectare_row:
#                         task_hectare_variable_formula += f'+{get_column_letter(column)}{item}'
#                     task_region_hectare = sheet.cell(column=column, row=row_index, value=task_hectare_variable_formula)
#                     task_region_hectare.alignment = align
#                     task_region_hectare.font = Font(name='Times New Roman', bold=True, size=12)
#                     task_region_row_hectare += f'+{task_region_hectare.column_letter}{row_index}'
#
#                     task_ton_variable_formula = '='
#                     for item in task_total_each_hectare_row:
#                         task_ton_variable_formula += f'+{get_column_letter(column + 2)}{item}'
#                     task_region_ton = sheet.cell(column=column + 2, row=row_index, value=task_ton_variable_formula)
#                     task_region_ton.alignment = align
#                     task_region_ton.font = Font(name='Times New Roman', bold=True, size=12)
#                     task_region_row_ton += f'+{task_region_ton.column_letter}{row_index}'
#                     t_r_p_c_formula = f'=IF({task_region_ton.column_letter}{row_index}={0},{0},{task_region_ton.column_letter}{row_index}*10/{task_region_hectare.column_letter}{row_index})'
#                     task_region_centner = sheet.cell(column=column + 1, row=row_index, value=t_r_p_c_formula)
#                     task_region_centner.font = Font(name='Times New Roman', bold=True, size=12)
#                     task_region_centner.alignment = align
#                     task_region_centner.number_format = '0.0'
#                     # -----------------------------------------------------------------------------------
#                     act_hectare_variable_formula = '='
#                     for item in task_total_each_ton_row:
#                         act_hectare_variable_formula += f'+{get_column_letter(column)}{item}'
#                     act_region_hectare = sheet.cell(column=column, row=row_index+1, value=act_hectare_variable_formula)
#                     act_region_hectare.alignment = align
#                     act_region_hectare.font = Font(name='Times New Roman', bold=True, size=12)
#                     act_region_row_hectare += f'+{act_region_hectare.column_letter}{row_index + 1}'
#
#                     act_ton_variable_formula = '='
#                     for item in task_total_each_ton_row:
#                         act_ton_variable_formula += f'+{get_column_letter(column + 2)}{item}'
#                     act_region_ton = sheet.cell(column=column + 2, row=row_index + 1, value=act_ton_variable_formula)
#                     act_region_ton.alignment = align
#                     act_region_ton.font = Font(name='Times New Roman', bold=True, size=12)
#                     act_region_row_ton += f'+{act_region_ton.column_letter}{row_index + 1}'
#                     a_r_p_c_formula = f'=IF({act_region_ton.column_letter}{row_index + 1}={0},{0},{act_region_ton.column_letter}{row_index + 1}*10/{act_region_hectare.column_letter}{row_index + 1})'
#                     act_region_centner = sheet.cell(column=column + 1, row=row_index + 1, value=a_r_p_c_formula)
#                     act_region_centner.font = Font(name='Times New Roman', bold=True, size=12)
#                     act_region_centner.alignment = align
#                     act_region_centner.number_format = '0.0'
#
#                     act_area_variable_formula = '='
#                     for item in act_total_each_area_row:
#                         act_area_variable_formula += f'+{get_column_letter(column + 3)}{item}'
#                     act_region_profit = sheet.cell(column=column + 3, row=row_index + 1, value=act_area_variable_formula)
#                     act_region_profit.alignment = align
#                     act_region_profit.font = Font(name='Times New Roman', bold=True, size=12)
#
#                     act_profit_variable_formula = '='
#                     for item in act_total_each_area_row:
#                         act_profit_variable_formula += f'+{get_column_letter(column + 4)}{item}'
#                     act_region_profit = sheet.cell(column=column + 4, row=row_index + 1, value=act_profit_variable_formula)
#                     act_region_profit.alignment = align
#                     act_region_profit.font = Font(name='Times New Roman', bold=True, size=12)
#
#                     # -----------------------------------------------------------------------------------
#                     percent_region_hectare_col_formula = f'=IF({get_column_letter(column)}{row_index}={0},{0},{get_column_letter(column)}{row_index}/{get_column_letter(column)}{row_index + 1}*{100})'
#                     percent_region_hectare = sheet.cell(column=column, row=row_index + 2, value=percent_region_hectare_col_formula)
#                     percent_region_hectare.alignment = align
#                     percent_region_hectare.font = Font(name='Times New Roman', bold=True, size=12)
#                     percent_region_hectare.number_format = '0.0'
#
#                     percent_region_centner_col_formula = f'=IF({get_column_letter(column + 1)}{row_index}={0},{0},{get_column_letter(column + 1)}{row_index}/{get_column_letter(column + 1)}{row_index + 1}*{100})'
#                     percent_region_centner = sheet.cell(column=column + 1, row=row_index + 2, value=percent_region_centner_col_formula)
#                     percent_region_centner.alignment = align
#                     percent_region_centner.font = Font(name='Times New Roman', bold=True, size=12)
#                     percent_region_centner.number_format = '0.0'
#
#                     percent_region_ton_col_formula = f'=IF({get_column_letter(column + 2)}{row_index}={0},{0},{get_column_letter(column + 2)}{row_index}/{get_column_letter(column + 2)}{row_index + 1}*{100})'
#                     percent_region_centner = sheet.cell(column=column + 2, row=row_index + 2, value=percent_region_ton_col_formula)
#                     percent_region_centner.alignment = align
#                     percent_region_centner.font = Font(name='Times New Roman', bold=True, size=12)
#                     percent_region_centner.number_format = '0.0'
#
#                     column += 5
#                 task_total_each_hectare_row = []
#                 task_total_each_ton_row = []
#                 act_total_each_area_row = []
#
#                 # --------------------------------- Columns D, E, F Task -----------------------------------
#                 task_region_hectare = sheet.cell(column=height_col, row=row_index, value=task_region_row_hectare)
#                 task_region_hectare.alignment = align
#                 task_region_hectare.font = Font(name='Times New Roman', bold=True, size=12)
#                 task_region_ton = sheet.cell(column=height_col + 2, row=row_index, value=task_region_row_ton)
#                 task_region_ton.alignment = align
#                 task_region_ton.font = Font(name='Times New Roman', bold=True, size=12)
#                 task_region_centner_formula = f'=IF({task_region_ton.column_letter}{row_index}={0},{0},{task_region_ton.column_letter}{row_index}*10/{task_region_hectare.column_letter}{row_index})'
#                 task_region_centner = sheet.cell(column=height_col + 1, row=row_index, value=task_region_centner_formula)
#                 task_region_centner.alignment = align
#                 task_region_centner.font = Font(name='Times New Roman', bold=True, size=12)
#                 task_region_centner.number_format = '0.0'
#                 # ------------------------------- Columns D, E, F InProgress --------------------------------------
#                 act_region_hectare = sheet.cell(column=height_col, row=row_index + 1, value=act_region_row_hectare)
#                 act_region_hectare.alignment = align
#                 act_region_hectare.font = Font(name='Times New Roman', bold=True, size=12)
#                 act_region_ton = sheet.cell(column=height_col + 2, row=row_index + 1, value=act_region_row_ton)
#                 act_region_ton.alignment = align
#                 act_region_ton.font = Font(name='Times New Roman', bold=True, size=12)
#
#                 act_region_centner_formula = f'=IF({act_region_ton.column_letter}{row_index + 1}={0},{0},{act_region_ton.column_letter}{row_index + 1}*10/{act_region_hectare.column_letter}{row_index + 1})'
#                 act_region_centner = sheet.cell(column=height_col + 1, row=row_index + 1, value=act_region_centner_formula)
#                 act_region_centner.alignment = align
#                 act_region_centner.font = Font(name='Times New Roman', bold=True, size=12)
#                 act_region_centner.number_format = '0.0'
#                 # ------------------------------- Columns D, E, F Percent -------------------------------------
#                 ltr_d = sheet.cell(column=4, row=row_index).column_letter
#                 percent_region_hectare_formula = f'=IF({ltr_d}{row_index}={0},{0},{ltr_d}{row_index + 1}/{ltr_d}{row_index}*{100})'
#                 percent_region_hectare = sheet.cell(column=height_col, row=row_index + 2, value=percent_region_hectare_formula)
#                 percent_region_hectare.alignment = align
#                 percent_region_hectare.font = Font(name='Times New Roman', bold=True, size=12)
#                 percent_region_hectare.number_format = '0.0'
#
#                 ltr_e = sheet.cell(column=5, row=row_index).column_letter
#                 percent_region_centner_formula = f'=IF({ltr_e}{row_index}={0},{0},{ltr_e}{row_index + 1}/{ltr_e}{row_index}*{100})'
#                 percent_region_centner = sheet.cell(
#                     column=height_col + 1, row=row_index + 2, value=percent_region_centner_formula)
#                 percent_region_centner.alignment = align
#                 percent_region_centner.font = Font(name='Times New Roman', bold=True, size=12)
#                 percent_region_centner.number_format = '0.0'
#
#                 ltr_f = sheet.cell(column=6, row=row_index).column_letter
#                 percent_region_ton_formula = f'=IF({ltr_f}{row_index}={0},{0},{ltr_f}{row_index + 1}/{ltr_f}{row_index}*{100})'
#                 percent_region_ton = sheet.cell(
#                     column=height_col + 2, row=row_index + 2, value=percent_region_ton_formula)
#                 percent_region_ton.alignment = align
#                 percent_region_ton.font = Font(name='Times New Roman', bold=True, size=12)
#                 percent_region_ton.number_format = '0.0'
#
#             row_index += 3
#
#         for letter in task_region_row_letters:
#             hectare_finish_formula = '='
#             for item in task_region_row:
#                 hectare_finish_formula += f'+{letter}{item}'
#             task_republic_total = sheet.cell(column=column_index_from_string(letter), row=row_index, value=hectare_finish_formula)
#             task_republic_total.alignment = align
#             task_republic_total.font = Font(name='Times New Roman', bold=True, size=12)
#
#             end = sheet.cell(column=column_index_from_string(letter) + 2, row=row_index)
#             formula_1 = f'=IF({end.column_letter}{row_index}={0},{0},{end.column_letter}{row_index}*10/{task_republic_total.column_letter}{row_index})'
#             task_centner_republic_total = sheet.cell(column=column_index_from_string(letter) + 1, row=row_index, value=formula_1)
#             task_centner_republic_total.font = Font(name='Times New Roman', bold=True, size=12)
#             task_centner_republic_total.alignment = align
#             task_centner_republic_total.number_format = '0.0'
#             begin_col_1 = sheet.cell(column=column_index_from_string(letter), row=row_index)
#             end_col_1 = sheet.cell(column=column_index_from_string(letter), row=row_index - 1)
#             republic_task_total_letter = f'=IF({end_col_1.column_letter}{row_index}={0},{0},{end_col_1.column_letter}{row_index + 1}/{begin_col_1.column_letter}{row_index}*{100})'
#             percent_task_republic_total = sheet.cell(column=column_index_from_string(letter), row=row_index + 2, value=republic_task_total_letter)
#             percent_task_republic_total.alignment = align
#             percent_task_republic_total.font = Font(name='Times New Roman', bold=True, size=12)
#             percent_task_republic_total.number_format = '0.0'
#
#             begin_col_2 = sheet.cell(column=column_index_from_string(letter) + 1, row=row_index)
#             end_col_2 = sheet.cell(column=column_index_from_string(letter) + 1, row=row_index - 1)
#             republic_centner_total_letter = f'=IF({end_col_2.column_letter}{row_index}={0},{0},{end_col_2.column_letter}{row_index + 1}/{begin_col_2.column_letter}{row_index}*{100})'
#
#             percent_centner_republic_total = sheet.cell(
#                 column=column_index_from_string(letter) + 1, row=row_index + 2, value=republic_centner_total_letter)
#             percent_centner_republic_total.alignment = align
#             percent_centner_republic_total.font = Font(name='Times New Roman', bold=True, size=12)
#             percent_centner_republic_total.number_format = '0.0'
#
#             begin_col_3 = sheet.cell(column=column_index_from_string(letter) + 2, row=row_index)
#             end_col_3 = sheet.cell(column=column_index_from_string(letter) + 2, row=row_index - 1)
#             republic_ton_total_letter = f'=IF({end_col_3.column_letter}{row_index}={0},{0},{end_col_3.column_letter}{row_index + 1}/{begin_col_3.column_letter}{row_index}*{100})'
#             percent_ton_republic_total = sheet.cell(column=column_index_from_string(letter) + 2, row=row_index + 2, value=republic_ton_total_letter)
#             percent_ton_republic_total.alignment = align
#             percent_ton_republic_total.font = Font(name='Times New Roman', bold=True, size=12)
#             percent_ton_republic_total.number_format = '0.0'
#
#         for letter in task_region_row_letters:
#             act_finish_formula = '='
#             for item in act_region_row:
#                 act_finish_formula += f'+{letter}{item}'
#             act_republic_total = sheet.cell(
#                 column=column_index_from_string(letter), row=row_index + 1, value=act_finish_formula)
#             act_republic_total.font = Font(name='Times New Roman', bold=True, size=12)
#             act_republic_total.alignment = align
#             end = sheet.cell(column=column_index_from_string(letter) + 2, row=row_index + 1)
#             formula_2 = f'=IF({end.column_letter}{row_index + 1}={0},{0},{end.column_letter}{row_index + 1}*10/{act_republic_total.column_letter}{row_index + 1})'
#             act_centner_republic_total = sheet.cell(column=column_index_from_string(letter) + 1, row=row_index + 1,value=formula_2)
#             act_centner_republic_total.font = Font(name='Times New Roman', bold=True, size=12)
#             act_centner_republic_total.alignment = align
#             act_centner_republic_total.number_format = '0.0'
#
#         # ------------------------------------------------------------------------------------
#         for letter in act_region_row_letters:
#             task_ton__finish_formula = '='
#             for item in task_region_row:
#                 task_ton__finish_formula += f'+{letter}{item}'
#             task_republic_total = sheet.cell(
#                 column=column_index_from_string(letter), row=row_index, value=task_ton__finish_formula)
#             task_republic_total.alignment = align
#             task_republic_total.font = Font(name='Times New Roman', bold=True, size=12)
#
#         for letter in act_region_row_letters:
#             act_ton_finish_formula = '='
#             for item in act_region_row:
#                 act_ton_finish_formula += f'+{letter}{item}'
#             act_republic_total = sheet.cell(
#                 column=column_index_from_string(letter), row=row_index + 1, value=act_ton_finish_formula)
#             act_republic_total.alignment = align
#             act_republic_total.font = Font(name='Times New Roman', bold=True, size=12)
#         for letter in act_area_row_letters:
#             act_profit_finish_formula = '='
#             for item in act_region_row:
#                 act_profit_finish_formula += f'+{letter}{item}'
#             act_republic_total = sheet.cell(column=column_index_from_string(letter), row=row_index + 1, value=act_profit_finish_formula)
#             act_republic_total.alignment = align
#             act_republic_total.font = Font(name='Times New Roman', bold=True, size=12)
#         for letter in act_profit_row_letters:
#             act_profit_finish_formula = '='
#             for item in act_region_row:
#                 act_profit_finish_formula += f'+{letter}{item}'
#             act_republic_total = sheet.cell(column=column_index_from_string(letter), row=row_index + 1, value=act_profit_finish_formula)
#             act_republic_total.alignment = align
#             act_republic_total.font = Font(name='Times New Roman', bold=True, size=12)
#
#         merge_republic_row = f'A{row_index}:B{row_index + 2}'
#         sheet.merge_cells(merge_republic_row)
#         total = sheet.cell(row=row_index, column=1, value="Республика бўйича")
#         total.alignment = align
#         total.font = Font(name='Times New Roman', bold=True, size=16)
#
#         total_republic_task = sheet.cell(column=3, row=row_index, value='Топшириқ')
#         total_republic_task.alignment = align
#         total_republic_task.font = Font(name='Times New Roman', bold=True, italic=True, size=12)
#
#         total_republic_progress = sheet.cell(column=3, row=row_index + 1, value='Амалда')
#         total_republic_progress.alignment = align
#         total_republic_progress.font = Font(name='Times New Roman', bold=True, italic=True, size=12)
#
#         total_republic_percent = sheet.cell(column=3, row=row_index + 2, value='Фоиз')
#         total_republic_percent.alignment = align
#         total_republic_percent.font = Font(name='Times New Roman', bold=True, italic=True, size=12)
#
#         all_task_hectare = '='
#         for ltr in task_region_row_letters:
#             all_task_hectare += f'+{ltr}{row_index}'
#         all_hectare_total_republic = sheet.cell(column=4, row=row_index, value=all_task_hectare)
#         all_hectare_total_republic.alignment = align
#         all_hectare_total_republic.font = Font(name='Times New Roman', bold=True, size=12)
#
#         all_ton_hectare = '='
#         for ltr in act_region_row_letters:
#             all_ton_hectare += f'+{ltr}{row_index}'
#         all_ton_total_republic = sheet.cell(column=6, row=row_index, value=all_ton_hectare)
#         all_ton_total_republic.alignment = align
#         all_ton_total_republic.font = Font(name='Times New Roman', bold=True,  size=12)
#
#         task_formula = f'=IF({all_ton_total_republic.column_letter}{row_index}={0},{0},{all_ton_total_republic.column_letter}{row_index}*10/{all_hectare_total_republic.column_letter}{row_index})'
#         all_centner_total_republic = sheet.cell(column=5, row=row_index, value=task_formula)
#         all_centner_total_republic.font = Font(name='Times New Roman', bold=True, size=12)
#         all_centner_total_republic.alignment = align
#         all_centner_total_republic.number_format = '0.0'
#         # -------------------------------------------------------------------------------------
#         all_act_hectare = '='
#         for ltr in task_region_row_letters:
#             all_act_hectare += f'+{ltr}{row_index + 1}'
#         all_act_hectare_total_republic = sheet.cell(column=4, row=row_index + 1, value=all_act_hectare)
#         all_act_hectare_total_republic.alignment = align
#         all_act_hectare_total_republic.font = Font(name='Times New Roman', bold=True, size=12)
#
#         all_centner_hectare = '='
#         for ltr in act_region_row_letters:
#             all_centner_hectare += f'+{ltr}{row_index + 1}'
#         all_act_ton_total_republic = sheet.cell(column=6, row=row_index + 1, value=all_centner_hectare)
#         all_act_ton_total_republic.alignment = align
#         all_act_ton_total_republic.font = Font(name='Times New Roman', bold=True, size=12)
#
#         act_formula = f'=IF({all_act_ton_total_republic.column_letter}{row_index + 1}={0},{0},{all_act_ton_total_republic.column_letter}{row_index + 1}*10/{all_act_hectare_total_republic.column_letter}{row_index + 1})'
#         all_act_centner_total_republic = sheet.cell(column=5, row=row_index + 1, value=act_formula)
#         all_act_centner_total_republic.font = Font(name='Times New Roman', bold=True, size=12)
#         all_act_centner_total_republic.alignment = align
#         all_act_centner_total_republic.number_format = '0.0'
#         # -------------------------------------------------------------------------------------
#         task_begin_cell = sheet.cell(row=row_index, column=4)
#         task_percent = f'=IF({task_begin_cell.column_letter}{row_index}={0},{0},{task_begin_cell.column_letter}{row_index}/{task_begin_cell.column_letter}{row_index + 1}*{100})'
#         finish_task_percent = sheet.cell(column=4, row=row_index + 2, value=task_percent)
#         finish_task_percent.alignment = align
#         finish_task_percent.font = Font(name='Times New Roman', bold=True, size=12)
#         finish_task_percent.number_format = '0.0'
#
#         centner_begin_cell = sheet.cell(row=row_index, column=5)
#         centner_percent = f'=IF({centner_begin_cell.column_letter}{row_index}={0},{0},{centner_begin_cell.column_letter}{row_index}/{centner_begin_cell.column_letter}{row_index + 1}*{100})'
#         finish_centner_percent = sheet.cell(column=5, row=row_index + 2, value=centner_percent)
#         finish_centner_percent.alignment = align
#         finish_centner_percent.font = Font(name='Times New Roman', bold=True, size=12)
#         finish_centner_percent.number_format = '0.0'
#
#         ton_begin_cell = sheet.cell(row=row_index, column=6)
#         ton_percent = f'=IF({ton_begin_cell.column_letter}{row_index}={0},{0},{ton_begin_cell.column_letter}{row_index}/{ton_begin_cell.column_letter}{row_index + 1}*{100})'
#         finish_ton_percent = sheet.cell(column=6, row=row_index + 2, value=ton_percent)
#         finish_ton_percent.alignment = align
#         finish_ton_percent.font = Font(name='Times New Roman', bold=True, size=12)
#         finish_ton_percent.number_format = '0.0'
#
#         def set_border(ws, cell_range):
#             thin = Side(border_style="thin", color="000000")
#             for row in ws[cell_range]:
#                 for cell in row:
#                     cell.border = Border(top=thin, left=thin, right=thin, bottom=thin)
#         set_border(sheet, f'A1:{get_column_letter(sheet.max_column)}{row_index + 2}')
#
#         sheet.freeze_panes = 'A5'
#         wb.save(response)
#         return response
#
#     def agricultural_product_prepare_raw_sql(self, department):
#         start = self.start_date  # date format '2021-01-01'
#         end = self.end_date
#         with connection.cursor() as cursor:
#             query = f"""SELECT
#                         SUM (ap.hectare) hec_plan, SUM (ap.weight) ton_plan,
#                         SUM (aa.hectare) hec_act, SUM (aa.weight) ton_act,
#                         SUM (aa.profit) profit, SUM (aa.yield_area) area
#                         FROM tree_plant tp
#                         LEFT JOIN agriculture_plan ap ON ap.tree_plant_id = tp.id AND ap.department_id = {department} AND ap.date BETWEEN '{start}' AND '{end}'
#                         LEFT JOIN agriculture_actual aa ON aa.tree_plant_id = tp.id AND ap.department_id = {department} AND aa.date BETWEEN '{start}' AND '{end}'
#                         LEFT JOIN tree_plant_types tpt ON tpt.treeplant_id = tp.id
#                         WHERE tpt.treetypes_id = {self.tree_type.pk}
#                         GROUP BY tp.id ORDER BY tp.id"""
#             cursor.execute(query)
#             row = cursor.fetchall()
#             return row
