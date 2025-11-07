// ゲーム状態管理
let gameState = null;
let currentPanel = null;

// API呼び出し
async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(endpoint, options);
        const result = await response.json();
        return result;
    } catch (error) {
        showMessage('エラーが発生しました: ' + error.message, 'error');
        return { success: false, message: error.message };
    }
}

// ゲーム開始
async function startGame() {
    const name = document.getElementById('player-name').value || '冒険者';
    
    const result = await apiCall('/api/start', 'POST', { name });
    
    if (result.success) {
        gameState = result.game_state;
        document.getElementById('start-screen').classList.add('hidden');
        document.getElementById('game-screen').classList.remove('hidden');
        updateStatus();
        showMessage('ゲームを開始しました！', 'success');
    } else {
        showMessage(result.message, 'error');
    }
}

// 状態更新
async function updateStatus() {
    const result = await apiCall('/api/status');
    
    if (result.success) {
        gameState = result.game_state;
        document.getElementById('current-area').textContent = gameState.current_area;
        document.getElementById('gold').textContent = gameState.player.gold;
        document.getElementById('f-tickets').textContent = gameState.player.f_tickets;
        
        // F券価値を計算
        const fTicketValue = gameState.f_ticket_system.base_value;
        const multipliers = {
            '好況': 1.5,
            '回復': 1.2,
            '安定': 1.0,
            '不況': 0.8,
            '恐慌': 0.5
        };
        const multiplier = multipliers[gameState.f_ticket_system.current_condition] || 1.0;
        const value = Math.floor(fTicketValue * multiplier);
        document.getElementById('f-ticket-value').textContent = value;
        document.getElementById('economy-condition').textContent = gameState.f_ticket_system.current_condition;
    }
}

// モーダル制御
function openBattleModal() {
    document.getElementById('battle-modal').classList.remove('hidden');
}

function closeBattleModal() {
    document.getElementById('battle-modal').classList.add('hidden');
}

function openShopModal() {
    document.getElementById('shop-modal').classList.remove('hidden');
}

function closeShopModal() {
    document.getElementById('shop-modal').classList.add('hidden');
}

function openReleaseModal() {
    document.getElementById('release-modal').classList.remove('hidden');
}

function closeReleaseModal() {
    document.getElementById('release-modal').classList.add('hidden');
    selectedReleaseMonster = null;
}

let selectedReleaseMonster = null;
let pendingRecruitMonster = null;

function selectReleaseMonster(monsterName) {
    selectedReleaseMonster = monsterName;
    document.querySelectorAll('.release-option-card').forEach(card => {
        card.classList.remove('selected');
    });
    event.target.closest('.release-option-card').classList.add('selected');
    document.getElementById('confirm-release-btn').disabled = false;
}

async function confirmRelease() {
    if (!selectedReleaseMonster || !pendingRecruitMonster) return;
    
    const result = await apiCall('/api/recruit_monster', 'POST', {
        monster_name: pendingRecruitMonster.name,
        release_name: selectedReleaseMonster
    });
    
    if (result.success) {
        gameState = result.game_state;
        updateStatus();
        showMessage(result.message, 'success');
        closeReleaseModal();
        // 戦闘画面を更新
        showBattleResult();
    } else {
        showMessage(result.message, 'error');
    }
}

// 戦闘状態
let currentBattleState = null;

// 冒険開始（戦闘モーダルを開く）
async function showAdventure() {
    currentPanel = 'adventure';
    openBattleModal();
    
    const result = await apiCall('/api/adventure', 'POST');
    
    if (result.success) {
        gameState = result.game_state;
        updateStatus();
        currentBattleState = result.battle_state;
        renderBattleScreen(result.battle_state);
    } else {
        showMessage(result.message, 'error');
        closeBattleModal();
    }
}

