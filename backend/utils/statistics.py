import numpy as np


def coefficient_of_variation(values: list[float]) -> float:
    if not values:
        return 0.0
    mean = np.mean(values)
    if mean == 0:
        return 0.0
    return float(np.std(values) / mean)


def moving_average(values: list[float], window: int) -> list[float]:
    if len(values) < window:
        return [float(np.mean(values))] if values else []
    result = []
    for i in range(len(values) - window + 1):
        result.append(float(np.mean(values[i:i + window])))
    return result
