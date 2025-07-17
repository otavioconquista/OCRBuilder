import numpy as np
import pandas as pd

def generate_json(text_data, keys_to_consider=None, max_distance=100):
    if keys_to_consider is None:
        keys_to_consider = ["pH", "P", "K", "Na", "Mg", "Al", "MO", "Zn", "Fe", "Mn", "Cu", "B", "S"]

    df = pd.DataFrame(text_data)[["text", "x_center", "y_center"]].copy()

    def is_number(text):
        try:
            float(str(text).replace(",", "."))
            return True
        except ValueError:
            return False

    json_output = {}
    potential_keys = {}
    for i, row in df.iterrows():
        key_candidate = str(row["text"]).strip()
        x1, y1 = row["x_center"], row["y_center"]
        if key_candidate in keys_to_consider:
            potential_keys[key_candidate] = {"index": i, "x": x1, "y": y1}

    for key, key_info in potential_keys.items():
        key_index = key_info["index"]
        x1, y1 = key_info["x"], key_info["y"]
        min_dist = float("inf")
        best_value = None
        for j, row2 in df.iterrows():
            val_candidate = str(row2["text"]).strip()
            x2, y2 = row2["x_center"], row2["y_center"]
            if key_index == j or not is_number(val_candidate):
                continue
            dist = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            if dist < min_dist and dist < max_distance:
                min_dist = dist
                best_value = val_candidate
        if best_value:
            try:
                json_output[key] = float(str(best_value).replace(",", "."))
            except ValueError:
                pass

    return json_output