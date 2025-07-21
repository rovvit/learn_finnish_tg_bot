from tortoise import fields
from tortoise.models import Model

class Category(Model):
    # Категории
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True, null=False)

class Noun(Model):
    # Существительные
    id = fields.IntField(pk=True)
    ru = fields.CharField(max_length=64, null=False)
    fi = fields.CharField(max_length=64, null=False)
    base = fields.CharField(max_length=64, null=True)
    type = fields.SmallIntField(null=True)
    isfinnish = fields.BooleanField(default=False)

class Verb(Model):
    # Глаголы
    id = fields.IntField(pk=True)
    ru = fields.CharField(max_length=64, null=False)
    fi = fields.CharField(max_length=64, null=False)
    base = fields.CharField(max_length=64, null=True)
    type = fields.SmallIntField(null=True)
    isfinnish = fields.BooleanField(default=False)

