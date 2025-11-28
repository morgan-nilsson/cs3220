from MiseryGame import MiseryGame
from src.gameClass import play_game
from src.players import random_player, smart_player
from src.algorithms import minimax_search

def main():

    strategies = {
        "Smart player": smart_player(minimax_search),
        "Random player": random_player,
    }

    players = list(strategies.keys())

    game = MiseryGame(players, game_over_at=5)


    final_state = play_game(game, strategies, verbose=True)
    print("Final state:", final_state, "Winner:", final_state.to_move)
    print("Game over.")

    print("================================================")

    def human_player(game, state):
        print(f"Current state: {state}")
        moves = game.actions(state)
        print(f"Available moves: {moves}")
        while True:
            try:
                move = int(input("Enter your move: "))
                if move in moves:
                    return move
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Please enter a valid integer.")

    strategies = {
        "Human player": human_player,
        "Smart player": smart_player(minimax_search),
    }

    players = list(strategies.keys())

    game = MiseryGame(players, game_over_at=5)

    final_state = play_game(game, strategies, verbose=True)
    print("Final state:", final_state, "Winner:", final_state.to_move)
    print("Game over.")

if __name__ == "__main__":
    main()