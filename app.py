import os
import re
from tkinter import filedialog, messagebox, Tk
from src import new_entity


def Get_Txt_File():
    txt_file = filedialog.askopenfilename(
        title='Txt do SQL', filetypes=(('Arquivo de Texto', '*txt'),))
    return txt_file


def Get_Txt_Data(txt_file: str) -> list:
    text = []
    with open(txt_file, 'r') as f:
        text = f.readlines()
    return text


def Remove_Empty(unfiltered: list):
    return [i for i in unfiltered if len(i) > 1]


def Strip_List(data: list) -> list:
    return [i.strip() for i in data]


def Remove_Quotations(data: list):
    return [i.replace('"', '') for i in data]


def Remove_Excess_Space(data: list):
    return [re.sub(' +', ' ', i) for i in data]


def Remove_Parentheses(data: list):
    rm1 = [i.replace('(', ' ') for i in data]
    return [i.replace(')', '') for i in rm1]


def Remove_Comma_Dot(data: list):
    rm1 = [i.replace(',', '') for i in data]
    return [i.replace('.', '') for i in rm1]


def Clear_Input(file_name: str):
    clear_data = Remove_Comma_Dot(Remove_Parentheses(Remove_Excess_Space(
        Remove_Quotations(Strip_List(Get_Txt_Data(file_name))))))
    return clear_data


if __name__ == '__main__':
    input_file = Get_Txt_File()
    clear_data = Clear_Input(input_file)

    var_list = []
    for n, i in enumerate(clear_data):
        sql_row = Remove_Empty(i.split(' '))
        var_obj = new_entity.java_entity()
        if n != 0:
            var_obj.SetVariable(sql_row)
            print(
                '{:^10} | {:^10} | {:^10} | {:^10}'.format(
                    str(var_obj.var_name),
                    str(var_obj.var_type),
                    str(var_obj.var_size),
                    str(var_obj.constrai)
                )
            )
        else:
            var_obj.database = sql_row[2]
            var_obj.dt_Table = sql_row[3]
            print(
                '\n{:^10} | {:^10}'.format(
                    str(var_obj.database),
                    str(var_obj.dt_Table)
                )
            )

        var_list.append(var_obj)

    print(var_list)
