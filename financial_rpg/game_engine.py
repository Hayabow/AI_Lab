#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ゲームエンジン
"""

from player import Player
from party import Party
from monster import get_random_monster, create_monster
from battle import Battle
from shop import Shop
from f_ticket import FTicketSystem, EconomyCondition
import random

class GameEngine:
    """ゲームエンジンクラス"""
    
    def __init__(self):
        self.player = Player()
        self.f_ticket_system = FTicketSystem()
        self.shop = Shop(self.player, self.f_ticket_system)
        self.current_area = 1
        self.story_progress = 0
    
    def start(self):
        """ゲーム開始"""
        print("\nようこそ、金融知識学習RPGへ！")
        print("このゲームでは、冒険を通じて金融の知識を学ぶことができます。\n")
        
        # 名前入力
        name = input("あなたの名前を入力してください: ").strip()
        if not name:
            name = "冒険者"
        
        self.player.create_main_character(name)
        
        # ストーリー開始
        self._show_intro_story()
        
        # メインループ
        self._main_loop()
    
    def _show_intro_story(self):
        """イントロストーリーを表示"""
        print("\n" + "=" * 60)
        print("プロローグ")
        print("=" * 60)
        print("""
金融の世界に住むあなたは、経済の混乱を引き起こすモンスターたちと
戦う冒険者として、この世界を救う使命を負っています。

モンスターを倒すと、お金と「F券」という特別な報酬がもらえます。
F券はエリアの経済情勢に応じて価値が変動するため、
タイミングを見極めて武器や防具と交換することが重要です。

また、モンスターは一定の確率で仲間になり、あなたのパーティを
強化してくれます。

さあ、冒険を始めましょう！
""")
        input("Enterキーで続ける...")
    
    def _main_loop(self):
        """メインゲームループ"""
        while True:
            print("\n" + "=" * 60)
            print("メインメニュー")
            print("=" * 60)
            print(f"エリア: {self.current_area}")
            print(f"所持金: {self.player.gold}G")
            print(f"F券: {self.player.f_tickets}枚")
            f_ticket_value = self.f_ticket_system.get_current_value()
            print(f"F券1枚の現在の価値: {f_ticket_value}G")
            print(f"経済状況: {self.f_ticket_system.current_condition.value}")
            print()
            print("1. 冒険に出る（戦闘）")
            print("2. ショップに行く")
            print("3. パーティを確認")
            print("4. 経済情勢を確認")
            print("5. 金融知識を学ぶ")
            print("0. ゲームを終了")
            print()
            
            choice = input("選択してください: ").strip()
            
            if choice == "0":
                print("\nゲームを終了します。お疲れ様でした！")
                break
            elif choice == "1":
                self._start_adventure()
            elif choice == "2":
                self.shop.show_menu()
            elif choice == "3":
                self._show_party()
            elif choice == "4":
                self._show_economy_status()
            elif choice == "5":
                self._show_financial_knowledge()
            else:
                print("無効な選択です。")
    
    def _start_adventure(self):
        """冒険を開始（戦闘）"""
        print("\n" + "=" * 60)
        print("冒険に出発！")
        print("=" * 60)
        
        # 経済状況が変動する可能性
        if random.random() < 0.3:  # 30%の確率で変動
            self.f_ticket_system.change_condition()
            print(f"\n経済情勢が変動しました！")
            print(f"現在の経済状況: {self.f_ticket_system.current_condition.value}")
            print(self.f_ticket_system.get_condition_description())
        
        # パーティの状態を回復
        self.player.party.heal_all(999)
        self.player.party.restore_all_mp(999)
        
        # 敵の生成
        enemy_party = Party()
        num_enemies = random.randint(1, 3)
        for _ in range(num_enemies):
            monster = get_random_monster(self.current_area)
            enemy_party.add_member(monster)
        
        print(f"\n{num_enemies}体のモンスターが現れた！")
        for enemy in enemy_party.members:
            print(f"  - {enemy.name}")
        
        input("\nEnterキーで戦闘開始...")
        
        # 戦闘実行
        battle = Battle(self.player.party, enemy_party)
        result = battle.execute_battle()
        
        if result['victory']:
            # 報酬を受け取る
            self.player.add_gold(result['rewards']['gold'])
            self.player.add_f_tickets(result['rewards']['f_tickets'])
            
            # 経験値とレベルアップ
            exp_gain = sum([e.level * 20 for e in enemy_party.members])
            for member in self.player.party.members:
                if member.is_alive():
                    leveled_up = member.add_experience(exp_gain)
                    if leveled_up:
                        print(f"\n{member.name}がレベルアップ！")
                        print(f"レベル {member.level - 1} → {member.level}")
            
            # モンスターを仲間に追加
            for monster in result['recruited_monsters']:
                # モンスターをリセット（HP/MP回復）
                monster.hp = monster.max_hp
                monster.mp = monster.max_mp
                self.player.party.add_member(monster)
            
            # ストーリー進行
            self.story_progress += 1
            if self.story_progress % 5 == 0:
                self._show_story_event()
        else:
            # 敗北時のペナルティ
            print("\n敗北により、報酬は受け取れませんでした...")
            self.player.gold = max(0, self.player.gold - 50)
        
        input("\nEnterキーでメインメニューに戻る...")
    
    def _show_party(self):
        """パーティを表示"""
        print("\n" + "=" * 60)
        print("パーティ状態")
        print("=" * 60)
        if not self.player.party.members:
            print("パーティメンバーがいません。")
        else:
            for member in self.player.party.members:
                print(f"\n{member}")
                if member.equipped_weapon:
                    print(f"  武器: {member.equipped_weapon.name}")
                if member.equipped_armor:
                    print(f"  防具: {member.equipped_armor.name}")
        
        input("\nEnterキーで戻る...")
    
    def _show_economy_status(self):
        """経済情勢を表示"""
        print("\n" + "=" * 60)
        print("経済情勢")
        print("=" * 60)
        print(f"現在の経済状況: {self.f_ticket_system.current_condition.value}")
        print(self.f_ticket_system.get_condition_description())
        print(f"\nF券1枚の現在の価値: {self.f_ticket_system.get_current_value()}G")
        print(f"所持F券: {self.player.f_tickets}枚")
        total_value = self.f_ticket_system.calculate_total_value(self.player.f_tickets)
        print(f"F券の合計価値: {total_value}G")
        
        if len(self.f_ticket_system.condition_history) > 1:
            print("\n最近の経済変動:")
            for condition in self.f_ticket_system.condition_history[-5:]:
                print(f"  - {condition.value}")
        
        input("\nEnterキーで戻る...")
    
    def _show_financial_knowledge(self):
        """金融知識を表示"""
        print("\n" + "=" * 60)
        print("金融知識")
        print("=" * 60)
        print(self.f_ticket_system.get_financial_knowledge())
        print()
        print("【金融の基礎知識】")
        print("""
