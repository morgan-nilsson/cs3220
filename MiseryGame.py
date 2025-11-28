from src.gameClass import Game

class State:
    def __init__(self, to_move: str, total: int):
        self.to_move = to_move
        self.total = total

    def __repr__(self) -> str:
        return f"State(to_move={self.to_move}, total={self.total})"

class MiseryGame(Game):
    def __init__(self, players, game_over_at=5):
        self.initial = State(to_move=players[0], total=1)
        self.game_over_at = game_over_at
        self.players = players

    def actions(self, state):
        return [1, 2, 3]

    def result(self, state, move):
        new_total = state.total + move
        next_player = self.players[1] if state.to_move == self.players[0] else self.players[0]
        return State(to_move=next_player, total=new_total)

    def is_terminal(self, state):
        return state.total >= self.game_over_at
    
    def utility(self, state, player):
        if self.is_terminal(state):
            if state.to_move == player:
                return 1  # Current player wins
            else:
                return -1  # Current player loses