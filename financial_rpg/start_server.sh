#!/bin/bash
# 金融知識学習RPG - サーバー起動スクリプト

cd "$(dirname "$0")"

echo "=========================================="
echo "金融知識学習RPG - サーバー起動"
echo "=========================================="
echo ""

# Pythonのバージョンを確認
if ! command -v python3 &> /dev/null; then
    echo "エラー: python3 が見つかりません"
    exit 1
fi

# 依存パッケージの確認
echo "依存パッケージを確認中..."
python3 -c "import flask" 2>/dev/null || {
    echo "Flaskがインストールされていません。インストールしますか？ (y/n)"
    read -r answer
    if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
        pip3 install -r requirements.txt
    else
        echo "キャンセルしました"
        exit 1
    fi
}

echo ""
echo "サーバーを起動しています..."
echo ""

# サーバーを起動
python3 app.py

