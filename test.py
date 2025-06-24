import pymysql
import sqlalchemy

DATABASE_URL = "mysql+pymysql://admin:Digitaldev1@group1-chats.c7c4ksi06r6a.ap-southeast-2.rds.amazonaws.com:3306/group1"


# データベースに接続
engine = sqlalchemy.create_engine(DATABASE_URL)
with engine.connect() as conn:
    # テーブル一覧を取得
    tables = conn.execute(sqlalchemy.text("SHOW TABLES;")).fetchall()
    print("Tables:")
    for table in tables:
        print(table[0])
        # 各テーブルの中身を表示
        rows = conn.execute(sqlalchemy.text(f"SELECT * FROM `{table[0]}` LIMIT 10;")).fetchall()
        for row in rows:
            print(row)
        print("-" * 40)