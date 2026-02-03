import pandas as pd
from geopy.geocoders import Nominatim
import time

print("="*50)
print("ADDING COORDINATES TO CITIES")
print("="*50)

# Read the city data
print("\nLoading avg_price_by_city.csv...")
df = pd.read_csv('powerbi/data/avg_price_by_city.csv')
print(f"Loaded {len(df)} cities")

# Initialize geocoder (THIS NEEDS TO BE AT THE TOP LEVEL)
print("\nInitializing geocoder...")
geolocator = Nominatim(user_agent="arizona_housing_dashboard")

# Add coordinate columns
print("\nGeocoding cities (this will take a few minutes)...")
latitudes = []
longitudes = []

for index, row in df.iterrows():
    city = row['city']
    state = row['state']
    
    try:
        # Search for "City, State, USA"
        location = geolocator.geocode(f"{city}, {state}, USA")
        
        if location:
            latitudes.append(location.latitude)
            longitudes.append(location.longitude)
            print(f"{city}: {location.latitude}, {location.longitude}")
        else:
            latitudes.append(None)
            longitudes.append(None)
            print(f"{city}: Not found")
        
        # Be nice to the API - wait 1 second between requests
        time.sleep(1)
        
    except Exception as e:
        latitudes.append(None)
        longitudes.append(None)
        print(f"{city}: Error - {e}")

# Add coordinates to dataframe
df['latitude'] = latitudes
df['longitude'] = longitudes

# Save updated file
print(f"\nSaving updated file...")
df.to_csv('powerbi/data/avg_price_by_city.csv', index=False)
print("✅ Coordinates added successfully!")

# Show summary
print(f"\nSummary:")
print(f"Total cities: {len(df)}")
print(f"Successfully geocoded: {df['latitude'].notna().sum()}")
print(f"Failed: {df['latitude'].isna().sum()}")