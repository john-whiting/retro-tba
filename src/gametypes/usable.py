from functools import partial
from types import FunctionType
from typing import List, Union

from .base import Base
from .status import Status

class Usable(Base):
    target_required: bool

    statuses: List[Status]

    use_func: FunctionType

    def __init__(self, state, name: str, target_required: bool, equipable: bool, desc: str = ''):
        super().__init__(state, name, desc)
        self.target_required = target_required
        self.equipable = equipable

        self.statuses = []

        self.use_func = lambda state, entity: None

    def use(self, state, entity) -> None:
        if not isinstance(self.use_func, FunctionType) and not (type(self.use_func) == partial):
            return
        self.use_func(state, entity)

    def set_use(self, use_func: FunctionType) -> bool:
        if not isinstance(use_func, FunctionType) and not (type(use_func) == partial):
            return False

        self.use_func = use_func
        return True

    def add_status(self, status: Status) -> bool:
        if not isinstance(status, Status):
            return False

        self.statuses.append(status)
        return True
    
    def tick(self, state, entity) -> None:
        for status in self.statuses:
            status.tick(state, entity)