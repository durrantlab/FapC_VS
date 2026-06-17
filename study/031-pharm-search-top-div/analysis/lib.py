from pathlib import Path
import csv
import json

def eucl_dist(a: list[int], b: list[int]) -> int:
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2) ** 0.5



def read_in_csv(interaction_csv_dir: Path) -> tuple[dict[str, list[str]], dict[str, list[str]], dict[str, list[list[str | list[int]]]]]:
    # read in interaction_csv_dir
    inter_csv_list: list[Path] = [item for item in interaction_csv_dir.iterdir() if item.is_file() and item.suffix == ".csv"]

    residues: dict[str, list[str]] = {}
    inter_type: dict[str, list[str]] = {}
    if_interact: dict[str, list[list[str | list[int]]]] = {}
    for inter_csv in inter_csv_list:
        region: str = "_".join(inter_csv.name.split(".")[0].split("_")[0:2])
        with open(inter_csv, newline="") as f:
            reader = csv.reader(f)
            next(reader)
            residues[region] = next(reader)
            inter_type[region] = next(reader)
            if_interact[region] = \
                [[[to_bool(u) for u in v.split(".")] for v in row if v != "False"] for row in list(reader)]
    
    return residues, inter_type, if_interact



def to_bool(s):
    return s.strip().lower() in ("true", "1", "t", "yes")



def load_concatenated_json(path: Path) -> list:
    """Will take in a concatanated JSON file (basically multiple JSONs in one)
    and return a list of JSON objects for each one

    Args:
        path (_type_): location of json

    Returns:
        list: list of the jsons in the file
    """
    with open(path) as f:
        text = f.read()

    decoder = json.JSONDecoder()
    objects = []
    idx = 0
    n = len(text)
    while idx < n:
        while idx < n and text[idx].isspace(): 
            idx += 1
        if idx >= n:
            break
        obj, end = decoder.raw_decode(text, idx)
        objects.append(obj)
        idx = end
    return objects