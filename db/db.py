from tortoise import Tortoise
from db.models import Noun

async def init():
    await Tortoise.init(
        db_url=f'postgres://root:root@localhost/fin',
        modules={'models': ['db.models']}
    )
    await Tortoise.generate_schemas()

async def get_nouns():
    return await Noun.all().values()