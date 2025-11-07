#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
モンスタークラス
"""

from character import Character, CharacterType
import random

class Monster(Character):
    """モンスタークラス"""
    
    def __init__(self, name: str, max_hp: int, max_mp: int, 
                 attack: int, defense: int, 
                 gold_reward: int, f_ticket_reward: int,
                 recruitment_rate: float = 0.1, base_level: int = 1):
        super().__init__(name, CharacterType.MONSTER, max_hp, max_mp, attack, defense)
        self.gold_reward = gold_reward
        self.f_ticket_reward = f_ticket_reward
        self.recruitment_rate = recruitment_rate  # 仲間になる確率（0.0-1.0）
        self.base_level = base_level  # 基本レベル
    
    def try_recruitment(self) -> bool:
        """仲間になるか試行"""
        return random.random() < self.recruitment_rate
    
    def get_rewards(self):
        """報酬を取得"""
        return {
            'gold': self.gold_reward,
            'f_tickets': self.f_ticket_reward
        }

# モンスター定義（レベル1-20まで、100種類）
MONSTER_TEMPLATES = {}

# レベル1-5のモンスター（初級）
level_1_5_monsters = [
    {'name': 'インフレゴブリン', 'max_hp': 50, 'max_mp': 10, 'attack': 15, 'defense': 5, 'gold_reward': 20, 'f_ticket_reward': 1, 'recruitment_rate': 0.15, 'description': '物価上昇を引き起こす小鬼。経済の仕組みを混乱させる。', 'emoji': '👹', 'base_level': 1},
    {'name': 'デフレスライム', 'max_hp': 40, 'max_mp': 5, 'attack': 10, 'defense': 8, 'gold_reward': 15, 'f_ticket_reward': 1, 'recruitment_rate': 0.20, 'description': '物価下落を引き起こすスライム。経済を停滞させる。', 'emoji': '🟢', 'base_level': 1},
    {'name': 'コインスライム', 'max_hp': 35, 'max_mp': 3, 'attack': 8, 'defense': 6, 'gold_reward': 12, 'f_ticket_reward': 1, 'recruitment_rate': 0.25, 'description': '小さなコインのスライム。初心者向け。', 'emoji': '🪙', 'base_level': 1},
    {'name': '紙幣ゴブリン', 'max_hp': 45, 'max_mp': 8, 'attack': 12, 'defense': 7, 'gold_reward': 18, 'f_ticket_reward': 1, 'recruitment_rate': 0.18, 'description': '紙幣を操る小さなゴブリン。', 'emoji': '🧾', 'base_level': 1},
    {'name': '貯金箱スライム', 'max_hp': 55, 'max_mp': 12, 'attack': 14, 'defense': 9, 'gold_reward': 22, 'f_ticket_reward': 1, 'recruitment_rate': 0.16, 'description': '貯金の概念を理解したスライム。', 'emoji': '🐷', 'base_level': 2},
    {'name': '金利コボルト', 'max_hp': 60, 'max_mp': 15, 'attack': 16, 'defense': 10, 'gold_reward': 25, 'f_ticket_reward': 1, 'recruitment_rate': 0.14, 'description': '金利の基礎を理解するコボルト。', 'emoji': '👺', 'base_level': 2},
    {'name': '為替スライム', 'max_hp': 50, 'max_mp': 10, 'attack': 13, 'defense': 8, 'gold_reward': 20, 'f_ticket_reward': 1, 'recruitment_rate': 0.17, 'description': '為替レートを理解し始めたスライム。', 'emoji': '💱', 'base_level': 2},
    {'name': '投資マウス', 'max_hp': 40, 'max_mp': 8, 'attack': 11, 'defense': 9, 'gold_reward': 17, 'f_ticket_reward': 1, 'recruitment_rate': 0.19, 'description': '投資の基礎を学ぶ小さなマウス。', 'emoji': '🐭', 'base_level': 1},
    {'name': '預金スライム', 'max_hp': 48, 'max_mp': 11, 'attack': 13, 'defense': 7, 'gold_reward': 19, 'f_ticket_reward': 1, 'recruitment_rate': 0.18, 'description': '預金の概念を持つスライム。', 'emoji': '💳', 'base_level': 1},
    {'name': '貸付ゴブリン', 'max_hp': 52, 'max_mp': 9, 'attack': 15, 'defense': 8, 'gold_reward': 21, 'f_ticket_reward': 1, 'recruitment_rate': 0.16, 'description': '貸付業務を行うゴブリン。', 'emoji': '📋', 'base_level': 2},
    {'name': '債権スライム', 'max_hp': 46, 'max_mp': 10, 'attack': 12, 'defense': 9, 'gold_reward': 18, 'f_ticket_reward': 1, 'recruitment_rate': 0.17, 'description': '債権を理解するスライム。', 'emoji': '📜', 'base_level': 1},
    {'name': '債務ゴブリン', 'max_hp': 54, 'max_mp': 11, 'attack': 14, 'defense': 7, 'gold_reward': 20, 'f_ticket_reward': 1, 'recruitment_rate': 0.15, 'description': '債務を管理するゴブリン。', 'emoji': '📊', 'base_level': 2},
    {'name': '信用コボルト', 'max_hp': 58, 'max_mp': 13, 'attack': 16, 'defense': 10, 'gold_reward': 24, 'f_ticket_reward': 1, 'recruitment_rate': 0.13, 'description': '信用の概念を理解するコボルト。', 'emoji': '⭐', 'base_level': 3},
    {'name': 'リスクスライム', 'max_hp': 42, 'max_mp': 9, 'attack': 11, 'defense': 8, 'gold_reward': 16, 'f_ticket_reward': 1, 'recruitment_rate': 0.20, 'description': 'リスクを理解するスライム。', 'emoji': '⚠️', 'base_level': 1},
    {'name': 'リターンゴブリン', 'max_hp': 56, 'max_mp': 12, 'attack': 15, 'defense': 9, 'gold_reward': 23, 'f_ticket_reward': 1, 'recruitment_rate': 0.14, 'description': 'リターンを追求するゴブリン。', 'emoji': '📈', 'base_level': 3},
    {'name': '現金スライム', 'max_hp': 38, 'max_mp': 6, 'attack': 9, 'defense': 7, 'gold_reward': 14, 'f_ticket_reward': 1, 'recruitment_rate': 0.22, 'description': '現金を管理するスライム。', 'emoji': '💵', 'base_level': 1},
    {'name': '預金コボルト', 'max_hp': 44, 'max_mp': 9, 'attack': 11, 'defense': 8, 'gold_reward': 17, 'f_ticket_reward': 1, 'recruitment_rate': 0.19, 'description': '預金業務を行うコボルト。', 'emoji': '🏦', 'base_level': 1},
    {'name': '借入スライム', 'max_hp': 41, 'max_mp': 7, 'attack': 10, 'defense': 7, 'gold_reward': 16, 'f_ticket_reward': 1, 'recruitment_rate': 0.21, 'description': '借入を理解するスライム。', 'emoji': '📝', 'base_level': 1},
    {'name': '利息ゴブリン', 'max_hp': 47, 'max_mp': 10, 'attack': 12, 'defense': 8, 'gold_reward': 19, 'f_ticket_reward': 1, 'recruitment_rate': 0.18, 'description': '利息を計算するゴブリン。', 'emoji': '💹', 'base_level': 2},
    {'name': '複利スライム', 'max_hp': 49, 'max_mp': 11, 'attack': 13, 'defense': 9, 'gold_reward': 20, 'f_ticket_reward': 1, 'recruitment_rate': 0.17, 'description': '複利を理解するスライム。', 'emoji': '📊', 'base_level': 2},
    {'name': '単利コボルト', 'max_hp': 43, 'max_mp': 8, 'attack': 11, 'defense': 8, 'gold_reward': 17, 'f_ticket_reward': 1, 'recruitment_rate': 0.20, 'description': '単利を計算するコボルト。', 'emoji': '📈', 'base_level': 1},
    {'name': '預金金利スライム', 'max_hp': 46, 'max_mp': 9, 'attack': 12, 'defense': 8, 'gold_reward': 18, 'f_ticket_reward': 1, 'recruitment_rate': 0.19, 'description': '預金金利を理解するスライム。', 'emoji': '💰', 'base_level': 2},
    {'name': '貸出金利ゴブリン', 'max_hp': 51, 'max_mp': 11, 'attack': 14, 'defense': 9, 'gold_reward': 21, 'f_ticket_reward': 1, 'recruitment_rate': 0.16, 'description': '貸出金利を管理するゴブリン。', 'emoji': '💸', 'base_level': 2},
    {'name': '固定金利スライム', 'max_hp': 48, 'max_mp': 10, 'attack': 13, 'defense': 8, 'gold_reward': 19, 'f_ticket_reward': 1, 'recruitment_rate': 0.18, 'description': '固定金利を扱うスライム。', 'emoji': '🔒', 'base_level': 2},
    {'name': '変動金利コボルト', 'max_hp': 50, 'max_mp': 11, 'attack': 13, 'defense': 9, 'gold_reward': 20, 'f_ticket_reward': 1, 'recruitment_rate': 0.17, 'description': '変動金利を扱うコボルト。', 'emoji': '📉', 'base_level': 2},
    {'name': '名目金利スライム', 'max_hp': 45, 'max_mp': 9, 'attack': 12, 'defense': 8, 'gold_reward': 18, 'f_ticket_reward': 1, 'recruitment_rate': 0.19, 'description': '名目金利を理解するスライム。', 'emoji': '📊', 'base_level': 2},
    {'name': '実質金利ゴブリン', 'max_hp': 53, 'max_mp': 12, 'attack': 14, 'defense': 9, 'gold_reward': 22, 'f_ticket_reward': 1, 'recruitment_rate': 0.15, 'description': '実質金利を計算するゴブリン。', 'emoji': '📈', 'base_level': 3},
    {'name': 'インフレ率スライム', 'max_hp': 42, 'max_mp': 8, 'attack': 11, 'defense': 8, 'gold_reward': 17, 'f_ticket_reward': 1, 'recruitment_rate': 0.20, 'description': 'インフレ率を理解するスライム。', 'emoji': '📊', 'base_level': 1},
    {'name': 'デフレ率コボルト', 'max_hp': 40, 'max_mp': 7, 'attack': 10, 'defense': 9, 'gold_reward': 16, 'f_ticket_reward': 1, 'recruitment_rate': 0.21, 'description': 'デフレ率を理解するコボルト。', 'emoji': '📉', 'base_level': 1},
    {'name': 'GDPスライム', 'max_hp': 57, 'max_mp': 13, 'attack': 15, 'defense': 10, 'gold_reward': 24, 'f_ticket_reward': 1, 'recruitment_rate': 0.13, 'description': 'GDPを理解するスライム。', 'emoji': '📊', 'base_level': 3},
    {'name': '経済成長率ゴブリン', 'max_hp': 55, 'max_mp': 12, 'attack': 14, 'defense': 10, 'gold_reward': 23, 'f_ticket_reward': 1, 'recruitment_rate': 0.14, 'description': '経済成長率を計算するゴブリン。', 'emoji': '📈', 'base_level': 3},
    {'name': '購買力スライム', 'max_hp': 46, 'max_mp': 9, 'attack': 12, 'defense': 8, 'gold_reward': 18, 'f_ticket_reward': 1, 'recruitment_rate': 0.19, 'description': '購買力平価を理解するスライム。', 'emoji': '🛒', 'base_level': 2},
]

# レベル6-10のモンスター（中級）
level_6_10_monsters = [
    {'name': '株式オーク', 'max_hp': 80, 'max_mp': 20, 'attack': 25, 'defense': 12, 'gold_reward': 50, 'f_ticket_reward': 3, 'recruitment_rate': 0.10, 'description': '株式市場の動きを反映するオーク。投資の知識を持っている。', 'emoji': '🐗', 'base_level': 6},
    {'name': '為替マーメイド', 'max_hp': 70, 'max_mp': 30, 'attack': 20, 'defense': 15, 'gold_reward': 45, 'f_ticket_reward': 2, 'recruitment_rate': 0.12, 'description': '為替レートの変動を操るマーメイド。国際金融の知識を持つ。', 'emoji': '🧜‍♀️', 'base_level': 6},
    {'name': '債券ウィッチ', 'max_hp': 90, 'max_mp': 40, 'attack': 22, 'defense': 18, 'gold_reward': 60, 'f_ticket_reward': 4, 'recruitment_rate': 0.08, 'description': '債券市場を支配する魔女。信用リスクを理解している。', 'emoji': '🧙‍♀️', 'base_level': 7},
    {'name': 'デリバティブデーモン', 'max_hp': 100, 'max_mp': 35, 'attack': 28, 'defense': 20, 'gold_reward': 70, 'f_ticket_reward': 5, 'recruitment_rate': 0.06, 'description': 'デリバティブ取引を操るデーモン。', 'emoji': '😈', 'base_level': 8},
    {'name': '不動産トロール', 'max_hp': 95, 'max_mp': 25, 'attack': 26, 'defense': 22, 'gold_reward': 65, 'f_ticket_reward': 4, 'recruitment_rate': 0.07, 'description': '不動産投資を専門とするトロール。', 'emoji': '🏠', 'base_level': 7},
    {'name': '商品先物オーク', 'max_hp': 85, 'max_mp': 28, 'attack': 24, 'defense': 16, 'gold_reward': 55, 'f_ticket_reward': 3, 'recruitment_rate': 0.09, 'description': '商品先物取引を操るオーク。', 'emoji': '🌾', 'base_level': 6},
    {'name': '外貨預金スフィンクス', 'max_hp': 88, 'max_mp': 32, 'attack': 23, 'defense': 19, 'gold_reward': 58, 'f_ticket_reward': 4, 'recruitment_rate': 0.08, 'description': '外貨預金を理解するスフィンクス。', 'emoji': '🦁', 'base_level': 7},
    {'name': '投資信託エレメント', 'max_hp': 75, 'max_mp': 38, 'attack': 21, 'defense': 17, 'gold_reward': 52, 'f_ticket_reward': 3, 'recruitment_rate': 0.10, 'description': '投資信託を操るエレメント。', 'emoji': '💎', 'base_level': 6},
    {'name': 'ETFオーク', 'max_hp': 78, 'max_mp': 22, 'attack': 22, 'defense': 14, 'gold_reward': 48, 'f_ticket_reward': 3, 'recruitment_rate': 0.11, 'description': 'ETFを扱うオーク。', 'emoji': '📊', 'base_level': 6},
    {'name': 'REITウィッチ', 'max_hp': 92, 'max_mp': 36, 'attack': 25, 'defense': 21, 'gold_reward': 63, 'f_ticket_reward': 4, 'recruitment_rate': 0.07, 'description': 'REITを操る魔女。', 'emoji': '🏢', 'base_level': 8},
    {'name': 'コモディティデーモン', 'max_hp': 98, 'max_mp': 30, 'attack': 27, 'defense': 19, 'gold_reward': 68, 'f_ticket_reward': 5, 'recruitment_rate': 0.06, 'description': 'コモディティ取引を操るデーモン。', 'emoji': '⛽', 'base_level': 8},
    {'name': 'FXトレーダーゴブリン', 'max_hp': 82, 'max_mp': 26, 'attack': 24, 'defense': 15, 'gold_reward': 54, 'f_ticket_reward': 3, 'recruitment_rate': 0.09, 'description': 'FX取引を行うゴブリン。', 'emoji': '💹', 'base_level': 7},
    {'name': '暗号資産スライム', 'max_hp': 72, 'max_mp': 40, 'attack': 20, 'defense': 13, 'gold_reward': 46, 'f_ticket_reward': 3, 'recruitment_rate': 0.12, 'description': '暗号資産を理解するスライム。', 'emoji': '₿', 'base_level': 6},
    {'name': 'ブロックチェーントロール', 'max_hp': 105, 'max_mp': 42, 'attack': 29, 'defense': 23, 'gold_reward': 75, 'f_ticket_reward': 6, 'recruitment_rate': 0.05, 'description': 'ブロックチェーン技術を操るトロール。', 'emoji': '⛓️', 'base_level': 9},
    {'name': 'スマートコントラクトエレメント', 'max_hp': 87, 'max_mp': 45, 'attack': 26, 'defense': 18, 'gold_reward': 61, 'f_ticket_reward': 4, 'recruitment_rate': 0.08, 'description': 'スマートコントラクトを理解するエレメント。', 'emoji': '🤖', 'base_level': 8},
]

# レベル11-15のモンスター（上級）
level_11_15_monsters = [
    {'name': '金利ドラゴン', 'max_hp': 150, 'max_mp': 50, 'attack': 35, 'defense': 20, 'gold_reward': 100, 'f_ticket_reward': 5, 'recruitment_rate': 0.05, 'description': '金利の概念を司る強大なドラゴン。金利の変動を操る。', 'emoji': '🐉', 'base_level': 11},
    {'name': '中央銀行ドラゴン', 'max_hp': 160, 'max_mp': 55, 'attack': 38, 'defense': 22, 'gold_reward': 110, 'f_ticket_reward': 6, 'recruitment_rate': 0.04, 'description': '中央銀行政策を司る強大なドラゴン。', 'emoji': '🏛️', 'base_level': 12},
    {'name': '金融政策デーモン', 'max_hp': 155, 'max_mp': 52, 'attack': 36, 'defense': 21, 'gold_reward': 105, 'f_ticket_reward': 5, 'recruitment_rate': 0.05, 'description': '金融政策を操るデーモン。', 'emoji': '📜', 'base_level': 11},
    {'name': 'ヘッジファンドマスター', 'max_hp': 170, 'max_mp': 60, 'attack': 40, 'defense': 25, 'gold_reward': 120, 'f_ticket_reward': 7, 'recruitment_rate': 0.03, 'description': 'ヘッジファンドを操るマスター。', 'emoji': '🎯', 'base_level': 13},
    {'name': 'プライベートエクイティドラゴン', 'max_hp': 165, 'max_mp': 58, 'attack': 39, 'defense': 24, 'gold_reward': 115, 'f_ticket_reward': 6, 'recruitment_rate': 0.04, 'description': 'プライベートエクイティを操るドラゴン。', 'emoji': '💼', 'base_level': 12},
    {'name': 'ベンチャーキャピタルウィッチ', 'max_hp': 145, 'max_mp': 65, 'attack': 34, 'defense': 19, 'gold_reward': 95, 'f_ticket_reward': 5, 'recruitment_rate': 0.06, 'description': 'ベンチャーキャピタルを操る魔女。', 'emoji': '🚀', 'base_level': 11},
    {'name': 'クレジットデフォルトスワップデーモン', 'max_hp': 175, 'max_mp': 62, 'attack': 42, 'defense': 26, 'gold_reward': 125, 'f_ticket_reward': 8, 'recruitment_rate': 0.02, 'description': 'CDSを操る危険なデーモン。', 'emoji': '💣', 'base_level': 14},
    {'name': 'レバレッジドラゴン', 'max_hp': 180, 'max_mp': 55, 'attack': 43, 'defense': 27, 'gold_reward': 130, 'f_ticket_reward': 8, 'recruitment_rate': 0.02, 'description': 'レバレッジ取引を操るドラゴン。', 'emoji': '⚡', 'base_level': 14},
    {'name': 'シャドウバンキングデーモン', 'max_hp': 168, 'max_mp': 60, 'attack': 41, 'defense': 25, 'gold_reward': 118, 'f_ticket_reward': 7, 'recruitment_rate': 0.03, 'description': 'シャドウバンキングを操るデーモン。', 'emoji': '👁️', 'base_level': 13},
    {'name': '証券化ウィッチ', 'max_hp': 152, 'max_mp': 57, 'attack': 37, 'defense': 22, 'gold_reward': 107, 'f_ticket_reward': 6, 'recruitment_rate': 0.04, 'description': '証券化商品を操る魔女。', 'emoji': '📦', 'base_level': 12},
    {'name': 'デリバティブマスター', 'max_hp': 185, 'max_mp': 68, 'attack': 45, 'defense': 28, 'gold_reward': 135, 'f_ticket_reward': 9, 'recruitment_rate': 0.01, 'description': 'デリバティブ取引のマスター。', 'emoji': '🎲', 'base_level': 15},
    {'name': 'ハイフレクエンシートレードデーモン', 'max_hp': 162, 'max_mp': 63, 'attack': 40, 'defense': 24, 'gold_reward': 112, 'f_ticket_reward': 7, 'recruitment_rate': 0.03, 'description': 'HFTを操るデーモン。', 'emoji': '⚡', 'base_level': 13},
    {'name': 'アルゴリズムトレードウィッチ', 'max_hp': 158, 'max_mp': 59, 'attack': 38, 'defense': 23, 'gold_reward': 109, 'f_ticket_reward': 6, 'recruitment_rate': 0.04, 'description': 'アルゴリズムトレードを操る魔女。', 'emoji': '🔮', 'base_level': 12},
    {'name': 'クォンツファンドドラゴン', 'max_hp': 172, 'max_mp': 64, 'attack': 42, 'defense': 26, 'gold_reward': 122, 'f_ticket_reward': 8, 'recruitment_rate': 0.02, 'description': 'クォンツファンドを操るドラゴン。', 'emoji': '📐', 'base_level': 14},
    {'name': 'ストラテジックアライアンスマスター', 'max_hp': 178, 'max_mp': 66, 'attack': 44, 'defense': 27, 'gold_reward': 128, 'f_ticket_reward': 8, 'recruitment_rate': 0.02, 'description': '戦略的提携を操るマスター。', 'emoji': '🤝', 'base_level': 14},
    {'name': 'リスク管理オーク', 'max_hp': 148, 'max_mp': 54, 'attack': 35, 'defense': 21, 'gold_reward': 103, 'f_ticket_reward': 6, 'recruitment_rate': 0.05, 'description': 'リスク管理を専門とするオーク。', 'emoji': '🛡️', 'base_level': 11},
    {'name': '分散投資ウィッチ', 'max_hp': 142, 'max_mp': 56, 'attack': 33, 'defense': 20, 'gold_reward': 98, 'f_ticket_reward': 5, 'recruitment_rate': 0.06, 'description': '分散投資を推奨する魔女。', 'emoji': '🎯', 'base_level': 11},
    {'name': '資産配分ドラゴン', 'max_hp': 155, 'max_mp': 59, 'attack': 37, 'defense': 23, 'gold_reward': 108, 'f_ticket_reward': 6, 'recruitment_rate': 0.04, 'description': '資産配分を操るドラゴン。', 'emoji': '⚖️', 'base_level': 12},
    {'name': 'ポートフォリオマスター', 'max_hp': 160, 'max_mp': 61, 'attack': 39, 'defense': 24, 'gold_reward': 113, 'f_ticket_reward': 7, 'recruitment_rate': 0.03, 'description': 'ポートフォリオを管理するマスター。', 'emoji': '📊', 'base_level': 13},
]

# レベル16-20のモンスター（最上級）
level_16_20_monsters = [
    {'name': '金融危機ドラゴン', 'max_hp': 220, 'max_mp': 80, 'attack': 55, 'defense': 35, 'gold_reward': 180, 'f_ticket_reward': 12, 'recruitment_rate': 0.01, 'description': '金融危機を引き起こす強大なドラゴン。', 'emoji': '🌋', 'base_level': 18},
    {'name': 'バブルキング', 'max_hp': 200, 'max_mp': 75, 'attack': 50, 'defense': 32, 'gold_reward': 160, 'f_ticket_reward': 10, 'recruitment_rate': 0.02, 'description': 'バブルを引き起こすキング。', 'emoji': '🫧', 'base_level': 17},
    {'name': '経済崩壊デーモン', 'max_hp': 240, 'max_mp': 85, 'attack': 60, 'defense': 38, 'gold_reward': 200, 'f_ticket_reward': 15, 'recruitment_rate': 0.005, 'description': '経済崩壊を引き起こすデーモン。', 'emoji': '💥', 'base_level': 20},
    {'name': 'システムリスクマスター', 'max_hp': 210, 'max_mp': 78, 'attack': 52, 'defense': 34, 'gold_reward': 170, 'f_ticket_reward': 11, 'recruitment_rate': 0.015, 'description': 'システムリスクを操るマスター。', 'emoji': '⚠️', 'base_level': 17},
    {'name': '流動性危機ドラゴン', 'max_hp': 230, 'max_mp': 82, 'attack': 58, 'defense': 36, 'gold_reward': 190, 'f_ticket_reward': 13, 'recruitment_rate': 0.008, 'description': '流動性危機を引き起こすドラゴン。', 'emoji': '🌊', 'base_level': 19},
    {'name': '規制リスクウィッチ', 'max_hp': 195, 'max_mp': 72, 'attack': 48, 'defense': 31, 'gold_reward': 150, 'f_ticket_reward': 9, 'recruitment_rate': 0.02, 'description': '規制リスクを操る魔女。', 'emoji': '📋', 'base_level': 16},
    {'name': 'マクロ経済ドラゴン', 'max_hp': 250, 'max_mp': 90, 'attack': 62, 'defense': 40, 'gold_reward': 210, 'f_ticket_reward': 16, 'recruitment_rate': 0.003, 'description': 'マクロ経済を操る最強のドラゴン。', 'emoji': '🌍', 'base_level': 20},
    {'name': 'グローバル金融マスター', 'max_hp': 235, 'max_mp': 88, 'attack': 59, 'defense': 37, 'gold_reward': 195, 'f_ticket_reward': 14, 'recruitment_rate': 0.006, 'description': 'グローバル金融を操るマスター。', 'emoji': '🌐', 'base_level': 19},
    {'name': '中央銀行総裁ドラゴン', 'max_hp': 245, 'max_mp': 92, 'attack': 61, 'defense': 39, 'gold_reward': 205, 'f_ticket_reward': 15, 'recruitment_rate': 0.004, 'description': '中央銀行総裁レベルの強大なドラゴン。', 'emoji': '👑', 'base_level': 20},
    {'name': '金融市場の支配者', 'max_hp': 255, 'max_mp': 95, 'attack': 65, 'defense': 42, 'gold_reward': 220, 'f_ticket_reward': 18, 'recruitment_rate': 0.001, 'description': '金融市場を支配する最強の存在。', 'emoji': '👑', 'base_level': 20},
    {'name': 'インフレーションキング', 'max_hp': 225, 'max_mp': 86, 'attack': 56, 'defense': 35, 'gold_reward': 185, 'f_ticket_reward': 13, 'recruitment_rate': 0.008, 'description': 'インフレーションを引き起こすキング。', 'emoji': '🔥', 'base_level': 18},
    {'name': 'デフレーションクイーン', 'max_hp': 215, 'max_mp': 80, 'attack': 54, 'defense': 33, 'gold_reward': 175, 'f_ticket_reward': 12, 'recruitment_rate': 0.01, 'description': 'デフレーションを引き起こすクイーン。', 'emoji': '❄️', 'base_level': 17},
    {'name': 'スタグフレーションデーモン', 'max_hp': 238, 'max_mp': 89, 'attack': 59, 'defense': 37, 'gold_reward': 198, 'f_ticket_reward': 15, 'recruitment_rate': 0.005, 'description': 'スタグフレーションを引き起こすデーモン。', 'emoji': '🌪️', 'base_level': 19},
    {'name': 'ハイパーインフレドラゴン', 'max_hp': 248, 'max_mp': 93, 'attack': 63, 'defense': 40, 'gold_reward': 208, 'f_ticket_reward': 16, 'recruitment_rate': 0.003, 'description': 'ハイパーインフレを引き起こすドラゴン。', 'emoji': '💥', 'base_level': 20},
    {'name': '為替介入マスター', 'max_hp': 232, 'max_mp': 87, 'attack': 57, 'defense': 36, 'gold_reward': 192, 'f_ticket_reward': 14, 'recruitment_rate': 0.006, 'description': '為替介入を操るマスター。', 'emoji': '💱', 'base_level': 18},
    {'name': '金融緩和ドラゴン', 'max_hp': 218, 'max_mp': 81, 'attack': 53, 'defense': 34, 'gold_reward': 178, 'f_ticket_reward': 12, 'recruitment_rate': 0.009, 'description': '金融緩和政策を操るドラゴン。', 'emoji': '💰', 'base_level': 17},
    {'name': '金融引き締めデーモン', 'max_hp': 228, 'max_mp': 84, 'attack': 56, 'defense': 35, 'gold_reward': 188, 'f_ticket_reward': 13, 'recruitment_rate': 0.007, 'description': '金融引き締め政策を操るデーモン。', 'emoji': '🔒', 'base_level': 18},
    {'name': '量的緩和ウィッチ', 'max_hp': 242, 'max_mp': 91, 'attack': 61, 'defense': 39, 'gold_reward': 202, 'f_ticket_reward': 15, 'recruitment_rate': 0.004, 'description': '量的緩和を操る魔女。', 'emoji': '📈', 'base_level': 19},
    {'name': '金融規制マスター', 'max_hp': 212, 'max_mp': 79, 'attack': 51, 'defense': 32, 'gold_reward': 172, 'f_ticket_reward': 11, 'recruitment_rate': 0.01, 'description': '金融規制を操るマスター。', 'emoji': '📋', 'base_level': 16},
    {'name': 'バーゼル規制ドラゴン', 'max_hp': 222, 'max_mp': 83, 'attack': 55, 'defense': 35, 'gold_reward': 182, 'f_ticket_reward': 13, 'recruitment_rate': 0.008, 'description': 'バーゼル規制を操るドラゴン。', 'emoji': '🏛️', 'base_level': 17},
    {'name': '資本充足率デーモン', 'max_hp': 205, 'max_mp': 77, 'attack': 49, 'defense': 31, 'gold_reward': 165, 'f_ticket_reward': 10, 'recruitment_rate': 0.012, 'description': '資本充足率を管理するデーモン。', 'emoji': '💎', 'base_level': 16},
    {'name': 'ストレステストマスター', 'max_hp': 235, 'max_mp': 88, 'attack': 58, 'defense': 37, 'gold_reward': 195, 'f_ticket_reward': 14, 'recruitment_rate': 0.006, 'description': 'ストレステストを実施するマスター。', 'emoji': '🧪', 'base_level': 18},
    {'name': 'リスクモデルウィッチ', 'max_hp': 198, 'max_mp': 74, 'attack': 47, 'defense': 30, 'gold_reward': 158, 'f_ticket_reward': 9, 'recruitment_rate': 0.015, 'description': 'リスクモデルを構築する魔女。', 'emoji': '📐', 'base_level': 16},
    {'name': 'VaR計算ドラゴン', 'max_hp': 208, 'max_mp': 78, 'attack': 50, 'defense': 32, 'gold_reward': 168, 'f_ticket_reward': 11, 'recruitment_rate': 0.01, 'description': 'VaRを計算するドラゴン。', 'emoji': '📊', 'base_level': 16},
    {'name': 'コンプライアンスマスター', 'max_hp': 188, 'max_mp': 70, 'attack': 45, 'defense': 29, 'gold_reward': 148, 'f_ticket_reward': 8, 'recruitment_rate': 0.018, 'description': 'コンプライアンスを管理するマスター。', 'emoji': '✅', 'base_level': 15},
    {'name': '内部統制デーモン', 'max_hp': 193, 'max_mp': 72, 'attack': 46, 'defense': 30, 'gold_reward': 153, 'f_ticket_reward': 9, 'recruitment_rate': 0.016, 'description': '内部統制を管理するデーモン。', 'emoji': '🔐', 'base_level': 15},
    {'name': 'ガバナンスウィッチ', 'max_hp': 183, 'max_mp': 68, 'attack': 44, 'defense': 28, 'gold_reward': 143, 'f_ticket_reward': 8, 'recruitment_rate': 0.02, 'description': 'コーポレートガバナンスを操る魔女。', 'emoji': '👔', 'base_level': 15},
    {'name': 'ESG投資ドラゴン', 'max_hp': 190, 'max_mp': 71, 'attack': 45, 'defense': 29, 'gold_reward': 150, 'f_ticket_reward': 9, 'recruitment_rate': 0.017, 'description': 'ESG投資を推進するドラゴン。', 'emoji': '🌱', 'base_level': 15},
    {'name': 'サステナブルファイナンスマスター', 'max_hp': 195, 'max_mp': 73, 'attack': 46, 'defense': 30, 'gold_reward': 155, 'f_ticket_reward': 9, 'recruitment_rate': 0.015, 'description': 'サステナブルファイナンスを推進するマスター。', 'emoji': '🌍', 'base_level': 15},
    {'name': 'グリーンファイナンスデーモン', 'max_hp': 200, 'max_mp': 75, 'attack': 48, 'defense': 31, 'gold_reward': 160, 'f_ticket_reward': 10, 'recruitment_rate': 0.013, 'description': 'グリーンファイナンスを推進するデーモン。', 'emoji': '🌿', 'base_level': 16},
    {'name': 'フィンテックウィッチ', 'max_hp': 177, 'max_mp': 65, 'attack': 43, 'defense': 27, 'gold_reward': 127, 'f_ticket_reward': 8, 'recruitment_rate': 0.02, 'description': 'フィンテックを操る魔女。', 'emoji': '💻', 'base_level': 14},
    {'name': 'AI金融マスター', 'max_hp': 182, 'max_mp': 67, 'attack': 44, 'defense': 28, 'gold_reward': 132, 'f_ticket_reward': 8, 'recruitment_rate': 0.018, 'description': 'AI金融を操るマスター。', 'emoji': '🤖', 'base_level': 14},
    {'name': '機械学習トレードドラゴン', 'max_hp': 180, 'max_mp': 66, 'attack': 43, 'defense': 27, 'gold_reward': 130, 'f_ticket_reward': 8, 'recruitment_rate': 0.019, 'description': '機械学習でトレードするドラゴン。', 'emoji': '🧠', 'base_level': 14},
    {'name': 'ビッグデータファイナンスデーモン', 'max_hp': 185, 'max_mp': 68, 'attack': 44, 'defense': 28, 'gold_reward': 135, 'f_ticket_reward': 8, 'recruitment_rate': 0.017, 'description': 'ビッグデータで金融を操るデーモン。', 'emoji': '📊', 'base_level': 14},
]

# レベル16-20のモンスター（最上級）

# 全てのモンスターを統合
all_monsters = level_1_5_monsters + level_6_10_monsters + level_11_15_monsters + level_16_20_monsters

# MONSTER_TEMPLATESに追加
for monster_data in all_monsters:
    MONSTER_TEMPLATES[monster_data['name']] = monster_data

def create_monster(template_name: str, level: int = 1) -> Monster:
    """モンスターを生成"""
    if template_name not in MONSTER_TEMPLATES:
        raise ValueError(f"Unknown monster: {template_name}")
    
    template = MONSTER_TEMPLATES[template_name].copy()
    # レベルによる補正（基本レベルからの差分で調整）
    base_level = template.get('base_level', 1)
    level_diff = level - base_level
    level_multiplier = 1.0 + level_diff * 0.15
    
    monster = Monster(
        name=template['name'],
        max_hp=int(template['max_hp'] * level_multiplier),
        max_mp=int(template['max_mp'] * level_multiplier),
        attack=int(template['attack'] * level_multiplier),
        defense=int(template['defense'] * level_multiplier),
        gold_reward=int(template['gold_reward'] * level_multiplier),
        f_ticket_reward=template['f_ticket_reward'],
        recruitment_rate=template['recruitment_rate'],
        base_level=base_level
    )
    monster.level = level
    return monster

def get_random_monster(player_level: int = 1) -> Monster:
    """プレイヤーレベルに応じたランダムなモンスターを生成"""
    # プレイヤーレベルに応じた出現確率を計算
    # レベル差が±2以内のモンスターが出現しやすい
    level_weights = {}
    
    for template_name, template in MONSTER_TEMPLATES.items():
        base_level = template.get('base_level', 1)
        level_diff = abs(base_level - player_level)
        
        # レベル差に応じた重み付け（差が小さいほど高い確率）
        if level_diff == 0:
            weight = 10.0  # 同じレベル
        elif level_diff == 1:
            weight = 7.0   # ±1レベル
        elif level_diff == 2:
            weight = 4.0   # ±2レベル
        elif level_diff == 3:
            weight = 2.0   # ±3レベル
        elif level_diff <= 5:
            weight = 0.5   # ±4-5レベル
        else:
            weight = 0.1   # それ以上離れている場合は低確率
        
        # プレイヤーレベルが低い場合、低レベルモンスターを優先
        if player_level <= 3 and base_level <= 3:
            weight *= 2.0
        elif player_level <= 5 and base_level <= 5:
            weight *= 1.5
        elif player_level <= 10 and base_level <= 10:
            weight *= 1.2
        
        level_weights[template_name] = weight
    
    # 重み付けに基づいてランダム選択
    if sum(level_weights.values()) == 0:
        # 重みがすべて0の場合はランダム
        template_name = random.choice(list(MONSTER_TEMPLATES.keys()))
    else:
        template_name = random.choices(
            list(level_weights.keys()),
            weights=list(level_weights.values())
        )[0]
    
    # 生成時のレベルはプレイヤーレベル±1の範囲でランダム
    monster_level = max(1, player_level + random.randint(-1, 1))
    return create_monster(template_name, monster_level)
