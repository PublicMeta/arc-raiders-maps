"""
ARC Raiders Interactive Map - Mapa interactivo con tiles del juego real
Basado en los datos de arcraidersmaps.app
"""

import streamlit as st
import streamlit.components.v1 as components
import json
import os

# ═══════════════════════════════════════════════════════════════════════════════
# ARC RAIDERS - MAPA INTERACTIVO (con tiles reales del juego)
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="ARC Raiders Maps",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CDN base para tiles
CDN_URL = "https://cdn.arcraidersmaps.app"

# --- Datos de los mapas con POIs reales ---
# NOTA: dam y spaceport usan {z}/{y}/{x}, los demás usan {z}/{x}/{y}
MAPS_DATA = {
    "dam": {
        "id": "dam",
        "name": "Dam Battlegrounds",
        "description": 'Alcantara Power Plant, or "The Dam", stands as a silent sentinel amidst a toxic, waterlogged land.',
        "tileUrl": f"{CDN_URL}/maps/dam/tiles/{{z}}/{{x}}/{{y}}.webp",
        "width": 8192,
        "height": 8192,
        "tilesize": 512,
        "maxZoom": 5,
        "minZoom": 1,
        "maxNativeZoom": 4,
        "thumbnail": f"{CDN_URL}/maps/dam/images/thumbnail.webp",
        "pois": [
            {"title": "Hydrophonic Dome Complex", "coords": [4010.5, 5237], "types": ["nature", "industrial", "security"]},
            {"title": "Power Generation Complex", "coords": [5188, 5560], "types": ["industrial", "electrical"]},
            {"title": "Water Treatment", "coords": [3306.5, 4091.5], "types": ["industrial", "mechanical"]},
            {"title": "Testing Annex", "coords": [5144.51, 3091.49], "types": ["medical", "commercial"]},
            {"title": "Research & Administration", "coords": [4357.53, 3744.5], "types": ["technological", "commercial"]},
            {"title": "Control Tower", "coords": [4498.61, 3902.69], "types": ["technological", "security"]},
            {"title": "Old Battlegrounds", "coords": [2616.3, 4816.27], "types": ["ARC"]},
            {"title": "Primary Facility", "coords": [4201.96, 3898.38], "types": ["mechanical", "industrial"]},
            {"title": "Electrical Substation", "coords": [3306.43, 3368.12], "types": ["electrical"]},
            {"title": "Pale Apartments", "coords": [2673.34, 5513.91], "types": ["residential"]},
            {"title": "Ruby Residence", "coords": [3181.13, 5864.72], "types": ["residential"]},
            {"title": "Pattern House", "coords": [4957.21, 6141.13], "types": ["residential"]},
            {"title": "South Swamp Outpost", "coords": [2454.58, 3978.27], "types": []},
            {"title": "Water Towers", "coords": [2854, 3017.96], "types": []},
            {"title": "Formicai Outpost", "coords": [4040, 2125.5], "types": []},
            {"title": "Electrical Tower", "coords": [5740.5, 3087], "types": []},
            {"title": "East Broken Bridge", "coords": [6157.04, 5228.68], "types": []},
            {"title": "Raider Outpost East", "coords": [5815.64, 5583.54], "types": []},
            {"title": "Pipeline Tower", "coords": [5186.65, 5045.37], "types": []},
            {"title": "The Breach", "coords": [4735.93, 4789.73], "types": []},
            {"title": "Red Lakes Balcony", "coords": [5077.73, 3439.54], "types": []},
            {"title": "Small Creek", "coords": [4240.71, 3244.9], "types": []},
            {"title": "Wreckage", "coords": [4476.18, 2681.21], "types": []},
            {"title": "Scrap Yard", "coords": [4050.31, 2731.08], "types": ["mechanical", "industrial"]},
        ]
    },
    "spaceport": {
        "id": "spaceport",
        "name": "The Spaceport",
        "description": "Acerra Spaceport is a majestic testament to humanity's past ambitions.",
        "tileUrl": f"{CDN_URL}/maps/spaceport/tiles/{{z}}/{{x}}/{{y}}.webp",
        "width": 8192,
        "height": 8192,
        "tilesize": 512,
        "maxZoom": 5,
        "minZoom": 1,
        "maxNativeZoom": 3,
        "thumbnail": f"{CDN_URL}/maps/spaceport/images/thumbnail.webp",
        "pois": [
            {"title": "Departure Building", "coords": [3252.48, 4490], "types": ["commercial", "technological"]},
            {"title": "Launch Towers", "coords": [3902.98, 4612.49], "types": ["technological", "security"]},
            {"title": "Arrival Building", "coords": [3259.76, 5296.4], "types": ["commercial", "technological"]},
            {"title": "Shipping Warehouse", "coords": [3680.6, 5760.07], "types": ["industrial", "mechanical"]},
            {"title": "North Trench Tower", "coords": [4479.74, 5793.37], "types": ["technological"]},
            {"title": "South Trench Tower", "coords": [4344.91, 5627.27], "types": ["technological"]},
            {"title": "Rocket Assembly", "coords": [5019, 4614], "types": ["ARC", "industrial"]},
            {"title": "Fuel Control", "coords": [4788.91, 4901.57], "types": ["mechanical", "electrical"]},
            {"title": "Container Storage", "coords": [4788.06, 3639.39], "types": ["industrial", "mechanical"]},
            {"title": "Vehicle Maintenance", "coords": [4216.93, 3458.96], "types": ["mechanical", "industrial"]},
            {"title": "Control Tower A6", "coords": [4194.39, 3838.68], "types": ["technological", "commercial"]},
            {"title": "East Plains Warehouse", "coords": [5842.82, 4453.53], "types": []},
            {"title": "Little Hangar", "coords": [5396.87, 5252.23], "types": []},
            {"title": "The Trench", "coords": [4604.75, 5464.13], "types": []},
            {"title": "Maintenance Hangar", "coords": [3777.31, 2707.67], "types": []},
            {"title": "Staff Parking", "coords": [4539.16, 2386.45], "types": []},
            {"title": "Communications Tower", "coords": [5938.41, 3353.48], "types": []},
        ]
    },
    "buried-city": {
        "id": "buried-city",
        "name": "Buried City",
        "description": "Amidst the sand dunes in this arid wasteland you will find a remnant of the old world.",
        "tileUrl": f"{CDN_URL}/maps/buried-city-v3/tiles/{{z}}/{{x}}/{{y}}.webp",
        "width": 8192,
        "height": 8192,
        "tilesize": 512,
        "maxZoom": 5,
        "minZoom": 1,
        "maxNativeZoom": 3,
        "thumbnail": f"{CDN_URL}/maps/buried-city-v3/images/thumbnail.webp",
        "pois": [
            {"title": "Library", "coords": [3614.87, 5390.1], "types": ["commercial", "old-world"]},
            {"title": "Hospital", "coords": [4242.34, 5901.56], "types": ["medical"]},
            {"title": "Parking Garage", "coords": [4533.58, 5248.26], "types": ["mechanical"]},
            {"title": "Galleria", "coords": [5213.82, 5297.44], "types": ["commercial"]},
            {"title": "Space Travel", "coords": [4819.81, 4889.46], "types": ["commercial", "technological"]},
            {"title": "Research", "coords": [4606.72, 4740.12], "types": ["medical", "technological"]},
            {"title": "Town Hall", "coords": [4560.34, 3891.2], "types": ["old-world"]},
            {"title": "Marano Park", "coords": [4083.82, 4574.24], "types": ["nature"]},
            {"title": "Plaza Rosa", "coords": [4240.89, 2325.54], "types": ["medical", "commercial"]},
            {"title": "Grandioso Apartments", "coords": [2556.38, 3031.45], "types": ["residential"]},
            {"title": "Santa Maria Houses", "coords": [4026.6, 3066.62], "types": ["residential", "old-world"]},
            {"title": "Outskirts", "coords": [2215.52, 5096.41], "types": ["industrial", "mechanical"]},
            {"title": "Red Tower", "coords": [4908.03, 2672.32], "types": ["residential"]},
            {"title": "Church Ruins", "coords": [6104, 1932], "types": []},
            {"title": "Corso Da Vinci", "coords": [4056, 3458], "types": []},
        ]
    },
    "blue-gate": {
        "id": "blue-gate",
        "name": "Blue Gate",
        "description": "Once a steadfast symbol of defiant connection, the Blue Gate now serves as a daunting entryway.",
        "tileUrl": f"{CDN_URL}/maps/blue-gate-v2/tiles/{{z}}/{{x}}/{{y}}.webp",
        "width": 8192,
        "height": 8192,
        "tilesize": 512,
        "maxZoom": 5,
        "minZoom": 1,
        "maxNativeZoom": 3,
        "thumbnail": f"{CDN_URL}/maps/blue-gate/images/thumbnail.webp",
        "pois": [
            {"title": "Trapper's Glade", "coords": [2568.2, 4785.13], "types": ["nature"]},
            {"title": "Raider's Refuge", "coords": [2574.96, 5131.62], "types": ["residential"]},
            {"title": "Adorned Wreckage", "coords": [2250.73, 4435.1], "types": ["mechanical", "industrial"]},
            {"title": "Village", "coords": [3266.64, 5617.17], "types": ["commercial", "residential"]},
            {"title": "Checkpoint", "coords": [3857, 4344.71], "types": ["mechanical"]},
            {"title": "Warehouse Complex", "coords": [4776.99, 4668.93], "types": ["industrial"]},
            {"title": "Gate Control Room", "coords": [4550.03, 4455.48], "types": []},
            {"title": "Reinforced Reception", "coords": [4025.86, 5332.24], "types": ["security", "technological"]},
            {"title": "Ancient Fort", "coords": [4159.61, 2534.44], "types": ["old-world", "technological"]},
            {"title": "Barren Clearing", "coords": [2010.27, 5384.93], "types": ["ARC"]},
        ]
    },
    "stella-montis": {
        "id": "stella-montis",
        "name": "Stella Montis",
        "description": "A secluded research facility amidst snow-draped peaks.",
        "layers": [
            {
                "id": "stella-montis-l2",
                "name": "Top Section",
                "tileUrl": f"{CDN_URL}/maps/stella-montis/layers/stella-montis-l2/tiles/{{z}}/{{x}}/{{y}}.webp",
            },
            {
                "id": "stella-montis-l1", 
                "name": "Bottom Section",
                "tileUrl": f"{CDN_URL}/maps/stella-montis/layers/stella-montis-l1/tiles/{{z}}/{{x}}/{{y}}.webp",
            }
        ],
        "width": 8192,
        "height": 8192,
        "tilesize": 512,
        "maxZoom": 5,
        "minZoom": 1,
        "maxNativeZoom": 3,
        "thumbnail": f"{CDN_URL}/maps/stella-montis/images/thumbnail-v2.webp",
        "pois": [
            {"title": "Seed Vault", "coords": [6306, 950], "types": ["industrial", "technological"]},
            {"title": "Sandbox", "coords": [3719.38, 3850.36], "types": ["mechanical", "technological"]},
            {"title": "Loading Bay", "coords": [1985.56, 4104.92], "types": ["industrial"]},
            {"title": "Assembly Workshops", "coords": [2435.5, 6270.24], "types": ["technological"]},
            {"title": "Business Center", "coords": [6029.23, 4766.19], "types": ["exodus", "commercial"]},
            {"title": "Cultural Archives", "coords": [6443.12, 3844.26], "types": ["old-world"]},
            {"title": "Medical Research", "coords": [1557.34, 3815.98], "types": ["medical", "technological"]},
        ]
    }
}

