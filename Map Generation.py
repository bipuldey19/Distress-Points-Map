import folium
from folium import IFrame
import base64

# Define valid folium colors for each severity level
folium_colors = {
    'High': 'red',
    'Medium': 'orange',
    'Low': 'green'
}

# Create the map centered on the mean latitude and longitude
center_lat = df['latitude_y'].mean()
center_lon = df['longitude_'].mean()
m = folium.Map(location=[center_lat, center_lon], zoom_start=10)

# Function to create popups with image and distress information
def create_popup(row):
    # HTML structure for popup
    html = f"""
    <b>Distress Type:</b> {row['Distress_Type']}<br>
    <b>Distress Level:</b> {row['Distress_Level']}<br>
    <b>Severity:</b> {row['Severity']}<br>
    <iframe src="{row['File_URL']}" width="200px"></iframe><br>
    <b>Date and Time:</b> {row['DateTime_1']}
    """
    return folium.Popup(IFrame(html, width=300, height=300))

# Add markers to the map with corresponding color and popup
for _, row in df.iterrows():
    folium.Marker(
        location=[row['latitude_y'], row['longitude_']],
        popup=create_popup(row),
        icon=folium.Icon(color=folium_colors.get(row['Severity'], 'blue'))  # Ensure valid color
    ).add_to(m)

# Save the map to a file
map_file_path = '/mnt/data/folium_map_with_images.html'
m.save(map_file_path)

map_file_path
