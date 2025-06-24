from fastapi import FastAPI, Query
import pandas as pd

app = FastAPI()

# Load plants data (make sure your CSV includes a Climate Zones column)
df = pd.read_csv("plants.csv")

# Load locations data (maps suburb/postcode to climate zone)
# locations.csv should have columns: Suburb, Postcode, Climate Zone
locations_df = pd.read_csv("locations.csv")

def get_climate_zone(location: str) -> str | None:
    """Return the climate zone for the given suburb name or postcode."""
    location_lower = location.lower().strip()
    
    # Try matching suburb ignoring case and whitespace
    match_suburb = locations_df['Suburb'].str.lower().str.strip() == location_lower
    
    # Try matching postcode as string equality
    match_postcode = locations_df['Postcode'].astype(str).str.strip() == location_lower
    
    match = locations_df[match_suburb | match_postcode]
    
    if not match.empty:
        return match.iloc[0]['Climate Zone']
    return None

@app.get("/recommend")
@app.get("/recommend")
def recommend(location: str, spot: str, sunlight: str):
    user_climate_zone = get_climate_zone(location)

    # Convert relevant columns to string and fill NaNs to avoid errors
    df['Climate Zones'] = df['Climate Zones'].astype(str).fillna('')
    df['Spot'] = df['Spot'].astype(str).fillna('')
    df['Sunlight'] = df['Sunlight'].astype(str).fillna('')

    if user_climate_zone:
        filtered = df[
            df['Climate Zones'].str.contains(user_climate_zone, case=False, na=False) &
            (df['Spot'].str.lower() == spot.lower()) &
            (df['Sunlight'].str.lower() == sunlight.lower())
        ]
    else:
        filtered = df[
            (df['Spot'].str.lower() == spot.lower()) &
            (df['Sunlight'].str.lower() == sunlight.lower())
        ]
    return filtered.to_dict(orient="records")

