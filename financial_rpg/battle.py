#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
戦闘システム（ドラゴンクエスト風）
"""

from party import Party
from character import Character
from monster import Monster
import random
import json

class Battle:
    """戦闘クラス"""
    
    def __init__(self, player_party: Party, enemy_party: Party):
        self.player_party = player_party
        self.enemy_party = enemy_party
        self.turn = 0
        self.current_character_index = 0
        self.battle_log = []
        self.is_player_turn = True
    
    def execute_battle(self, silent=False) -> dict:
        """戦闘を実行して結果を返す（自動戦闘用）"""
        if not silent:
            print("\n" + "=" * 60)
            print("戦闘開始！")
            print("=" * 60)
        
        turn = 0
        
        while not self.player_party.is_all_dead() and not self.enemy_party.is_all_dead():
            turn += 1
            if not silent:
                print(f"\n--- ターン {turn} ---\n")
            
            # プレイヤー側の行動
            self._player_turn(silent)
            
            if self.enemy_party.is_all_dead():
                break
            
            # 敵側の行動
            self._enemy_turn(silent)
            
            if self.player_party.is_all_dead():
                break
            
            # 状態表示
            if not silent:
                self._show_status()
        
        return self._battle_result(silent)
    
    def get_battle_state(self) -> dict:
        """現在の戦闘状態を取得"""
        return {
            'turn': self.turn,
            'is_player_turn': self.is_player_turn,
            'current_character_index': self.current_character_index,
            'player_party': [self._serialize_character(c) for c in self.player_party.members],
            'enemy_party': [self._serialize_character(c) for c in self.enemy_party.members],
            'battle_log': self.battle_log[-10:],  # 最後の10件
            'is_battle_over': self.player_party.is_all_dead() or self.enemy_party.is_all_dead()
        }
    
    def _serialize_character(self, char):
        """キャラクターをシリアライズ"""
        from monster import MONSTER_TEMPLATES
        emoji = '👤'
        if isinstance(char, Monster):
            for template_name, template in MONSTER_TEMPLATES.items():
                if template['name'] == char.name:
                    emoji = template.get('emoji', '👤')
                    break
        
        return {
            'name': char.name,
            'character_type': char.character_type.value,
            'hp': char.hp,
            'max_hp': char.max_hp,
            'mp': char.mp,
            'max_mp': char.max_mp,
            'level': char.level,
            'emoji': emoji,
            'is_alive': char.is_alive()
        }
    
    def player_action(self, action_type: str, target_index: int = None, item_name: str = None, spell_name: str = None) -> dict:
        """プレイヤーの行動を処理"""
        alive_players = self.player_party.get_alive_members()
        alive_enemies = self.enemy_party.get_alive_members()
        
        if not alive_players:
            return {'success': False, 'message': '全滅しています'}
        
        if not alive_enemies and action_type != 'item':
            return {'success': False, 'message': '敵が全滅しています'}
        
        # 現在のキャラクターを取得
        current_char = alive_players[self.current_character_index % len(alive_players)]
        
        result = {'success': True, 'action_type': action_type, 'character': current_char.name}
        
        if action_type == 'attack':
            if target_index is None or target_index >= len(alive_enemies):
                target = random.choice(alive_enemies)
            else:
                target = alive_enemies[target_index]
            
            damage = current_char.calculate_damage()
            actual_damage = target.take_damage(damage)
            result['target'] = target.name
            result['damage'] = actual_damage
            result['message'] = f'{current_char.name}は{target.name}に{actual_damage}のダメージを与えた！'
            self.battle_log.append(result['message'])
            
            if not target.is_alive():
                result['message'] += f' {target.name}を倒した！'
                self.battle_log.append(f'{target.name}を倒した！')
        
        elif action_type == 'spell':
            if spell_name is None:
                return {'success': False, 'message': '魔法名が指定されていません'}
            
            spell_result = current_char.use_spell(spell_name)
            if not spell_result['success']:
                return spell_result
            
            if 'damage' in spell_result:
                # 攻撃魔法
                if target_index is None or target_index >= len(alive_enemies):
                    target = random.choice(alive_enemies)
                else:
                    target = alive_enemies[target_index]
                
                damage = spell_result['damage']
                actual_damage = target.take_damage(damage)
                result['target'] = target.name
                result['damage'] = actual_damage
                result['message'] = f'{current_char.name}は{spell_name}を唱えた！{target.name}に{actual_damage}のダメージ！'
                self.battle_log.append(result['message'])
                
                if not target.is_alive():
                    result['message'] += f' {target.name}を倒した！'
                    self.battle_log.append(f'{target.name}を倒した！')
            elif 'heal_amount' in spell_result:
                # 回復魔法
                result['heal_amount'] = spell_result['heal_amount']
                result['message'] = f'{current_char.name}は{spell_name}を唱えた！HPが{spell_result["heal_amount"]}回復した！'
                self.battle_log.append(result['message'])
        
        elif action_type == 'item':
            # アイテム使用は別のAPIで処理
            return {'success': False, 'message': 'アイテムは別のAPIを使用してください'}
        
        elif action_type == 'defend':
            current_char.defend()
            result['message'] = f'{current_char.name}は身構えた！'
            self.battle_log.append(result['message'])
        
        # 次のキャラクターに移る
        self.current_character_index += 1
        
        # 全員行動したら敵のターン
        if self.current_character_index >= len(alive_players):
            self.current_character_index = 0
            self.is_player_turn = False
            # 敵の行動を自動実行
            self._enemy_turn(silent=True)
            self.is_player_turn = True
        
        return result
    
    def _player_turn(self, silent=False):
        """プレイヤー側のターン"""
        alive_players = self.player_party.get_alive_members()
        alive_enemies = self.enemy_party.get_alive_members()
        
        if not alive_players or not alive_enemies:
            return
        
        for player in alive_players:
            if not player.is_alive():
                continue
            
            if not silent:
                print(f"\n{player.name}のターン")
            
            # 行動選択（簡易版：自動で攻撃）
            target = random.choice(alive_enemies)
            damage = player.calculate_damage()
            actual_damage = target.take_damage(damage)
            
            if not silent:
                print(f"{player.name}は{target.name}に{actual_damage}のダメージを与えた！")
            
            if not target.is_alive():
                if not silent:
                    print(f"{target.name}を倒した！")
                alive_enemies = self.enemy_party.get_alive_members()
                if not alive_enemies:
                    break
    
    def _enemy_turn(self, silent=False):
        """敵側のターン"""
        alive_players = self.player_party.get_alive_members()
        alive_enemies = self.enemy_party.get_alive_members()
        
        if not alive_players or not alive_enemies:
            return
        
        for enemy in alive_enemies:
            if not enemy.is_alive():
                continue
            
            target = random.choice(alive_players)
            damage = enemy.calculate_damage()
            actual_damage = target.take_damage(damage)
            
            if not silent:
                print(f"{enemy.name}は{target.name}に{actual_damage}のダメージを与えた！")
            
            if not target.is_alive():
                if not silent:
                    print(f"{target.name}は倒れた...")
    
    def _show_status(self):
        """状態を表示"""
        print("\n【パーティ状態】")
        for member in self.player_party.get_alive_members():
            print(f"  {member}")
        
        print("\n【敵状態】")
        for enemy in self.enemy_party.get_alive_members():
            print(f"  {enemy}")
    
    def _battle_result(self, silent=False) -> dict:
        """戦闘結果を返す"""
        if self.player_party.is_all_dead():
            if not silent:
                print("\n" + "=" * 60)
                print("全滅してしまった...")
                print("=" * 60)
            return {
                'victory': False,
                'recruited_monsters': [],
                'rewards': {'gold': 0, 'f_tickets': 0}
            }
        
        # 勝利
        if not silent:
            print("\n" + "=" * 60)
            print("勝利！")
            print("=" * 60)
        
        # 報酬とモンスター仲間化
        total_gold = 0
        total_f_tickets = 0
        recruited_monsters = []
        
        for enemy in self.enemy_party.members:
            if isinstance(enemy, Monster):
                rewards = enemy.get_rewards()
                total_gold += rewards['gold']
                total_f_tickets += rewards['f_tickets']
                
                # 仲間化判定
                if enemy.try_recruitment():
                    recruited_monsters.append(enemy)
                    if not silent:
                        print(f"{enemy.name}が仲間になった！")
        
        if not silent:
            print(f"\n獲得報酬: ゴールド {total_gold}G, F券 {total_f_tickets}枚")
        
        return {
            'victory': True,
            'recruited_monsters': recruited_monsters,
            'rewards': {
                'gold': total_gold,
                'f_tickets': total_f_tickets
            }
        }

