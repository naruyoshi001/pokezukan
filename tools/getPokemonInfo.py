import requests

TABLE_NAME = "pokemon"

# テーブルCREATE文
CREATE_SQL = f"""
DROP TABLE IF EXISTS {TABLE_NAME};
CREATE TABLE {TABLE_NAME} (
  id INTEGER PRIMARY KEY,
  name TEXT,
  type1 TEXT,
  type2 TEXT,
  hp INTEGER,
  atk INTEGER,
  def INTEGER,
  sp_atk INTEGER,
  sp_def INTEGER,
  spd INTEGER,
  ability1 TEXT,
  ability2 TEXT
);
"""

# Flaskモデル出力用
MODEL_TXT = """
class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    type1 = db.Column(db.String(10), nullable=False)
    type2 = db.Column(db.String(10))
    hp = db.Column(db.Integer)
    atk = db.Column(db.Integer)
    def_ = db.Column("def", db.Integer)
    sp_atk = db.Column(db.Integer)
    sp_def = db.Column(db.Integer)
    spd = db.Column(db.Integer)
    ability1 = db.Column(db.String(40))
    ability2 = db.Column(db.String(40))
"""

# detail.htmlテンプレート
DETAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{{ pokemon.name }}の詳細</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
  <h1>{{ pokemon.name }}（No.{{ pokemon.id }}）</h1>
  <ul>
      <li>タイプ1：{{ pokemon.type1 }}</li>
      <li>タイプ2：{{ pokemon.type2 or 'なし' }}</li>
      <li>HP：{{ pokemon.hp }}</li>
      <li>こうげき：{{ pokemon.atk }}</li>
      <li>ぼうぎょ：{{ pokemon.def }}</li>
      <li>とくこう：{{ pokemon.sp_atk }}</li>
      <li>とくぼう：{{ pokemon.sp_def }}</li>
      <li>すばやさ：{{ pokemon.spd }}</li>
      <li>とくせい1：{{ pokemon.ability1 }}</li>
      <li>とくせい2：{{ pokemon.ability2 or 'なし' }}</li>
  </ul>
  <a href="{{ url_for('index') }}">一覧に戻る</a>
</body>
</html>
"""

POKEAPI_BASE = "https://pokeapi.co/api/v2/pokemon/"

def get_pokemon_info(poke_id):
    poke_url = f"{POKEAPI_BASE}{poke_id}"
    resp = requests.get(poke_url)
    if resp.status_code != 200:
        return None
    data = resp.json()
    type1 = data['types'][0]['type']['name']
    type2 = data['types'][1]['type']['name'] if len(data['types']) > 1 else ''
    base_stats = { stat['stat']['name']: stat['base_stat'] for stat in data['stats'] }
    hp = base_stats.get('hp', 0)
    atk = base_stats.get('attack', 0)
    def_ = base_stats.get('defense', 0)
    sp_atk = base_stats.get('special-attack', 0)
    sp_def = base_stats.get('special-defense', 0)
    spd = base_stats.get('speed', 0)
    ability1 = data['abilities'][0]['ability']['name']
    ability2 = data['abilities'][1]['ability']['name'] if len(data['abilities']) > 1 else ''
    # 日本語名取得
    species_url = data['species']['url']
    resp2 = requests.get(species_url)
    if resp2.status_code != 200:
        return None
    species = resp2.json()
    jp_name = ''
    for name_obj in species['names']:
        if name_obj['language']['name'] == 'ja':
            jp_name = name_obj['name']
            break
    return (poke_id, jp_name, type1, type2, hp, atk, def_, sp_atk, sp_def, spd, ability1, ability2)

def main():
    output_sql = "poke_info.sql"
    output_model = "pokemon_model.txt"
    output_detail = "detail_template.txt"

    # Flaskモデル定義txt出力
    with open(output_model, "w", encoding="utf-8") as f:
        f.write(MODEL_TXT.strip())
    print(f"Flaskモデル定義を {output_model} に出力しました")

    # detail.htmlテンプレートtxt出力
    with open(output_detail, "w", encoding="utf-8") as f:
        f.write(DETAIL_TEMPLATE.strip())
    print(f"detail.html用テンプレートを {output_detail} に出力しました")

    # SQLファイル出力
    with open(output_sql, "w", encoding="utf-8") as f:
        f.write("-- DROP & CREATE table\n")
        f.write(CREATE_SQL.strip() + "\n\n")
        for i in range(1, 152):  # 必要に応じて範囲を拡張
            info = get_pokemon_info(i)
            if info:
                (poke_id, name_ja, type1, type2, hp, atk, def_, sp_atk, sp_def, spd, ability1, ability2) = info
                # エスケープ
                name_ja = name_ja.replace("'", "''")
                type1 = type1.replace("'", "''")
                type2 = type2.replace("'", "''")
                ability1 = ability1.replace("'", "''")
                ability2 = ability2.replace("'", "''")
                f.write(
                    f"INSERT INTO {TABLE_NAME} (id, name, type1, type2, hp, atk, def, sp_atk, sp_def, spd, ability1, ability2) "
                    f"VALUES ({poke_id}, '{name_ja}', '{type1}', '{type2}', {hp}, {atk}, {def_}, {sp_atk}, {sp_def}, {spd}, '{ability1}', '{ability2}');\n"
                )
                print(f"Got: {name_ja}")

    print(f"SQLファイルを {output_sql} に出力しました")

if __name__ == "__main__":
    main()
