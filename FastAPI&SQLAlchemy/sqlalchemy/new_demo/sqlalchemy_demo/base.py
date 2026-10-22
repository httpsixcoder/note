# 延迟注解求值
from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """全局ORM基类，所有数据库模型继承此类"""
    pass

