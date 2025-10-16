import random
import time
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

# load environment variables for the API key
load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

# initialize the model
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3, api_key=OPENAI_KEY)


def draw_card():
    # draw a number between 2 and 11
    return random.randint(2, 11)

class Dealer:
    def __init__(self):
        self.players = {}

    def register_player(self, name):
        self.players[name] = []

    def deal_card(self, player):
        card = draw_card()
        self.players[player].append(card)
        print(f"Dealer gives {player} a card: {card}")
        return card

    def total(self, player):
        return sum(self.players[player])

    def show_hand(self, player):
        cards = self.players[player]
        total = self.total(player)
        print(f"{player}'s cards: {cards} (Total: {total})")
        return total

def ai_decision(player, cards):
    prompt = (
        f"You are {player} playing a card game. "
        f"Your cards are {cards}. The total is {sum(cards)}. "
        "Say only 'hit' if you want another card or 'stand' if you want to stop."
    )
    response = llm.invoke([HumanMessage(content=prompt)]).content.lower()
    if "hit" in response:
        print(f"{player} wants another card.")
        return "hit"
    else:
        print(f"{player} stops here.")
        return "stand"

def play_game():
    print("\nWelcome! Let's start the game.\n")
    dealer = Dealer()
    players = ["You", "AI_1", "AI_2", "AI_3"]

    for p in players:
        dealer.register_player(p)
        dealer.deal_card(p)

    for p in players:
        print(f"\nNow it's {p}'s turn.")
        while len(dealer.players[p]) < 3:
            total = dealer.total(p)
            if total >= 21:
                break

            if p == "You":
                move = input("Type 'next' for a card or 'stop' to stay: ").lower()
                if "next" in move:
                    dealer.deal_card(p)
                elif "stop" in move:
                    print("You decided to stop.")
                    break
                else:
                    print("Try typing 'next' or 'stop'.")
                    continue
            else:
                decision = ai_decision(p, dealer.players[p])
                if decision == "hit":
                    dealer.deal_card(p)
                else:
                    break

            dealer.show_hand(p)
            if dealer.total(p) > 21:
                print(f"{p} went over 21!")
                break
            time.sleep(1)

    print("\nGame results:")
    scores = {}
    for p in players:
        total = dealer.total(p)
        dealer.show_hand(p)
        if total <= 21:
            scores[p] = total

    if not scores:
        print("No winner.")
    else:
        winner = max(scores, key=scores.get)
        print(f"Winner: {winner} with {scores[winner]} points.")

    print("\nGame over.")

if __name__ == "__main__":
    play_game()
