#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
金融知識学習RPG - メインゲームループ
"""

from game_engine import GameEngine

def main():
    """メイン関数"""
    print("=" * 60)
    print("金融知識学習RPG")
    print("=" * 60)
    print()
    
    game = GameEngine()
    game.start()

if __name__ == "__main__":
    main()

