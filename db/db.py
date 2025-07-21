from tortoise import Tortoise

async def init():
    await Tortoise.init(
        db_url=f'postgres://root:root@localhost/fin',
        modules={'models': ['models']}
    )
    await Tortoise.generate_schemas()