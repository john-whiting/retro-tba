from functools import partial
from typing import List, Union
from gametypes.entity import Entity
from gametypes.room import Room
from gametypes.usable import Usable
from utils.io import IO

def player_death(state, entity):
    IO.print(f'&b&cYOU DIED!!!!!')
    state['quit'] = True

def entity_death(state, entity):
    IO.print(f'&2You succesfully killed {entity.name}!')
    state['cur_room'].entities.remove(entity)

def entity_action(state, entity, damage: int = 0):
    IO.print(f'&c{entity.name} hit you for {damage} hp!')
    state['player'].hp -= damage

def task_entity_check(state):
    return len(state['cur_room'].entities) == 0

def complete_task(state, room_id: Union[int, List[int]] = 0):
    IO.print('&eThe task fairy cried and opened the exits for you!')
    if isinstance(room_id, list):
        state['unlocked_rooms'] += room_id
    else:
        state['unlocked_rooms'] += [room_id]

def attack_entity(state, entity: Entity, damage: int = 0):
    IO.print(f'&eYou stabbed that {entity.name} for {damage} hp!')
    entity.hp -= damage

def give_sword(state):
    IO.print('&eYou pick up a sword! Use this to kill enemies!')

    sword = Usable(state, 'Sword', True, False, 'Stick the pointy end in something.')
    sword.set_use(partial(attack_entity, damage=5))
    state['player'].add_usable(sword)
    return True

def use_potion(state, entity: Entity = None, potion: Usable = None, recovery: int = 0):
    IO.print(f'&eYou used a {potion.name} for {recovery} hp!')
    state['player'].hp += recovery
    state['player'].usables.remove(potion)

def use_chest(state):
    IO.print('&eYou look into the chest, find a health potion, and pick it up.')
    potion = Usable(state, 'Health Potion', False, False, 'Heals 10 hp')
    potion.set_use(partial(use_potion, potion=potion, recovery=10))
    state['player'].add_usable(potion)
    return True

def task_potion_check(state):
    item = state['player'].get_item(state, 'Health Potion')
    return (item is None) and len(state['cur_room'].thingies) == 0

def pull_lever(state, room_id: Union[int, List[int]] = 0):
    IO.print('&eYou pulled the lever! Good for you...')
    state['num_levers_pulled'] = state.get('num_levers_pulled', 0) + 1

    if state['num_levers_pulled'] == 2:
        IO.print('&eThe task fairy cried and opened the exits for you!')
        if isinstance(room_id, list):
            state['unlocked_rooms'] += room_id
        else:
            state['unlocked_rooms'] += [room_id]


def start():
    IO.clear_console()
    state = {
        'player': None,
        'cur_room': None,
        'rooms_entered': [],
        'id_counter': 0,
        'unlocked_rooms': [],
        'quit': False,
    }

    # Player definitions
    player = Entity(state, 'Player', 100, 100)
    player.set_death_action(player_death)

    # Entity defintions
    goblin = Entity(state, 'Goblin Dude', 10, 0, 'This is a goblin!')
    goblin.add_action(partial(entity_action, damage=5))
    goblin.set_death_action(entity_death)

    # Room definitions
    start_room = Room(state, 'Spawn Room', '')
    training_room = Room(state, 'Combat Training', 'You should look around the room.')
    east_room = Room(state, 'East Room', 'You notice a big swith in the corner of the room.')
    south_room = Room(state, 'South Room', 'You notice a big switch in the corner of the room.')
    final_room = Room(state, 'Final Room', 'You notice a big plaque that says \'End of Demo\'.')

    start_room.adj_rooms['east'] = training_room
    start_room.entities.append(goblin)
    start_room.set_task_complete_action(partial(complete_task, room_id=training_room.id))
    start_room.add_task(task_entity_check)
    start_room.thingies['Sword'] = give_sword
    
    training_room.adj_rooms['south'] = south_room
    training_room.adj_rooms['east'] = east_room
    training_room.set_task_complete_action(partial(complete_task, room_id=[south_room.id, east_room.id]))
    training_room.add_task(task_potion_check)
    training_room.thingies['Chest'] = use_chest

    south_room.adj_rooms['north'] = training_room
    south_room.adj_rooms['east'] = final_room
    south_room.thingies['lever'] = partial(pull_lever, room_id=final_room.id)

    east_room.adj_rooms['west'] = training_room
    east_room.adj_rooms['south'] = final_room
    east_room.thingies['lever'] = partial(pull_lever, room_id=final_room.id)
    
    # Set original state
    state['unlocked_rooms'] += [start_room.id]
    state['player'] = player
    state['cur_room'] = start_room

    game_loop(state)


def game_loop(state):
    while not state['quit']:
        should_proceed = False
        while not should_proceed:
            should_proceed = IO.prompt(state, 'What do you want to do next?')

        state['cur_room'].tick(state)

    IO.print('&2Thanks for playing!')

