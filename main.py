import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os

class BlackjackGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Blackjack Game")
        self.master.geometry("800x600")
        
        self.suits = ['H', 'D', 'C', 'S']
        self.values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.deck = [f"{v}{s}" for s in self.suits for v in self.values]
        self.score = 0
        
        self.player_hand = []
        self.dealer_hand = []
        
        self.card_images = {}
        self.load_card_images()
        
        self.setup_ui()
        self.new_game()

    def load_card_images(self):
        for card in self.deck:
            image = Image.open(f"cards/{card}.png")
            image = image.resize((100, 150), Image.LANCZOS)
            self.card_images[card] = ImageTk.PhotoImage(image)
        self.card_back = ImageTk.PhotoImage(Image.open("cards/BACK.png").resize((100, 150), Image.LANCZOS))

    def setup_ui(self):
        self.player_frame = tk.Frame(self.master)
        self.player_frame.pack(side=tk.BOTTOM, pady=20)

        self.dealer_frame = tk.Frame(self.master)
        self.dealer_frame.pack(side=tk.TOP, pady=20)

        # Score frame (in the middle)
        score_frame = tk.Frame(self.master)
        score_frame.pack(expand=True)

        self.score_label = tk.Label(score_frame, text=f"Score: {self.score}", font=('Arial', 16))
        self.score_label.pack()

        self.player_total_label = tk.Label(score_frame, text="Your total:", font=('Arial', 14))
        self.player_total_label.pack()

        # Button frame (bottom right)
        button_frame = tk.Frame(self.master)
        button_frame.pack(side=tk.BOTTOM, anchor='se', padx=20, pady=20)

        button_width = 10
        button_height = 2

        self.play_button = tk.Button(button_frame, text="Confirm", command=self.play, 
                                    width=button_width, height=button_height)
        self.play_button.grid(row=0, column=0, padx=5, pady=5)

        self.new_game_button = tk.Button(button_frame, text="New Game", command=self.new_game, 
                                        width=button_width, height=button_height)
        self.new_game_button.grid(row=0, column=1, padx=5, pady=5)  

    def new_game(self):
        self.deck = [f"{v}{s}" for s in self.suits for v in self.values]
        random.shuffle(self.deck)
        
        self.player_hand = []
        self.dealer_hand = []
        
        for _ in range(3):
            self.player_hand.append(self.draw_card())
            self.dealer_hand.append(self.draw_card())
        
        self.update_display()

    def draw_card(self):
        return self.deck.pop()

    def calculate_hand(self, hand):
        total = 0
        aces = 0
        for card in hand:
            value = card[:-1]  # Remove the suit
            if value in ['J', 'Q', 'K']:
                total += 10
            elif value == 'A':
                aces += 1
            else:
                total += int(value)
        
        for _ in range(aces):
            if total + 11 <= 21:
                total += 11
            else:
                total += 1
        
        return total

    def update_display(self):
        for widget in self.player_frame.winfo_children():
            widget.destroy()
        for widget in self.dealer_frame.winfo_children():
            widget.destroy()

        for card in self.player_hand:
            # tk.Label(self.player_frame, image=self.card_images[card]).pack(side=tk.LEFT)
            tk.Label(self.player_frame, image=self.card_back).pack(side=tk.LEFT)

        for i, card in enumerate(self.dealer_hand):
            if i == 0:
                # tk.Label(self.dealer_frame, image=self.card_images[card]).pack(side=tk.LEFT)
                tk.Label(self.dealer_frame, image=self.card_back).pack(side=tk.LEFT)
            else:
                tk.Label(self.dealer_frame, image=self.card_back).pack(side=tk.LEFT)

        player_total = self.calculate_hand(self.player_hand)
        self.player_total_label.config(text=f"Your total: {player_total}")
        self.score_label.config(text=f"Score: {self.score}")

    def play(self):
        player_total = self.calculate_hand(self.player_hand)
        dealer_total = self.calculate_hand(self.dealer_hand)

        if player_total > 21 and dealer_total > 21:
            result = "Both busted! It's a tie!"
        elif player_total > 21:
            result = "You busted!"
            self.score -= 1
        elif dealer_total > 21:
            result = "Dealer busted! You win!"
            self.score += 1
        elif player_total > dealer_total:
            result = "You win!"
            self.score += 1
        elif player_total < dealer_total:
            result = "You lose!"
            self.score -= 1
        else:
            result = "It's a tie!"

        # Show dealer's cards
        for widget in self.dealer_frame.winfo_children():
            widget.destroy()
        for card in self.dealer_hand:
            tk.Label(self.dealer_frame, image=self.card_images[card]).pack(side=tk.LEFT)

        messagebox.showinfo("Game Result", f"{result}\nYour total: {player_total}\nDealer's total: {dealer_total}")
        self.update_display()
        self.new_game()

if __name__ == "__main__":
    root = tk.Tk()
    game = BlackjackGame(root)
    root.mainloop()
