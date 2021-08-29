from pony.orm.dbapiprovider import StrConverter


class StrInt:
    @classmethod
    def init(cls, db):
        db.provider.converter_classes.append((StrInt, StrIntConverter))


class StrIntConverter(StrConverter):
    def validate(self, val, obj=None):
        if not isinstance(val, int):
            raise ValueError(f"Must be an int. Got {val}")
        return val

    def py2sql(self, val: int) -> str:
        return str(val)

    def sql2py(self, val: str) -> int:
        return int(val)

    def sql_type(self):
        return 'TEXT'
