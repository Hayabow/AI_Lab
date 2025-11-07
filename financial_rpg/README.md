# 金融知識学習RPG

金融の知識を学びながら冒険するRPGゲームです。

## 特徴

- ドラゴンクエスト風のターン制戦闘システム
- モンスターが一定確率で仲間になる
- モンスターと人間キャラクターを組み合わせたパーティ編成
- モンスターを倒すとお金と「F券」がもらえる
- F券の価値はエリアの経済情勢に応じて変動
- F券を武器や防具と交換可能
- ストーリーを通じて金融知識を学べる
- Webブラウザでプレイ可能

## セットアップ

### 1. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 2. ゲームの起動

以下のいずれかの方法で起動できます：

**方法1: Pythonで直接起動**
```bash
python app.py
```

**方法2: 起動スクリプトを使用（推奨）**
```bash
./start_server.sh
```

**方法3: テストサーバーで動作確認**
```bash
python test_server.py
```

まずは `python test_server.py` でテストページにアクセスできるか確認してください。

### 3. ブラウザでアクセス

サーバー起動時に表示されるURLにアクセスしてください（通常は以下のいずれか）:

```
http://localhost:5000
http://localhost:8080
http://127.0.0.1:5000
```

ポート5000が使用中の場合は、自動的に別のポート（8080、3000など）が使用されます。

## 実行方法

### Web版（推奨）

```bash
python app.py
```

### コマンドライン版（旧版）

```bash
python main.py
```

## プロジェクト構造

```
financial_rpg/
├── app.py              # Flask Webアプリケーション
├── main.py             # コマンドライン版（旧版）
├── game_engine.py      # ゲームエンジン
├── character.py        # キャラクターシステム
├── monster.py          # モンスターシステム
├── party.py            # パーティシステム
├── battle.py           # 戦闘システム
├── player.py           # プレイヤー管理
├── shop.py             # ショップシステム
├── f_ticket.py         # F券システム
├── item.py             # アイテムシステム
├── templates/          # HTMLテンプレート
│   └── index.html
└── static/             # 静的ファイル
    ├── css/
    │   └── style.css
    └── js/
        └── game.js
```