// 戦闘画面をレンダリング
function renderBattleScreen(battleState) {
    // 敵を表示
    const enemyContainer = document.getElementById('enemy-container');
    enemyContainer.innerHTML = '';
    
    battleState.enemy_party.forEach((enemy, index) => {
        if (enemy.is_alive) {
            const enemyDiv = document.createElement('div');
            enemyDiv.className = 'enemy-sprite';
            enemyDiv.innerHTML = `
                <div class="enemy-name">${enemy.name}</div>
                <div class="enemy-emoji">${enemy.emoji || '👾'}</div>
            `;
            enemyContainer.appendChild(enemyDiv);
        }
    });
    
    // 現在のプレイヤーキャラクターを表示
    const alivePlayers = battleState.player_party.filter(p => p.is_alive);
    if (alivePlayers.length > 0) {
        const currentIndex = battleState.current_character_index % alivePlayers.length;
        const currentChar = alivePlayers[currentIndex];
        document.getElementById('player-name-display').textContent = currentChar.name;
    }
}

// 戦闘アクションを実行
async function battleAction(actionType, targetIndex = null, itemName = null, spellName = null) {
    closeSpellMenu();
    closeItemMenu();
    
    const result = await apiCall('/api/battle/action', 'POST', {
        action_type: actionType,
        target_index: targetIndex,
        item_name: itemName,
        spell_name: spellName
    });
    
    if (result.success) {
        if (result.result && result.result.message) {
            showMessage(result.result.message, 'success');
        }
        
        currentBattleState = result.battle_state;
        renderBattleScreen(result.battle_state);
        
        // 戦闘が終了した場合
        if (result.battle_result) {
            setTimeout(() => {
                handleBattleEnd(result.battle_result);
            }, 1000);
        }
    } else {
        showMessage(result.result?.message || 'アクションに失敗しました', 'error');
    }
}

// 戦闘終了処理
function handleBattleEnd(battleResult) {
    if (battleResult.victory) {
        showMessage('戦闘に勝利しました！', 'success');
        updateStatus();
        
        // 報酬表示
        let message = `獲得: ${battleResult.rewards.gold}G, ${battleResult.rewards.f_tickets}枚のF券`;
        if (battleResult.recruited_monsters && battleResult.recruited_monsters.length > 0) {
            message += '\n' + battleResult.recruited_monsters.map(m => m.name).join(', ') + 'が仲間になりました！';
        }
        showMessage(message, 'success');
    } else {
        showMessage('全滅してしまいました...', 'error');
    }
    
    setTimeout(() => {
        closeBattleModal();
    }, 2000);
}

// 魔法メニューを表示
function showSpellMenu() {
    document.getElementById('spell-modal').classList.remove('hidden');
}

// 魔法メニューを閉じる
function closeSpellMenu() {
    document.getElementById('spell-modal').classList.add('hidden');
}

// アイテムメニューを表示
function showItemMenu() {
    const itemList = document.getElementById('item-list');
    itemList.innerHTML = '';
    
    if (gameState && gameState.player && gameState.player.inventory_consumables) {
        const consumables = gameState.player.inventory_consumables;
        let hasItems = false;
        
        for (const [itemName, quantity] of Object.entries(consumables)) {
            if (quantity > 0) {
                hasItems = true;
                const itemBtn = document.createElement('button');
                itemBtn.className = 'item-option';
                itemBtn.textContent = `${itemName} × ${quantity}`;
                itemBtn.onclick = () => {
                    // アイテム使用は別途実装が必要
                    showMessage('アイテム機能は準備中です', 'warning');
                    closeItemMenu();
                };
                itemList.appendChild(itemBtn);
            }
        }
        
        if (!hasItems) {
            itemList.innerHTML = '<p style="color: white; text-align: center;">所持アイテムがありません</p>';
        }
    } else {
        itemList.innerHTML = '<p style="color: white; text-align: center;">所持アイテムがありません</p>';
    }
    
    document.getElementById('item-modal').classList.remove('hidden');
}

// アイテムメニューを閉じる
function closeItemMenu() {
    document.getElementById('item-modal').classList.add('hidden');
}

// 戦闘結果を表示（旧バージョン - 互換性のため残す）
function showBattleResult(result = null) {
    // この関数は旧バージョン用。新しいインタラクティブ戦闘では使用しない
}

