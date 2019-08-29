import os
import xlsxwriter
import datetime as dt

from restFul.util_services.file_service import FileService

class ExcelGeneratorV2:
    __excel_folder_path = 'excel_temp'

    def __init__(self, subject, is_head=True):
        self.page = 1
        self.subject = subject
        self.is_head = is_head
        self.subject_length = 0

        FileService.file_check(self.__excel_folder_path)
        self.xlsx_file_path = os.path.join(self.__excel_folder_path, str(dt.datetime.now().strftime('%Y%m%d%H%M%S')) + subject + '.xlsx')

        self.work_book = xlsxwriter.Workbook(self.xlsx_file_path)
        self.work_sheet = self.work_book.add_worksheet()
        self.work_sheet.set_column(0, 10, 20)

        # header variable
        self.header_key = []        # get data key  [['a_key1',... ], ['b_key1', ... ] ]
        self.header_value = []      # write header value [['a_header1',... ], ['b_header1', ... ] ]
        self.header_option = []     # { header_value[i] : option : value } header_option
        self.sub_heading = None

        # field variable
        self.field_list = []        # [[{},...], [{},...], ...]
        self.field_format = []      # [{}, {}, ... ]
        self.field_count = 0        # len(filed_list) 테이블 갯수
        self.field_distance = 2     #

        self.footer = None

        self.format = {}
        self.__set_format__()

    def get_xlsx_path(self):
        return self.xlsx_file_path

    def __set_format__(self):
        self.format['string'] = self.work_book.add_format({'border': 1, 'align': 'left', 'font_size': 9, 'valign': 'vcenter', 'num_format': '@'})
        self.format['number'] = self.work_book.add_format({'border': 1, 'align': 'left', 'font_size': 9, 'valign': 'vcenter'})
        self.format['won'] = self.work_book.add_format({'border': 1, 'align': 'left', 'font_size': 9, 'num_format': '"₩"#,##0', 'valign': 'vcenter'})
        self.format['cash'] = self.work_book.add_format({'border': 1, 'align': 'left', 'font_size': 9, 'num_format': '#,##0', 'valign': 'vcenter'})
        self.format['percent'] = self.work_book.add_format({'border': 1, 'align': 'left', 'font_size': 9, 'num_format': '0.0"%"', 'valign': 'vcenter'})
        self.format['date'] = self.work_book.add_format({'border':1, 'align':'left', 'font_size': 9, 'num_format': 'yyyy/mm/dd' , 'valign': 'vcenter'})
        self.format['red'] = self.work_book.add_format({'bold': 1, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'font_size': 9, 'fg_color': '#FA5858'})
        self.format['yellow'] = self.work_book.add_format({'bold': 1, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'font_size': 9,
                   'fg_color': '#F3F781'})
        self.format['blue'] = self.work_book.add_format({'bold': 1, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'font_size': 9, 'fg_color': '#5882FA'})
        self.format['none'] = self.work_book.add_format({'bold': 1, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'font_size': 9})
        self.format['default'] = self.work_book.add_format({'bold': 1, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'font_size': 9,
                               'fg_color': '#D9D9D9'})
        self.format['subject'] = self.work_book.add_format({'bold': 1, 'align': 'center', 'valign': 'vcenter', 'font_size': 12})
        self.format['explanation'] = self.work_book.add_format({'align': 'left', 'font_size': 10, 'valign': 'vcenter'})
        self.format['header'] = self.work_book.add_format({'bold': 1, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'font_size': 9, 'fg_color': '#D9D9D9'})
        self.format['cash_yellow'] = self.work_book.add_format({'bold': 1, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'font_size': 9,
                   'fg_color': '#F3F781', 'num_format': '#,##0'})

    def set_page(self, page):
        if not isinstance(page, int):
            print("page is not int")
        self.page = page
        return self.page

    def set_header(self, header_key, header_value):
        if not isinstance(header_key, list):
            print(header_key, "is not list")
        if not isinstance(header_value, list):
            print(header_value, "is not list")

        self.header_value.append(header_value)
        self.header_key.append(header_key)

    def set_header_opt(self, opt):
        if not isinstance(opt, dict):
            print(opt, 'is not dict')
        self.header_option.append(opt)

    def set_sub_heading(self, sub_heading):
        if not isinstance(sub_heading, dict):
            print(sub_heading, 'is not dict')
        self.sub_heading = sub_heading

    def set_footer(self, footer):
        if not isinstance(footer, dict):
            print(footer, 'is not dict')
        self.footer = footer

    # [[{ 'row_header' : 'row_value'}...{}],...[{}]]
    def set_field(self, field_list, field_distance=None):
        if not isinstance(field_list, list):
            print(field_list, "is not list")
        self.field_list.append(field_list)

        if field_distance is not None:
            self.field_distance = field_distance

    def set_field_format(self, format_dict):
        if not isinstance(format_dict, dict):
            print(format_dict, 'is not dict')
        self.field_format.append(format_dict)

    def set_subject_length(self):
        if not self.header_key:
            print(self.header_key, "is empty")

        self.field_count = len(self.field_list)
        cnt = 0
        subject_length = 0
        max_length = 0
        if self.field_count <= self.page:
            for idx in range(self.field_count):
                self.subject_length += len(self.header_key[idx]) + self.field_distance
        else:
            for idx in range(self.field_count):
                cnt += 1
                subject_length += len(self.header_key[idx]) + self.field_distance
                if cnt >= 2:
                    max_length = subject_length if subject_length > max_length else max_length
                    subject_length = 0
                    cnt = 0
            self.subject_length = max_length

        self.subject_length -= self.field_distance

    def write_validation(self):
        if not len(self.field_list) == len(self.field_format) == len(self.header_value) == len(self.header_key):
            return True

    # def row_col_col(self,):
    #     sum_col = 0
    def get_row_merge_val(self, cur_col, row_merge_col, header_max_size):
        col = 0
        for i in range(cur_col, header_max_size):
            if row_merge_col.get(i) is None:
                break
            else:
                col += row_merge_col.get(i)
        return col

    def write_dual_header(self, row, col, header_group, header_opt):
        row_merge = 0
        row_merge_col = {}
        merge = 0
        cur_col = col

        top_header_size = len(header_group[0])
        bottom_header_size = len(header_group[1])

        header_max_size = top_header_size if top_header_size > bottom_header_size else bottom_header_size

        for header_list in header_group:
            for header in header_list:
                header_format = 'header'
                header_option = header_opt.get(header)
                if header_option is not None:
                    if header_option.get('merge') is not None:
                        merge = header_option.get('merge')
                    if header_option.get('row_merge') is not None:
                        row_merge= header_option.get('row_merge')
                    if header_option.get('format') is not None:
                        header_format = header_option.get('format')

                cur_col += self.get_row_merge_val(cur_col, row_merge_col, header_max_size)

                if merge > 0:
                    self.work_sheet.merge_range(row, cur_col, row, cur_col + merge, header, self.format.get(header_format))
                    cur_col += merge
                elif row_merge > 0:
                    self.work_sheet.merge_range(row, cur_col, row + row_merge, cur_col+merge, header, self.format.get(header_format))
                    row_merge_col[cur_col] = 1 if merge < 0 else merge + 1
                else:
                    self.work_sheet.write(row, cur_col, header, self.format.get(header_format))
                merge = 0
                row_merge = 0
                cur_col += 1
            row += 1
            cur_col = col
        return row - 1

    def write_header(self, row, col, header_value, header_opt):
        # merge = merge range values
        merge= None
        for header in header_value:
            header_option = header_opt.get(header)
            if header_option is not None:
                if header_option.get('merge') is not None:
                    merge = header_option.get('merge')
            if merge is not None:
                self.work_sheet.merge_range(row, col, row, col+merge, header, self.format.get('header'))
                col += merge
                merge = None
            else:
                self.work_sheet.write(row, col, header, self.format.get('header'))
            col += 1

    def write_field(self, row, col, header_key, field_data, field_format):
        current_col_num = col
        for row_data in field_data:
            row += 1
            current_col_num = col
            for header in header_key:
                if isinstance(row_data, dict):
                    self.work_sheet.write(row, current_col_num, row_data.get(header), self.format.get(field_format.get(header)))
                else:
                    self.work_sheet.write(row, current_col_num, getattr(row_data, header, None), self.format.get(field_format.get(header)))
                current_col_num += 1

        return row, current_col_num

    def write_sub_heading(self, sub_heading, base_row, base_col):
        if sub_heading is not None:
            merge = sub_heading.get('merge')
            text = sub_heading.get('text')
            self.work_sheet.merge_range(base_row-1, base_col, base_row-1, base_col+merge, text, self.format.get('subject'))
        return

    def write_footer(self, footer_list, base_row, base_col):
        # ex footer_list : [{'option': ... , 'text': .... }]
        if footer_list is None:
            return base_row, base_col

        merge = None
        for footer_column in footer_list:
            footer_format = 'yellow'
            footer_option = footer_column.get('option')
            if footer_option is not None:
                merge = footer_option.get('merge')

                footer_format = footer_option.get('format')
                footer_format = footer_format if footer_format is not None else 'yellow'

            if merge is not None:
                self.work_sheet.merge_range(base_row, base_col, base_row, base_col + merge, footer_column.get('text'), self.format.get(footer_format))
                base_col += merge
                merge = None
            else:
                self.work_sheet.write(base_row, base_col, footer_column.get('text'), self.format.get(footer_format))
            base_col += 1

        return base_row, base_col

    def write_excel(self):
        self.set_subject_length()
        if self.is_head:
            subject_row_num = 1
            self.work_sheet.merge_range(subject_row_num, 0, subject_row_num, self.subject_length - 1, self.subject,
                                        self.format.get('subject'))
            cur_row_num = subject_row_num +2
        else:
            cur_row_num = 0

            # 엑셀 제목 작업
        cur_col_num = 0
        max_row = 0
        max_col = 0

        # 나머지 엑셀 그리기
        for idx in range(self.field_count):

            # 필드당 해야할 작업
            header_key = self.header_key[idx]
            header_value = self.header_value[idx]
            header_option = self.header_option[idx]
            field_obj_list = self.field_list[idx]
            field_format = self.field_format[idx]

            if self.sub_heading is not None:
                self.write_sub_heading(self.sub_heading.get(idx), cur_row_num, cur_col_num)

            if isinstance(header_value[0], list):
                cur_row_num = self.write_dual_header(cur_row_num, cur_col_num, header_value, header_option)
            else:
                self.write_header(cur_row_num, cur_col_num, header_value, header_option)
            tmp_row_num, tmp_col_num = self.write_field(cur_row_num, cur_col_num, header_key, field_obj_list, field_format)

            if self.footer is not None and self.footer.get(idx) is not None:
                tmp_row_num, tmp_col_num = self.write_footer(self.footer.get(idx), tmp_row_num+1, cur_col_num)

            max_row = max_row if max_row > tmp_row_num else tmp_row_num
            max_col = max_col if max_col > tmp_col_num else tmp_col_num

            cur_field = idx + 1
            if cur_field == self.field_count:
                break

            if cur_field % self.page == 0:
                # 0일때 즉 밑으로 내려가야 할 때
                cur_row_num = max_row + self.field_distance + 1
                cur_col_num = 0
                max_col = 0
            else:
                cur_col_num = max_col + self.field_distance

        # 엑셀 종료
        self.work_book.close()