"""
ARC Raiders Interactive Map + AI Search
"""

import streamlit as st
import streamlit.components.v1 as components
import json
import os

# Ruta absoluta al archivo de items
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ITEMS_FILE = os.path.join(SCRIPT_DIR, "items_data.json")

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="ARC Raiders Maps",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cargar items
@st.cache_data
def load_items():
    try:
        with open(ITEMS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error cargando items: {e}")
        return []

GAME_ITEMS = load_items()

# Traducciones ES -> EN
TRANS = {
    "bateria": "battery", "baterias": "battery", "pila": "battery", "pilas": "battery",
    "energia": "power", "electrico": "electrical", "electricidad": "electrical",
    "mecanico": "mechanical", "medico": "medical", "medicina": "medical",
    "arma": "weapon", "municion": "ammo", "vendaje": "bandage",
    "componente": "component", "cable": "cable", "chatarra": "scrap",
}

# POIs por mapa
MAPS = {
    "dam": {
        "name": "Dam Battlegrounds",
        "pois": [
            {"title": "Power Generation Complex", "types": ["industrial", "electrical"]},
            {"title": "Electrical Substation", "types": ["electrical"]},
            {"title": "Water Treatment", "types": ["industrial", "mechanical"]},
            {"title": "Testing Annex", "types": ["medical", "commercial"]},
            {"title": "Research & Administration", "types": ["technological"]},
            {"title": "Old Battlegrounds", "types": ["ARC"]},
            {"title": "Primary Facility", "types": ["mechanical", "industrial"]},
            {"title": "Scrap Yard", "types": ["mechanical", "industrial"]},
            {"title": "Pale Apartments", "types": ["residential"]},
            {"title": "Ruby Residence", "types": ["residential"]},
            {"title": "Hydrophonic Dome", "types": ["nature"]},
        ]
    },
    "spaceport": {
        "name": "The Spaceport",
        "pois": [
            {"title": "Fuel Control", "types": ["mechanical", "electrical"]},
            {"title": "Rocket Assembly", "types": ["ARC", "industrial"]},
            {"title": "Shipping Warehouse", "types": ["industrial", "mechanical"]},
            {"title": "Container Storage", "types": ["industrial"]},
            {"title": "Vehicle Maintenance", "types": ["mechanical"]},
            {"title": "Departure Building", "types": ["commercial"]},
        ]
    },
    "buried-city": {
        "name": "Buried City",
        "pois": [
            {"title": "Hospital", "types": ["medical"]},
            {"title": "Research", "types": ["medical", "technological"]},
            {"title": "Parking Garage", "types": ["mechanical"]},
            {"title": "Outskirts", "types": ["industrial", "mechanical"]},
            {"title": "Galleria", "types": ["commercial"]},
            {"title": "Grandioso Apartments", "types": ["residential"]},
            {"title": "Marano Park", "types": ["nature"]},
        ]
    },
}

# ═══════════════════════════════════════════════════════════════════════════════
# BÚSQUEDA
# ═══════════════════════════════════════════════════════════════════════════════

def normalize(text):
    text = text.lower().strip()
    for a, b in [('á','a'),('é','e'),('í','i'),('ó','o'),('ú','u'),('ñ','n')]:
        text = text.replace(a, b)
    return text

def search_items(query):
    q = normalize(query)
    terms = {q}
    
    # Agregar traducción
    if q in TRANS:
        terms.add(TRANS[q])
    for word in q.split():
        if word in TRANS:
            terms.add(TRANS[word])
        terms.add(word)
    
    results = []
    for item in GAME_ITEMS:
        name = item.get("name", "").lower()
        desc = item.get("description", "").lower()
        
        score = 0
        for t in terms:
            if t in name:
                score += 10
            if t in desc:
                score += 3
        
        if score > 0:
            results.append((score, item))
    
    results.sort(key=lambda x: -x[0])
    return [item for _, item in results[:10]]

def get_locations(item, map_id):
    found_in = [f.lower() for f in item.get("foundIn", [])]
    if not found_in:
        return []
    
    pois = MAPS.get(map_id, {}).get("pois", [])
    matches = []
    for poi in pois:
        poi_types = [t.lower() for t in poi.get("types", [])]
        for f in found_in:
            if f in poi_types:
                matches.append(poi["title"])
                break
    return matches

def do_search(query, map_id):
    items = search_items(query)
    
    if not items:
        return f"❌ No encontré '{query}'. Prueba: battery, electrical, mechanical, medical", []
    
    response = f"🔍 **{len(items)} items encontrados:**\n\n"
    all_locs = []
    
    emojis = {"common": "⚪", "uncommon": "🟢", "rare": "🔵", "epic": "🟣", "legendary": "🟡"}
    
    for item in items[:6]:
        e = emojis.get(item.get("rarity"), "⚪")
        response += f"{e} **{item['name']}**"
        
        found_in = item.get("foundIn", [])
        if found_in:
            response += f" → _{', '.join(found_in)}_"
        
        locs = get_locations(item, map_id)
        if locs:
            all_locs.extend(locs)
            response += f"\n   📍 {', '.join(locs[:3])}"
        
        response += "\n\n"
    
    if all_locs:
        response += f"✅ **{len(set(all_locs))} ubicaciones sugeridas**"
    
    return response, list(set(all_locs))

# ═══════════════════════════════════════════════════════════════════════════════
# CSS
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
    .stApp { background: #0d1117; }
    section[data-testid="stSidebar"] { background: #161b22 !important; min-width: 300px !important; }
    .block-container { padding: 0 !important; max-width: 100% !important; }
    header, footer, #MainMenu { display: none !important; }
    
    h1,h2,h3 { color: #fff !important; font-size: 1rem !important; margin: 0.5rem 0 !important; }
    p, span, label { color: #c9d1d9 !important; }
    
    .stButton>button { background: #238636 !important; color: #fff !important; border: none !important; }
    .stButton>button:hover { background: #2ea043 !important; }
    
    .result-box {
        background: #21262d;
        border-left: 3px solid #4CAF50;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        font-size: 0.85rem;
    }
    .loc-tag {
        display: inline-block;
        background: #238636;
        color: #fff;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.75rem;
        margin: 2px;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ESTADO
# ═══════════════════════════════════════════════════════════════════════════════

if "current_map" not in st.session_state:
    st.session_state.current_map = "dam"
if "last_result" not in st.session_state:
    st.session_state.last_result = ""
if "last_locs" not in st.session_state:
    st.session_state.last_locs = []

# Mapas de MapGenie
MAP_URLS = {
    "dam": "https://mapgenie.io/arc-raiders/maps/dam-battlegrounds",
    "spaceport": "https://mapgenie.io/arc-raiders/maps/the-spaceport",
    "buried-city": "https://mapgenie.io/arc-raiders/maps/buried-city"
}

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## 🗺️ ARC Raiders Maps")
    
    st.session_state.current_map = st.selectbox(
        "Seleccionar mapa:",
        list(MAPS.keys()),
        format_func=lambda x: MAPS[x]["name"]
    )
    
    st.markdown("---")
    st.markdown("### 🔍 Buscar Items")
    st.caption(f"📦 {len(GAME_ITEMS)} items en la base de datos")
    
    query = st.text_input("¿Qué buscas?", placeholder="batería, médico, eléctrico...")
    
    col1, col2 = st.columns(2)
    with col1:
        search_clicked = st.button("🔍 Buscar", use_container_width=True)
    with col2:
        if st.button("🗑️ Limpiar", use_container_width=True):
            st.session_state.last_result = ""
            st.session_state.last_locs = []
            st.rerun()
    
    if search_clicked and query:
        result, locs = do_search(query, st.session_state.current_map)
        st.session_state.last_result = result
        st.session_state.last_locs = locs
    
    # Mostrar resultado
    if st.session_state.last_result:
        st.markdown("---")
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown(st.session_state.last_result)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Ubicaciones
    if st.session_state.last_locs:
        st.markdown("### 📍 Ubicaciones")
        locs_html = "".join([f'<span class="loc-tag">{loc}</span>' for loc in st.session_state.last_locs])
        st.markdown(locs_html, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🗺️ Abrir Mapa")
    map_url = MAP_URLS.get(st.session_state.current_map, MAP_URLS['dam'])
    
    st.markdown(
        f'<a href="{map_url}" target="_blank" style="text-decoration:none;">' +
        '<button style="width:100%;padding:12px;background:#238636;color:#fff;border:none;border-radius:5px;cursor:pointer;font-size:15px;font-weight:bold;">' +
        f'🗺️ Abrir {MAPS[st.session_state.current_map]["name"]}</button></a>',
        unsafe_allow_html=True
    )
    st.caption("✅ Se abre en nueva pestaña con tu sesión")
    st.caption("💡 Inicia sesión una vez y tus marcadores se guardan")
    
    st.markdown("---")
    st.markdown("### ⚡ Búsqueda Rápida")
    
    quick = [
        ("🔋 Batería", "battery"),
        ("⚡ Eléctrico", "electrical"),
        ("🔧 Mecánico", "mechanical"), 
        ("💊 Médico", "medical"),
        ("🤖 ARC", "ARC powercell"),
    ]
    
    cols = st.columns(2)
    for i, (label, q) in enumerate(quick):
        with cols[i % 2]:
            if st.button(label, key=f"quick_{i}", use_container_width=True):
                result, locs = do_search(q, st.session_state.current_map)
                st.session_state.last_result = result
                st.session_state.last_locs = locs
                st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# ÁREA PRINCIPAL - INSTRUCCIONES Y PREVIEW
# ═══════════════════════════════════════════════════════════════════════════════

map_id = st.session_state.current_map
map_name = MAPS[map_id]["name"]
map_url = MAP_URLS[map_id]

st.markdown(f"""
<div style="padding: 2rem; max-width: 900px; margin: 0 auto;">
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">🗺️ {map_name}</h1>
        <p style="font-size: 1.1rem; color: #8b949e;">Mapa interactivo con marcadores personalizados</p>
    </div>
    
    <div style="background: #161b22; padding: 2rem; border-radius: 10px; border: 1px solid #30363d; margin-bottom: 2rem;">
        <h2 style="font-size: 1.5rem; margin-bottom: 1rem;">✨ Características de MapGenie</h2>
        <ul style="font-size: 1rem; line-height: 1.8; color: #c9d1d9;">
            <li>✅ <strong>Marcadores personalizados</strong> - Marca ubicaciones importantes</li>
            <li>✅ <strong>Filtros avanzados</strong> - Encuentra items específicos rápidamente</li>
            <li>✅ <strong>Sincronización</strong> - Accede desde cualquier dispositivo</li>
            <li>✅ <strong>Progreso trackeable</strong> - Marca zonas exploradas</li>
            <li>✅ <strong>Notas privadas</strong> - Añade recordatorios a cada marcador</li>
        </ul>
    </div>
    
    <div style="background: #21262d; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #238636; margin-bottom: 2rem;">
        <h3 style="font-size: 1.2rem; margin-bottom: 0.5rem;">💡 Cómo usar</h3>
        <ol style="font-size: 1rem; line-height: 1.8; color: #c9d1d9;">
            <li>Click en <strong>"Abrir {map_name}"</strong> en el menú lateral</li>
            <li>Inicia sesión en MapGenie (solo la primera vez)</li>
            <li>Explora el mapa y crea tus marcadores</li>
            <li>Usa la búsqueda del menú para encontrar items específicos</li>
        </ol>
    </div>
    
    <div style="text-align: center;">
        <a href="{map_url}" target="_blank" style="text-decoration: none;">
            <button style="
                background: linear-gradient(135deg, #238636 0%, #2ea043 100%);
                color: white;
                font-size: 1.2rem;
                font-weight: bold;
                padding: 1rem 3rem;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                box-shadow: 0 4px 12px rgba(35, 134, 54, 0.3);
                transition: transform 0.2s;
            " onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                🚀 Abrir Mapa Interactivo
            </button>
        </a>
        <p style="margin-top: 1rem; color: #8b949e; font-size: 0.9rem;">Se abre en nueva pestaña • Sesión persistente</p>
    </div>
    
    <div style="margin-top: 3rem; padding-top: 2rem; border-top: 1px solid #30363d; text-align: center;">
        <p style="color: #8b949e; font-size: 0.9rem;">
            📊 Base de datos: {len(GAME_ITEMS)} items • 🗺️ {len(MAPS)} mapas disponibles
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

