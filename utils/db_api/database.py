from aiogram import types
from asyncpg import Connection, Record
from asyncpg.exceptions import UniqueViolationError


class DBCommands:
    ADD_NEW_USER_REFERRAL = "INSERT INTO users(user_id, username, first_name, referral) " \
                            "VALUES ($1, $2, $3, $4) RETURNING id"
    ADD_NEW_USER = "INSERT INTO users(user_id, username, first_name) VALUES ($1, $2, $3) RETURNING id"
    COUNT_USERS = "SELECT COUNT(*) FROM users"
    GET_ID = "SELECT id FROM users WHERE user_id = $1"
    CHECK_REFERRALS = "SELECT user_id FROM users WHERE referral=" \
                      "(SELECT id FROM users WHERE user_id=$1)"
    CHECK_BALANCE = "SELECT balance FROM users WHERE user_id = $1"
    ADD_MONEY = "UPDATE users SET balance=balance+$1 WHERE user_id = $2"

    def __init__(self, pool: Connection):
        self.pool = pool

    async def add_new_user(self, user_id, username, first_name, referral=None):
        args = user_id, username, first_name

        if referral:
            args += (int(referral),)
            command = self.ADD_NEW_USER_REFERRAL
        else:
            command = self.ADD_NEW_USER

        try:
            record_id = await self.pool.fetchval(command, *args)
            return record_id
        except UniqueViolationError:
            pass

    async def count_users(self):
        record: Record = await self.pool.fetchval(self.COUNT_USERS)
        return record

    async def get_id(self):
        command = self.GET_ID
        user_id = types.User.get_current().id
        return await self.pool.fetchval(command, user_id)

    async def check_referrals(self, user_id):
        command = self.CHECK_REFERRALS
        rows = await self.pool.fetch(command, user_id)
        return rows

    async def check_balance(self, user_id):
        command = self.CHECK_BALANCE
        return await self.pool.fetchval(command, user_id)

    async def add_money(self, user_id, money):
        command = self.ADD_MONEY
        return await self.pool.fetchval(command, money, user_id)
