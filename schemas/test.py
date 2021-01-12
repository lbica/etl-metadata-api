from ma import ma
from models.test import TestModel


class TestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TestModel
        load_only = ("name",)
        load_instance = True
        # fields = ("name", "email")
        # dump_only = ("id", )

    # id  = fields.Int()
    # name = ma.auto_field(load_only=True)
    # email = ma.auto_field(load_only=True)
