import json
from collections import deque
from typing import Any, Dict
def handle_data(data: Any) -> Dict[str, Any]:
    if data is None:
        return {"value": None}
    if not isinstance(data, (dict, list)):
        return {"value": data}
    result = {}
    queue = deque([(data, "")])
    safety_counter = 0
    max_items = 1000
    while queue:
        current, path = queue.popleft()
        if isinstance(current, dict):
            for key, value in current.items():
                new_path = f"{path}.{key}" if path else key
                if isinstance(value, (dict, list)) and safety_counter < max_items:
                    queue.append((value, new_path))
                else:
                    result[new_path] = value
        elif isinstance(current, list):
            for idx, item in enumerate(current):
                new_path = f"{path}.{idx}" if path else str(idx)
                if isinstance(item, (dict, list)) and safety_counter < max_items:
                    queue.append((item, new_path))
                else:
                    result[new_path] = item
        else:
            result[path] = current
        safety_counter += 1
        if safety_counter > max_items:
            result["__safety_limit_reached__"] = True
            break
    return result
def combine_data(*data_dicts: Dict[str, Any]) -> Dict[str, Any]:
    combined = {}
    for d in data_dicts:
        for k, v in d.items():
            if k in combined:
                if not isinstance(combined[k], list):
                    combined[k] = [combined[k]]
                combined[k].append(v)
            else:
                combined[k] = v
    return combined
def get_data_summary(data: Dict[str, Any]) -> Dict[str, Any]:
    summary = {
        "total_keys": len(data),
        "sample_keys": list(data.keys())[:5],
        "has_truncation": "__safety_limit_reached__" in data
    }
    return summary