1. インフレーション（インフレ）
   - 物価が継続的に上昇する現象
   - お金の価値が下がるため、同じ金額で買えるものが減る

2. デフレーション（デフレ）
   - 物価が継続的に下落する現象
   - お金の価値が上がるが、経済が停滞する可能性がある

3. 金利
   - お金を借りたり貸したりする際の費用
   - 経済状況に応じて変動する

4. 株式
   - 企業の所有権の一部を表す証券
   - 企業の業績に応じて価値が変動する

5. 為替
   - 異なる通貨を交換する際のレート
   - 国際経済の動きに影響される

6. 債券
   - 企業や政府が発行する借金の証書
   - 信用リスクと金利リスクがある
""")
        input("\nEnterキーで戻る...")
    
    def _show_story_event(self):
        """ストーリーイベントを表示"""
        events = [
            {
                'title': '経済の理解',
                'content': """
あなたは戦いを通じて、経済の仕組みを理解し始めています。
インフレやデフレがどのように経済に影響を与えるかを学びました。
"""
            },
            {
                'title': '投資の重要性',
                'content': """
モンスターとの戦いの中で、投資の重要性に気づきました。
適切なタイミングで資産を運用することで、より強力な装備を
手に入れることができることを学びました。
"""
            },
            {
                'title': 'リスク管理',
                'content': """
リスクを管理することの重要性を理解しました。
すべての資産を一つの方法に集中させるのではなく、
分散させることでリスクを軽減できることを学びました。
"""
            }
        ]
        
        if self.story_progress // 5 <= len(events):
            event = events[(self.story_progress // 5) - 1]
            print("\n" + "=" * 60)
            print(event['title'])
            print("=" * 60)
            print(event['content'])
            input("Enterキーで続ける...")

