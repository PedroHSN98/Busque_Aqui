#banco.py
from pathlib import Path
import sqlite3
from data.estabelecimentos import ESTABELECIMENTOS  # precisa existir essa lista

DB_PATH = Path(__file__).resolve().parent / "data" / "estabelecimentos.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS estabelecimentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    endereco TEXT NOT NULL,
    lat REAL,
    lon REAL,
    categoria TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (nome, endereco, categoria)  -- permite o mesmo nome/endereço em categorias diferentes
);
CREATE INDEX IF NOT EXISTS idx_estab_categoria ON estabelecimentos(categoria);
"""

def criar_ou_atualizar_banco(recreate: bool = False):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    if recreate:
        cur.execute("DROP TABLE IF EXISTS estabelecimentos")

    # cria tabela/índices
    for stmt in SCHEMA_SQL.split(";"):
        if stmt.strip():
            cur.execute(stmt)

    # prepara os dados
    rows = []
    for e in ESTABELECIMENTOS:
        rows.append((
            e.get("nome"),
            e.get("endereco"),
            float(e["lat"]) if e.get("lat") is not None else None,
            float(e["lon"]) if e.get("lon") is not None else None,
            e.get("categoria")
        ))

    # insere ignorando duplicatas (pela UNIQUE acima)
    cur.executemany(
        """
        INSERT OR IGNORE INTO estabelecimentos (nome, endereco, lat, lon, categoria)
        VALUES (?, ?, ?, ?, ?)
        """,
        rows
    )

    conn.commit()

    total = cur.execute("SELECT COUNT(*) FROM estabelecimentos").fetchone()[0]
    amostra = cur.execute(
        "SELECT nome, categoria, endereco FROM estabelecimentos LIMIT 3"
    ).fetchall()

    conn.close()

    print(f"Banco criado/atualizado em: {DB_PATH}")
    print(f"Registros no banco: {total}")
    print("Amostra:", amostra)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Cria/popula o banco SQLite com os estabelecimentos.")
    parser.add_argument("--recreate", action="store_true",
                        help="Apaga e recria a tabela antes de inserir (cuidado: perde dados).")
    args = parser.parse_args()
    criar_ou_atualizar_banco(recreate=args.recreate)
