#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
プレイヤー管理システム
"""

from character import Character, CharacterType
from party import Party
from item import WEAPONS, ARMORS, CONSUMABLES, Weapon, Armor, Consumable
from typing import Dict, List

class Player:
    """プレイヤークラス"""
    
    def __init__(self):
        self.gold = 500  # 初期資金
        self.f_tickets = 0  # F券
        self.inventory_weapons: List[Weapon] = []
        self.inventory_armors: List[Armor] = []
        self.inventory_consumables: Dict[str, int] = {}  # アイテム名: 個数
        self.party = Party()
        self.main_character = None
        
    def create_main_character(self, name: str):
        """メインキャラクターを作成"""
        self.main_character = Character(
            name=name,
            character_type=CharacterType.HUMAN,
            max_hp=100,
            max_mp=20,
            attack=15,
            defense=10
        )
        self.party.add_member(self.main_character)
    
    def add_gold(self, amount: int):
        """ゴールドを追加"""
        self.gold += amount
    
    def spend_gold(self, amount: int) -> bool:
        """ゴールドを消費（足りなければFalse）"""
        if self.gold >= amount:
            self.gold -= amount
            return True
        return False
    
    def add_f_tickets(self, amount: int):
        """F券を追加"""
        self.f_tickets += amount
    
    def spend_f_tickets(self, amount: int) -> bool:
        """F券を消費（足りなければFalse）"""
        if self.f_tickets >= amount:
            self.f_tickets -= amount
            return True
        return False
    
    def buy_weapon(self, weapon_name: str, use_f_tickets: bool = False) -> bool:
        """武器を購入"""
        if weapon_name not in WEAPONS:
            return False
        
        weapon_template = WEAPONS[weapon_name]
        weapon = Weapon(
            weapon_template.name,
            weapon_template.attack_bonus,
            weapon_template.price_gold,
            weapon_template.price_f_tickets,
            weapon_template.description
        )
        
        if use_f_tickets:
            if self.spend_f_tickets(weapon.price_f_tickets):
                self.inventory_weapons.append(weapon)
                return True
        else:
            if self.spend_gold(weapon.price_gold):
                self.inventory_weapons.append(weapon)
                return True
        
        return False
    
    def buy_armor(self, armor_name: str, use_f_tickets: bool = False) -> bool:
        """防具を購入"""
        if armor_name not in ARMORS:
            return False
        
        armor_template = ARMORS[armor_name]
        armor = Armor(
            armor_template.name,
            armor_template.defense_bonus,
            armor_template.price_gold,
            armor_template.price_f_tickets,
            armor_template.description
        )
        
        if use_f_tickets:
            if self.spend_f_tickets(armor.price_f_tickets):
                self.inventory_armors.append(armor)
                return True
        else:
            if self.spend_gold(armor.price_gold):
                self.inventory_armors.append(armor)
                return True
        
        return False
    
    def equip_weapon_to_character(self, character: Character, weapon_name: str) -> bool:
        """キャラクターに武器を装備"""
        weapon = None
        for w in self.inventory_weapons:
            if w.name == weapon_name:
                weapon = w
                break
        
        if weapon is None:
            return False
        
        character.equip_weapon(weapon)
        return True
    
    def equip_armor_to_character(self, character: Character, armor_name: str) -> bool:
        """キャラクターに防具を装備"""
        armor = None
        for a in self.inventory_armors:
            if a.name == armor_name:
                armor = a
                break
        
        if armor is None:
            return False
        
        character.equip_armor(armor)
        return True
    
    def buy_consumable(self, consumable_name: str, use_f_tickets: bool = False, quantity: int = 1) -> bool:
        """消費アイテムを購入"""
        if consumable_name not in CONSUMABLES:
            return False
        
        consumable_template = CONSUMABLES[consumable_name]
        total_price_gold = consumable_template.price_gold * quantity
        total_price_f_tickets = consumable_template.price_f_tickets * quantity
        
        if use_f_tickets:
            if self.spend_f_tickets(total_price_f_tickets):
                self.inventory_consumables[consumable_name] = self.inventory_consumables.get(consumable_name, 0) + quantity
                return True
        else:
            if self.spend_gold(total_price_gold):
                self.inventory_consumables[consumable_name] = self.inventory_consumables.get(consumable_name, 0) + quantity
                return True
        
        return False
    
    def use_consumable(self, character: Character, consumable_name: str) -> bool:
        """消費アイテムを使用"""
        if consumable_name not in self.inventory_consumables:
            return False
        
        if self.inventory_consumables[consumable_name] <= 0:
            return False
        
        if consumable_name not in CONSUMABLES:
            return False
        
        consumable_template = CONSUMABLES[consumable_name]
        
        # HPとMPを回復
        if consumable_template.hp_restore > 0:
            character.heal(consumable_template.hp_restore)
        if consumable_template.mp_restore > 0:
            character.restore_mp(consumable_template.mp_restore)
        
        # アイテムを消費
        self.inventory_consumables[consumable_name] -= 1
        if self.inventory_consumables[consumable_name] <= 0:
            del self.inventory_consumables[consumable_name]
        
        return True
    
    def get_status(self) -> str:
        """プレイヤーの状態を文字列で取得"""
        status = f"所持金: {self.gold}G\n"
        status += f"F券: {self.f_tickets}枚\n"
        status += f"パーティメンバー: {len(self.party.members)}人\n"
        return status

