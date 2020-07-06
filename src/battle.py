class Battle:
    def __init__(self, showdown, roomid:str, title:str = None):
        self.showdown = showdown
        self.roomid = roomid
        self.players = {}
        if roomid:
            self.title = title

    def set_title(self, title):
        self.title = title

    def set_player(self, player_num:int, username:str, rating:int = None):
        self.players[player_num] = {
            "USERNAME" : username,
            "POKEMON" : {}
        }
        if rating:
            self.players[player_num]["RATING"] = rating

    def set_party(self, player_num:int, username:str, pokemon:[dict]):
        if player_num not in self.players:
            self.set_player(player_num, username)
        for slot, pkmn in enumerate(pokemon):
            self.set_pokemon(player_num, slot + 1, pkmn)

    def set_pokemon(self, player_num:int, pokemon_slot:int, pokemon:dict):
        pokemon_list = self.players[player_num]["POKEMON"]
        pokemon_list[pokemon_slot] = pokemon
