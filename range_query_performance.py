import csv
import timeit
from BTrees.OOBTree import OOBTree

def load_data_from_csv(file_path):
    """
    Loads product data from a CSV file.
    Each row is expected to have columns: ID, Name, Category, Price.
    :param file_path: Path to the CSV file.
    :return: A list of dictionaries, where each dictionary represents a product.
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

def add_item_to_tree(tree, item):
    """
    Adds a product to the OOBTree, using 'Price' as the key.
    If there are multiple items with the same price, they are stored in a list.

    :param tree: An OOBTree instance.
    :param item: A product dictionary with keys: "ID", "Name", "Category", "Price".
    """
    price = item["Price"]
    if price not in tree:
        tree[price] = []
    tree[price].append(item)

def add_item_to_dict(dictionary, item):
    """
    Adds a product to a standard Python dict, using 'ID' as the key.
    
    :param dictionary: A Python dict.
    :param item: A product dictionary with keys: "ID", "Name", "Category", "Price".
    """
    dictionary[item["ID"]] = item

def range_query_tree(tree, min_price, max_price):
    """
    Performs a range query on the OOBTree by price (key).
    Returns all products whose price is between min_price and max_price (inclusive).
    
    :param tree: An OOBTree instance keyed by price.
    :param min_price: The minimum price for the query range.
    :param max_price: The maximum price for the query range.
    :return: A list of product dictionaries within the specified price range.
    """
    results = []
    # tree.items(min_key, max_key) returns an iterator of (price, [items]) 
    # for all prices between min_price and max_price (inclusive).
    for price, items_list in tree.items(min_price, max_price):
        results.extend(items_list)
    return results

def range_query_dict(dictionary, min_price, max_price):
    """
    Performs a range query on a Python dict keyed by ID.
    It scans through all products and filters them by price.
    This is a linear search (O(n)).
    
    :param dictionary: A Python dict of products keyed by ID.
    :param min_price: The minimum price for the query range.
    :param max_price: The maximum price for the query range.
    :return: A list of product dictionaries within the specified price range.
    """
    return [
        product
        for product in dictionary.values()
        if min_price <= product["Price"] <= max_price
    ]

def main():
    # Path to the CSV file. Adjust if needed.
    file_path = "./generated_items_data.csv"

    # 1. Load items from CSV
    items = load_data_from_csv(file_path)

    # 2. Initialize data structures
    tree = OOBTree()    # keyed by Price
    dictionary = {}     # keyed by ID

    # 3. Add items to both structures
    for item in items:
        add_item_to_tree(tree, item)
        add_item_to_dict(dictionary, item)

    # Define the price range for queries
    min_price = 50.0
    max_price = 150.0

    # 4. Measure performance for OOBTree (100 queries)
    tree_time = timeit.timeit(
        lambda: range_query_tree(tree, min_price, max_price),
        number=100
    )

    # 5. Measure performance for dict (100 queries)
    dict_time = timeit.timeit(
        lambda: range_query_dict(dictionary, min_price, max_price),
        number=100
    )

    # 6. Print total time results
    print(f"Total range_query time for OOBTree: {tree_time:.6f} seconds")
    print(f"Total range_query time for Dict: {dict_time:.6f} seconds")

    # 7. Compare results for correctness (compare sets of IDs instead of raw lists)
    tree_results = range_query_tree(tree, min_price, max_price)
    dict_results = range_query_dict(dictionary, min_price, max_price)

    tree_ids = {item["ID"] for item in tree_results}
    dict_ids = {item["ID"] for item in dict_results}

    if tree_ids != dict_ids:
        raise AssertionError("Results do not match between OOBTree and Dict!")
    else:
        print("Range query results match by ID set!")

if __name__ == "__main__":
    main()
