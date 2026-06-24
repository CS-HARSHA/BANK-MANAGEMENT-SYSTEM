import json
from pathlib import Path

def save_data(bank , file_path: str ="data/accounts.json") -> bool:
    """Serializes the bank object and saves it to a JSON file."""
    # Ensure the target directory exists
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Open file and write the dictionary directly to JSON
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(bank.to_dict(), f, indent=4)
        print(" Bank data successfully saved.")
        return True
        
    except Exception as e:
        print(f" Critical Error saving data: {e}")
        return False
    
def load_data(filepath: str = "data/accounts.json"):
    """Reads the JSON file and reconstructs the Bank object."""
    file_path = Path(filepath)
    
    # If the file doesn't exist yet (e.g., first run), return None safely
    if not file_path.exists():
        return None
        
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Local import to prevent circular dependency with bank.py
        from bank.bank import Bank 
        
        return Bank.from_dict(data)
        
    except json.JSONDecodeError:
        print(" Error: The save file is corrupted or empty.")
        return None
    except Exception as e:
        print(f" Critical Error loading data: {e}")
        return None
    