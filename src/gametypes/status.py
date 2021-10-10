from functools import partial
from types import FunctionType
from typing import Union
from .base import Base

class Status(Base):
    effect_func: FunctionType

    def __init__(self, id: int, name: str, desc: str = ''):
        super().__init__(id, name, desc)
        self.effect_func = lambda state, entity: None

    def effect(self, state, entity) -> None:
        if not isinstance(self.effect_func, FunctionType) and not (type(self.effect_func) == partial):
            return
        self.effect_func(state, entity)

    def set_effect(self, effect_func: FunctionType) -> bool:
        if not isinstance(effect_func, FunctionType):
            return False

        self.effect_func = effect_func
        return True

    def tick(self, state, entity):
        self.effect(state, entity)