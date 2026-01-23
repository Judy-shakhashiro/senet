from GameEngine.State import State
from GameEngine.Chance import Chance
from GameEngine.Player import RandomPlayer, LastPawnPlayer, HumanPlayer
from AI.AIPlayer import AIPlayer



def choose_player(player_number, chance):
    print(f" Choose your player {player_number}")
    print("1- AI")
    print("2- Human")
    print("3- Random")
    print("4- Last Pawn")

    while True:
        choice = input("Your choice: ")

        if choice == "1":
            depth = int(input("Enter depth into the search :"))
            return AIPlayer(chance, depth), True

        elif choice == "2":
            return HumanPlayer(), False

        elif choice == "3":
            return RandomPlayer(), False

        elif choice == "4":
            return LastPawnPlayer(), False

        else:
            print("Invalid Choose")


def main():

    state = State()
    chance = Chance()

    player1, debug1 = choose_player(1, chance)
    player2, debug2 = choose_player(2, chance)

    print("The game has started")
    state.play_two_players(
        player1,
        player2,
        chance,
        debug1=debug1,
        debug2=debug2
    )



if __name__ == "__main__":
    main()
