import json  # For JSON loading
import csv  # For CSV dict writer


def get_leaves(item, key=None, key_prefix=""):
    """
    This function converts nested dictionary structure to flat
    """
    if isinstance(item, dict):
        leaves = {}
        """Iterates the dictionary and go to leaf node after that calls to get_leaves function recursively to go to leaves level"""
        for item_key in item.keys():
            """Some times leaves and parents or some other leaves might have same key that's why adding leave node key to distinguish"""
            temp_key_prefix = (
                item_key if (key_prefix == "") else (key_prefix + "_" + str(item_key))
            )
            leaves.update(get_leaves(item[item_key], item_key, temp_key_prefix))
        return leaves
    elif isinstance(item, list):
        leaves = {}
        elements = []
        """Iterates the list and go to leaf node after that if it is leave then simply add value to current key's list or 
        calls to get_leaves function recursively to go to leaves level"""
        for element in item:
            if isinstance(element, dict) or isinstance(element, list):
                leaves.update(get_leaves(element, key, key_prefix))
            else:
                elements.append(element)
        if len(elements) > 0:
            leaves[key] = elements
        return leaves
    else:
        return {key_prefix: item}


with open("data.json") as f_input, open("output.csv", "w", newline="") as f_output:
    json_data = json.load(f_input, strict=False)
    """'First parse all entries to get the unique fieldnames why because already we have file in RAM level and
    if we put each dictionary after parsing in list or some data structure it will crash your system due to memory constraint
    that's why first we will get the keys first then we convert each dictionary and put it to CSV"""
    fieldnames = set()
    for entry in json_data:
        fieldnames.update(get_leaves(entry).keys())
    csv_output = csv.DictWriter(f_output, delimiter=";", fieldnames=sorted(fieldnames))
    csv_output.writeheader()
    csv_output.writerows(get_leaves(entry) for entry in json_data)
