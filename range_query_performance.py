import csv
import timeit
from BTrees import OOBTree

# Function to load data from CSV
def load_data_from_csv(file_path):
    """
    Loads data from a CSV file and returns it as a list of dictionaries.
    """
    items = []
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            item = {
                "ID": int(row["ID"]),
                "Name": row["Name"],
                "Category": row["Category"],
                "Price": float(row["Price"])
            }
            items.append(item)
    return items

# Function to add items to OOBTree
def add_item_to_tree(tree, item):
    """
    Adds an item to the OOBTree.
    """
    tree[item["ID"]] = item

# Function to add items to dict
def add_item_to_dict(dictionary, item):
    """
    Adds an item to the dictionary.
    """
    dictionary[item["ID"]] = item

# Function to perform range query on OOBTree
def range_query_tree(tree, min_price, max_price):
    """
    Performs a range query on the OOBTree to find items within the price range.
    """
    return [
        value for _, value in tree.items()
        if min_price <= value["Price"] <= max_price
    ]

# Function to perform range query on dict
def range_query_dict(dictionary, min_price, max_price):
    """
    Performs a range query on the dictionary to find items within the price range.
    """
    return [
        value for value in dictionary.values()
        if min_price <= value["Price"] <= max_price
    ]

# Main function for analysis
def main():
    file_path = "generated_items_data.csv"
    items = load_data_from_csv(file_path)

    # Initialize data structures
    tree = OOBTree()
    dictionary = {}

    # Add items to data structures
    for item in items:
        add_item_to_tree(tree, item)
        add_item_to_dict(dictionary, item)

    # Define range for queries
    min_price = 50.0
    max_price = 150.0

    # Measure performance for OOBTree
    tree_time = timeit.timeit(
        lambda: range_query_tree(tree, min_price, max_price),
        number=100
    )

    # Measure performance for dict
    dict_time = timeit.timeit(
        lambda: range_query_dict(dictionary, min_price, max_price),
        number=100
    )

    # Print results
    print(f"Total range_query time for OOBTree: {tree_time:.6f} seconds")
    print(f"Total range_query time for Dict: {dict_time:.6f} seconds")

    # Optional: Compare results for correctness
    tree_results = range_query_tree(tree, min_price, max_price)
    dict_results = range_query_dict(dictionary, min_price, max_price)

    assert tree_results == dict_results, "Results do not match between OOBTree and Dict!"

if __name__ == "__main__":
    main()
