import os
import re
from tkinter import filedialog, messagebox, Tk
from src import new_entity


def Get_Txt_File():
    try:
        txt_file = filedialog.askopenfilename(
            title='Txt do SQL', filetypes=(('Arquivo de Texto', '*txt'),))
        if txt_file == '':
            raise FileNotFoundError
    except FileNotFoundError:
        messagebox.showerror('ERRO', 'Nenhum arquivo selecionado!')
        answer = messagebox.askyesno(
            'INFO', 'Ainda deseja selecionar um arquivo?')
        if answer:
            txt_file = Get_Txt_File()
        else:
            exit()
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


def Extract_Data(sql_data, class_name):
    var_list = []
    enti_obj = new_entity.java_entity()
    enti_obj.class_name = class_name
    for n, i in enumerate(sql_data):
        var_obj = new_entity.java_variable()
        sql_row = Remove_Empty(i.split(' '))
        if n != 0:
            var_obj.SetVariable(sql_row)

        else:
            enti_obj.dtb_schema = sql_row[2]
            enti_obj.data_Table = sql_row[3]

        enti_obj.varia_list.append(var_obj)
        var_list.append(var_obj)
    return var_list, enti_obj


def WriteScript(text: str, name: str):
    '''Pergunta onde quer salvar e Cria/Sobrescreve arquivo .java'''
    where = filedialog.askdirectory(initialdir='./', title='Salvar Script')
    with open(f'{where}/{name}.java', 'w') as f:
        f.write(text)


if __name__ == '__main__':
    input_file = Get_Txt_File()
    class_name = input("Insira o nome da Classe: ")
    clear_data = Clear_Input(input_file)
    var_list, entity_obj = Extract_Data(clear_data, class_name)

    script_content = entity_obj.EntityConstructor()

    Tk().withdraw()
    WriteScript(script_content, class_name)
    input('Programa finalizado!\nPressione [ENTER] para fechar o programa!')
