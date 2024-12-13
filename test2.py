import tkinter as tk
from tkinter import messagebox
import random

# 定义卡牌类
class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{self.value}{self.suit}"

# 定义游戏类
class CardGame:
    def __init__(self, master):
        self.master = master
        self.master.title("卡牌游戏")
        
        self.deck = self.create_deck()
        self.player_hand = []
        self.computer_hand = []
        self.pool = []
        self.player_score = 0
        self.computer_score = 0
        
        self.player_turn = True
        self.setup_game()
        self.setup_ui()
        
    def create_deck(self):
        suits = ['♠', '♥', '♦', '♣']
        values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        return [Card(suit, value) for suit in suits for value in values]
    
    def setup_game(self):
        random.shuffle(self.deck)
        self.player_hand = [self.deck.pop() for _ in range(5)]
        self.computer_hand = [self.deck.pop() for _ in range(5)]
        self.pool = [self.deck.pop() for _ in range(10)]
    
    def setup_ui(self):
        # 创建电脑手牌区域
        self.computer_frame = tk.Frame(self.master)
        self.computer_frame.pack(side=tk.TOP, pady=10)
        
        # 创建池子区域
        self.pool_frame = tk.Frame(self.master)
        self.pool_frame.pack(side=tk.TOP, pady=10)
        
        # 创建玩家手牌区域
        self.player_frame = tk.Frame(self.master)
        self.player_frame.pack(side=tk.BOTTOM, pady=10)
        
        # 创建信息显示区域
        self.info_frame = tk.Frame(self.master)
        self.info_frame.pack(side=tk.TOP, pady=10)
        
        self.deck_label = tk.Label(self.info_frame, text=f"牌堆剩余: {len(self.deck)}")
        self.deck_label.pack(side=tk.LEFT, padx=10)
        
        self.score_label = tk.Label(self.info_frame, text=f"玩家得分: {self.player_score} | 电脑得分: {self.computer_score}")
        self.score_label.pack(side=tk.LEFT, padx=10)
        
        # 添加游戏提示文字栏
        self.message_label = tk.Label(self.master, text="游戏开始, 请点击牌配对成 10", font=("Arial", 12), wraplength=400)
        self.message_label.pack(side=tk.BOTTOM, pady=10)
        
        self.update_ui()
    
    def update_ui(self):
        # 更新电脑手牌
        for widget in self.computer_frame.winfo_children():
            widget.destroy()
        for _ in range(len(self.computer_hand)):
            tk.Label(self.computer_frame, text="*", font=("Arial", 12), width=4, height=2, bg="light blue", relief="raised").pack(side=tk.LEFT, padx=2)
        
        # 更新池子
        for widget in self.pool_frame.winfo_children():
            widget.destroy()
        for card in self.pool:
            tk.Label(self.pool_frame, text=f"{card.value}\n{card.suit}", font=("Arial", 20), width=2, height=2, relief="raised").pack(side=tk.LEFT, padx=2)
        
        for widget in self.player_frame.winfo_children():
            widget.destroy()
        for card in self.player_hand:
            can_match = self.find_match(card) is not None
            btn = tk.Button(self.player_frame, text=f"{card.value}\n{card.suit}", font=("Arial", 20), width=2, height=2, 
                            command=lambda c=card: self.player_move(c))
            if can_match:
                btn.config(bg="light yellow", highlightthickness=2, highlightbackground="red")
            else:
                btn.config(state=tk.DISABLED)
            btn.pack(side=tk.LEFT, padx=2)
        
        # 更新信息
        self.deck_label.config(text=f"牌堆剩余: {len(self.deck)}")
        self.score_label.config(text=f"玩家得分: {self.player_score} | 电脑得分: {self.computer_score}")
    
    def player_move(self, selected_card):
        if not self.player_turn:
            self.show_message("当前轮到：电脑 - 请等待电脑操作")
            return

        matched_card = self.find_match(selected_card)
        if matched_card:
            self.player_hand.remove(selected_card)
            self.pool.remove(matched_card)
            self.player_score += 10
            self.replenish_cards()
            self.player_turn = False
            self.update_ui()
            self.show_message(f"当前轮到：你 - 匹配了 {selected_card} 和 {matched_card}")
            self.master.after(1000, self.computer_move)
        else:
            self.show_message("当前轮到：你 - 这张牌无法匹配，请选择其他牌")
            return
        
        self.check_game_over()
        self.update_ui()

    
    def computer_move(self):
        if self.player_turn:
            return

        for card in self.computer_hand:
            matched_card = self.find_match(card)
            if matched_card:
                self.computer_hand.remove(card)
                self.pool.remove(matched_card)
                self.computer_score += 10
                self.replenish_cards()
                self.show_message(f"当前轮到：电脑 - 匹配了 {card} 和 {matched_card}")
                break
        else:
            self.show_message("当前轮到：电脑 - 电脑没有可以匹配的牌")
        
        self.player_turn = True
        self.check_game_over()
        self.update_ui()
        
    def show_message(self, message):
        self.message_label.config(text=message)
    
    def check_game_over(self):
        if not self.player_hand or not self.computer_hand or (not self.find_any_match()):
            winner = "平局"
            if self.player_score > self.computer_score:
                winner = "玩家获胜"
            elif self.computer_score > self.player_score:
                winner = "电脑获胜"
            self.show_message(f"游戏结束 - {winner}!\n玩家得分: {self.player_score}\n电脑得分: {self.computer_score}")
            self.master.after(3000, self.master.quit)  # 3秒后关闭游戏
    
    def replenish_cards(self):
        if self.deck:
            if len(self.player_hand) < 5:
                self.player_hand.append(self.deck.pop())
            if len(self.computer_hand) < 5:
                self.computer_hand.append(self.deck.pop())
        if self.deck and len(self.pool) < 10:
            self.pool.append(self.deck.pop())
    
    def find_match(self, card):
        card_value = self.get_card_value(card.value)
        for pool_card in self.pool:
            pool_value = self.get_card_value(pool_card.value)
            if (card_value + pool_value == 10) or (card.value in ['J', 'Q', 'K'] and card.value == pool_card.value) or \
               (card.value == '10' and pool_card.value == '10'):
                return pool_card
        return None
    
    def get_card_value(self, value):
        if value in ['J', 'Q', 'K']:
            return 10
        elif value == 'A':
            return 1
        else:
            return int(value)

    
    def check_game_over(self):
        if not self.player_hand or not self.computer_hand or (not self.find_any_match()):
            winner = "平局"
            if self.player_score > self.computer_score:
                winner = "玩家获胜"
            elif self.computer_score > self.player_score:
                winner = "电脑获胜"
            messagebox.showinfo("游戏结束", f"{winner}!\n玩家得分: {self.player_score}\n电脑得分: {self.computer_score}")
            self.master.quit()
    
    def find_any_match(self):
        for card in self.player_hand + self.computer_hand:
            if self.find_match(card):
                return True
        return False

# 创建主窗口并运行游戏
root = tk.Tk()
game = CardGame(root)
root.mainloop()
