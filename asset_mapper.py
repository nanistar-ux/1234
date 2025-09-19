import numpy as np
import cv2

def analyze_assets(image_path: str):
    """Dummy asset analysis: vegetation, water, built areas."""
    if not image_path:
        return {"vegetation": None, "water": None, "built": None, "other": None}

    img = cv2.imread(image_path)
    if img is None:
        return {"error": "Image not found"}

    h, w, _ = img.shape
    grid_size = 50
    tiles = []
    for y in range(0, h, grid_size):
        for x in range(0, w, grid_size):
            tile = img[y:y+grid_size, x:x+grid_size]
            if tile.size > 0:
                tiles.append(tile)

    summary = {"vegetation": 0, "water": 0, "built": 0, "other": 0}
    for tile in tiles:
        avg_color = tile.mean(axis=(0, 1))  # BGR
        if avg_color[1] > 100:  # green → vegetation
            summary["vegetation"] += 1
        elif avg_color[0] > 120:  # blue → water
            summary["water"] += 1
        elif avg_color[2] > 120:  # red → built
            summary["built"] += 1
        else:
            summary["other"] += 1

    total = sum(summary.values())
    return {k: {"count": v, "pct": round((v/total)*100, 2)} for k, v in summary.items()}
