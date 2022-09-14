from uuid import UUID
from typing import Optional

from base import do

from .util import pyformat2psql
from . import pool_handler


async def add(url: str, s3_file_uuid: UUID) -> int:
    sql, params = pyformat2psql(
        sql=fr"INSERT INTO sheet"
            fr"            (url, s3_file_uuid)"
            fr"     VALUES (%(url)s, %(s3_file_uuid)s)"
            fr"  RETURNING id",
        url=url, s3_file_uuid=s3_file_uuid
    )
    _id, = await pool_handler.pool.fetchrow(sql, *params)
    return _id


async def get(url: str) -> Optional[do.Sheet]:
    sql, params = pyformat2psql(
        sql=fr"SELECT id, url, s3_file_uuid"
            fr"  FROM sheet"
            fr" WHERE url = %(url)s",
        url=url,
    )
    try:
        _id, url, s3_file_uuid = await pool_handler.pool.fetchrow(sql, *params)
    except TypeError:
        return None
    return do.Sheet(id=_id, url=url, s3_file_uuid=s3_file_uuid)