function showReleaseModalForMonster(monster) {
    pendingRecruitMonster = monster;
    const releaseOptions = document.getElementById('release-options');
    releaseOptions.innerHTML = '';
    
    // モンスターのみを表示（メインキャラクターは除外）
    gameState.player.party.forEach(member => {
        if (member.character_type === 'モンスター') {
            const card = document.createElement('div');
            card.className = 'release-option-card';
            card.onclick = () => selectReleaseMonster(member.name);
            card.innerHTML = `
                <div style="font-size: 3em; margin-bottom: 10px;">${member.emoji || '👾'}</div>
                <div><strong>${member.name}</strong></div>
                <div>Lv.${member.level}</div>
                <div>HP: ${member.hp}/${member.max_hp}</div>
            `;
            releaseOptions.appendChild(card);
        }
    });
    
    openReleaseModal();
}

// ショップ表示（モーダル）
async function showShop() {
    currentPanel = 'shop';
    openShopModal();
    
    const shopContent = document.getElementById('shop-content');
    shopContent.innerHTML = '<div style="text-align: center; padding: 50px;">商品を読み込んでいます...</div>';
    
    const itemsResult = await apiCall('/api/shop/items');
    await updateStatus();
    
    if (!itemsResult.success) {
        showMessage('ショップ情報の取得に失敗しました', 'error');
        closeShopModal();
        return;
    }
    
    const fTicketValue = Math.floor(gameState.f_ticket_system.base_value * 
        ({'好況': 1.5, '回復': 1.2, '安定': 1.0, '不況': 0.8, '恐慌': 0.5}[gameState.f_ticket_system.current_condition] || 1.0));
    
    let html = '<div class="panel-title">ショップ</div>';
    html += `<div style="text-align: center; margin-bottom: 20px;">`;
    html += `<p>所持金: ${gameState.player.gold}G</p>`;
    html += `<p>F券: ${gameState.player.f_tickets}枚 (1枚 = ${fTicketValue}G相当)</p>`;
    html += `</div>`;
    
    // 武器
    html += '<h3 style="margin-top: 30px; color: #667eea;">⚔️ 武器</h3>';
    html += '<div class="shop-items">';
    itemsResult.weapons.forEach(weapon => {
        const fTicketPrice = Math.floor(weapon.price_f_tickets * fTicketValue);
        html += `<div class="item-card">`;
        html += `<div class="item-name">${weapon.emoji || '⚔️'} ${weapon.name}</div>`;
        html += `<div class="item-description">${weapon.description}</div>`;
        html += `<div class="item-stats">💪 攻撃力: +${weapon.attack_bonus}</div>`;
        html += `<div class="item-price">`;
        html += `<span class="price-tag">💰 ${weapon.price_gold}G</span>`;
        html += `<span class="price-tag">🎫 ${weapon.price_f_tickets}枚 (${fTicketPrice}G相当)</span>`;
        html += `</div>`;
        html += `<div style="display: flex; gap: 10px;">`;
        // HTMLエスケープを避けるため、data属性を使用
        const weaponNameSafe = weapon.name.replace(/"/g, '&quot;').replace(/'/g, '&#39;');
        html += `<button class="btn btn-success buy-item-btn" data-type="weapon" data-name="${weaponNameSafe}" data-use-ftickets="false">💰 ゴールドで購入</button>`;
        html += `<button class="btn btn-success buy-item-btn" data-type="weapon" data-name="${weaponNameSafe}" data-use-ftickets="true">🎫 F券で購入</button>`;
        html += `</div>`;
        html += `</div>`;
    });
    html += '</div>';
    
    // 防具
    html += '<h3 style="margin-top: 30px; color: #667eea;">🛡️ 防具</h3>';
    html += '<div class="shop-items">';
    itemsResult.armors.forEach(armor => {
        const fTicketPrice = Math.floor(armor.price_f_tickets * fTicketValue);
        html += `<div class="item-card">`;
        html += `<div class="item-name">${armor.emoji || '🛡️'} ${armor.name}</div>`;
        html += `<div class="item-description">${armor.description}</div>`;
        html += `<div class="item-stats">🛡️ 防御力: +${armor.defense_bonus}</div>`;
        html += `<div class="item-price">`;
        html += `<span class="price-tag">💰 ${armor.price_gold}G</span>`;
        html += `<span class="price-tag">🎫 ${armor.price_f_tickets}枚 (${fTicketPrice}G相当)</span>`;
        html += `</div>`;
        html += `<div style="display: flex; gap: 10px;">`;
        const armorNameSafe = armor.name.replace(/"/g, '&quot;').replace(/'/g, '&#39;');
        html += `<button class="btn btn-success buy-item-btn" data-type="armor" data-name="${armorNameSafe}" data-use-ftickets="false">💰 ゴールドで購入</button>`;
        html += `<button class="btn btn-success buy-item-btn" data-type="armor" data-name="${armorNameSafe}" data-use-ftickets="true">🎫 F券で購入</button>`;
        html += `</div>`;
        html += `</div>`;
    });
    html += '</div>';
    
    // 回復アイテム
    html += '<h3 style="margin-top: 30px; color: #667eea;">💊 回復アイテム</h3>';
    html += '<div class="shop-items">';
    itemsResult.consumables.forEach(consumable => {
        const fTicketPrice = Math.floor(consumable.price_f_tickets * fTicketValue);
        html += `<div class="item-card">`;
        html += `<div class="item-name">${consumable.emoji || '💊'} ${consumable.name}</div>`;
        html += `<div class="item-description">${consumable.description}</div>`;
        html += `<div class="item-stats">`;
        if (consumable.hp_restore > 0) html += `❤️ HP回復: +${consumable.hp_restore === 999 ? '全回復' : consumable.hp_restore} `;
        if (consumable.mp_restore > 0) html += `💙 MP回復: +${consumable.mp_restore === 999 ? '全回復' : consumable.mp_restore}`;
        html += `</div>`;
        html += `<div class="item-price">`;
        html += `<span class="price-tag">💰 ${consumable.price_gold}G</span>`;
        html += `<span class="price-tag">🎫 ${consumable.price_f_tickets}枚 (${fTicketPrice}G相当)</span>`;
        html += `</div>`;
        html += `<div style="display: flex; gap: 10px;">`;
        const consumableNameSafe = consumable.name.replace(/"/g, '&quot;').replace(/'/g, '&#39;');
        html += `<button class="btn btn-success buy-consumable-btn" data-name="${consumableNameSafe}" data-use-ftickets="false">💰 ゴールドで購入</button>`;
        html += `<button class="btn btn-success buy-consumable-btn" data-name="${consumableNameSafe}" data-use-ftickets="true">🎫 F券で購入</button>`;
        html += `</div>`;
        html += `</div>`;
    });
    html += '</div>';
    
    // 所持アイテム
    html += '<h3 style="margin-top: 30px; color: #667eea;">所持アイテム</h3>';
    html += '<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 15px;">';
    
    if (gameState.player.inventory_weapons.length > 0) {
        html += '<div><strong>⚔️ 武器:</strong>';
        gameState.player.inventory_weapons.forEach(weapon => {
            html += `<div>⚔️ ${weapon.name} (攻撃力+${weapon.attack_bonus})</div>`;
        });
        html += '</div>';
    }
    
    if (gameState.player.inventory_armors.length > 0) {
        html += '<div><strong>🛡️ 防具:</strong>';
        gameState.player.inventory_armors.forEach(armor => {
            html += `<div>🛡️ ${armor.name} (防御力+${armor.defense_bonus})</div>`;
        });
        html += '</div>';
    }
    
    if (gameState.player.inventory_consumables && Object.keys(gameState.player.inventory_consumables).length > 0) {
        html += '<div><strong>💊 回復アイテム:</strong>';
        for (const [itemName, quantity] of Object.entries(gameState.player.inventory_consumables)) {
            if (quantity > 0) {
                html += `<div>💊 ${itemName} × ${quantity}</div>`;
            }
        }
        html += '</div>';
    }
    
    html += '</div>';
    
    shopContent.innerHTML = html;
    
    // イベントリスナーを追加（動的に追加されたボタン用）
    shopContent.querySelectorAll('.buy-item-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const type = this.getAttribute('data-type');
            const name = this.getAttribute('data-name');
            const useFTickets = this.getAttribute('data-use-ftickets') === 'true';
            buyItem(type, name, useFTickets);
        });
    });
    
    shopContent.querySelectorAll('.buy-consumable-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const name = this.getAttribute('data-name');
            const useFTickets = this.getAttribute('data-use-ftickets') === 'true';
            buyConsumable(name, useFTickets);
        });
    });
}

