import ParserXls
from datetime import datetime, timedelta

date_time_format = "%m/%d/%Y %H:%M"
date_format = "%m/%d/%Y"

origData = ParserXls.get_facility_row_data(ParserXls.file_path_to_parse, ParserXls.get_facility_start_data_row(
    ParserXls.file_path_to_parse))


# for each_parsed_data in origData:
#     print(each_parsed_data)


def parse_all_data_for_dates(start_date, end_date, original_data):
    list_of_data_for_calculation = []
    for each_data in original_data:
        if is_date_in_date_rage(start_date, end_date, each_data[0]):
            list_of_data_for_calculation.append(each_data)
    return list_of_data_for_calculation


def find_all_events(data_to_parse, start_date, end_date):
    events_list = []
    for each_data in data_to_parse:
        if convert_string_to_date_time(start_date) <= convert_string_to_date_time(each_data[0]) <= convert_string_to_date_time(end_date):
            if "None" in str(each_data[2]) or str(each_data[2]) == "Bypass":
                continue
            else:
                events_list.append(each_data)
    return events_list


def generate_data_for_recent_days_for_all_events_calc(data, look_back_window, start_date, end_date):
    all_event_data = []
    events = find_all_events(data, start_date, end_date)
    for each_event in events:
        all_event_data.append(generate_data_for_single_event(data, each_event, look_back_window))
    return all_event_data


def check_if_weekend_day(date):
    if date.weekday() == 5 or date.weekday() == 6:
        print("Weekend date has been found: " + str(date))
        return True

def get_number_of_events_per_day(data, date):
    number_of_events = 0
    for each_data in data:
        if convert_string_to_date_time(date) == each_data[-1][0]:
            number_of_events += 1
    return number_of_events


# def generate_data_for_single_event(original_file, list_of_all_events_in_file, date_of_event, look_back_window):
#     single_event_data = []
#     look_back_date = convert_string_to_date_time(date_of_event) - timedelta(1)
#     original_look_back_date = date_of_event - timedelta(look_back_window)
#     for each_event in list_of_all_events_in_file:
#         if look_back_date.date() == convert_string_to_date(each_event[0]).date():
#             date_of_event -= timedelta(1)
#             for each_row in original_file:
#                 if each_row[0]== date_of_event
#
#
#     return single_event_data


#########################################################
def convert_string_to_date_time(date_to_convert):
    return datetime.strptime(date_to_convert, date_time_format)


def convert_string_to_date(date_to_convert):
    return datetime.strptime(date_to_convert, date_format)


def is_date_in_date_rage(start_date, end_date, date_to_check):
    return start_date <= date_to_check <= end_date


def is_event_exists(row_where_to_check):
    if "None" in str(row_where_to_check[2]):
        return False
    elif "Bypass" == str(row_where_to_check[2]):
        return False
    else:
        return True


def events_on_same_day(original_file_to_parse, date_for_check):
    event_per_day = []
    _date_for_check = date_for_check.date()
    for each_row_event in original_file_to_parse:
        if _date_for_check == convert_string_to_date_time(each_row_event[0]).date():
            if is_event_exists(each_row_event):
                event_per_day.append(each_row_event)
    return event_per_day


def day_has_zero_power_consumption(original_file_to_parse, date_for_check):
    _date_for_check = date_for_check.date()
    for each_row_event in original_file_to_parse:
        if _date_for_check == convert_string_to_date_time(each_row_event[0]).date():
            print(each_row_event)
            if each_row_event[1] == "0":
                print("Found 0 consumption with zero  value: " + str(each_row_event))
                return True

def parse_all_data_for_date(original_file_to_parse, date_for_check):
    _date_for_check = date_for_check.date()
    list_of_data_for_calculation = []
    for each_data_row in original_file_to_parse:
        if _date_for_check == convert_string_to_date_time(each_data_row[0]).date():
            list_of_data_for_calculation.append(each_data_row)
    return list_of_data_for_calculation


def parse_data_with_look_back_window(original_file_to_parse, event_date, look_back_window):
    data_for_dates_with_values = []
    exclude_date = [str(event_date.date())]
    for i in range(1, look_back_window+1):
        new_look_back_date = event_date - timedelta(i)
        for each_date in exclude_date:
            if each_date == str(new_look_back_date.date()):
                continue
            else:
                event_per_day = events_on_same_day(original_file_to_parse, new_look_back_date)
                if day_has_zero_power_consumption(original_file_to_parse, new_look_back_date) or check_if_weekend_day(new_look_back_date) or len(event_per_day) > 1:
                    print("Excluding condition has been found:")
                    print("Going to exclude date: " + str(new_look_back_date.date()))
                    exclude_date.append(str(new_look_back_date.date()))
                    continue
                else:
                    data_for_dates_with_values.append(
                        [event_date, parse_all_data_for_date(original_file_to_parse, new_look_back_date)])


def create_data_for_cbl_calculation_dates(original_file_to_parse,
                            start_date,
                            end_date,
                            look_back_window=None,
                            extend_look_back_window=None,
                            recent_days_count=None,
                            highest_days_count=None,
                            middle_days_count=None,
                            exclude_prior_event_days=None,
                            exclude_zero_power_consumption=None):
    data_for_calculation = []
    start_date_converted = convert_string_to_date_time(start_date)
    end_date_converted = convert_string_to_date_time(end_date)
    for each_data_row in original_file_to_parse:
        current_date_time = convert_string_to_date_time(each_data_row[0])
        if is_date_in_date_rage(start_date_converted, end_date_converted, current_date_time):
            if is_event_exists(each_data_row):
                event_per_day = events_on_same_day(original_file_to_parse,current_date_time)
                if len(event_per_day) > 1:
                    print("More that 1 event per day found")
                    print(event_per_day)
                else:
                    print("Single event found " + str(event_per_day))
                    event_data_for_cbl_calculation = [[current_date_time,
                                                       parse_data_with_look_back_window(original_file_to_parse,
                                                                                        current_date_time,
                                                                                        look_back_window)]]
                    if len(event_data_for_cbl_calculation) < 1:
                        current_date_time = current_date_time - timedelta(look_back_window)
                        event_data_for_cbl_calculation.append([current_date_time, parse_data_with_look_back_window(original_file_to_parse, current_date_time, extend_look_back_window)])
                        if len(event_data_for_cbl_calculation) < 1:
                            data_for_calculation.append([current_date_time, "Unsuccessful"])
    return data_for_calculation









# print(create_data_for_cbl_calculation_dates(origData, "11/20/2021 01:00", "12/02/2021 06:00",5,5))
# print(parse_all_data_for_date(origData, convert_string_to_date_time("11/26/2021 01:00")))
print(parse_data_with_look_back_window(origData, convert_string_to_date_time("12/02/2021 06:00"),30))
# print (day_has_zero_power_consumption(origData, convert_string_to_date_time("11/26/2021 01:00")))
# data_for_recent_days = generate_data_for_recent_days_for_all_events_calc(origData, 2)
#
# for each_data in data_for_recent_days:
#     print(each_data)
