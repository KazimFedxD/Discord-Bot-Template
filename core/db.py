from typing import Any
import asyncsqlite


class DB:
    async def init(self):
        """
        Initialize the database connection
        """
        self.conn = await asyncsqlite.connect("main.db")
        self.cursor = await self.conn.cursor()
        self.cursorqueue: list[str] = []
        await self.commit()

    async def close(self):
        """
        Close the database connection
        """
        await self.cursor.close()
        await self.conn.close()
        await self.commit()

    async def acreatetable(self, table: str, **columns: str):
        """Immediately create a table

        Args:
            table (str): Name of the table
        Keyword Args:
            **columns (str): Name of the column and its type
        Example:
            await db.acreatetable('users', id='INTEGER PRIMARY KEY', name='TEXT')
        """
        column = ", ".join([f"{k} {v}" for k, v in columns.items()])
        await self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} ({column})")
        await self.commit()

    async def insert(self, table: str, **values: str):
        """Insert a row into the table

        Args:
            table (str): Name of the table
        Keyword Args:
            **values (str): Column name and its value
        Example:
            await db.insert('users', name='John Doe', age='23')
        """

        keys = ", ".join(values.keys())
        value = ", ".join([f'"{v}"' for v in values.values()])
        await self.cursor.execute(f"INSERT INTO {table} ({keys}) VALUES ({value})")
        await self.commit()

    async def select(self, table: str, amounttofetch: int | str = 1, **where: str):
        """Select rows from the table

        Args:
            table (str): Name of the table
            amounttofetch (int | str, optional): The amount of rows to fetch. Defaults to 1.

        Keyword Args:
            **where (str): Column name and its value

        Raises:
            ValueError: Invalid amount if amount is not an integer or 'all'

        Returns:
            Iterable[Row] | None: Returns the fetched rows if any
        """
        wherestr = " AND ".join([f'{k}="{v}"' for k, v in where.items()])
        await self.cursor.execute(
            f"SELECT {amounttofetch} FROM {table} WHERE {wherestr}"
        )
        try:
            amounttofetch = int(amounttofetch)
        except:
            pass
        if isinstance(amounttofetch, int):
            return await self.cursor.fetchmany(amounttofetch)
        if not amounttofetch == "all":
            raise ValueError("Invalid amount")
        return await self.cursor.fetchall()

    async def delete(self, table: str, **where: str):
        """Delete a row from the table
        Args:
            table (str): Name of the table
        Keyword Args:
            **where (str): Column name and its value
        Example:
            await db.delete('users', id='1')
        """

        wherestr = " AND ".join([f'{k}="{v}"' for k, v in where.items()])
        await self.cursor.execute(f"DELETE FROM {table} WHERE {wherestr}")
        await self.commit()

    async def update(self, table: str, conditions: int = 1, **values: str):
        """Update a row in the table

        Args:
            table (str): Name of the table
            conditions (int, optional): The amount of conditions to use. Defaults to 1.
            (Fetches Conditions from the start of the values dict)
        Keyword Args:
            **values (str): Column name and its value
        Example:
            await db.update('users', id=1, name='John Doe', age='23')
        """
        conditionlist: list[tuple[str, Any]] = []
        items = list(values.items())
        for _ in range(conditions):
            conditionlist.append(items.pop(0))
        conditionstr = " AND ".join([f'{k}="{v}"' for k, v in conditionlist])
        valuestr = ", ".join([f'{k}="{v}"' for k, v in items])
        await self.cursor.execute(f"UPDATE {table} SET {valuestr} WHERE {conditionstr}")
        await self.commit()

    async def commit(self):
        """
        Commit the changes to the database
        """
        await self.conn.commit()

    async def executequeue(self):
        """
        Execute the queued queries
        """
        for query in self.cursorqueue:
            await self.cursor.execute(query)
        self.cursorqueue = []
        await self.commit()

    def createtable(self, table: str, **columns: str):
        """Add a query to create a table to the queue

        Args:
            table (str): Name of the table
        Keyword Args:
            **columns (str): Name of the column and its type
        Example:
            db.createtable('users', id='INTEGER PRIMARY KEY', name='TEXT')
        """
        column = ", ".join([f"{k} {v}" for k, v in columns.items()])
        self.cursorqueue.append(f"CREATE TABLE IF NOT EXISTS {table} ({column})")
