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
    'decimal': 'BigDecimal',
    'timestamp': 'Date',
}

transparency = [
    'public',
    'private'
]


class entity():
    def __init__(self) -> None:
        self.database = ''
        self.dattable = ''
        self.var_name = ''
        self.var_type = ''
        self.var_size = ''
        self.constrai = []

        self.get_func = ''
        self.set_func = ''
        self.var_inst = ''

    def SetVarName(self, var_name: str):
        name = var_name.replace('"', '').lower()

        for i in translate_dict:
            if i in name:
                self.var_name = translate_dict[i]
                break
            else:
                self.var_name = name

    def SetVarType(self, var_type: str):
        if '(' in var_type:
            v_type = var_type.lower().split('(')[0]
            self.var_size = var_type.lower().split(
                '(')[1].replace(')', '').strip()
        else:
            v_type = var_type.lower()

        if v_type in java_var_types:
            self.var_type = java_var_types[v_type].capitalize()

    def SetConstraints(self, column_name: str):
        column = column_name.replace('"', '').strip()
        if self.var_name == 'id':
            self.constrai.append('@Id')
            self.constrai.append('@NotNull')
            self.constrai.append(
                f'@GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "SQ{self.dattable}_{column}")')
            self.constrai.append(
                f'@SequenceGenerator(name = "SQ{self.dattable}_{column}", sequenceName = "{self.database}.SQ{self.dattable}_{column}", allocationSize = 1)')

        if self.var_type == 'Long':
            self.constrai.append(f'@Max({self.var_size})')
        elif self.var_type == "String" or self.var_type:
            self.constrai.append(f'@Length(max={self.var_size})')

        self.constrai.append(f'@Column(name="{column}")')

    def GetFullTableName(self):
        return f"{self.database}.{self.dattable}"

    def GenerateInstance(self):
        self.var_inst = ' '.join([
            transparency[1],
            self.var_type,
            f'{self.var_name};',
        ])

    def GenerateGetSet(self):
        self.get_func = ' '.join([
            transparency[0],
            self.var_type,
            f'get{self.var_name.capitalize()}()',
            r'{',
            f'return {self.var_name};',
            r'}'

        ])

        self.set_func = ' '.join([
            transparency[0],
            'void',
            f'set{self.var_name.capitalize()}',
            f'({self.var_type} {self.var_name})',
            r'{',
            f'this.{self.var_name} = {self.var_name};'
            r'}'
        ])

    def GenerateVarInstance(self):
        return '\n'.join([
            '\n'.join(self.constrai),
            self.var_inst,
            self.get_func,
            self.set_func
        ])
