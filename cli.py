import requests

BASE_URL = "http://127.0.0.1:5000"

def print_menu():
    print("\n📦 Inventory CLI Menu")
    print("1. Add new item manually")
    print("2. View all inventory")
    print("3. View item details")
    print("4. Update item")
    print("5. Delete an item")
    print("6. Find item on OpenFoodFacts API and add")
    print("0. Exit")

def add_manual_item():
    name = input("Product name: ").strip()
    brand = input("Brand: ").strip()
    ingredients = input("Ingredients: ").strip()
    nutriscore = input("Nutriscore grade: ").strip()

    item = {
        "product_name": name,
        "brands": brand,
        "ingredients_text": ingredients,
        "nutriscore": nutriscore
    }

    try:
        res = requests.post(f"{BASE_URL}/inventory", json=item)
        res.raise_for_status()
        print("✅ Item added:", res.json())
    except Exception as e:
        print("❌ Failed to add item:", e)

def view_all():
    try:
        res = requests.get(f"{BASE_URL}/inventory")
        res.raise_for_status()
        items = res.json()
        if not items:
            print("⚠️ No inventory items found.")
            return
        for item in items:
            print(f"🆔 {item['id']}: {item['product_name']} ({item['brands']})")
    except Exception as e:
        print("❌ Failed to fetch inventory:", e)

def view_item_details():
    try:
        item_id = int(input("Enter item ID: "))
        res = requests.get(f"{BASE_URL}/inventory/{item_id}")
        res.raise_for_status()
        item = res.json()
        print("📋 Item Details:")
        for k, v in item.items():
            print(f"{k}: {v}")
    except Exception as e:
        print("❌ Failed to fetch item:", e)

def update_item():
    try:
        item_id = int(input("Enter item ID: "))
        field = input("Field to update (product_name, brands, ingredients_text, nutriscore): ").strip()
        value = input(f"New value for {field}: ").strip()
        if field not in ["product_name", "brands", "ingredients_text", "nutriscore"]:
            print("⚠️ Invalid field")
            return
        res = requests.patch(f"{BASE_URL}/inventory/{item_id}", json={field: value})
        res.raise_for_status()
        print("✅ Item updated:", res.json())
    except Exception as e:
        print("❌ Failed to update item:", e)

def delete_item():
    try:
        item_id = int(input("Enter item ID: "))
        res = requests.delete(f"{BASE_URL}/inventory/{item_id}")
        res.raise_for_status()
        print("🗑️ Item deleted successfully.")
    except Exception as e:
        print("❌ Failed to delete item:", e)

def fetch_from_openfoodfacts():
    try:
        query = input("Enter product name to search on OpenFoodFacts: ").strip()
        res = requests.post(f"{BASE_URL}/fetch-and-add", json={"query": query})
        res.raise_for_status()
        print("✅ Item fetched and added:", res.json())
    except Exception as e:
        print("❌ Failed to fetch from OpenFoodFacts:", e)

def main():
    while True:
        print_menu()
        choice = input("Select an option: ").strip()
        if choice == "1":
            add_manual_item()
        elif choice == "2":
            view_all()
        elif choice == "3":
            view_item_details()
        elif choice == "4":
            update_item()
        elif choice == "5":
            delete_item()
        elif choice == "6":
            fetch_from_openfoodfacts()
        elif choice == "0":
            print("👋 Goodbye!")
            break
        else:
            print("⚠️ Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
