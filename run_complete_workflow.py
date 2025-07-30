#!/usr/bin/env python3
"""
完全なワークフロー実行スクリプト

1. 二次合成による評価と順位リスト作成
2. 三次合成による評価と近接周波数フィルタリング
3. 最終結果の表示
"""

import os
import sys
from create_secondary_ranking import main as create_secondary_ranking
from apply_tertiary_filter import main as apply_tertiary_filter

def check_required_files():
    """必要なファイルの存在をチェック"""
    required_files = ['freq.txt', 'vtxtable.txt', 'LED.txt']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("エラー: 以下の必要なファイルが見つかりません:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    
    return True

def main():
    """完全なワークフローを実行"""
    print("=" * 80)
    print("IMD評価完全ワークフロー")
    print("=" * 80)
    
    # 必要なファイルの存在をチェック
    if not check_required_files():
        sys.exit(1)
    
    print("\nステップ1: 二次合成による評価と順位リスト作成")
    print("-" * 60)
    
    try:
        # 二次合成による評価を実行
        secondary_results = create_secondary_ranking()
        
        if not secondary_results:
            print("エラー: 二次合成による評価が失敗しました")
            sys.exit(1)
        
        print(f"\n✅ 二次合成による評価が完了しました")
        print(f"   結果: {len(secondary_results)}個の組み合わせを評価")
        
    except Exception as e:
        print(f"エラー: 二次合成による評価中にエラーが発生しました: {e}")
        sys.exit(1)
    
    print("\nステップ2: 三次合成による評価と近接周波数フィルタリング")
    print("-" * 60)
    
    try:
        # 三次合成による評価とフィルタリングを実行
        apply_tertiary_filter()
        
        print(f"\n✅ 三次合成による評価とフィルタリングが完了しました")
        
    except Exception as e:
        print(f"エラー: 三次合成による評価中にエラーが発生しました: {e}")
        sys.exit(1)
    
    print("\nステップ3: 最終結果の確認")
    print("-" * 60)
    
    # 生成されたファイルの確認
    output_files = ['secondary_ranking.txt', 'filtered_ranking.txt']
    
    for file in output_files:
        if os.path.exists(file):
            file_size = os.path.getsize(file)
            print(f"✅ {file}: {file_size} bytes")
        else:
            print(f"❌ {file}: ファイルが見つかりません")
    
    print("\n" + "=" * 80)
    print("ワークフロー完了!")
    print("=" * 80)
    print("\n生成されたファイル:")
    print("- secondary_ranking.txt: 二次合成による順位リスト")
    print("- filtered_ranking.txt: 三次合成評価とフィルタリング結果")
    print("\n次のステップ:")
    print("1. filtered_ranking.txtを確認して採用候補を選択")
    print("2. 必要に応じて追加の分析を実行")

if __name__ == "__main__":
    main() 