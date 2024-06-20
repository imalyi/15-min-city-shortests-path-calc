# this script generates geojson with all building borders from db
import pymongo
import geojson
MONGO_CONNECT = "mongodb://root:example@node:27777/"
# MongoDB connection
client = pymongo.MongoClient(MONGO_CONNECT)
db = client["15min"]
collection = db["address"]

# Fetch documents
documents = collection.find()

# Function to swap coordinates
def swap_coordinates(coordinates):
    return [[lat, lon] for lon, lat in coordinates]

# Function to ensure the first and last coordinates are the same
def ensure_closed_ring(ring):
    if ring[0] != ring[-1]:
        ring.append(ring[0])
    return ring

# Prepare GeoJSON FeatureCollection
features = []

for doc in documents:
    if 'geometry' in doc and isinstance(doc['geometry'], list):
        # Convert to GeoJSON Polygon format and swap coordinates
        geometry = {
            "type": "Polygon",
            "coordinates": [ensure_closed_ring((ring)) for ring in doc['geometry']]
        }
        feature = geojson.Feature(
            geometry=geometry,
            
        )
        features.append(feature)

feature_collection = geojson.FeatureCollection(features)

# Write to GeoJSON file
with open('output.geojson', 'w') as f:
    geojson.dump(feature_collection, f, indent=2)

print("GeoJSON file created: output.geojson")