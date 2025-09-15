def from_mongo(data):
    """Convert MongoDB Ids to strings in the data."""
    for item in data:
        if "_id" in item:
            item["_id"] = str(item["_id"])
    return data