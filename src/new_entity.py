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


class java_variable():
    def __init__(self):
        self.var_name = ''
        self.var_type = ''
        self.var_size = 0
        self.constrai = ''
        self.transpar = ''

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
        self.var_name = self.TranslateName(row[0])
        self.var_type = self.TranslateType(row[1])
        self.transpar = transparency[1]
        try:
            self.var_size = int(row[2])
            self.constrai = self.TranslateConstraint(row[3:5])
        except ValueError:
            self.constrai = self.TranslateConstraint(row[2:4])

    def VarConstructor(self):
        return f'{self.transpar} {self.var_type} {self.var_name};'


class java_entity(java_variable):
    def __init__(self):
        super().__init__()
        self.dt_Table = ''
        self.database = ''
        self.cons_str = ''
