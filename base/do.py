"""
data objects
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass
class S3File:
    uuid: UUID
    key: str
    bucket: str