// 回復アイテム購入
async function buyConsumable(name, useFTickets) {
    const result = await apiCall('/api/shop/buy_consumable', 'POST', {
        name: name,
        use_f_tickets: useFTickets,
        quantity: 1
    });
    
    if (result.success) {
        gameState = result.game_state;
        updateStatus();
        showMessage(result.message, 'success');
        showShop(); // ショップ画面を再表示
    } else {
        showMessage(result.message, 'error');
    }
}

// 回復アイテム使用
async function useConsumable(characterName, itemName) {
    const result = await apiCall('/api/use_consumable', 'POST', {
        character_name: characterName,
        name: itemName
    });
    
    if (result.success) {
        gameState = result.game_state;
        updateStatus();
        showMessage(result.message, 'success');
        showParty(); // パーティ画面を再表示
    } else {
        showMessage(result.message, 'error');
    }
}

// アイテム購入
async function buyItem(type, name, useFTickets) {
    const result = await apiCall('/api/shop/buy', 'POST', {
        type: type,
        name: name,
        use_f_tickets: useFTickets
    });
    
    if (result.success) {
        gameState = result.game_state;
        updateStatus();
        showMessage(result.message, 'success');
        showShop(); // ショップ画面を再表示
    } else {
        showMessage(result.message, 'error');
    }
}

