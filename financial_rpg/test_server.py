#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
簡単なテストサーバー - アクセステスト用
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>テストページ</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 50px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            h1 {
                font-size: 3em;
                margin-bottom: 20px;
            }
            p {
                font-size: 1.5em;
            }
        </style>
    </head>
    <body>
        <h1>✅ サーバーは正常に動作しています！</h1>
        <p>このページが表示されれば、Flaskサーバーは正常に動作しています。</p>
        <p><a href="/" style="color: white; text-decoration: underline;">金融知識学習RPGにアクセス</a></p>
    </body>
    </html>
    '''

if __name__ == '__main__':
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
        except OSError:
            continue
    
    if port is None:
        print("エラー: 利用可能なポートが見つかりませんでした。")
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print(f"テストサーバー起動中")
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
        sys.exit(1)

