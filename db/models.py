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

class User(Model):
    id = fields.IntField(pk=True)
    telegram_id = fields.BigIntField(unique=True)
    username = fields.CharField(max_length=255, null=True)
    full_name = fields.CharField(max_length=255, null=True)
    is_admin = fields.BooleanField(default=False)
    mode = fields.CharField(max_length=50, default='user')
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "users"

    def __str__(self):
        return f"<User {self.telegram_id} ({self.mode})>"