// パーティ表示
async function showParty() {
    currentPanel = 'party';
    await updateStatus();
    
    const panel = document.getElementById('game-panel');
    let html = '<div class="panel-title">パーティ状態</div>';
    html += '<div class="party-list">';
    
    gameState.player.party.forEach(member => {
        const hpPercent = (member.hp / member.max_hp) * 100;
        const mpPercent = member.max_mp > 0 ? (member.mp / member.max_mp) * 100 : 0;
        const expNeeded = member.exp_needed || (member.level * 100);
        const expPercent = member.experience !== undefined ? (member.experience / expNeeded) * 100 : 0;
        
        html += `<div class="character-card">`;
        html += `<div class="character-name" style="display: flex; align-items: center; gap: 10px;">`;
        html += `<span style="font-size: 2em;">${member.emoji || '👤'}</span>`;
        html += `<span>${member.name} (Lv.${member.level})</span>`;
        html += `</div>`;
        html += `<div class="character-stats">`;
        html += `<div class="stat-item"><span>❤️ HP:</span><span>${member.hp}/${member.max_hp}</span></div>`;
        if (member.max_mp > 0) {
            html += `<div class="stat-item"><span>💙 MP:</span><span>${member.mp}/${member.max_mp}</span></div>`;
        }
        html += `<div class="stat-item"><span>💪 攻撃力:</span><span>${member.attack}</span></div>`;
        html += `<div class="stat-item"><span>🛡️ 防御力:</span><span>${member.defense}</span></div>`;
        if (member.experience !== undefined) {
            html += `<div class="stat-item"><span>⭐ 経験値:</span><span>${member.experience}/${expNeeded}</span></div>`;
        }
        html += `</div>`;
        html += `<div class="hp-bar"><div class="hp-bar-fill" style="width: ${hpPercent}%"></div></div>`;
        if (member.max_mp > 0) {
            html += `<div class="mp-bar"><div class="mp-bar-fill" style="width: ${mpPercent}%"></div></div>`;
        }
        if (member.experience !== undefined) {
            html += `<div style="background: #e9ecef; border-radius: 5px; height: 15px; margin: 5px 0; overflow: hidden; position: relative;">`;
            html += `<div style="background: linear-gradient(90deg, #ffc107, #ff9800); height: 100%; width: ${Math.min(expPercent, 100)}%; transition: width 0.3s;"></div>`;
            html += `<div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; display: flex; align-items: center; justify-content: center; font-size: 10px; color: #333;">${member.experience}/${expNeeded}</div>`;
            html += `</div>`;
        }
        if (member.equipped_weapon) {
            html += `<div style="margin-top: 10px;"><strong>⚔️ 武器:</strong> ${member.equipped_weapon}</div>`;
        }
        if (member.equipped_armor) {
            html += `<div><strong>🛡️ 防具:</strong> ${member.equipped_armor}</div>`;
        }
        // 回復アイテム使用ボタン
        if (gameState.player.inventory_consumables && Object.keys(gameState.player.inventory_consumables).length > 0) {
            html += `<div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #e9ecef;">`;
            html += `<strong>💊 回復アイテム:</strong><br>`;
            for (const [itemName, quantity] of Object.entries(gameState.player.inventory_consumables)) {
                if (quantity > 0) {
                    html += `<button class="btn btn-secondary use-consumable-btn" style="margin: 5px; padding: 5px 10px; font-size: 0.9em;" data-character="${member.name.replace(/"/g, '&quot;')}" data-item="${itemName.replace(/"/g, '&quot;')}">${itemName} × ${quantity}</button>`;
                }
            }
            html += `</div>`;
        }
        html += `</div>`;
    });
    
    html += '</div>';
    
    // 装備変更セクション
    if (gameState.player.inventory_weapons.length > 0 || gameState.player.inventory_armors.length > 0) {
        html += '<div style="margin-top: 30px;">';
        html += '<h3 style="color: #667eea;">装備変更</h3>';
        html += '<select id="equip-character" style="padding: 10px; margin: 10px 0; width: 100%;">';
        gameState.player.party.forEach(member => {
            html += `<option value="${member.name}">${member.name}</option>`;
        });
        html += '</select>';
        
        if (gameState.player.inventory_weapons.length > 0) {
            html += '<select id="equip-weapon" style="padding: 10px; margin: 10px 0; width: 100%;">';
            html += '<option value="">武器を選択</option>';
            gameState.player.inventory_weapons.forEach(weapon => {
                html += `<option value="${weapon.name}">${weapon.name}</option>`;
            });
            html += '</select>';
        }
        
        if (gameState.player.inventory_armors.length > 0) {
            html += '<select id="equip-armor" style="padding: 10px; margin: 10px 0; width: 100%;">';
            html += '<option value="">防具を選択</option>';
            gameState.player.inventory_armors.forEach(armor => {
                html += `<option value="${armor.name}">${armor.name}</option>`;
            });
            html += '</select>';
        }
        
        html += '<button class="btn btn-primary equip-items-btn" style="width: 100%;">装備する</button>';
        html += '</div>';
    }
    
    panel.innerHTML = html;
    
    // 装備変更ボタンと回復アイテム使用ボタンのイベントリスナー
    const equipBtn = panel.querySelector('.equip-items-btn');
    if (equipBtn) {
        equipBtn.addEventListener('click', equipItems);
    }
    
    panel.querySelectorAll('.use-consumable-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const characterName = this.getAttribute('data-character');
            const itemName = this.getAttribute('data-item');
            useConsumable(characterName, itemName);
        });
    });
}

