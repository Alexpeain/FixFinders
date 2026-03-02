import json
import random

# Valid category IDs in your Supabase database
VALID_CATEGORIES = [3, 4, 5, 6, 7]

try:
    with open('profiles.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    modified_count = 0
    for item in data:
        if item.get('model') == 'providers.providerprofile':
            current_category = item['fields'].get('category')
            # If the category is invalid, assign it a valid one
            if current_category not in VALID_CATEGORIES:
                item['fields']['category'] = random.choice(VALID_CATEGORIES)
                modified_count += 1
                
    with open('fixed_profiles.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
        
    print(f"Successfully fixed {modified_count} profiles. Saved to 'fixed_profiles.json'.")

except Exception as e:
    print(f"Error: {e}")
