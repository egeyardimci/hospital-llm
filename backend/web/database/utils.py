def from_mongo(data):
    """Convert MongoDB Ids to strings in the data."""
    for item in data:
        if "_id" in item:
            item["_id"] = str(item["_id"])
    return data

def remove_objectid (obj):
    if isinstance(obj, list):
        return [remove_objectid(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: remove_objectid(value) for key, value in obj.items() if key != '_id'}
    else:
        return obj
