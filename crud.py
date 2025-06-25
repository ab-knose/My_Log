"""
crud操作APIを記述するファイル。
Backend For Frontendの考え方に基づき、
main.pyの大きなAPIから、crud.pyの小さなAPIを呼び出す形にする。
ただし、開発初期の段階では、構造の単純化を優先して、main.pyに直接記述しよう。
ある程度小さなAPIができたら、crud.pyに分離することを検討する。
"""

# 開発が進んだら、ここにCRUD操作を行うための関数を分離する。