# --- Colores por tipo de POI ---
POI_COLORS = {
    "nature": "#4CAF50",
    "industrial": "#FF9800", 
    "security": "#F44336",
    "electrical": "#FFEB3B",
    "mechanical": "#9E9E9E",
    "medical": "#E91E63",
    "commercial": "#2196F3",
    "technological": "#00BCD4",
    "residential": "#795548",
    "ARC": "#9C27B0",
    "old-world": "#607D8B",
    "exodus": "#673AB7",
    "default": "#FFFFFF"
}

# --- Archivo para guardar marcadores personalizados ---
MARKERS_FILE = "custom_markers.json"

def load_custom_markers():
    """Carga marcadores personalizados del archivo."""
    if os.path.exists(MARKERS_FILE):
        with open(MARKERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_custom_markers(markers):
    """Guarda marcadores personalizados al archivo."""
    with open(MARKERS_FILE, "w", encoding="utf-8") as f:
        json.dump(markers, f, ensure_ascii=False, indent=2)

def get_poi_color(types):
    """Obtener color basado en el tipo de POI"""
    if not types:
        return POI_COLORS["default"]
    return POI_COLORS.get(types[0], POI_COLORS["default"])

def create_map_html(map_data, custom_markers=None, selected_layer=None, use_embedded_site=False):
    """Generar el HTML del mapa con Leaflet y tiles reales del juego"""
    
    # Opción: Incrustar el sitio original directamente
    if use_embedded_site:
        map_id = map_data["id"]
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                html, body {{ margin: 0; padding: 0; height: 100%; overflow: hidden; }}
                iframe {{ width: 100%; height: 100%; border: none; }}
            </style>
        </head>
        <body>
            <iframe src="https://arcraidersmaps.app/{map_id}" allowfullscreen></iframe>
        </body>
        </html>
        '''
    
    # Determinar la URL de tiles
    if "layers" in map_data and selected_layer:
        layer = next((l for l in map_data["layers"] if l["id"] == selected_layer), map_data["layers"][0])
        tile_url = layer["tileUrl"]
    elif "tileUrl" in map_data:
        tile_url = map_data["tileUrl"]
    else:
        tile_url = map_data["layers"][0]["tileUrl"]
    
    # Generar marcadores de POIs del juego
    markers_js = ""
    for poi in map_data.get("pois", []):
        # Convertir coordenadas del juego a coordenadas Leaflet
        x, y = poi["coords"][0], poi["coords"][1]
        lat = -(y / map_data['width'] * 256)
        lng = x / map_data['width'] * 256
        
        color = get_poi_color(poi.get("types", []))
        types_str = ", ".join(poi.get("types", [])) if poi.get("types") else "Location"
        
        markers_js += f"""
        L.circleMarker([{lat}, {lng}], {{
            radius: 8,
            fillColor: '{color}',
            color: '#000',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.85
        }}).addTo(markersLayer)
          .bindPopup('<div style="min-width:150px"><b>{poi["title"]}</b><br><small style="color:#aaa">{types_str}</small></div>');
        """
    
    # Generar marcadores personalizados
    if custom_markers:
        for marker in custom_markers:
            x, y = marker.get("x", 4096), marker.get("y", 4096)
            lat = -(y / map_data['width'] * 256)
            lng = x / map_data['width'] * 256
            
            markers_js += f"""
            L.marker([{lat}, {lng}], {{
                icon: L.divIcon({{
                    className: 'custom-marker',
                    html: '<div style="background:#FF5722;width:24px;height:24px;border-radius:50%;border:3px solid #fff;box-shadow:0 2px 5px rgba(0,0,0,0.5);"></div>',
                    iconSize: [24, 24],
                    iconAnchor: [12, 12]
                }})
            }}).addTo(markersLayer)
              .bindPopup('<div style="min-width:150px"><b>{marker.get("name", "Custom")}</b><br><small>{marker.get("notes", "")}</small></div>');
            """
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <style>
            html, body {{ margin: 0; padding: 0; height: 100%; }}
            #map {{ width: 100%; height: 100%; background: #0d1117; }}
            .leaflet-container {{ background: #0d1117; }}
            .leaflet-popup-content-wrapper {{
                background: rgba(13, 17, 23, 0.95);
                color: #fff;
                border-radius: 8px;
                border: 1px solid #30363d;
            }}
            .leaflet-popup-tip {{ background: rgba(13, 17, 23, 0.95); }}
            .leaflet-popup-content {{ margin: 12px; }}
            .leaflet-control-zoom a {{
                background: rgba(13, 17, 23, 0.9) !important;
                color: #fff !important;
                border: 1px solid #30363d !important;
            }}
            .leaflet-control-zoom a:hover {{
                background: rgba(30, 40, 50, 0.95) !important;
            }}
            .coords-display {{
                position: absolute;
                bottom: 10px;
                left: 10px;
                background: rgba(13, 17, 23, 0.9);
                color: #58a6ff;
                padding: 8px 12px;
                border-radius: 6px;
                font-family: monospace;
                font-size: 12px;
                z-index: 1000;
                border: 1px solid #30363d;
            }}
        </style>
    </head>
    <body>
        <div id="map"></div>
        <div class="coords-display" id="coords">Click en el mapa para coordenadas</div>
        <script>
            // Configuración del mapa
            var mapSize = {map_data['width']};
            var tileSize = {map_data['tilesize']};
            
            // Crear mapa con CRS simple (sin proyección geográfica)
            var map = L.map('map', {{
                crs: L.CRS.Simple,
                minZoom: {map_data['minZoom']},
                maxZoom: {map_data['maxZoom']},
                zoomControl: true,
                attributionControl: false
            }});
            
            // Calcular límites del mapa  
            var bounds = [[0, 0], [-256, 256]];
            
            // Añadir capa de tiles del juego real
            L.tileLayer('{tile_url}', {{
                minZoom: {map_data['minZoom']},
                maxZoom: {map_data['maxZoom']},
                maxNativeZoom: {map_data['maxNativeZoom']},
                tileSize: tileSize,
                noWrap: true,
                bounds: bounds,
                errorTileUrl: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII='
            }}).addTo(map);
            
            // Establecer vista inicial centrada
            map.setView([-128, 128], 2);
            map.setMaxBounds([[-300, -50], [50, 306]]);
            
            // Capa para marcadores
            var markersLayer = L.layerGroup().addTo(map);
            
            // Añadir marcadores de POIs
            {markers_js}
            
            // Mostrar coordenadas del juego al hacer click
            var coordsDisplay = document.getElementById('coords');
            map.on('click', function(e) {{
                var gameX = (e.latlng.lng / 256) * mapSize;
                var gameY = (-e.latlng.lat / 256) * mapSize;
                coordsDisplay.innerHTML = 'X: ' + gameX.toFixed(0) + ' | Y: ' + gameY.toFixed(0);
            }});
            
            map.on('mousemove', function(e) {{
                var gameX = (e.latlng.lng / 256) * mapSize;
                var gameY = (-e.latlng.lat / 256) * mapSize;
                if (gameX >= 0 && gameX <= mapSize && gameY >= 0 && gameY <= mapSize) {{
                    coordsDisplay.innerHTML = 'X: ' + gameX.toFixed(0) + ' | Y: ' + gameY.toFixed(0);
                }}
            }});
        </script>
    </body>
    </html>
    """
    return html

# Inicializar estado de sesión
if "custom_markers" not in st.session_state:
    st.session_state.custom_markers = load_custom_markers()

if "selected_map" not in st.session_state:
    st.session_state.selected_map = "dam"

# --- CSS Personalizado ---
st.markdown("""
<style>
    .stApp { background-color: #0d1117; }
    /* Eliminar TODOS los paddings y margins */
    .main .block-container { 
        padding: 0 !important; 
        max-width: 100% !important; 
        padding-top: 0 !important;
        margin: 0 !important;
    }
    .stMainBlockContainer { padding: 0 !important; }
    .block-container { padding: 0 !important; }
    /* Ocultar header y footer de Streamlit */
    header[data-testid="stHeader"] { display: none !important; }
    footer { display: none !important; }
    #MainMenu { display: none !important; }
    /* Sidebar compacto */
    [data-testid="stSidebar"] { 
        min-width: 280px !important;
        max-width: 280px !important;
        background-color: #161b22 !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        background-color: #161b22 !important;
        padding-top: 0.5rem;
    }
    .stSelectbox label, .stTextInput label, .stTextArea label, .stNumberInput label { color: #c9d1d9; }
    h1, h2, h3, h4, h5, h6 { color: #fff !important; }
    p, span, label { color: #c9d1d9; }
    .stButton > button {
        background-color: #21262d;
        color: #c9d1d9;
        border: 1px solid #30363d;
    }
    .stButton > button:hover {
        background-color: #30363d;
        border-color: #8b949e;
    }
    .legend-item {
        display: inline-flex;
        align-items: center;
        margin-right: 8px;
        margin-bottom: 4px;
        font-size: 0.75rem;
        color: #c9d1d9;
    }
    .legend-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 4px;
        border: 1px solid rgba(255,255,255,0.3);
    }
    /* Iframe a pantalla completa */
    iframe { 
        border: none !important; 
        border-radius: 0 !important;
        width: 100% !important;
    }
    .stSidebar [data-testid="stMarkdownContainer"] p { color: #c9d1d9; }
    /* Elemento del mapa sin margins */
    .element-container:has(iframe) {
        margin: 0 !important;
        padding: 0 !important;
    }
    .stElementContainer { margin: 0 !important; padding: 0 !important; }
</style>
""", unsafe_allow_html=True)

# --- UI Principal ---

# Sidebar
with st.sidebar:
    st.markdown("### 🎮 Seleccionar Mapa")
    
    selected_map = st.selectbox(
        "Mapa:",
        options=list(MAPS_DATA.keys()),
        format_func=lambda x: MAPS_DATA[x]["name"],
        key="map_selector"
    )
    st.session_state.selected_map = selected_map
    
    map_data = MAPS_DATA[selected_map]
    
    st.markdown(f"*{map_data['description']}*")
    
    # Si el mapa tiene capas (como Stella Montis)
    selected_layer = None
    if "layers" in map_data:
        st.markdown("---")
        st.markdown("### 🗂️ Capa del Mapa")
        layer_names = {l["id"]: l["name"] for l in map_data["layers"]}
        selected_layer = st.selectbox(
            "Seleccionar capa:",
            options=list(layer_names.keys()),
            format_func=lambda x: layer_names[x]
        )
    
    st.markdown("---")
    st.markdown("### 🏷️ Leyenda de POIs")
    
    # Mostrar leyenda compacta
    legend_html = '<div style="display:flex;flex-wrap:wrap;">'
    for poi_type, color in POI_COLORS.items():
        if poi_type != "default":
            legend_html += f'<div class="legend-item"><div class="legend-dot" style="background-color: {color};"></div>{poi_type.replace("-", " ").title()}</div>'
    legend_html += '</div>'
    st.markdown(legend_html, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### ⚙️ Opciones")
    use_embedded = st.checkbox("📺 Usar mapa embebido (arcraidersmaps.app)", value=True, help="Si los tiles no cargan, usa el sitio original embebido")
    
    st.markdown("---")
    st.markdown("### 📊 Estadísticas")
    poi_count = len(map_data.get("pois", []))
    st.metric("POIs en este mapa", poi_count)
    
    st.markdown("---")
    st.markdown("### 📍 Añadir Marcador Personal")
    
    with st.form("add_marker_form"):
        marker_name = st.text_input("Nombre:")
        
        col1, col2 = st.columns(2)
        with col1:
            marker_x = st.number_input("Coord X:", value=4096, min_value=0, max_value=8192)
        with col2:
            marker_y = st.number_input("Coord Y:", value=4096, min_value=0, max_value=8192)
        
        marker_notes = st.text_area("Notas:", height=60)
        
        submitted = st.form_submit_button("➕ Añadir Marcador")
        
        if submitted and marker_name:
            if selected_map not in st.session_state.custom_markers:
                st.session_state.custom_markers[selected_map] = []
            
            new_marker = {
                "name": marker_name,
                "x": marker_x,
                "y": marker_y,
                "notes": marker_notes
            }
            st.session_state.custom_markers[selected_map].append(new_marker)
            save_custom_markers(st.session_state.custom_markers)
            st.success(f"✅ '{marker_name}' añadido!")
            st.rerun()
    
    st.markdown("---")
    st.caption(f"[🔗 arcraidersmaps.app](https://arcraidersmaps.app/{selected_map})  •  [🔗 ardb.app](https://ardb.app/)")
    
    # Lista de marcadores personalizados en sidebar
    current_markers = st.session_state.custom_markers.get(selected_map, [])
    if current_markers:
        st.markdown("---")
        st.markdown("### 📋 Tus Marcadores")
        for i, marker in enumerate(current_markers):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.caption(f"📍 **{marker['name']}** ({marker['x']}, {marker['y']})")
            with col2:
                if st.button("🗑️", key=f"del_{i}"):
                    st.session_state.custom_markers[selected_map].pop(i)
                    save_custom_markers(st.session_state.custom_markers)
                    st.rerun()

# --- Mapa Principal ---
map_data = MAPS_DATA[st.session_state.selected_map]

# Obtener marcadores personalizados
custom_markers = st.session_state.custom_markers.get(st.session_state.selected_map, [])

# Mapa a pantalla completa (calc: 100vh - margen mínimo)
map_html = create_map_html(map_data, custom_markers, selected_layer, use_embedded_site=use_embedded)
components.html(map_html, height=950, scrolling=False)

# Lista de marcadores movida al sidebar para ahorrar espacio
