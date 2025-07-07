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

def main():
    # ...（略）...
    output_detail = "detail_template.txt"
    with open(output_detail, "w", encoding="utf-8") as f:
        f.write(DETAIL_TEMPLATE.strip())
    print(f"detail.html用テンプレートを {output_detail} に出力しました")

    # ...（あとの処理はそのまま）...
