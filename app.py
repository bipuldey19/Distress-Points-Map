import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap, MarkerCluster
from streamlit_folium import folium_static

# Load the CSV file
csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRYSUOh5kElFlNoJb7j8f1gNMBs6m76JSj0nAknc6vomY5JkCBsVVLPr4kBu6J03__pH0rJsuVkoYOO/pub?output=csv"
df = pd.read_csv(csv_url)

# Set up page configuration for a fullscreen experience
st.set_page_config(layout="wide")

st.markdown("""
    <style>
    @media (min-width: 576px) {
        section.stMain {
            overflow: hidden;
        }
        .block-container {
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
    }
    
    iframe.stIFrame {
    width: 100%;
    }
    
    </style>
""", unsafe_allow_html=True)

# Layout split into two columns: 1 for sidebar, 1 for map
left_col, right_col = st.columns([1, 4])  # Left (left_col) is 1 part, right (right_col) is 4 parts

with left_col:
    # Sidebar section for layers and title
    st.title('Distress Points Map')
    layer = st.selectbox(
        'Select layer',
        ['All Distresses', 'By Severity', 'By Distress Type', 'Distress Heatmap', 'Distress Type Clustering']
    )

    # Conditionally display the "Select severity" or "Select distress type" dropdown based on the chosen layer
    if layer == 'By Severity':
        severity = st.selectbox('Select severity', df['Severity'].unique())

    if layer == 'By Distress Type':
        distress_type = st.selectbox('Select distress type', df['Distress_Type'].unique())

    # Footer with copyright_col text at the bottom of the sidebar
    st.markdown("<br><br><br><br><br><br><br>", unsafe_allow_html=True)  # Spacer for alignment
    st.markdown("---")
    st.markdown("© **Bipul Dey**, Department of Urban & Regional Planning, RUET 2024.")

# Initialize the map at the center of the coordinates
center_lat = df['latitude_y'].mean()
center_lon = df['longitude_'].mean()
map = folium.Map(location=[center_lat, center_lon], zoom_start=15)

folium.plugins.Fullscreen(
    position="topright",
    title="Expand me",
    title_cancel="Exit me",
    force_separate_button=True,
).add_to(map)

# Function to create popups with image and distress information
def create_popup(row):
    html = f"""
    <b>Distress Type:</b> {row['Distress_Type']}<br>
    <b>Distress Level:</b> {row['Distress_Level']}<br>
    <b>Severity:</b> {row['Severity']}<br>
    <iframe src="{row['File_URL']}" width="200px"></iframe><br>
    <b>Date and Time:</b> {row['DateTime_1']}
    """
    return folium.Popup(folium.IFrame(html, width=300, height=300))

# Layer: All Distresses
if layer == 'All Distresses':
    for _, row in df.iterrows():
        folium.Marker(
            location=[row['latitude_y'], row['longitude_']],
            popup=create_popup(row),
            icon=folium.Icon(color='red' if row['Severity'] == 'High' else 
                            ('orange' if row['Severity'] == 'Medium' else 'green'))
        ).add_to(map)

# Layer: By Severity
elif layer == 'By Severity':
    filtered_df = df[df['Severity'] == severity]  # Use the severity selected above
    
    for _, row in filtered_df.iterrows():
        folium.Marker(
            location=[row['latitude_y'], row['longitude_']],
            popup=create_popup(row),
            icon=folium.Icon(color='red' if row['Severity'] == 'High' else 
                            ('orange' if row['Severity'] == 'Medium' else 'green'))
        ).add_to(map)

# Layer: By Distress Type
elif layer == 'By Distress Type':
    filtered_df = df[df['Distress_Type'] == distress_type]  # Use the distress type selected above
    
    for _, row in filtered_df.iterrows():
        folium.Marker(
            location=[row['latitude_y'], row['longitude_']],
            popup=create_popup(row),
            icon=folium.Icon(color='red' if row['Severity'] == 'High' else 
                            ('orange' if row['Severity'] == 'Medium' else 'green'))
        ).add_to(map)

# Layer: Distress Heatmap
elif layer == 'Distress Heatmap':
    heat_data = [[row['latitude_y'], row['longitude_']] for index, row in df.iterrows()]
    HeatMap(heat_data).add_to(map)

# Layer: Distress Type Clustering
elif layer == 'Distress Type Clustering':
    marker_cluster = MarkerCluster().add_to(map)
    for _, row in df.iterrows():
        folium.Marker(
            location=[row['latitude_y'], row['longitude_']],
            popup=create_popup(row),
            icon=folium.Icon(color='red' if row['Severity'] == 'High' else 
                            ('orange' if row['Severity'] == 'Medium' else 'green'))
        ).add_to(marker_cluster)

# Display the map in Streamlit (using the second column for the map)
with right_col:
    folium_static(map, width=1400)  # Make map large within the second column
