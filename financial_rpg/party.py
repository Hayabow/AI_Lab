#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
パーティシステム
"""

from character import Character
from typing import List

class Party:
    """パーティクラス"""
    
    def __init__(self):
        self.members: List[Character] = []
    
    def add_member(self, character: Character) -> bool:
        """メンバーを追加（最大4体まで）"""
        if len(self.members) >= 4:
            return False  # パーティが満員
        self.members.append(character)
        return True
    
    def remove_member(self, character: Character):
        """メンバーを削除"""
        if character in self.members:
            self.members.remove(character)
    
    def get_alive_members(self) -> List[Character]:
        """生存しているメンバーを取得"""
        return [member for member in self.members if member.is_alive()]
    
    def is_all_dead(self) -> bool:
        """全員が倒れたか"""
        return len(self.get_alive_members()) == 0
    
    def heal_all(self, amount: int):
        """全員を回復"""
        for member in self.members:
            member.heal(amount)
    
    def restore_all_mp(self, amount: int):
        """全員のMPを回復"""
        for member in self.members:
            member.restore_mp(amount)
    
    def __str__(self):
        if not self.members:
            return "パーティは空です"
        return "\n".join([str(member) for member in self.members])

