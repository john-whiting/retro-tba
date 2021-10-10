from utils.io import IO

#Action commands

def go(state, dir: str = '') -> bool:
    if not (dir in state['cur_room'].adj_rooms.keys()):
        IO.print('&cYou just ran into a wall.')
        return False

    next_room = state['cur_room'].adj_rooms[dir]

    if not (next_room.id in state['unlocked_rooms']):
        IO.print('&cThat door is locked, idiot!')
        return False

    state['cur_room'].on_leave(state)
    state['cur_room'] = next_room
    state['cur_room'].on_enter(state)

    return True

def inspect(state, name: str = '') -> bool:
    for thingy, func in state['cur_room'].thingies.items():
        if thingy.lower() == name:
            should_remove = func(state)
            if should_remove:
                del state['cur_room'].thingies[thingy] 
            return True
    IO.print('&cYou are inspecting nothing!')
    return False


def use(state, *args) -> bool:
    if 'on' in args:
        on_idx = args.index('on')
        item_name = (' '.join(args[0:on_idx])).lower()
        entity_name = (' '.join(args[on_idx+1:])).lower()
    else:
        item_name = ' '.join(args)
        entity_name = ''

    item = state['player'].get_item(state, item_name)
    if item is None:
        IO.print('&cYou don\'t have that item, idiot!')
        return False

    if item.target_required:
        cur_entities = {entity.name.lower(): entity for entity in state['cur_room'].entities}
        if not (entity_name in cur_entities.keys()):
            IO.print('&cYou used that item on nothing!')
            return False
        item.use(state, cur_entities[entity_name])
    else:
        item.use(state, state['player'])
    return True

###########################################################################

#Info Commands

def help(state) -> bool:
    IO.print(
"""
&l&1--------------------------------
&eHere is a list of all commands:

&eThese commands use up your turn, they are &laction &ecommands:
&2go <direction> - &1Use this to navigate between rooms (some rooms are one way only)
&2inspect <oddity> - &1Use this to interact with different oddities in a room
&2use <item name> [on] [entity name] - &1Use this to use an item either on yourself or on an entity

&eThese commands do not use up your turn, they are &linformational &ecommands:
&2help - &1Use this to display the different commands you can run
&2info <item name> - &1Use this to display the description of an item
&2inventory - &1Use this to view the different items in your inventory
&2look - &1Use this to view the attributes of the room, like inspectables, adjacent rooms, and entities
&2status - &1Use this to view your stats like HP, Mana Points, and your current status effects

&2quit - &1This will exit the game at any time
&l&1--------------------------------
"""
    )
    return False

def info(state, item_name: str = '') -> bool:
    item = state['player'].get_item(state, item_name)
    if item is None:
        IO.print('&cYou don\'t have that item, idiot!')
        return False

    IO.print(f'&eYou examine {item.name}...')
    IO.print(f'&2{item.desc}')
    return False

def inventory(state) -> bool:
    for item in state['player'].usables:
        IO.print(f'&1{item.name} - &2{item.desc}')
    return False

def look(state) -> bool:
    if len(state['cur_room'].adj_rooms) == 0:
        IO.print('&eYou observe no exits.')
    else:
        IO.print('&eYou observe the following exits:')
        for dir in state['cur_room'].adj_rooms.keys():
            IO.print(f'&f- &2{dir}')

    if len(state['cur_room'].entities) == 0:
        IO.print('&eYou observe no creatures.')
    else:
        IO.print('&eYou observe the following creatures in the room:')
        for entity in state['cur_room'].entities:
            IO.print(f'&f- &2{entity.name}')

    if len(state['cur_room'].thingies) == 0:
        IO.print('&eYou observe no oddities.')
    else:
        IO.print('&eYou observe the following oddities in the room:')
        for thingy in state['cur_room'].thingies.keys():
            IO.print(f'&f- &2{thingy}')


def status(state) -> bool:
    IO.print(f'&cHP: {state["player"].hp}')
    IO.print(f'&cMana: {state["player"].mana}')  
    
    for status in state['player'].statuses:
        IO.print(f'&1{status.name} - &2{status.desc}')

def quit(state):
    state['quit'] = True
    return True

commands = {
    'go': go,
    'use': use,
    
    'help': help,
    'info': info,
    'inspect': inspect,
    'inventory': inventory,
    'look': look,
    'status': status,

    'quit': quit,
}