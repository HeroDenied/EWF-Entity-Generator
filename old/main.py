# https://www.alt-codes.net/

# Imports
from src import entity as ent, interface
from tkinter import filedialog, messagebox, Tk


# Functions
def Select_File() -> str:
    '''Abre um seletor de arquivos para obter um arquivo de texto.'''
    file_name = filedialog.askopenfilename(
        initialdir='/', title="Browse File", filetypes=(("text file", "*.txt"),))

    if file_name == '':
        messagebox.showerror('Erro', 'Nenhum arquivo de texto selecionado!')
        exit()
    return file_name


def Read_File(file_path: str) -> list:
    '''Lê o arquivo de texto com a estrutura de criação da tabela (CREATE TABLE).'''
    file = open(file_path, "r")
    content = [f for f in file]
    file.close()
    return content


def Filter_Content(content: list) -> list:
    '''Remove espaços e caracteres especiais dos dados extraídos do arquivo.'''
    stripped = [i.strip() for i in content]
    return stripped


def Remove_Small(line: list) -> list:
    '''Retorna linha se tiver mais de uma posição.'''
    if len(line) > 1:
        return line


def Remove_Constraint(line: list) -> list:
    '''Retorna linha se não tenha a palavra CONSTRAINT.'''
    if line[0] != 'CONSTRAINT':
        return line


def Extract_Entity_Data(commands: list) -> dict:
    '''Extrai dados da lista para preencher os campos do objeto de entidade.'''
    entity_list = []
    db = commands[0].split('.')[0].split('"')[-2].strip()
    tb = commands[0].split('.')[-1].split(' ')[0]
    for command in commands:
        if command != commands[0]:
            try:
                filtered = Remove_Constraint(Remove_Small(command.split(' ')))
                entity = ent.entity()

                entity.database = db
                entity.dattable = tb.replace('"', '').strip()
                entity.SetVarName(filtered[0])
                entity.SetVarType(filtered[1])
                entity.SetConstraints(filtered[0])
                entity.GenerateGetSet()
                entity.GenerateInstance()
                entity_list.append(entity)

            except TypeError as e:
                print(e)

    return entity_list


def BuildContent(lista: str) -> any:
    '''Constroi conteudo provindo da lista'''
    entity_table = ''
    entity_content = []
    for e in lista:
        entity_content.append(e.GenerateVarInstance())
        entity_table = e.GetFullTableName()

    return entity_content, entity_table


def WriteScript(text: str, name: str):
    '''Pergunta onde quer salvar e Cria/Sobrescreve arquivo .java'''
    where = filedialog.askdirectory(initialdir='./', title='Salvar Script')
    with open(f'{where}/{name}.java', 'w') as f:
        f.write(text)


def Create_Entity(content: str, tb: str, script_name: str):
    '''Concatena todo conteúdo do script de entidade.'''
    imports = '\n'.join(["package br.gov.emprel.modelo.domain;\n",
                        "import java.util.Date;",
                         "import java.io.Serializable;\n",
                         "import javax.persistence.Column;",
                         "import javax.persistence.Entity;",
                         "import javax.persistence.GeneratedValue;",
                         "import javax.persistence.GenerationType;",
                         "import javax.persistence.Id;",
                         "import javax.persistence.JoinColumn;",
                         "import javax.persistence.ManyToOne;",
                         "import javax.persistence.SequenceGenerator;",
                         "import javax.persistence.Table;",
                         "import javax.validation.constraints.Max;",
                         "import javax.validation.constraints.NotNull;",
                         "import org.hibernate.validator.constraints.Length;"])
    header = '\n'.join(["@Entity",
                       f'@Table(name = "{tb}")',
                        "public class " + script_name + " implements Serializable {"])
    footer = '}'
    output_text = '\n'.join([header, content, footer])
    WriteScript(output_text, script_name)


def Run(ui: interface.Ui):
    '''Executa o programa'''
    script_name = ui.input_entry.get()
    try:
        file_path = Select_File()
        if script_name == '':
            raise Exception('Nome da Entidade Vasio!')
        content = Read_File(file_path)
        filtered = Filter_Content(content)
        entity_obj_list = Extract_Entity_Data(filtered)
        final_content, entity_table = BuildContent(entity_obj_list)

        Create_Entity('\n'.join(final_content), entity_table, script_name)
        messagebox.showinfo('INFO', 'Script gerado com sucesso!')
    except Exception as e:
        print(str(e))
        messagebox.showerror(
            'ERRO', 'Campo "Nome da Entidade" vasio!\nPor favor preencha o campo e tente novamente!')


# Execution
if __name__ == "__main__":
    ui = interface.Ui()
    ui.Start(Run)
