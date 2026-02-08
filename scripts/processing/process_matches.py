import os
import json
import pandas as pd
from sqlalchemy import create_engine

# ---------- PATHS ----------
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
raw_path = os.path.join(project_root, "data", "raw_json")

all_matches = []

# ---------- LOOP THROUGH DATASETS ----------
for folder in os.listdir(raw_path):

    folder_path = os.path.join(raw_path, folder)

    if os.path.isdir(folder_path):

        print(f"\nProcessing {folder}...")

        files = os.listdir(folder_path)

        for file in files:

            file_path = os.path.join(folder_path, file)

            skipped = 0
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

            except Exception as e:
                print(f"Skipping corrupted file: {file}")
                skipped += 1
                continue

            info = data.get("info", {})

            # ---------- WIN MARGIN FIX ----------
            outcome_by = info.get("outcome", {}).get("by", {})

            win_margin = None

            if "runs" in outcome_by:
                win_margin = f"{outcome_by['runs']} runs"

            elif "wickets" in outcome_by:
                win_margin = f"{outcome_by['wickets']} wickets"

            # ---------- MATCH RECORD ----------
            match = {
                "match_id": file.replace(".json", ""),
                "match_type": info.get("match_type"),
                "team1": info.get("teams", [None, None])[0],
                "team2": info.get("teams", [None, None])[1],
                "venue": info.get("venue"),
                "city": info.get("city"),
                "match_date": info.get("dates", [None])[0],
                "toss_winner": info.get("toss", {}).get("winner"),
                "toss_decision": info.get("toss", {}).get("decision"),
                "winner": info.get("outcome", {}).get("winner"),
                "win_margin": win_margin
            }

            all_matches.append(match)
        
        print("Skipped files:", skipped)


# ---------- DATAFRAME ----------
df = pd.DataFrame(all_matches)

print("\nTotal Matches Processed:", len(df))

# ---------- MYSQL CONNECTION ----------
engine = create_engine(
    "mysql+pymysql://root:Root@localhost/cricsheet_db"
)

# ---------- BATCH INSERT ----------
batch_size = 500
total_rows = len(df)

for start in range(0, total_rows, batch_size):

    end = start + batch_size
    batch_df = df.iloc[start:end]

    batch_df.to_sql(
        name="matches",
        con=engine,
        if_exists="append",
        index=False
    )

    print(f"Inserted rows {start} → {end}")

print("\nFull dataset inserted into MySQL ✅")