// 装備変更
async function equipItems() {
    const characterName = document.getElementById('equip-character').value;
    const weaponName = document.getElementById('equip-weapon')?.value;
    const armorName = document.getElementById('equip-armor')?.value;
    
    if (weaponName) {
        const result = await apiCall('/api/equip', 'POST', {
            character_name: characterName,
            type: 'weapon',
            name: weaponName
        });
        
        if (result.success) {
            gameState = result.game_state;
            showMessage(result.message, 'success');
        } else {
            showMessage(result.message, 'error');
        }
    }
    
    if (armorName) {
        const result = await apiCall('/api/equip', 'POST', {
            character_name: characterName,
            type: 'armor',
            name: armorName
        });
        
        if (result.success) {
            gameState = result.game_state;
            showMessage(result.message, 'success');
        } else {
            showMessage(result.message, 'error');
        }
    }
    
    if (weaponName || armorName) {
        showParty();
    }
}

// 経済情勢表示
async function showEconomy() {
    currentPanel = 'economy';
    await updateStatus();
    
    const fTicketValue = Math.floor(gameState.f_ticket_system.base_value * 
        ({'好況': 1.5, '回復': 1.2, '安定': 1.0, '不況': 0.8, '恐慌': 0.5}[gameState.f_ticket_system.current_condition] || 1.0));
    const totalValue = fTicketValue * gameState.player.f_tickets;
    
    const panel = document.getElementById('game-panel');
    let html = '<div class="panel-title">経済情勢</div>';
    html += '<div class="economy-info">';
    html += `<div class="economy-condition">${gameState.f_ticket_system.current_condition}</div>`;
    
    const descriptions = {
        '好況': '経済が好調で、F券の価値が上昇しています。',
        '回復': '経済が回復傾向にあり、F券の価値が少し上がっています。',
        '安定': '経済は安定しており、F券の価値は変動していません。',
        '不況': '経済が不況で、F券の価値が下落しています。',
        '恐慌': '経済恐慌により、F券の価値が大幅に下落しています。'
    };
    
    html += `<p>${descriptions[gameState.f_ticket_system.current_condition] || ''}</p>`;
    html += `<div style="margin-top: 20px;">`;
    html += `<p><strong>F券1枚の現在の価値:</strong> ${fTicketValue}G</p>`;
    html += `<p><strong>所持F券:</strong> ${gameState.player.f_tickets}枚</p>`;
    html += `<p><strong>F券の合計価値:</strong> ${totalValue}G</p>`;
    html += `</div>`;
    html += '</div>';
    
    panel.innerHTML = html;
}

