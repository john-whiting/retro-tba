from functools import partial
from types import FunctionType
from typing import Dict, List, Union

from .base import Base
from .entity import Entity

from utils.io import IO

class Room(Base):
    entities: List[Entity]
    thingies: Dict[str, FunctionType]
    initial_action: FunctionType
    enter_action: FunctionType

    task_complete_action: FunctionType
    ran_task_complete: bool

    adj_rooms = any
    tasks = List[FunctionType]

    def __init__(self, state, name: str, desc: str = ''):
        super().__init__(state, name, desc)

        self.entities = []
        self.thingies = {}
        self.initial_action = lambda state: None
        self.enter_action = lambda state: None
        self.leave_action = lambda state: None
        self.task_complete_action = lambda state: None
        self.ran_task_complete = False
        
        self.adj_rooms = {}
        self.tasks = []

    def on_enter(self, state):
        IO.print(f'&eYou entered another room, and you decided to call it {self.name}')
        IO.print(f'&2{self.desc}')
        if not (self.id in state['rooms_entered']):
            state['rooms_entered'].append(self.id)
            self.initial_action(state)
        self.enter_action(state)

    def on_leave(self, state):
        self.leave_action(state)

    def add_task(self, task: FunctionType):
        if not isinstance(task, FunctionType) and not (type(task) == partial):
            return False

        self.tasks.append(task)
        return True

    def set_initial_action(self, action: FunctionType):
        if not isinstance(action, FunctionType) and not (type(action) == partial):
            return False

        self.initial_action = action
        return True

    def set_enter_action(self, action: FunctionType):
        if not isinstance(action, FunctionType) and not (type(action) == partial):
            return False

        self.enter_action = action
        return True

    def set_leave_action(self, action: FunctionType):
        if not isinstance(action, FunctionType) and not (type(action) == partial):
            return False

        self.leave_action = action
        return True

    def set_task_complete_action(self, action: FunctionType):
        if not isinstance(action, FunctionType) and not (type(action) == partial):
            return False

        self.task_complete_action = action
        return True

    def tick(self, state):
        for entity in self.entities:
            entity.tick(state)

        num_tasks_completed = 0
        for task in self.tasks:
            if task(state):
                num_tasks_completed += 1

        if not self.ran_task_complete and len(self.tasks) == num_tasks_completed:
            self.task_complete_action(state)
            self.ran_task_complete = True
        
        state['player'].tick(state)