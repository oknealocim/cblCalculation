import  openpyxl
from pathlib import Path

file_path_to_parse = Path('/home/micolaenko/Downloads/EA_Facility.xlsx')


def get_first_data_row(sheet_content):
    for n in range(1,10):
        print(sheet_content[n][0])


def get_facility_start_data_row(file_stream, sheet_name='Worksheet'):
    book = openpyxl.load_workbook(file_stream)
    sheet = book.active
    for n in range(1, 10):
        if 'Facility:' in sheet[n][0].value:
            return sheet[n][0].value, n + 1


def get_facility_row_data(file_stream, first_row_number_with_data):
    book = openpyxl.load_workbook(file_stream)
    sheet = book.active

    dict_with_values = []
    start_parse_row = first_row_number_with_data[1]
    while True:
        if sheet[start_parse_row][0].value:
            dict_with_values.append([
                str(sheet[start_parse_row][0].value),
                str(sheet[start_parse_row][1].value),
                str(sheet[start_parse_row][5].value)])
            start_parse_row +=1
        else:
            return dict_with_values


# for each_parsed_data in get_facility_row_data(file_path_to_parse, get_facility_start_data_row(file_path_to_parse)):
#     print(each_parsed_data)
