#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F券システム
"""

from enum import Enum
import random

class EconomyCondition(Enum):
    """経済状況"""
    BOOM = "好況"      # 経済が好調
    RECOVERY = "回復"  # 経済が回復中
    STABLE = "安定"    # 経済が安定
    RECESSION = "不況" # 経済が不況
    DEPRESSION = "恐慌" # 経済恐慌

class FTicketSystem:
    """F券システム"""
    
    # 経済状況ごとの価値倍率
    VALUE_MULTIPLIERS = {
        EconomyCondition.BOOM: 1.5,
        EconomyCondition.RECOVERY: 1.2,
        EconomyCondition.STABLE: 1.0,
        EconomyCondition.RECESSION: 0.8,
        EconomyCondition.DEPRESSION: 0.5
    }
    
    # 経済状況の説明
    CONDITION_DESCRIPTIONS = {
        EconomyCondition.BOOM: "経済が好調で、F券の価値が上昇しています。",
        EconomyCondition.RECOVERY: "経済が回復傾向にあり、F券の価値が少し上がっています。",
        EconomyCondition.STABLE: "経済は安定しており、F券の価値は変動していません。",
        EconomyCondition.RECESSION: "経済が不況で、F券の価値が下落しています。",
        EconomyCondition.DEPRESSION: "経済恐慌により、F券の価値が大幅に下落しています。"
    }
    
    def __init__(self):
        self.base_value = 50  # F券1枚の基本価値（ゴールド）
        self.current_condition = EconomyCondition.STABLE
        self.condition_history = [EconomyCondition.STABLE]
    
    def get_current_value(self) -> int:
        """現在のF券1枚の価値を取得"""
        multiplier = self.VALUE_MULTIPLIERS[self.current_condition]
        return int(self.base_value * multiplier)
    
    def change_condition(self):
        """経済状況をランダムに変更"""
        # 前の状況から遷移しやすい状況に変更
        transitions = {
            EconomyCondition.BOOM: [
                EconomyCondition.BOOM, EconomyCondition.RECOVERY, EconomyCondition.STABLE
            ],
            EconomyCondition.RECOVERY: [
                EconomyCondition.RECOVERY, EconomyCondition.STABLE, EconomyCondition.BOOM
            ],
            EconomyCondition.STABLE: [
                EconomyCondition.STABLE, EconomyCondition.RECOVERY, EconomyCondition.RECESSION
            ],
            EconomyCondition.RECESSION: [
                EconomyCondition.RECESSION, EconomyCondition.STABLE, EconomyCondition.DEPRESSION
            ],
            EconomyCondition.DEPRESSION: [
                EconomyCondition.DEPRESSION, EconomyCondition.RECESSION, EconomyCondition.STABLE
            ]
        }
        
        possible_conditions = transitions.get(self.current_condition, [EconomyCondition.STABLE])
        self.current_condition = random.choice(possible_conditions)
        self.condition_history.append(self.current_condition)
        
        # 履歴が長すぎる場合は削除
        if len(self.condition_history) > 10:
            self.condition_history.pop(0)
    
    def get_condition_description(self) -> str:
        """現在の経済状況の説明を取得"""
        return self.CONDITION_DESCRIPTIONS[self.current_condition]
    
    def calculate_total_value(self, ticket_count: int) -> int:
        """F券の合計価値を計算"""
        return self.get_current_value() * ticket_count
    
    def get_financial_knowledge(self) -> str:
        """金融知識の説明を取得"""
        knowledge = {
            EconomyCondition.BOOM: (
                "好況時には、投資や消費が活発になり、資産価値が上昇します。\n"
                "しかし、過熱するとバブルが発生する可能性があります。"
            ),
            EconomyCondition.RECOVERY: (
                "経済回復期には、適切な投資タイミングと判断が重要です。\n"
                "リスクを管理しながら資産を増やすチャンスでもあります。"
            ),
            EconomyCondition.STABLE: (
                "安定した経済状況では、リスクの少ない投資が適切です。\n"
                "分散投資により、リスクを軽減できます。"
            ),
            EconomyCondition.RECESSION: (
                "不況時には、資産価値が下落しますが、\n"
                "長期的な視点で投資を続けることも重要です。"
            ),
            EconomyCondition.DEPRESSION: (
                "経済恐慌時には、流動性の確保が最優先です。\n"
                "危機的な状況では、現金保持も重要な選択肢です。"
            )
        }
        return knowledge.get(self.current_condition, "")

