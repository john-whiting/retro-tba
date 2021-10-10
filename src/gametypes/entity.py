from functools import partial
import random
from types import FunctionType
from typing import List, Union

from .base import Base
from .status import Status
from .usable import Usable

class Entity(Base):
    max_hp: int
    hp: int
    max_mana: int
    mana: int

    pending_hp: int
    pending_mana: int

    equipped: List[Usable]
    statuses: List[Status]
    usables: List[Usable]

    actions: List[FunctionType]
    death_action: FunctionType

    def __init__(self, state, name: str, max_hp: int, max_mana: int, desc: str = ''):
        super().__init__(state, name, desc)
        self.max_hp = max_hp
        self.hp = max_hp
        self.max_mana = max_mana
        self.mana = max_mana

        self.pending_hp = max_hp
        self.pending_mana = max_mana

        self.equipped = []
        self.statuses = []
        self.usables = []

        self.actions = []
        self.death_action = lambda state, entity: None

    def take_turn(self, state):
        if len(self.actions) == 0:
            return

        if self.hp <= 0:
            return

        action = random.choice(self.actions)
        action(state, self)

    def on_death(self, state):
        self.death_action(state, self)

    def add_usable(self, usable: Usable) -> bool:
        if not isinstance(usable, Usable):
            return False

        self.usables.append(usable)
        return True

    def add_status(self, status: Status) -> bool:
        if not isinstance(status, Status):
            return False

        self.statuses.append(status)
        return True

    def add_equipment(self, equipment: Usable) -> bool:
        if not isinstance(equipment, Usable):
            return False

        self.equipped.append(equipment)
        return True

    def add_action(self, action: FunctionType) -> bool:
        if not isinstance(action, FunctionType) and not (type(action) == partial):
            return False

        self.actions.append(action)
        return True

    def set_death_action(self, action: FunctionType):
        if not isinstance(action, FunctionType) and not (type(action) == partial):
            return False

        self.death_action = action
        return True

    def get_item(self, state, item_name: str = ''):
        item_name = item_name.lower()
        cur_usables = {usable.name.lower(): usable for usable in self.usables}

        if not (item_name in cur_usables.keys()):
            return None
        
        return cur_usables[item_name]

    def tick(self, state) -> None:
        self.pending_hp = self.hp
        self.pending_mana = self.mana

        for status in self.statuses:
            status.tick(self, state)

        for equipment in self.equipped:
            equipment.tick(self, state)

        self.hp = self.pending_hp
        self.mana = self.pending_mana

        if self.hp <= 0:
            self.on_death(state)

        self.take_turn(state)