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
# MAPA PRINCIPAL - PANTALLA COMPLETA
# ═══════════════════════════════════════════════════════════════════════════════

map_id = st.session_state.current_map

# CSS adicional para eliminar espacio extra
st.markdown("""
<style>
    .main .block-container { padding: 0 !important; margin: 0 !important; }
    .stHtml { margin: 0 !important; padding: 0 !important; }
    iframe { margin: 0 !important; }
    section[data-testid="stMain"] { padding: 0 !important; }
    .element-container { margin: 0 !important; padding: 0 !important; }
</style>
""", unsafe_allow_html=True)

# Iframe que ocupa toda la pantalla disponible
components.html(
    f'''<!DOCTYPE html>
    <html style="margin:0;padding:0;height:100%;overflow:hidden;">
    <body style="margin:0;padding:0;height:100%;overflow:hidden;background:#0d1117;">
        <iframe src="https://arcraidersmaps.app/{map_id}" 
                style="width:100%;height:100vh;border:none;display:block;"></iframe>
    </body>
    </html>''',
    height=950,
    scrolling=False
)
