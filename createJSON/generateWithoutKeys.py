import numpy as np
import pandas as pd

def generate_json(text_data, max_distance=100):
    df = pd.DataFrame(text_data)[["text", "x_center", "y_center"]].copy()

    def is_number(text):
        try:
            float(str(text).replace(",", "."))
            return True
        except ValueError:
            return False

    json_output = {}

    for i, row in df.iterrows():
        key_candidate = str(row["text"]).strip()
        x1, y1 = row["x_center"], row["y_center"]

        # Ignore if key_candidate is a number
        if is_number(key_candidate):
            continue

        min_dist = float("inf")
        best_value = None

        for j, row2 in df.iterrows():
            if i == j:
                continue
            val_candidate = str(row2["text"]).strip()
            x2, y2 = row2["x_center"], row2["y_center"]

            if not is_number(val_candidate):
                continue

            dist = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            if dist < min_dist and dist < max_distance:
                min_dist = dist
                best_value = val_candidate

        if best_value:
            try:
                json_output[key_candidate] = float(str(best_value).replace(",", "."))
            except ValueError:
                pass  # Ignore conversion errors

    return json_output