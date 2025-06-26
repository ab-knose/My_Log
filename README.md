# My_Log

DARABASE_URL = "mysql+pymysql://admin:Digitaldev1@group1-chats.c7c4ksi06r6a.ap-southeast-2.rds.amazonaws.com:3306/group1"

User: admin
PW: Digitaldev1
schema: group1
→ 作り直します

# python ハンズオン

python 仮想環境

<!-- 作成 -->

python -m venv .venv

<!-- 環境に入る(作成したフォルダで) -->

.venv\Scripts\activate.ps1

<!-- 仮想環境に入った状態で -->

python.exe -m pip install --upgrade pip
pip install -r .\requirements.txt

環境から出る
deactivate

<!-- 仮想環境に入った状態でアプリを立ち上げる -->
<!-- mainは変更 -->

uvicorn main:app --reload

<!-- github pycacheをコミットしないために -->

git rm -r --cached **pycache**/

<!-- テストたくみ -->

now

<!-- Vue環境セットアップ-->
npm create vite@latest vue_env
cd vue_env
npm install
npm run dev

npm install axios
npm install vue-router
npm install vue-cal