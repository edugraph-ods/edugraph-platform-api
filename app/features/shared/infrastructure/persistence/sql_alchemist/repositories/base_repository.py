from sqlalchemy import select, update as sqlalchemy_update
from sqlalchemy.exc import NoResultFound

class BaseRepository:
    def __init__(self, session, model):
        self.session = session
        self.model = model

    async def create(self, obj):
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get_by_id(self, id):
        query = select(self.model).where(self.model.id == id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_all(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def update(self, id, data: dict):
        query = (
            sqlalchemy_update(self.model)
            .where(self.model.id == id)
            .values(**data)
            .execution_options(synchronize_session="fetch")
        )

        await self.session.execute(query)
        await self.session.commit()
        return await self.get_by_id(id)

    async def delete(self, obj):
        await self.session.delete(obj)
        await self.session.commit()
