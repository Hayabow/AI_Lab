#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
キャラクタークラス
"""

from enum import Enum
from typing import Optional

class CharacterType(Enum):
    """キャラクタータイプ"""
    HUMAN = "人間"
    MONSTER = "モンスター"

class Character:
    """キャラクター基本クラス"""
    
    def __init__(self, name: str, character_type: CharacterType, 
                 max_hp: int, max_mp: int, attack: int, defense: int):
        self.name = name
        self.character_type = character_type
        self.max_hp = max_hp
        self.max_mp = max_mp
        self.hp = max_hp
        self.mp = max_mp
        self.base_attack = attack
        self.base_defense = defense
        self.attack = attack
        self.defense = defense
        self.level = 1
        self.experience = 0
        self.equipped_weapon = None
        self.equipped_armor = None
        
    def take_damage(self, damage: int) -> int:
        """ダメージを受ける"""
        actual_damage = max(1, damage - self.defense)
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage
    
    def heal(self, amount: int):
        """HPを回復"""
        self.hp = min(self.max_hp, self.hp + amount)
    
    def restore_mp(self, amount: int):
        """MPを回復"""
        self.mp = min(self.max_mp, self.mp + amount)
    
    def is_alive(self) -> bool:
        """生存しているか"""
        return self.hp > 0
    
    def calculate_damage(self) -> int:
        """攻撃ダメージを計算"""
        base_damage = self.attack
        # 武器による補正
        if self.equipped_weapon:
            base_damage += self.equipped_weapon.attack_bonus
        return base_damage
    
    def equip_weapon(self, weapon):
        """武器を装備"""
        if self.equipped_weapon:
            self.attack -= self.equipped_weapon.attack_bonus
        self.equipped_weapon = weapon
        if weapon:
            self.attack += weapon.attack_bonus
    
    def equip_armor(self, armor):
        """防具を装備"""
        if self.equipped_armor:
            self.defense -= self.equipped_armor.defense_bonus
        self.equipped_armor = armor
        if armor:
            self.defense += armor.defense_bonus
    
    def level_up(self):
        """レベルアップ"""
        self.level += 1
        hp_gain = self.max_hp // 10 + 5
        mp_gain = self.max_mp // 10 + 2
        self.max_hp += hp_gain
        self.max_mp += mp_gain
        self.hp = self.max_hp
        self.mp = self.max_mp
        self.base_attack += 2
        self.base_defense += 2
        self.attack = self.base_attack
        self.defense = self.base_defense
        if self.equipped_weapon:
            self.attack += self.equipped_weapon.attack_bonus
        if self.equipped_armor:
            self.defense += self.equipped_armor.defense_bonus
    
    def add_experience(self, exp: int) -> bool:
        """経験値を追加し、レベルアップしたかどうかを返す"""
        self.experience += exp
        exp_needed = self.level * 100
        if self.experience >= exp_needed:
            self.experience -= exp_needed
            self.level_up()
            return True
        return False
    
    def use_spell(self, spell_name: str, target=None) -> dict:
        """魔法を使用"""
        spells = {
            'メラ': {'mp_cost': 3, 'damage_multiplier': 1.5, 'description': '敵に炎のダメージを与える'},
            'ギラ': {'mp_cost': 5, 'damage_multiplier': 2.0, 'description': '敵に強力な炎のダメージを与える'},
            'ホイミ': {'mp_cost': 3, 'heal_amount': 30, 'description': 'HPを回復する'},
            'ベホイミ': {'mp_cost': 8, 'heal_amount': 80, 'description': 'HPを大幅に回復する'},
        }
        
        if spell_name not in spells:
            return {'success': False, 'message': '未知の魔法です'}
        
        spell = spells[spell_name]
        
        if self.mp < spell['mp_cost']:
            return {'success': False, 'message': 'MPが足りません'}
        
        self.mp -= spell['mp_cost']
        
        result = {'success': True, 'spell_name': spell_name, 'mp_cost': spell['mp_cost']}
        
        if 'damage_multiplier' in spell:
            # 攻撃魔法
            base_damage = self.calculate_damage()
            damage = int(base_damage * spell['damage_multiplier'])
            result['damage'] = damage
            result['description'] = spell['description']
        elif 'heal_amount' in spell:
            # 回復魔法
            heal_amount = spell['heal_amount']
            self.heal(heal_amount)
            result['heal_amount'] = heal_amount
            result['description'] = spell['description']
        
        return result
    
    def defend(self):
        """防御状態になる（次のターンまで防御力が1.5倍）"""
        self.defense = int(self.defense * 1.5)
        return {'success': True, 'message': f'{self.name}は身構えた！'}
    
    def __str__(self):
        status = f"{self.name} (Lv.{self.level})"
        status += f" HP:{self.hp}/{self.max_hp}"
        if self.max_mp > 0:
            status += f" MP:{self.mp}/{self.max_mp}"
        return status

