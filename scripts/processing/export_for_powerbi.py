import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://root:Root@localhost/cricsheet_db"
)

# Matches table
matches = pd.read_sql("SELECT * FROM matches", engine)
matches.to_csv("data/processed/matches.csv", index=False)

# Deliveries table (aggregated for performance)
batsman_runs = pd.read_sql("""
    SELECT batsman,
           SUM(runs_batsman) AS total_runs
    FROM deliveries
    GROUP BY batsman
""", engine)

batsman_runs.to_csv("data/processed/batsman_runs.csv", index=False)

bowler_wickets = pd.read_sql("""
    SELECT bowler,
           COUNT(*) AS wickets
    FROM deliveries
    WHERE wicket = 1
    GROUP BY bowler
""", engine)

bowler_wickets.to_csv("data/processed/bowler_wickets.csv", index=False)

print("Data exported for Power BI ✅")
