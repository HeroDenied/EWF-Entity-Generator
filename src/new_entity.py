translate_dict = {
    'ccodi': 'id',
    'cdesc': 'descricao',
    'ecodi': 'empresa',
    'cmatr': 'matricula',
    'culat': 'atualizacao',
}

java_var_types = {
    'varchar': 'String',
    'char': 'String',
    'smallint': 'Long',
    'integer': 'Long',
    'bigint': 'Long',
    'date': 'Date',
    'object': 'ObjectName',
    'decimal': 'Bigdecimal',
    'timestamp': 'Date',
}

transparency = [
    'public',
    'private'
]


class java_variable():
    def __init__(self):
        self.var_name = ''
        self.var_type = ''
        self.var_size = 0
        self.constrai = ''
        self.transpar = ''
        self.var_colu = ''

    def TranslateName(self, name: str) -> str:
        temp_name = name.lower()
        for i in translate_dict:
            if i in temp_name:
                return translate_dict[i]
        return temp_name

    def TranslateType(self, v_type: str) -> str:
        temp_type = v_type.lower()

        if temp_type in java_var_types:
            return java_var_types[temp_type].capitalize()

    def TranslateConstraint(self, constrai: list) -> str:
        return ' '.join(constrai)

    def SetVariable(self, row: list) -> None:
        self.var_colu = row[0]
        self.var_name = self.TranslateName(row[0])
        self.var_type = self.TranslateType(row[1])
        self.transpar = transparency[1]
        try:
            self.var_size = int(row[2])
            self.constrai = self.TranslateConstraint(row[3:5])
        except ValueError:
            self.constrai = self.TranslateConstraint(row[2:4])
        except IndexError:
            self.constrai = ''

    def VarConstructor(self):
        return f'{self.transpar} {self.var_type} {self.var_name};'


class java_entity():
    def __init__(self):
        self.class_name = ''
        self.data_Table = ''
        self.dtb_schema = ''
        self.constr_str = ''
        self.varia_list = []

    def InstanciateVariables(self):
        instanced_var = ''
        param_size = ''
        for i in self.varia_list:
            if i.var_type == 'Long':
                param_size = f'@Max({i.var_size})'
            elif i.var_type != 'Date':
                param_size = f'@Length(max={i.var_size})'

            contr = '\n'.join([
                '\t@NotNull',
                f'\t{param_size}',
                f'\t@Column(name="{i.var_colu}")'
            ])
            var_build = i.VarConstructor()
            if '  ;' not in var_build:
                instanced_var += f'{contr}\n\t{var_build}\n\n'
                # print(f'{contr}\n\t{var_build}\n')
        return instanced_var

    def EntityConstructor(self):
        imports = '\n'.join([
            'import java.io.Serializable;',
            'import java.util.Date;\n',
            'import javax.persistence.Column;',
            'import javax.persistence.Entity;',
            'import javax.persistence.Id;',
            'import javax.persistence.Table;',
            'import javax.persistence.GenerationType;',
            'import javax.persistence.GeneratedValue;',
            'import javax.persistence.SequenceGenerator;',
            'import javax.validation.constraints.NotNull;',
            'import javax.validation.constraints.Max;\n',
            'import org.hibernate.validator.constraints.Length;\n'
        ])
        coments = '\n'.join([
            'Adicione get, set, hashCode, equals e toString pelo eclipse.',
            'O padrão do sequence, caso precise:',
            '@GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "nomeDaSequencia")',
            '@SequenceGenerator(name = "nomeDaSequencia", sequenceName = "DATABASE.TABELADASEQUENCIA", allocationSize = 1)\n',
        ])
        file_content = '{}\n{}\n{}/*{}*/\n'
        class_init = f'@Entity\n@Table(name = "{self.dtb_schema}.{self.data_Table}")\npublic class {self.class_name} implements Serializable ' + '{'

        return file_content.format(imports, class_init, self.InstanciateVariables(), coments)+'}'
