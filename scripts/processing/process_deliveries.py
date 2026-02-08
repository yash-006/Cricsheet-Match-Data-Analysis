import os
import json
import pandas as pd
from sqlalchemy import create_engine

# ---------- PATHS ----------
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
raw_path = os.path.join(project_root, "data", "raw_json")

# ---------- MYSQL CONNECTION ----------
engine = create_engine(
    "mysql+pymysql://root:Root@localhost/cricsheet_db"
)

batch_data = []
batch_size = 5000
inserted_rows = 0

# ---------- LOOP THROUGH DATASETS ----------
for folder in os.listdir(raw_path):

    folder_path = os.path.join(raw_path, folder)

    if os.path.isdir(folder_path):

        print(f"\nProcessing {folder}...")

        for file in os.listdir(folder_path):

            if not file.endswith(".json"):
                continue

            file_path = os.path.join(folder_path, file)
            match_id = file.replace(".json", "")

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except:
                print(f"Skipping corrupted file: {file}")
                continue

            innings_list = data.get("innings", [])

            # ---------- LOOP INNINGS ----------
            for inning_index, inning in enumerate(innings_list, start=1):

                overs = inning.get("overs", [])

                # ---------- LOOP OVERS ----------
                for over in overs:

                    over_no = over.get("over")

                    deliveries = over.get("deliveries", [])

                    # ---------- LOOP BALLS ----------
                    for ball_index, delivery in enumerate(deliveries, start=1):

                        batsman = delivery.get("batter")
                        bowler = delivery.get("bowler")

                        runs = delivery.get("runs", {})

                        runs_batsman = runs.get("batter", 0)
                        runs_extras = runs.get("extras", 0)
                        runs_total = runs.get("total", 0)

                        wicket = 0
                        dismissal_kind = None
                        player_dismissed = None

                        if "wickets" in delivery:
                            wicket = 1
                            dismissal = delivery["wickets"][0]
                            dismissal_kind = dismissal.get("kind")
                            player_dismissed = dismissal.get("player_out")

                        record = {
                            "match_id": match_id,
                            "inning": inning_index,
                            "over_no": over_no,
                            "ball_no": ball_index,
                            "batsman": batsman,
                            "bowler": bowler,
                            "runs_batsman": runs_batsman,
                            "runs_extras": runs_extras,
                            "runs_total": runs_total,
                            "wicket": wicket,
                            "dismissal_kind": dismissal_kind,
                            "player_dismissed": player_dismissed
                        }

                        batch_data.append(record)

                        # ---------- BATCH INSERT ----------
                        if len(batch_data) >= batch_size:

                            df = pd.DataFrame(batch_data)

                            df.to_sql(
                                name="deliveries",
                                con=engine,
                                if_exists="append",
                                index=False
                            )

                            inserted_rows += len(df)
                            print(f"Inserted {inserted_rows} deliveries...")

                            batch_data = []

# ---------- FINAL INSERT ----------
if batch_data:
    df = pd.DataFrame(batch_data)

    df.to_sql(
        name="deliveries",
        con=engine,
        if_exists="append",
        index=False
    )

    inserted_rows += len(df)

print(f"\nTotal Deliveries Inserted: {inserted_rows} ✅")