// 金融知識表示
async function showFinancialKnowledge() {
    currentPanel = 'knowledge';
    const result = await apiCall('/api/financial_knowledge');
    
    if (!result.success) {
        showMessage(result.message, 'error');
        return;
    }
    
    const panel = document.getElementById('game-panel');
    let html = '<div class="panel-title">金融知識</div>';
    html += '<div class="knowledge-content">';
    html += `<h3>現在の経済状況: ${result.condition}</h3>`;
    html += `<p>${result.description}</p>`;
    html += `<div style="margin-top: 30px;">`;
    html += `<h3>金融の基礎知識</h3>`;
    html += `<p>${result.knowledge}</p>`;
    html += `<div style="margin-top: 20px;">`;
    html += `<h4>金融用語の説明:</h4>`;
    html += `<ul style="line-height: 2;">`;
    html += `<li><strong>インフレーション（インフレ）:</strong> 物価が継続的に上昇する現象。お金の価値が下がるため、同じ金額で買えるものが減る。</li>`;
    html += `<li><strong>デフレーション（デフレ）:</strong> 物価が継続的に下落する現象。お金の価値が上がるが、経済が停滞する可能性がある。</li>`;
    html += `<li><strong>金利:</strong> お金を借りたり貸したりする際の費用。経済状況に応じて変動する。</li>`;
    html += `<li><strong>株式:</strong> 企業の所有権の一部を表す証券。企業の業績に応じて価値が変動する。</li>`;
    html += `<li><strong>為替:</strong> 異なる通貨を交換する際のレート。国際経済の動きに影響される。</li>`;
    html += `<li><strong>債券:</strong> 企業や政府が発行する借金の証書。信用リスクと金利リスクがある。</li>`;
    html += `</ul>`;
    html += `</div>`;
    html += `</div>`;
    html += '</div>';
    
    panel.innerHTML = html;
}

// メッセージ表示
function showMessage(message, type = 'success') {
    const messageArea = document.getElementById('message-area');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = message;
    
    messageArea.appendChild(messageDiv);
    
    setTimeout(() => {
        messageDiv.remove();
    }, 3000);
}

