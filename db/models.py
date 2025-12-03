from tortoise import fields
from tortoise.models import Model
from db import DB_URL

class BaseModel(Model):
    id = fields.IntField(pk=True)

    class Meta:
        abstract = True

    @classmethod
    async def get_random(cls):
        count = await cls.all().count()
        if count == 0:
            return None

        import random
        random_index = random.randint(0, count - 1)
        return await cls.all().offset(random_index).first()

    @classmethod
    async def get_by_id(cls, id_):
        return await cls.filter(id=id_).first()

class Category(BaseModel):
    # Категории
    name = fields.CharField(max_length=255, unique=True, null=False)

class Noun(BaseModel):
    # Существительные
    ru = fields.CharField(max_length=64, null=False)
    fi = fields.CharField(max_length=64, null=False)
    base = fields.CharField(max_length=64, null=True)
    type = fields.SmallIntField(null=True)
    isfinnish = fields.BooleanField(default=False)

class Verb(BaseModel):
    # Глаголы
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

class Pronoun(BaseModel):
    ru = fields.CharField(max_length=16, null=False)
    fi = fields.CharField(max_length=16, null=False)
    plural = fields.BooleanField(default=False)
    negative = fields.CharField(max_length=16, null=False)
    ending = fields.CharField(max_length=8, null=True)

    def __str__(self):
        return f"<User {self.telegram_id} ({self.mode})>"


# Tortoise config exported for aerich
TORTOISE_ORM = {
    "connections": {"default": DB_URL},
    "apps": {
        "models": {
            "models": ["aerich.models", "db.models"],
            "default_connection": "default",
        },
    },
}