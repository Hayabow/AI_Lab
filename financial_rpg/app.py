#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask Webアプリケーション
"""

from flask import Flask, render_template, request, jsonify, session
import json
import random
import os
from player import Player
from party import Party
from monster import get_random_monster
from battle import Battle
from f_ticket import FTicketSystem, EconomyCondition
from item import WEAPONS, ARMORS, CONSUMABLES

# テンプレートと静的ファイルのパスを絶対パスで設定
base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, 'templates')
static_dir = os.path.join(base_dir, 'static')

app = Flask(__name__, 
            template_folder=template_dir,
            static_folder=static_dir)
app.secret_key = 'financial_rpg_secret_key_change_in_production'

def serialize_game_state(player, f_ticket_system, current_area, story_progress):
    """ゲーム状態をシリアライズ"""
    return {
        'player': {
            'gold': player.gold,
            'f_tickets': player.f_tickets,
            'inventory_weapons': [{'name': w.name, 'attack_bonus': w.attack_bonus} for w in player.inventory_weapons],
            'inventory_armors': [{'name': a.name, 'defense_bonus': a.defense_bonus} for a in player.inventory_armors],
            'inventory_consumables': player.inventory_consumables,
            'party': [serialize_character(m) for m in player.party.members]
        },
        'f_ticket_system': {
            'current_condition': f_ticket_system.current_condition.value,
            'base_value': f_ticket_system.base_value
        },
        'current_area': current_area,
        'story_progress': story_progress
    }

def serialize_character(char):
    """キャラクターをシリアライズ"""
    from monster import MONSTER_TEMPLATES, Monster
    
    emoji = '👤'  # デフォルト（人間キャラクター）
    if isinstance(char, Monster):
        # モンスターの絵文字を取得
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
        'attack': char.attack,
        'defense': char.defense,
        'level': char.level,
        'experience': char.experience,
        'exp_needed': char.level * 100,
        'equipped_weapon': char.equipped_weapon.name if char.equipped_weapon else None,
        'equipped_armor': char.equipped_armor.name if char.equipped_armor else None,
        'emoji': emoji
    }

def deserialize_game_state(state_data):
    """ゲーム状態をデシリアライズ"""
    from character import Character, CharacterType
    from monster import create_monster, MONSTER_TEMPLATES
    
    player = Player()
    player.gold = state_data['player']['gold']
    player.f_tickets = state_data['player']['f_tickets']
    
    # 武器・防具を復元
    for w_data in state_data['player']['inventory_weapons']:
        if w_data['name'] in WEAPONS:
            from item import Weapon
            weapon = Weapon(
                WEAPONS[w_data['name']].name,
                WEAPONS[w_data['name']].attack_bonus,
                WEAPONS[w_data['name']].price_gold,
                WEAPONS[w_data['name']].price_f_tickets,
                WEAPONS[w_data['name']].description
            )
            player.inventory_weapons.append(weapon)
    
    for a_data in state_data['player']['inventory_armors']:
        if a_data['name'] in ARMORS:
            from item import Armor
            armor = Armor(
                ARMORS[a_data['name']].name,
                ARMORS[a_data['name']].defense_bonus,
                ARMORS[a_data['name']].price_gold,
                ARMORS[a_data['name']].price_f_tickets,
                ARMORS[a_data['name']].description
            )
            player.inventory_armors.append(armor)
    
    # 消費アイテムを復元
    player.inventory_consumables = state_data['player'].get('inventory_consumables', {})
    
    # パーティを復元
    for char_data in state_data['player']['party']:
        if char_data['character_type'] == '人間':
            char = Character(
                char_data['name'],
                CharacterType.HUMAN,
                char_data['max_hp'],
                char_data['max_mp'],
                char_data['attack'],
                char_data['defense']
            )
        else:
            # モンスターの場合はテンプレートから復元を試みる
            monster_name = char_data['name']
            if monster_name in MONSTER_TEMPLATES:
                char = create_monster(monster_name, char_data['level'])
            else:
                continue
        
        char.hp = char_data['hp']
        char.mp = char_data['mp']
        char.level = char_data['level']
        char.experience = char_data.get('experience', 0)
        
        # 装備を復元
        if char_data['equipped_weapon']:
            for w in player.inventory_weapons:
                if w.name == char_data['equipped_weapon']:
                    char.equip_weapon(w)
                    break
        
        if char_data['equipped_armor']:
            for a in player.inventory_armors:
                if a.name == char_data['equipped_armor']:
                    char.equip_armor(a)
                    break
        
        player.party.add_member(char)
    
    f_ticket_system = FTicketSystem()
    f_ticket_system.current_condition = EconomyCondition(state_data['f_ticket_system']['current_condition'])
    f_ticket_system.base_value = state_data['f_ticket_system']['base_value']
    
    current_area = state_data['current_area']
    story_progress = state_data['story_progress']
    
    return player, f_ticket_system, current_area, story_progress

@app.route('/')
def index():
    """メインページ"""
    return render_template('index.html')

@app.route('/api/start', methods=['POST'])
def start_game():
    """ゲーム開始"""
    data = request.json
    name = data.get('name', '冒険者')
    
    player = Player()
    player.create_main_character(name)
    f_ticket_system = FTicketSystem()
    current_area = 1
    story_progress = 0
    
    game_state = serialize_game_state(player, f_ticket_system, current_area, story_progress)
    session['game_state'] = json.dumps(game_state)
    
    return jsonify({
        'success': True,
        'game_state': game_state,
        'message': 'ゲームを開始しました！'
    })

@app.route('/api/status', methods=['GET'])
def get_status():
    """ゲーム状態を取得"""
    if 'game_state' not in session:
        return jsonify({'success': False, 'message': 'ゲームが開始されていません'})
    
    game_state = json.loads(session['game_state'])
    return jsonify({'success': True, 'game_state': game_state})

@app.route('/api/adventure', methods=['POST'])
def start_adventure():
    """冒険を開始（インタラクティブ戦闘用）"""
    if 'game_state' not in session:
        return jsonify({'success': False, 'message': 'ゲームが開始されていません'})
    
    game_state_data = json.loads(session['game_state'])
    old_condition = game_state_data.get('f_ticket_system', {}).get('current_condition', '安定')
    
    player, f_ticket_system, current_area, story_progress = deserialize_game_state(game_state_data)
    
    # 経済状況が変動する可能性
    if random.random() < 0.3:
        f_ticket_system.change_condition()
    
    economy_changed = f_ticket_system.current_condition.value != old_condition
    
    # パーティの状態を回復
    player.party.heal_all(999)
    player.party.restore_all_mp(999)
    
    # 敵の生成（プレイヤーの平均レベルを使用）
    player_avg_level = sum([m.level for m in player.party.members]) // len(player.party.members) if player.party.members else 1
    player_avg_level = max(1, player_avg_level)
    
    enemy_party = Party()
    num_enemies = random.randint(1, 3)
    enemies = []
    for _ in range(num_enemies):
        monster = get_random_monster(player_avg_level)
        enemy_party.add_member(monster)
        enemies.append(serialize_character(monster))
    
    # インタラクティブ戦闘を開始
    battle = Battle(player.party, enemy_party)
    session['battle'] = {
        'player_party': [serialize_character(m) for m in player.party.members],
        'enemy_party': [serialize_character(m) for m in enemy_party.members],
        'enemies': enemies
    }
    
    # 状態を保存（戦闘中）
    game_state = serialize_game_state(player, f_ticket_system, current_area, story_progress)
    session['game_state'] = json.dumps(game_state)
    session['battle_instance'] = json.dumps({
        'player_party_data': [serialize_character(m) for m in player.party.members],
        'enemy_party_data': [serialize_character(m) for m in enemy_party.members]
    })
    
    return jsonify({
        'success': True,
        'battle_state': battle.get_battle_state(),
        'game_state': game_state,
        'economy_changed': economy_changed
    })

@app.route('/api/battle/action', methods=['POST'])
def battle_action():
    """戦闘アクションを実行"""
    if 'game_state' not in session or 'battle_instance' not in session:
        return jsonify({'success': False, 'message': '戦闘が開始されていません'})
    
    data = request.json
    action_type = data.get('action_type')  # 'attack', 'spell', 'item', 'defend'
    target_index = data.get('target_index')
    spell_name = data.get('spell_name')
    item_name = data.get('item_name')
    
    game_state_data = json.loads(session['game_state'])
    player, f_ticket_system, current_area, story_progress = deserialize_game_state(game_state_data)
    
    battle_data = json.loads(session['battle_instance'])
    
    # パーティと敵パーティを復元
    from monster import create_monster, MONSTER_TEMPLATES
    from character import Character, CharacterType
    
    player_party = Party()
    for char_data in battle_data['player_party_data']:
        if char_data['character_type'] == '人間':
            char = Character(
                char_data['name'],
                CharacterType.HUMAN,
                char_data['max_hp'],
                char_data['max_mp'],
                char_data['attack'],
                char_data['defense']
            )
        else:
            monster_name = char_data['name']
            if monster_name in MONSTER_TEMPLATES:
                char = create_monster(monster_name, char_data['level'])
            else:
                continue
        char.hp = char_data['hp']
        char.mp = char_data['mp']
        char.level = char_data['level']
        player_party.add_member(char)
    
    enemy_party = Party()
    for char_data in battle_data['enemy_party_data']:
        monster_name = char_data['name']
        if monster_name in MONSTER_TEMPLATES:
            char = create_monster(monster_name, char_data['level'])
            char.hp = char_data['hp']
            char.mp = char_data['mp']
            enemy_party.add_member(char)
    
    battle = Battle(player_party, enemy_party)
    result = battle.player_action(action_type, target_index, item_name, spell_name)
    
    # 戦闘状態を更新
    battle_data['player_party_data'] = [serialize_character(m) for m in player_party.members]
    battle_data['enemy_party_data'] = [serialize_character(m) for m in enemy_party.members]
    session['battle_instance'] = json.dumps(battle_data)
    
    # 戦闘が終了したかチェック
    battle_state = battle.get_battle_state()
    battle_result = None
    
    if battle_state['is_battle_over']:
        if player_party.is_all_dead():
            battle_result = {'victory': False, 'rewards': {'gold': 0, 'f_tickets': 0}, 'recruited_monsters': []}
        else:
            # 勝利
            total_gold = 0
            total_f_tickets = 0
            recruited_monsters = []
            
            for enemy in enemy_party.members:
                if isinstance(enemy, Monster):
                    rewards = enemy.get_rewards()
                    total_gold += rewards['gold']
                    total_f_tickets += rewards['f_tickets']
                    if enemy.try_recruitment():
                        recruited_monsters.append(enemy)
            
            battle_result = {
                'victory': True,
                'rewards': {'gold': total_gold, 'f_tickets': total_f_tickets},
                'recruited_monsters': [serialize_character(m) for m in recruited_monsters]
            }
            
            # 報酬を付与
            player.add_gold(total_gold)
            player.add_f_tickets(total_f_tickets)
            
            # 経験値
            exp_gain = sum([e.level * 20 for e in enemy_party.members])
            for member in player_party.members:
                if member.is_alive():
                    member.add_experience(exp_gain)
            
            # モンスターを仲間に追加
            for monster in recruited_monsters:
                monster.hp = monster.max_hp
                monster.mp = monster.max_mp
                if len(player.party.members) < 4:
                    player.party.add_member(monster)
            
            story_progress += 1
            
            # パーティの状態を更新
            for i, member in enumerate(player.party.members):
                if i < len(player_party.members):
                    battle_member = player_party.members[i]
                    member.hp = battle_member.hp
                    member.mp = battle_member.mp
                    member.level = battle_member.level
                    member.experience = battle_member.experience
            
            game_state = serialize_game_state(player, f_ticket_system, current_area, story_progress)
            session['game_state'] = json.dumps(game_state)
            session.pop('battle_instance', None)
            session.pop('battle', None)
    
    return jsonify({
        'success': result.get('success', True),
        'result': result,
        'battle_state': battle_state,
        'battle_result': battle_result,
        'game_state': serialize_game_state(player, f_ticket_system, current_area, story_progress) if battle_result else None
    })

@app.route('/api/battle/state', methods=['GET'])
def get_battle_state():
    """戦闘状態を取得"""
    if 'battle_instance' not in session:
        return jsonify({'success': False, 'message': '戦闘が開始されていません'})
    
    battle_data = json.loads(session['battle_instance'])
    
    from monster import create_monster, MONSTER_TEMPLATES
    from character import Character, CharacterType
    
    player_party = Party()
    for char_data in battle_data['player_party_data']:
        if char_data['character_type'] == '人間':
            char = Character(
                char_data['name'],
                CharacterType.HUMAN,
                char_data['max_hp'],
                char_data['max_mp'],
                char_data['attack'],
                char_data['defense']
            )
        else:
            monster_name = char_data['name']
            if monster_name in MONSTER_TEMPLATES:
                char = create_monster(monster_name, char_data['level'])
            else:
                continue
        char.hp = char_data['hp']
        char.mp = char_data['mp']
        char.level = char_data['level']
        player_party.add_member(char)
    
    enemy_party = Party()
    for char_data in battle_data['enemy_party_data']:
        monster_name = char_data['name']
        if monster_name in MONSTER_TEMPLATES:
            char = create_monster(monster_name, char_data['level'])
            char.hp = char_data['hp']
            char.mp = char_data['mp']
            enemy_party.add_member(char)
    
    battle = Battle(player_party, enemy_party)
    return jsonify({
        'success': True,
        'battle_state': battle.get_battle_state()
    })

@app.route('/api/recruit_monster', methods=['POST'])
def recruit_monster():
    """モンスターを仲間に追加（手放し処理込み）"""
    if 'game_state' not in session:
        return jsonify({'success': False, 'message': 'ゲームが開始されていません'})
    
    data = request.json
    monster_name = data.get('monster_name')
    release_name = data.get('release_name')  # 手放すモンスターの名前（オプション）
    
    game_state = json.loads(session['game_state'])
    player, f_ticket_system, current_area, story_progress = deserialize_game_state(game_state)
    
    from monster import create_monster, MONSTER_TEMPLATES
    
    # 手放すモンスターを削除
    if release_name:
        for member in player.party.members[:]:
            if member.name == release_name:
                player.party.remove_member(member)
                break
    
    # 新しいモンスターを追加
    if monster_name in MONSTER_TEMPLATES:
        # モンスターのレベルを決定（プレイヤーの平均レベル）
        player_avg_level = sum([m.level for m in player.party.members]) // len(player.party.members) if player.party.members else 1
        monster = create_monster(monster_name, max(1, player_avg_level))
        monster.hp = monster.max_hp
        monster.mp = monster.max_mp
        
        if player.party.add_member(monster):
            game_state = serialize_game_state(player, f_ticket_system, current_area, story_progress)
            session['game_state'] = json.dumps(game_state)
            return jsonify({
                'success': True,
                'message': f'{monster.name}が仲間になりました！',
                'game_state': game_state
            })
        else:
            return jsonify({
                'success': False,
                'message': 'パーティが満員です'
            })
    else:
        return jsonify({
            'success': False,
            'message': '無効なモンスター名です'
        })

@app.route('/api/release_monster', methods=['POST'])
def release_monster():
    """モンスターを手放す"""
    if 'game_state' not in session:
        return jsonify({'success': False, 'message': 'ゲームが開始されていません'})
    
    data = request.json
    monster_name = data.get('name')
    
    game_state = json.loads(session['game_state'])
    player, f_ticket_system, current_area, story_progress = deserialize_game_state(game_state)
    
    # モンスターを削除（メインキャラクターは削除できない）
    for member in player.party.members[:]:
        if member.name == monster_name and member.character_type.value == 'モンスター':
            player.party.remove_member(member)
            game_state = serialize_game_state(player, f_ticket_system, current_area, story_progress)
            session['game_state'] = json.dumps(game_state)
            return jsonify({
                'success': True,
                'message': f'{monster_name}を手放しました',
                'game_state': game_state
            })
    
    return jsonify({
        'success': False,
        'message': 'モンスターが見つかりません'
    })

@app.route('/api/shop/items', methods=['GET'])
def get_shop_items():
    """ショップアイテム一覧を取得"""
    weapons = [{
        'name': w.name,
        'attack_bonus': w.attack_bonus,
        'price_gold': w.price_gold,
        'price_f_tickets': w.price_f_tickets,
        'description': w.description,
        'emoji': '⚔️'
    } for w in WEAPONS.values()]
    
    armors = [{
        'name': a.name,
        'defense_bonus': a.defense_bonus,
        'price_gold': a.price_gold,
        'price_f_tickets': a.price_f_tickets,
        'description': a.description,
        'emoji': '🛡️'
    } for a in ARMORS.values()]
    
    consumables = [{
        'name': c.name,
        'hp_restore': c.hp_restore,
        'mp_restore': c.mp_restore,
        'price_gold': c.price_gold,
        'price_f_tickets': c.price_f_tickets,
        'description': c.description,
        'emoji': c.emoji
    } for c in CONSUMABLES.values()]
    
    return jsonify({
        'success': True,
        'weapons': weapons,
        'armors': armors,
        'consumables': consumables
    })

@app.route('/api/shop/buy', methods=['POST'])
def buy_item():
    """アイテムを購入"""
    if 'game_state' not in session:
        return jsonify({'success': False, 'message': 'ゲームが開始されていません'})
    
    data = request.json
    item_type = data.get('type')  # 'weapon' or 'armor'
    item_name = data.get('name')
    use_f_tickets = data.get('use_f_tickets', False)
    
    game_state = json.loads(session['game_state'])
    player, f_ticket_system, current_area, story_progress = deserialize_game_state(game_state)
    
    success = False
    if item_type == 'weapon':
        success = player.buy_weapon(item_name, use_f_tickets)
    elif item_type == 'armor':
        success = player.buy_armor(item_name, use_f_tickets)
    
    if success:
        game_state = serialize_game_state(player, f_ticket_system, current_area, story_progress)
        session['game_state'] = json.dumps(game_state)
        return jsonify({
            'success': True,
            'message': f'{item_name}を購入しました！',
            'game_state': game_state
        })
    else:
        return jsonify({
            'success': False,
            'message': '購入に失敗しました（資金不足または無効なアイテム）'
        })

@app.route('/api/equip', methods=['POST'])
def equip_item():
    """アイテムを装備"""
    if 'game_state' not in session:
        return jsonify({'success': False, 'message': 'ゲームが開始されていません'})
    
    data = request.json
    character_name = data.get('character_name')
    item_type = data.get('type')  # 'weapon' or 'armor'
    item_name = data.get('name')
    
    game_state = json.loads(session['game_state'])
    player, f_ticket_system, current_area, story_progress = deserialize_game_state(game_state)
    
    # キャラクターを探す
    character = None
    for member in player.party.members:
        if member.name == character_name:
            character = member
            break
    
    if not character:
        return jsonify({'success': False, 'message': 'キャラクターが見つかりません'})
    
    success = False
    if item_type == 'weapon':
        success = player.equip_weapon_to_character(character, item_name)
    elif item_type == 'armor':
        success = player.equip_armor_to_character(character, item_name)
    
    if success:
        game_state = serialize_game_state(player, f_ticket_system, current_area, story_progress)
        session['game_state'] = json.dumps(game_state)
        return jsonify({
            'success': True,
            'message': f'{character_name}に{item_name}を装備しました！',
            'game_state': game_state
        })
    else:
        return jsonify({
            'success': False,
            'message': '装備に失敗しました（アイテムが所持品にない）'
        })

@app.route('/api/shop/buy_consumable', methods=['POST'])
def buy_consumable():
    """消費アイテムを購入"""
    if 'game_state' not in session:
        return jsonify({'success': False, 'message': 'ゲームが開始されていません'})
    
    data = request.json
    item_name = data.get('name')
    use_f_tickets = data.get('use_f_tickets', False)
    quantity = data.get('quantity', 1)
    
    game_state = json.loads(session['game_state'])
    player, f_ticket_system, current_area, story_progress = deserialize_game_state(game_state)
    
    success = player.buy_consumable(item_name, use_f_tickets, quantity)
    
    if success:
        game_state = serialize_game_state(player, f_ticket_system, current_area, story_progress)
        session['game_state'] = json.dumps(game_state)
        return jsonify({
            'success': True,
            'message': f'{item_name}を{quantity}個購入しました！',
            'game_state': game_state
        })
    else:
        return jsonify({
            'success': False,
            'message': '購入に失敗しました（資金不足または無効なアイテム）'
        })

@app.route('/api/use_consumable', methods=['POST'])
def use_consumable():
    """消費アイテムを使用"""
    if 'game_state' not in session:
        return jsonify({'success': False, 'message': 'ゲームが開始されていません'})
    
    data = request.json
    character_name = data.get('character_name')
    item_name = data.get('name')
    
    game_state = json.loads(session['game_state'])
    player, f_ticket_system, current_area, story_progress = deserialize_game_state(game_state)
    
    # キャラクターを探す
    character = None
    for member in player.party.members:
        if member.name == character_name:
            character = member
            break
    
    if not character:
        return jsonify({'success': False, 'message': 'キャラクターが見つかりません'})
    
    success = player.use_consumable(character, item_name)
    
    if success:
        game_state = serialize_game_state(player, f_ticket_system, current_area, story_progress)
        session['game_state'] = json.dumps(game_state)
        return jsonify({
            'success': True,
            'message': f'{character_name}は{item_name}を使用しました！',
            'game_state': game_state
        })
    else:
        return jsonify({
            'success': False,
            'message': 'アイテムの使用に失敗しました（所持していない、またはHP/MPが満タン）'
        })

@app.route('/api/financial_knowledge', methods=['GET'])
def get_financial_knowledge():
    """金融知識を取得"""
    if 'game_state' not in session:
        return jsonify({'success': False, 'message': 'ゲームが開始されていません'})
    
    game_state = json.loads(session['game_state'])
    _, f_ticket_system, _, _ = deserialize_game_state(game_state)
    
    return jsonify({
        'success': True,
        'condition': f_ticket_system.current_condition.value,
        'description': f_ticket_system.get_condition_description(),
        'knowledge': f_ticket_system.get_financial_knowledge(),
        'f_ticket_value': f_ticket_system.get_current_value()
    })

if __name__ == '__main__':
    # ポート5000が使用中の場合は別のポートを使用
    import socket
    import sys
    
    port = None
    for test_port in [5000, 8080, 3000, 5001, 8000]:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(('127.0.0.1', test_port))
                port = test_port
                break
        except OSError as e:
            continue
    
    if port is None:
        print("エラー: 利用可能なポートが見つかりませんでした。")
        print("他のポートを使用しているアプリケーションを終了してください。")
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print(f"金融知識学習RPG - サーバー起動中")
    print(f"{'='*60}")
    print(f"ポート: {port}")
    print(f"\nブラウザで以下のURLにアクセスしてください:")
    print(f"  → http://localhost:{port}")
    print(f"  → http://127.0.0.1:{port}")
    print(f"\nサーバーを停止するには Ctrl+C を押してください")
    print(f"{'='*60}\n")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=port, use_reloader=False)
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")
        print("別のポートを試してください。")
        sys.exit(1)
