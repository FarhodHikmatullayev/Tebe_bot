import datetime
from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config
from data.config import DEVELOPMENT_MODE


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        if DEVELOPMENT_MODE:
            self.pool = await asyncpg.create_pool(
                user=config.DB_USER,
                password=config.DB_PASS,
                host=config.DB_HOST,
                database=config.DB_NAME
            )
        else:
            self.pool = await asyncpg.create_pool(
                dsn=config.DATABASE_URL
            )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    # for users
    async def create_user(self, phone, username, telegram_id, full_name):
        sql = "INSERT INTO Users (phone, username, telegram_id, full_name) VALUES($1, $2, $3, $4) returning *"
        return await self.execute(sql, phone, username, telegram_id, full_name, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_users(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    # for categories
    async def select_all_categories(self):
        sql = "SELECT * FROM category"
        return await self.execute(sql, fetch=True)

    async def select_categories(self, **kwargs):
        sql = "SELECT * FROM Category WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    # async def create_post(self, category_id, text, image, video):
    #     sql = "INSERT INTO Users (category_id, text, image, video) VALUES($1, $2, $3, $4) returning *"
    #     return await self.execute(sql, category_id, text, image, video, fetchrow=True)

    # for posts
    async def select_posts(self, **kwargs):
        sql = "SELECT * FROM Post WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def create_post(self, category_id, text, image, video, user_id, created_time):
        sql = "INSERT INTO Post (category_id, text, image, video, user_id) VALUES($1, $2, $3, $4, $5) returning *"
        return await self.execute(sql, category_id, text, image, video, user_id, fetchrow=True)

    async def update_post(self, id, text, image, video):
        sql = "UPDATE Post SET text=$2, image=$3, video=$4 WHERE id=$1"
        return await self.execute(sql, id, text, image, video, execute=True)

    async def delete_post(self, id):
        sql = "DELETE FROM Post WHERE id = $1"
        result = None  # Define and assign a default value to result
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                result = await connection.execute(sql, id)
        return result

    # for tests

    async def select_tests(self, **kwargs):
        sql = "SELECT * FROM Test WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    # for results
    async def create_result(self, counts_true, counts_false, time_duration, is_successful, user_id, test_id,
                            created_at=datetime.datetime.now()):
        sql = "INSERT INTO Result (counts_true, counts_false, time_duration, is_successful, user_id, test_id, created_at) VALUES($1, $2, $3, $4, $5, $6, $7) returning *"
        return await self.execute(sql, counts_true, counts_false, time_duration, is_successful, user_id, test_id,
                                  created_at,
                                  fetchrow=True)

    async def select_result(self, **kwargs):
        sql = "SELECT * FROM Result WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)
