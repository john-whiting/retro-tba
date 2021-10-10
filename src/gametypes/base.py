class Base:
    id: int
    name: str
    desc: str

    def __init__(self, state, name: str, desc: str = ''):
        state['id_counter'] += 1
        self.id = state['id_counter']
        self.name = name
        self.desc = desc