#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ショップシステム
"""

from item import WEAPONS, ARMORS
from player import Player
from f_ticket import FTicketSystem

class Shop:
    """ショップクラス"""
    
    def __init__(self, player: Player, f_ticket_system: FTicketSystem):
        self.player = player
        self.f_ticket_system = f_ticket_system
    
    def show_menu(self):
        """ショップメニューを表示"""
        while True:
            print("\n" + "=" * 60)
            print("ショップ")
            print("=" * 60)
            print(f"所持金: {self.player.gold}G")
            print(f"F券: {self.player.f_tickets}枚")
            f_ticket_value = self.f_ticket_system.get_current_value()
            print(f"F券1枚の現在の価値: {f_ticket_value}G")
            print()
            print("1. 武器を購入（ゴールド）")
            print("2. 防具を購入（ゴールド）")
            print("3. 武器を購入（F券）")
            print("4. 防具を購入（F券）")
            print("5. 所持アイテムを確認")
            print("6. 装備を確認・変更")
            print("7. 金融知識を学ぶ")
            print("0. ショップを出る")
            print()
            
            choice = input("選択してください: ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                self._buy_weapon_with_gold()
            elif choice == "2":
                self._buy_armor_with_gold()
            elif choice == "3":
                self._buy_weapon_with_f_tickets()
            elif choice == "4":
                self._buy_armor_with_f_tickets()
            elif choice == "5":
                self._show_inventory()
            elif choice == "6":
                self._equip_items()
            elif choice == "7":
                self._show_financial_knowledge()
            else:
                print("無効な選択です。")
    
    def _buy_weapon_with_gold(self):
        """ゴールドで武器を購入"""
        print("\n【武器一覧（ゴールド購入）】")
        weapons = list(WEAPONS.items())
        for i, (name, weapon) in enumerate(weapons, 1):
            print(f"{i}. {weapon.name} - 攻撃力+{weapon.attack_bonus} - {weapon.price_gold}G")
            print(f"   {weapon.description}")
        
        try:
            choice = int(input("\n購入する武器の番号（0でキャンセル）: ").strip())
            if choice == 0:
                return
            if 1 <= choice <= len(weapons):
                weapon_name = weapons[choice - 1][0]
                if self.player.buy_weapon(weapon_name, use_f_tickets=False):
                    print(f"{weapon_name}を購入しました！")
                else:
                    print("ゴールドが足りません。")
            else:
                print("無効な番号です。")
        except ValueError:
            print("数字を入力してください。")
    
    def _buy_armor_with_gold(self):
        """ゴールドで防具を購入"""
        print("\n【防具一覧（ゴールド購入）】")
        armors = list(ARMORS.items())
        for i, (name, armor) in enumerate(armors, 1):
            print(f"{i}. {armor.name} - 防御力+{armor.defense_bonus} - {armor.price_gold}G")
            print(f"   {armor.description}")
        
        try:
            choice = int(input("\n購入する防具の番号（0でキャンセル）: ").strip())
            if choice == 0:
                return
            if 1 <= choice <= len(armors):
                armor_name = armors[choice - 1][0]
                if self.player.buy_armor(armor_name, use_f_tickets=False):
                    print(f"{armor_name}を購入しました！")
                else:
                    print("ゴールドが足りません。")
            else:
                print("無効な番号です。")
        except ValueError:
            print("数字を入力してください。")
    
    def _buy_weapon_with_f_tickets(self):
        """F券で武器を購入"""
        print("\n【武器一覧（F券購入）】")
        f_ticket_value = self.f_ticket_system.get_current_value()
        print(f"現在のF券1枚の価値: {f_ticket_value}G\n")
        
        weapons = list(WEAPONS.items())
        for i, (name, weapon) in enumerate(weapons, 1):
            total_value = self.f_ticket_system.calculate_total_value(weapon.price_f_tickets)
            print(f"{i}. {weapon.name} - 攻撃力+{weapon.attack_bonus} - {weapon.price_f_tickets}枚 ({total_value}G相当)")
            print(f"   {weapon.description}")
        
        try:
            choice = int(input("\n購入する武器の番号（0でキャンセル）: ").strip())
            if choice == 0:
                return
            if 1 <= choice <= len(weapons):
                weapon_name = weapons[choice - 1][0]
                if self.player.buy_weapon(weapon_name, use_f_tickets=True):
                    print(f"{weapon_name}をF券で購入しました！")
                else:
                    print("F券が足りません。")
            else:
                print("無効な番号です。")
        except ValueError:
            print("数字を入力してください。")
    
    def _buy_armor_with_f_tickets(self):
        """F券で防具を購入"""
        print("\n【防具一覧（F券購入）】")
        f_ticket_value = self.f_ticket_system.get_current_value()
        print(f"現在のF券1枚の価値: {f_ticket_value}G\n")
        
        armors = list(ARMORS.items())
        for i, (name, armor) in enumerate(armors, 1):
            total_value = self.f_ticket_system.calculate_total_value(armor.price_f_tickets)
            print(f"{i}. {armor.name} - 防御力+{armor.defense_bonus} - {armor.price_f_tickets}枚 ({total_value}G相当)")
            print(f"   {armor.description}")
        
        try:
            choice = int(input("\n購入する防具の番号（0でキャンセル）: ").strip())
            if choice == 0:
                return
            if 1 <= choice <= len(armors):
                armor_name = armors[choice - 1][0]
                if self.player.buy_armor(armor_name, use_f_tickets=True):
                    print(f"{armor_name}をF券で購入しました！")
                else:
                    print("F券が足りません。")
            else:
                print("無効な番号です。")
        except ValueError:
            print("数字を入力してください。")
    
    def _show_inventory(self):
        """所持アイテムを表示"""
        print("\n【所持武器】")
        if not self.player.inventory_weapons:
            print("  （なし）")
        else:
            for i, weapon in enumerate(self.player.inventory_weapons, 1):
                print(f"{i}. {weapon.name} - 攻撃力+{weapon.attack_bonus}")
        
        print("\n【所持防具】")
        if not self.player.inventory_armors:
            print("  （なし）")
        else:
            for i, armor in enumerate(self.player.inventory_armors, 1):
                print(f"{i}. {armor.name} - 防御力+{armor.defense_bonus}")
        
        input("\nEnterキーで戻る...")
    
    def _equip_items(self):
        """装備を変更"""
        if not self.player.party.members:
            print("パーティメンバーがいません。")
            return
        
        print("\n【パーティメンバー】")
        for i, member in enumerate(self.player.party.members, 1):
            print(f"{i}. {member.name}")
        
        try:
            char_choice = int(input("\n装備を変更するキャラクターの番号: ").strip())
            if not (1 <= char_choice <= len(self.player.party.members)):
                print("無効な番号です。")
                return
            
            character = self.player.party.members[char_choice - 1]
            
            print(f"\n{character.name}の装備")
            print(f"武器: {character.equipped_weapon.name if character.equipped_weapon else 'なし'}")
            print(f"防具: {character.equipped_armor.name if character.equipped_armor else 'なし'}")
            
            if self.player.inventory_weapons:
                print("\n装備可能な武器:")
                for i, weapon in enumerate(self.player.inventory_weapons, 1):
                    print(f"{i}. {weapon.name}")
                weapon_choice = input("装備する武器の番号（Enterでスキップ）: ").strip()
                if weapon_choice:
                    try:
                        idx = int(weapon_choice) - 1
                        if 0 <= idx < len(self.player.inventory_weapons):
                            self.player.equip_weapon_to_character(character, self.player.inventory_weapons[idx].name)
                            print(f"{self.player.inventory_weapons[idx].name}を装備しました！")
                    except ValueError:
                        pass
            
            if self.player.inventory_armors:
                print("\n装備可能な防具:")
                for i, armor in enumerate(self.player.inventory_armors, 1):
                    print(f"{i}. {armor.name}")
                armor_choice = input("装備する防具の番号（Enterでスキップ）: ").strip()
                if armor_choice:
                    try:
                        idx = int(armor_choice) - 1
                        if 0 <= idx < len(self.player.inventory_armors):
                            self.player.equip_armor_to_character(character, self.player.inventory_armors[idx].name)
                            print(f"{self.player.inventory_armors[idx].name}を装備しました！")
                    except ValueError:
                        pass
        except ValueError:
            print("数字を入力してください。")
    
    def _show_financial_knowledge(self):
        """金融知識を表示"""
        print("\n" + "=" * 60)
        print("金融知識")
        print("=" * 60)
        print(f"\n現在の経済状況: {self.f_ticket_system.current_condition.value}")
        print(self.f_ticket_system.get_condition_description())
        print()
        print(self.f_ticket_system.get_financial_knowledge())
        print()
        input("Enterキーで戻る...")

