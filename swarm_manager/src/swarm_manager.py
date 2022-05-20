from random import choice

from http_mock.src.http_mock import HttpMock
from swarm_manager.src.swarm_connectivity_level import SwarmConnectivityLevel
from swarm_bot.src.swarm_bot import SwarmBot

class SwarmManager(object):
    def __init__(self, swarm_connectivity_level: SwarmConnectivityLevel):
        self.swarm_connectivity_level = swarm_connectivity_level

        self.http_mock = HttpMock()

        self.central_swarm_bot = None

        self.swarm_bots = {}

    def add_swarm_bot(self, new_bot: SwarmBot) -> None:
        if self.swarm_connectivity_level == SwarmConnectivityLevel.FULLY_CONNECTED:
            for bot_id, bot in self.swarm_bots.items():
                bot.connect_to_swarm_bot(new_bot)
                new_bot.connect_to_swarm_bot(bot)
        elif self.swarm_connectivity_level == SwarmConnectivityLevel.PARTIALLY_CONNECTED:
            if len(self.swarm_bots.keys()) > 0:
                connected_bot_id, connected_bot = choice(list(self.swarm_bots.items()))
                connected_bot.connect_to_swarm_bot(new_bot)
                new_bot.connect_to_swarm_bot(connected_bot)
        elif self.swarm_connectivity_level == SwarmConnectivityLevel.CENTRALIZED:
            if len(self.swarm_bots.keys()) == 0:
                self.central_swarm_bot = new_bot
            else:
                self.central_swarm_bot.connect_to_swarm_bot(new_bot)
                new_bot.connect_to_swarm_bot(self.central_swarm_bot)
        else:
            raise Exception("ERROR: unknown connectivity level: " + str(self.swarm_connectivity_level))

        new_id = new_bot.get_id()
        if new_id not in self.swarm_bots:
            self.swarm_bots[new_id] = new_bot

        new_bot.set_http_mock(self.http_mock)

    def get_central_swarm_bot(self):
        return self.central_swarm_bot

    def get_swarm_bots(self):
        return self.swarm_bots