import logging
import random

logger = logging.getLogger(__name__)


class Conversation:
    def __init__(self, game, engine, xhr, version, challenge_queue):
        self.game = game
        self.engine = engine
        self.xhr = xhr
        self.version = version
        self.challengers = challenge_queue

    command_prefix = "!"

    def react(self, line, game):
        logger.info("*** {} [{}] {}: {}".format(self.game.url(), line.room, line.username, line.text.encode("utf-8")))
        if (line.text[0] == self.command_prefix):
            self.command(line, game, line.text[1:].lower())

    def command(self, line, game, cmd):
        if cmd == "commands" or cmd == "help":
            self.send_reply(line, "Supported commands: !wait, !name, !howto, !eval, !queue, !chessmodels")
        elif cmd == "wait" and game.is_abortable():
            game.ping(60, 120)
            self.send_reply(line, "Waiting 60 seconds...")
        elif cmd == "name":
            name = game.me.name
            self.send_reply(line, "{} using c++ and java codes running {} (lichess-bot v{}) on heroku server.".format(name, self.engine.name(), self.version))
        elif cmd == "id":
            self.send_reply(line, "RaviharaV")
        elif cmd == "howto":
            self.send_reply(line, "How to run your own bot: Check out 'Lichess Bot API' or go to https://github.com/LichessBot-Coders/Lichess-Coded-Bot")
        elif cmd == "eval":
            stats = self.engine.get_stats()
            self.send_reply(line, ", ".join(stats))
        elif cmd == "eval":
            self.send_reply(line, "That's the evaluation of the position according to my engine! ")
        elif cmd == "queue":
            if self.challengers:
                challengers = ", ".join(["@" + challenger.challenger_name for challenger in reversed(self.challengers)])
                self.send_reply(line, "Challenge queue: {}".format(challengers))
            else:
                self.send_reply(line, "No challenges queued. Wait for my current game to finish then kindly challenge.")
        elif cmd == "chessmodels":
             random = random.randint(Good players develop a tactical instinct, The most important feature of the chess position is the activity of the pieces, I prefer to lose a really good game than to win a bad one, Without error there can be no brilliancy, One of these modest little moves may be more embarrassing to your opponent than the biggest threat, Chess strength in general and chess strength in a specific match are by no means one and the same thing)
            self.send_reply(line, ", ".join(random))

    def send_reply(self, line, reply):
        self.xhr.chat(self.game.id, line.room, reply)


class ChatLine:
    def __init__(self, json):
        self.room = json.get("room")
        self.username = json.get("username")
        self.text = json.get("text")
