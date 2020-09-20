class Battle:
    def __init__(self, showdown, roomid:str, title:str = None):
        self.showdown = showdown
        self.roomid = roomid
        self.players = [None] * 2
        if title:
            self.title = title

    def set_title(self, title:str):
        self.title = title

    def get_title(self):
        return self.title

    def new_player(self, player_id:int, username:str, rating:int = None):
        self.players[player_id - 1] = Player(username)

    def get_player(self, player_id:int):
        return self.players[player_id - 1]

    def set_party(self, player_id:int, party:[Pokemon]):
        self.players[player_id].set_party(party)

    def set_pokemon(self, player_id:int, pokemon_slot:int, pokemon:Pokemon):
        self.players[player_id].set_pokemon(pokemon_slot, pokemon)

class Player:
    def __init__(self, username):
        self.username = username
        self.party = [None] * 6

    def set_username(self, username:str):
        self.username = username

    def set_party(self, party:[Pokemon]):
        for slot, pkmn in enumerate(party):
            self.set_pokemon(slot + 1, pkmn)

    def set_pokemon(self, pokemon_slot:int, pokemon:Pokemon):
        self.party[pokemon_slot - 1] = pokemon

class Pokemon:
    def __init__(self, species:str, nickname:str, gender:str, level:int, shiny:bool):
        self.species = species
        self.nickname = nickname
        self.gender = gender
        self.level = level
        self.moves = [None] * 4
        self.major_condition = None
        self.shiny = shiny
        self.minor_conditions = set()

    def is_shiny(self):
        return shiny

    def set_major_condition(self, major_condition):
        self.major_condition = major_condition

    def get_major_condition(self):
        return self.major_condition

    def add_minor_condition(self, minor_condition):
        self.minor_conditions.add(minor_condition)

    def remove_minor_condition(self, minor_condition):
        self.minor_conditions.remove(minor_condition)

    def set_item(self, item:str):
        self.item = item

    def get_item(self):
        return self.item

    def set_ability(self, ability:str):
        self.ability = ability

    def get_ability(self):
        return self.ability

    def set_move(self, move_slot:int, move:str):
        self.moves[move_slot - 1] = move

    def set_moves(self, moves:[str]):
        for slot, move in enumerate(moves):
            set_move(slot + 1, move)

    def get_move(self, move_slot:int):
        return self.moves[move_slot - 1]

    def set_hp(self, hp:int):
        self.hp = hp

    def get_hp(self):
        return self.hp

    def set_current_hp(self, current_hp:int):
        self.set_current_hp = current_hp

    def get_current_hp(self):
        return self.current_hp

    def set_atk(self, atk:int):
        self.atk = atk

    def get_atk(self):
        return self.atk

    def set_def(self, def:int):
        self.def = def

    def get_def(self):
        return self.def

    def set_spa(self, spa:int):
        self.spa = spa

    def get_spa(self):
        return self.spa

    def set_spd(self, spd:int):
        self.spd = spd

    def get_spd(self):
        return self.spd

    def set_spe(self, spe:int):
        self.spe = spe

    def get_spe(self):
        return self.spe
