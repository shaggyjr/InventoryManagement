import json
import math
import streamlit as st

INVENTORY_FILE = "inventory.json"

CUSTOM_STYLE = """
<style>
.main {
    background-image:linear-gradient(rgba(0,0,0,0.5),rgba(0,0,0,0.5)),url("https://images.prismic.io//intuzwebsite/184d404d-1f1f-4b56-a821-11ae147357c2_IoT+Applications+in+inventory+management.png?w=1200&q=80&auto=format,compress&fm=png8");
    background-repeat: no-repeat;
    background-position: cover;
    background-size: cover;
}
</style>
"""

# custom css 
st.markdown(CUSTOM_STYLE, unsafe_allow_html=True)


def load_inventory():
    try:
        with open(INVENTORY_FILE) as file:
            inventory = json.load(file)
    except FileNotFoundError:
        inventory = []
    return inventory


def save_inventory(inventory):
    with open(INVENTORY_FILE, "w") as file:
        json.dump(inventory, file)


def display_home_page():
    st.write("This site allows you to manage your inventory by adding, updating, and removing items. You can also display the current inventory, search for specific items, and generate a report.")


def add_item(inventory):
    name = st.text_input("Enter the item name")
    quantity = st.number_input("Enter the quantity", value=0, min_value=0)
    price = st.number_input("Enter the price", value=0.0, min_value=0.0)
    supplier = st.text_input("Enter the supplier name")
    lead_time = st.number_input("Enter the lead time (in days)", value=0, min_value=0)
    demand_rate = st.number_input("Enter the demand rate (in units per day)", value=0, min_value=0)
    setup_cost = st.number_input("Enter the setup cost", value=0, min_value=0)
    holding_cost = st.number_input("Enter the holding cost", value=0, min_value=0)

    if st.button("Add Item"):
        item = {
            "name": name,
            "quantity": quantity,
            "price": price,
            "supplier": supplier,
            "lead_time": lead_time,
            "demand_rate": demand_rate,
            "setup_cost": setup_cost,
            "holding_cost": holding_cost
        }
        inventory.append(item)
        save_inventory(inventory)
        st.success("Item added successfully.")


def update_quantity(inventory):
    name = st.text_input("Enter the item name")
    quantity = st.number_input("Enter the new quantity", value=0, min_value=0)

    if st.button("Update Quantity"):
        for item in inventory:
            if item["name"] == name:
                item["quantity"] = quantity
                save_inventory(inventory)
                st.success("Quantity updated successfully.")
                return

        st.error("Item not found.")


def remove_item(inventory):
    name = st.text_input("Enter the item name")

    if st.button("Remove Item"):
        for item in inventory:
            if item["name"] == name:
                inventory.remove(item)
                save_inventory(inventory)
                st.success("Item removed successfully.")
                return

        st.error("Item not found.")


def display_inventory(inventory):
    st.subheader("Inventory:")
    for item in inventory:
        st.write(f"Name: {item['name']}, Quantity: {item['quantity']}, Price: {item['price']}, Supplier: {item['supplier']}<br>")
    st.write()



def search_item(inventory):
    search_product = st.text_input("Enter the search product")

    if st.button("Search"):
        results = []
        for item in inventory:
            if search_product.lower() in item['name'].lower():
                results.append(item)

        if results:
            st.subheader("Search Results:")
            for item in results:
                st.write(f"Name: {item['name']}, Quantity: {item['quantity']}, Price: {item['price']}, Supplier: {item['supplier']}")
        else:
            st.warning("No items found matching the search term.")


def generate_report(inventory):
    st.markdown("## Inventory Report")
    for item in inventory:
        demand_rate = item.get("demand_rate", 0)
        setup_cost = item.get("setup_cost", 0)
        holding_cost = item.get("holding_cost", 0)
        eoq = math.sqrt((2 * demand_rate * setup_cost) / holding_cost)

        st.write("Name:", item['name'])
        st.write("Quantity:", item['quantity'])
        st.write("Price:", item['price'])
        st.write("EOQ:", eoq)
        st.write("---")  

    st.write()


def delete_inventory():
    confirmation = st.warning("Are you sure you want to delete the entire inventory? This action cannot be undone.")

    if st.button("Confirm"):
        inventory = []
        save_inventory(inventory)
        st.success("Inventory deleted successfully.")


def main_menu():
    st.title("Inventory Management System")

    inventory = load_inventory()

    st.sidebar.markdown("<h1 class='sidebar-title'></h1>", unsafe_allow_html=True)
    page = st.sidebar.radio("Go to", ["Home", "Add Item", "Update Quantity", "Remove Item", "Display Inventory", "Search Item", "Generate Report", "Delete Inventory"])

    if page == "Home":
        display_home_page()
    elif page == "Add Item":
        add_item(inventory)
    elif page == "Update Quantity":
        update_quantity(inventory)
    elif page == "Remove Item":
        remove_item(inventory)
    elif page == "Display Inventory":
        display_inventory(inventory)
    elif page == "Search Item":
        search_item(inventory)
    elif page == "Generate Report":
        if st.button("Generate Report"):
            generate_report(inventory)
    elif page == "Delete Inventory":
        delete_inventory()


if __name__ == "__main__":
    main_menu()
