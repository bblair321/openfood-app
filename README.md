# OpenFoodFacts Inventory App

A simple Python project consisting of a Flask REST API backend and a CLI frontend to manage a product inventory using data from the OpenFoodFacts database.

## Installation

Clone the repository:

   ```bash
   git clone https://github.com/yourusername/openfood-inventory.git
   cd openfood-inventory

python3 -m venv venv
source venv/bin/activate    # Linux/macOS
.\venv\Scripts\activate     # Windows PowerShell

pip install -r requirements.txt

Running the Application
Start the Flask API server:

bash
Copy code
python3 app.py
In a new terminal window, run the CLI:

bash
Copy code
python3 cli.py

CLI Usage
Once the Flask server is running, the CLI interacts with the API:

Add new item manually: Enter product details directly.

View all inventory: List all items with IDs and names.

View item details: Show full details by item ID.

Update item: Modify fields of an existing item by ID.

Delete item: Remove an item by ID.

Find item on OpenFoodFacts: Search OpenFoodFacts by product name and add the first found product automatically.