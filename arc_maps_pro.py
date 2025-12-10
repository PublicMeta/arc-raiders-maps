"""
ARC Raiders Maps Pro - Interactive Map + AI Chat + Crafteo + Rutas
"""

import streamlit as st
import streamlit.components.v1 as components
import json
import os
from openai import OpenAI
from dotenv import load_dotenv

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════════════════════

load_dotenv()
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ITEMS_FILE = os.path.join(SCRIPT_DIR, "items_data.json")

st.set_page_config(
    page_title="ARC Raiders Maps Pro",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cliente OpenAI
@st.cache_resource
def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return OpenAI(api_key=api_key)
    return None

client = get_openai_client()

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

# Crear índice de items por nombre
@st.cache_data
def create_items_index():
    return {item["name"].lower(): item for item in GAME_ITEMS}

ITEMS_INDEX = create_items_index()

# ═══════════════════════════════════════════════════════════════════════════════
# DATOS DEL JUEGO
# ═══════════════════════════════════════════════════════════════════════════════

# Traducciones ES -> EN
TRANS = {
    "bateria": "battery", "baterias": "battery", "pila": "battery", "pilas": "battery",
    "energia": "power", "electrico": "electrical", "electricidad": "electrical",
    "mecanico": "mechanical", "medico": "medical", "medicina": "medical",
    "arma": "weapon", "municion": "ammo", "vendaje": "bandage",
    "componente": "component", "cable": "cable", "chatarra": "scrap",
    "quimico": "chemical", "plastico": "plastic", "metal": "metal",
    "tela": "cloth", "pegamento": "adhesive", "cinta": "tape",
}

# POIs por mapa con coordenadas aproximadas para rutas
MAPS = {
    "dam": {
        "name": "Dam Battlegrounds",
        "pois": [
            {"title": "Power Generation Complex", "types": ["industrial", "electrical"], "x": 45, "y": 30},
            {"title": "Electrical Substation", "types": ["electrical"], "x": 55, "y": 25},
            {"title": "Water Treatment", "types": ["industrial", "mechanical"], "x": 35, "y": 45},
            {"title": "Testing Annex", "types": ["medical", "commercial"], "x": 60, "y": 50},
            {"title": "Research & Administration", "types": ["technological"], "x": 50, "y": 55},
            {"title": "Old Battlegrounds", "types": ["ARC"], "x": 40, "y": 65},
            {"title": "Primary Facility", "types": ["mechanical", "industrial"], "x": 30, "y": 40},
            {"title": "Scrap Yard", "types": ["mechanical", "industrial"], "x": 65, "y": 35},
            {"title": "Pale Apartments", "types": ["residential"], "x": 25, "y": 55},
            {"title": "Ruby Residence", "types": ["residential"], "x": 70, "y": 60},
            {"title": "Hydrophonic Dome", "types": ["nature"], "x": 50, "y": 70},
        ]
    },
    "spaceport": {
        "name": "The Spaceport",
        "pois": [
            {"title": "Fuel Control", "types": ["mechanical", "electrical"], "x": 40, "y": 30},
            {"title": "Rocket Assembly", "types": ["ARC", "industrial"], "x": 55, "y": 25},
            {"title": "Shipping Warehouse", "types": ["industrial", "mechanical"], "x": 45, "y": 45},
            {"title": "Container Storage", "types": ["industrial"], "x": 60, "y": 40},
            {"title": "Vehicle Maintenance", "types": ["mechanical"], "x": 35, "y": 55},
            {"title": "Departure Building", "types": ["commercial"], "x": 50, "y": 60},
        ]
    },
    "buried-city": {
        "name": "Buried City",
        "pois": [
            {"title": "Hospital", "types": ["medical"], "x": 45, "y": 35},
            {"title": "Research", "types": ["medical", "technological"], "x": 55, "y": 30},
            {"title": "Parking Garage", "types": ["mechanical"], "x": 40, "y": 50},
            {"title": "Outskirts", "types": ["industrial", "mechanical"], "x": 30, "y": 45},
            {"title": "Galleria", "types": ["commercial"], "x": 60, "y": 55},
            {"title": "Grandioso Apartments", "types": ["residential"], "x": 50, "y": 65},
            {"title": "Marano Park", "types": ["nature"], "x": 65, "y": 40},
        ]
    },
}

# URLs de MapGenie
MAP_URLS = {
    "dam": "https://mapgenie.io/arc-raiders/maps/dam-battlegrounds",
    "spaceport": "https://mapgenie.io/arc-raiders/maps/the-spaceport",
    "buried-city": "https://mapgenie.io/arc-raiders/maps/buried-city"
}

# Sistema de Crafteo - Recetas conocidas
RECIPES = {
    "bandage": {
        "name": "Bandage",
        "materials": [("Cloth", 2)],
        "category": "medical",
        "description": "Cura heridas menores"
    },
    "medkit": {
        "name": "Medkit", 
        "materials": [("Bandage", 2), ("Chemical", 1)],
        "category": "medical",
        "description": "Restaura una cantidad moderada de salud"
    },
    "advanced_medkit": {
        "name": "Advanced Medkit",
        "materials": [("Medkit", 1), ("Advanced Medical Components", 1)],
        "category": "medical",
        "description": "Restaura gran cantidad de salud"
    },
    "basic_electrical_components": {
        "name": "Basic Electrical Components",
        "materials": [("Cable", 2), ("Battery", 1)],
        "category": "electrical",
        "description": "Componente básico para crafting eléctrico"
    },
    "basic_mechanical_components": {
        "name": "Basic Mechanical Components",
        "materials": [("Scrap Metal", 2), ("Adhesive", 1)],
        "category": "mechanical",
        "description": "Componente básico para crafting mecánico"
    },
    "shield_booster": {
        "name": "Shield Booster",
        "materials": [("Basic Electrical Components", 2), ("ARC Powercell", 1)],
        "category": "utility",
        "description": "Aumenta la regeneración de escudo temporalmente"
    },
    "stamina_booster": {
        "name": "Stamina Booster",
        "materials": [("Agave", 2), ("Chemical", 1)],
        "category": "utility",
        "description": "Aumenta la regeneración de stamina"
    },
    "emp_grenade": {
        "name": "EMP Grenade",
        "materials": [("Advanced Electrical Components", 1), ("Battery", 2), ("Explosive", 1)],
        "category": "weapon",
        "description": "Desactiva robots y drones temporalmente"
    },
}

# ═══════════════════════════════════════════════════════════════════════════════
# FUNCIONES DE BÚSQUEDA
# ═══════════════════════════════════════════════════════════════════════════════

def normalize(text):
    text = text.lower().strip()
    for a, b in [('á','a'),('é','e'),('í','i'),('ó','o'),('ú','u'),('ñ','n')]:
        text = text.replace(a, b)
    return text

def search_items(query, limit=10):
    q = normalize(query)
    terms = {q}
    
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
        item_type = item.get("type", "").lower()
        
        score = 0
        for t in terms:
            if t in name:
                score += 10
            if t in desc:
                score += 3
            if t in item_type:
                score += 5
        
        if score > 0:
            results.append((score, item))
    
    results.sort(key=lambda x: -x[0])
    return [item for _, item in results[:limit]]

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

# ═══════════════════════════════════════════════════════════════════════════════
# SISTEMA DE CRAFTEO
# ═══════════════════════════════════════════════════════════════════════════════

def get_recipe_tree(recipe_id, quantity=1, depth=0):
    """Obtiene árbol completo de materiales necesarios"""
    if recipe_id not in RECIPES:
        return None
    
    recipe = RECIPES[recipe_id]
    tree = {
        "name": recipe["name"],
        "quantity": quantity,
        "materials": [],
        "depth": depth
    }
    
    for mat_name, mat_qty in recipe["materials"]:
        mat_id = mat_name.lower().replace(" ", "_")
        if mat_id in RECIPES and depth < 3:
            subtree = get_recipe_tree(mat_id, mat_qty * quantity, depth + 1)
            if subtree:
                tree["materials"].append(subtree)
            else:
                tree["materials"].append({"name": mat_name, "quantity": mat_qty * quantity, "base": True})
        else:
            tree["materials"].append({"name": mat_name, "quantity": mat_qty * quantity, "base": True})
    
    return tree

def calculate_base_materials(recipe_id, quantity=1):
    """Calcula materiales base totales necesarios"""
    base_mats = {}
    
    def collect(tree):
        if tree.get("base"):
            name = tree["name"]
            base_mats[name] = base_mats.get(name, 0) + tree["quantity"]
        else:
            for mat in tree.get("materials", []):
                collect(mat)
    
    tree = get_recipe_tree(recipe_id, quantity)
    if tree:
        collect(tree)
    
    return base_mats

def format_recipe(recipe_id):
    """Formatea una receta para mostrar"""
    if recipe_id not in RECIPES:
        return None
    
    recipe = RECIPES[recipe_id]
    output = f"### 🔨 {recipe['name']}\n"
    output += f"*{recipe['description']}*\n\n"
    output += "**Materiales directos:**\n"
    
    for mat_name, mat_qty in recipe["materials"]:
        output += f"- {mat_qty}x {mat_name}\n"
    
    base = calculate_base_materials(recipe_id)
    if base and len(base) != len(recipe["materials"]):
        output += "\n**Materiales base totales:**\n"
        for name, qty in sorted(base.items()):
            output += f"- {qty}x {name}\n"
    
    return output

def find_recipe_by_name(query):
    """Busca recetas por nombre"""
    q = normalize(query)
    for rid, recipe in RECIPES.items():
        if q in normalize(recipe["name"]):
            return rid, recipe
    return None, None

# ═══════════════════════════════════════════════════════════════════════════════
# RUTAS DE FARMEO
# ═══════════════════════════════════════════════════════════════════════════════

def calculate_farming_route(map_id, target_type):
    """Calcula ruta óptima para farmear un tipo de recurso"""
    pois = MAPS.get(map_id, {}).get("pois", [])
    relevant = []
    
    for poi in pois:
        types = [t.lower() for t in poi.get("types", [])]
        if target_type.lower() in types:
            relevant.append(poi)
    
    if not relevant:
        return None, []
    
    # Ordenar por proximidad (greedy nearest neighbor)
    if len(relevant) > 1:
        route = [relevant[0]]
        remaining = relevant[1:]
        
        while remaining:
            last = route[-1]
            nearest = min(remaining, key=lambda p: 
                ((p["x"] - last["x"])**2 + (p["y"] - last["y"])**2)**0.5)
            route.append(nearest)
            remaining.remove(nearest)
        
        return route, relevant
    
    return relevant, relevant

def get_best_map_for_type(target_type):
    """Encuentra el mejor mapa para un tipo de recurso"""
    results = []
    
    for map_id, map_data in MAPS.items():
        count = sum(1 for poi in map_data["pois"] 
                   if target_type.lower() in [t.lower() for t in poi.get("types", [])])
        if count > 0:
            results.append((map_data["name"], count, map_id))
    
    results.sort(key=lambda x: -x[1])
    return results

# ═══════════════════════════════════════════════════════════════════════════════
# CHAT IA
# ═══════════════════════════════════════════════════════════════════════════════

def build_context():
    """Construye contexto del juego para la IA"""
    items_summary = []
    for item in GAME_ITEMS[:100]:  # Top 100 items
        found = ", ".join(item.get("foundIn", [])) or "unknown"
        items_summary.append(f"- {item['name']} ({item.get('rarity', 'common')}): {found}")
    
    recipes_summary = []
    for rid, recipe in RECIPES.items():
        mats = ", ".join([f"{q}x {n}" for n, q in recipe["materials"]])
        recipes_summary.append(f"- {recipe['name']}: necesita {mats}")
    
    maps_summary = []
    for mid, mdata in MAPS.items():
        pois = ", ".join([p["title"] for p in mdata["pois"][:5]])
        maps_summary.append(f"- {mdata['name']}: {pois}...")
    
    return f"""Eres un asistente experto de ARC Raiders, un videojuego de supervivencia cooperativo.

MAPAS DISPONIBLES:
{chr(10).join(maps_summary)}

TIPOS DE UBICACIONES: electrical, mechanical, medical, industrial, residential, commercial, nature, ARC, technological

ALGUNOS ITEMS ({len(GAME_ITEMS)} totales):
{chr(10).join(items_summary[:30])}

RECETAS DE CRAFTEO:
{chr(10).join(recipes_summary)}

REGLAS:
1. Responde en español
2. Sé conciso y directo
3. Da recomendaciones específicas de ubicaciones
4. Si preguntan por crafteo, detalla los materiales
5. Para farmeo, sugiere rutas eficientes
6. Si no sabes algo, dilo honestamente
7. Tienes acceso a información actualizada del juego hasta tu fecha de entrenamiento"""

def chat_with_ai(user_message, history, current_map):
    """Genera respuesta de IA conversacional"""
    if not client:
        return "❌ API key de OpenAI no configurada. Añade OPENAI_API_KEY al archivo .env"
    
    try:
        messages = [{"role": "system", "content": build_context()}]
        
        # Agregar contexto del mapa actual
        map_name = MAPS.get(current_map, {}).get("name", current_map)
        messages.append({
            "role": "system", 
            "content": f"El usuario está viendo el mapa: {map_name}"
        })
        
        # Historial de conversación
        for msg in history[-6:]:  # Últimos 6 mensajes
            messages.append(msg)
        
        messages.append({"role": "user", "content": user_message})
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=600,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"❌ Error de IA: {str(e)}"

# ═══════════════════════════════════════════════════════════════════════════════
# CSS - Layout optimizado sin conflictos
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
    /* === LAYOUT PRINCIPAL === */
    .stApp { background: #0d1117; }
    
    /* Sidebar compacto a la izquierda */
    section[data-testid="stSidebar"] {
        background: #161b22 !important;
        width: 280px !important;
        min-width: 280px !important;
        max-width: 280px !important;
    }
    section[data-testid="stSidebar"] > div {
        padding: 0.5rem !important;
    }
    
    /* Área principal - sin padding para el mapa */
    .block-container { 
        padding: 0 !important; 
        max-width: 100% !important; 
        margin: 0 !important;
    }
    
    /* Ocultar elementos de Streamlit */
    header, footer, #MainMenu, .stDeployButton { display: none !important; }
    
    /* === TIPOGRAFÍA === */
    h1,h2,h3 { color: #fff !important; font-size: 0.95rem !important; margin: 0.3rem 0 !important; }
    p, span, label { color: #c9d1d9 !important; font-size: 0.85rem !important; }
    
    /* === BOTONES === */
    .stButton>button {
        background: #238636 !important;
        color: #fff !important;
        border: none !important;
        font-size: 0.8rem !important;
        padding: 0.4rem 0.8rem !important;
    }
    .stButton>button:hover { background: #2ea043 !important; }
    
    /* === COMPONENTES === */
    .result-box {
        background: #21262d;
        border-left: 3px solid #4CAF50;
        padding: 8px;
        border-radius: 5px;
        margin: 5px 0;
        font-size: 0.8rem;
    }
    .chat-user {
        background: #1f6feb;
        color: #fff;
        padding: 6px 10px;
        border-radius: 8px;
        margin: 3px 0;
        text-align: right;
        font-size: 0.8rem;
    }
    .chat-ai {
        background: #21262d;
        border-left: 3px solid #8b5cf6;
        padding: 6px 10px;
        border-radius: 5px;
        margin: 3px 0;
        font-size: 0.8rem;
    }
    .loc-tag {
        display: inline-block;
        background: #238636;
        color: #fff;
        padding: 2px 6px;
        border-radius: 8px;
        font-size: 0.7rem;
        margin: 1px;
    }
    .route-step {
        background: #1f6feb;
        color: #fff;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
        margin: 2px;
        display: inline-block;
    }
    
    /* === TABS COMPACTOS === */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background: #21262d;
        border-radius: 5px;
        padding: 3px;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 4px;
        color: #c9d1d9;
        padding: 6px 10px;
        font-size: 0.9rem;
    }
    .stTabs [aria-selected="true"] {
        background: #238636 !important;
        color: #fff !important;
    }
    
    /* === INPUTS COMPACTOS === */
    .stTextInput input {
        font-size: 0.85rem !important;
        padding: 0.4rem !important;
    }
    .stSelectbox > div > div {
        font-size: 0.85rem !important;
    }
    
    /* Reducir espaciado general en sidebar */
    section[data-testid="stSidebar"] .stMarkdown {
        margin-bottom: 0.2rem !important;
    }
    section[data-testid="stSidebar"] hr {
        margin: 0.5rem 0 !important;
    }
</style>
""", unsafe_allow_html=True)# ═══════════════════════════════════════════════════════════════════════════════
# ESTADO
# ═══════════════════════════════════════════════════════════════════════════════

if "current_map" not in st.session_state:
    st.session_state.current_map = "dam"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "favorites" not in st.session_state:
    st.session_state.favorites = []
if "search_history" not in st.session_state:
    st.session_state.search_history = []

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("### 🗺️ ARC Maps Pro")
    
    # Selector de mapa compacto
    st.session_state.current_map = st.selectbox(
        "Mapa:",
        list(MAPS.keys()),
        format_func=lambda x: MAPS[x]["name"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")

    # Tabs para diferentes funciones
    tab_search, tab_chat, tab_craft, tab_routes, tab_favs = st.tabs([
        "🔍", "🤖", "🔨", "⚡", "⭐"
    ])    # ═══════════════════════════════════════════════════════════════════════
    # TAB: BÚSQUEDA
    # ═══════════════════════════════════════════════════════════════════════
    with tab_search:
        st.markdown("### 🔍 Buscar Items")
        st.caption(f"📦 {len(GAME_ITEMS)} items disponibles")
        
        query = st.text_input("¿Qué buscas?", placeholder="batería, médico...", key="search_query")
        
        if st.button("🔍 Buscar", use_container_width=True, key="btn_search"):
            if query:
                items = search_items(query)
                if items:
                    # Guardar en historial
                    if query not in st.session_state.search_history:
                        st.session_state.search_history.insert(0, query)
                        st.session_state.search_history = st.session_state.search_history[:10]
                    
                    st.markdown(f"**{len(items)} resultados:**")
                    emojis = {"common": "⚪", "uncommon": "🟢", "rare": "🔵", "epic": "🟣", "legendary": "🟡"}
                    
                    for item in items[:8]:
                        e = emojis.get(item.get("rarity"), "⚪")
                        found = item.get("foundIn", [])
                        locs = get_locations(item, st.session_state.current_map)
                        
                        with st.container():
                            col1, col2 = st.columns([4, 1])
                            with col1:
                                st.markdown(f"{e} **{item['name']}**")
                                if found:
                                    st.caption(f"→ {', '.join(found)}")
                                if locs:
                                    locs_html = "".join([f'<span class="loc-tag">{l}</span>' for l in locs[:3]])
                                    st.markdown(locs_html, unsafe_allow_html=True)
                            with col2:
                                if st.button("⭐", key=f"fav_{item['id']}", help="Añadir a favoritos"):
                                    if item['name'] not in st.session_state.favorites:
                                        st.session_state.favorites.append(item['name'])
                else:
                    st.warning("No encontrado. Prueba: battery, electrical, medical")
        
        # Abrir mapa
        st.markdown("---")
        st.markdown("**🗺️ Mapa:**")
        map_url = MAP_URLS.get(st.session_state.current_map, MAP_URLS['dam'])
        st.markdown(
            f'<a href="{map_url}" target="_blank" style="text-decoration:none;">' +
            '<div style="background:linear-gradient(135deg,#238636,#2ea043);padding:14px;border-radius:8px;text-align:center;box-shadow:0 4px 12px rgba(35,134,54,0.4);">' +
            f'<div style="color:#fff;font-size:15px;font-weight:bold;">🗺️ {MAPS[st.session_state.current_map]["name"]}</div>' +
            '<div style="color:#d1fae5;font-size:12px;margin-top:4px;">Click para abrir →</div>' +
            '</div></a>',
            unsafe_allow_html=True
        )
        st.info("🔐 **Primera vez:** Inicia sesión arriba-derecha en MapGenie")
        
        # Búsqueda rápida
        st.markdown("---")
        st.markdown("**⚡ Rápido:**")
        quick_cols = st.columns(3)
        quick = [("🔋", "battery"), ("⚡", "electrical"), ("🔧", "mechanical"), 
                 ("💊", "medical"), ("🤖", "ARC"), ("🏠", "residential")]
        
        for i, (icon, q) in enumerate(quick):
            with quick_cols[i % 3]:
                if st.button(icon, key=f"q_{q}", help=q):
                    items = search_items(q, limit=5)
                    if items:
                        st.session_state.quick_results = items
    
    # ═══════════════════════════════════════════════════════════════════════
    # TAB: CHAT IA
    # ═══════════════════════════════════════════════════════════════════════
    with tab_chat:
        st.markdown("### 🤖 Asistente IA")
        
        if not client:
            st.warning("⚠️ Configura OPENAI_API_KEY en .env")
        else:
            st.caption("Pregunta sobre items, crafteo, ubicaciones...")
            
            # Mostrar historial
            chat_container = st.container()
            with chat_container:
                for msg in st.session_state.chat_history[-8:]:
                    if msg["role"] == "user":
                        st.markdown(f'<div class="chat-user">{msg["content"]}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="chat-ai">{msg["content"]}</div>', unsafe_allow_html=True)
            
            # Input
            user_input = st.text_input("Tu mensaje:", placeholder="¿Dónde encuentro baterías?", key="chat_input")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💬 Enviar", use_container_width=True, key="btn_send"):
                    if user_input:
                        # Agregar mensaje usuario
                        st.session_state.chat_history.append({"role": "user", "content": user_input})
                        
                        # Obtener respuesta
                        with st.spinner("Pensando..."):
                            response = chat_with_ai(user_input, st.session_state.chat_history, 
                                                   st.session_state.current_map)
                        
                        st.session_state.chat_history.append({"role": "assistant", "content": response})
                        st.rerun()
            
            with col2:
                if st.button("🗑️ Limpiar", use_container_width=True, key="btn_clear_chat"):
                    st.session_state.chat_history = []
                    st.rerun()
            
            # Sugerencias rápidas
            st.markdown("**💡 Preguntas sugeridas:**")
            suggestions = [
                "¿Mejor mapa para farmear electrical?",
                "¿Qué necesito para craftear Medkit?",
                "¿Dónde hay componentes ARC?",
            ]
            for sug in suggestions:
                if st.button(sug, key=f"sug_{hash(sug)}", use_container_width=True):
                    st.session_state.chat_history.append({"role": "user", "content": sug})
                    with st.spinner("Pensando..."):
                        response = chat_with_ai(sug, st.session_state.chat_history, 
                                               st.session_state.current_map)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                    st.rerun()
    
    # ═══════════════════════════════════════════════════════════════════════
    # TAB: CRAFTEO
    # ═══════════════════════════════════════════════════════════════════════
    with tab_craft:
        st.markdown("### 🔨 Sistema de Crafteo")
        
        # Selector de receta
        recipe_names = {rid: r["name"] for rid, r in RECIPES.items()}
        selected_recipe = st.selectbox(
            "Selecciona receta:",
            list(recipe_names.keys()),
            format_func=lambda x: recipe_names[x]
        )
        
        quantity = st.number_input("Cantidad:", min_value=1, max_value=10, value=1)
        
        if selected_recipe:
            recipe = RECIPES[selected_recipe]
            
            st.markdown(f"**{recipe['name']}**")
            st.caption(recipe["description"])
            
            st.markdown("**📋 Materiales directos:**")
            for mat_name, mat_qty in recipe["materials"]:
                total = mat_qty * quantity
                st.markdown(f"- {total}x {mat_name}")
            
            # Materiales base
            base = calculate_base_materials(selected_recipe, quantity)
            if base and len(base) != len(recipe["materials"]):
                st.markdown("**🔧 Materiales base totales:**")
                for name, qty in sorted(base.items()):
                    # Buscar dónde encontrar
                    items = search_items(name, limit=1)
                    if items and items[0].get("foundIn"):
                        found = items[0]["foundIn"][0]
                        st.markdown(f"- {qty}x {name} → _{found}_")
                    else:
                        st.markdown(f"- {qty}x {name}")
        
        # Calculadora inversa
        st.markdown("---")
        st.markdown("**🔄 ¿Qué puedo craftear con...?**")
        material = st.text_input("Material:", placeholder="battery, cloth...", key="craft_mat")
        
        if material and st.button("Buscar recetas", key="btn_find_recipes"):
            mat_lower = material.lower()
            found_recipes = []
            for rid, recipe in RECIPES.items():
                for mat_name, _ in recipe["materials"]:
                    if mat_lower in mat_name.lower():
                        found_recipes.append(recipe["name"])
                        break
            
            if found_recipes:
                st.success(f"Puedes craftear: {', '.join(found_recipes)}")
            else:
                st.info("No se encontraron recetas con ese material")
    
    # ═══════════════════════════════════════════════════════════════════════
    # TAB: RUTAS
    # ═══════════════════════════════════════════════════════════════════════
    with tab_routes:
        st.markdown("### ⚡ Rutas de Farmeo")
        
        # Selector de tipo de recurso
        resource_types = ["electrical", "mechanical", "medical", "industrial", 
                         "residential", "commercial", "ARC", "nature"]
        
        selected_type = st.selectbox("Tipo de recurso:", resource_types)
        
        if st.button("📍 Calcular Ruta", use_container_width=True, key="btn_route"):
            route, all_pois = calculate_farming_route(st.session_state.current_map, selected_type)
            
            if route:
                st.success(f"✅ {len(route)} ubicaciones encontradas")
                
                st.markdown("**🗺️ Ruta optimizada:**")
                for i, poi in enumerate(route, 1):
                    st.markdown(f'<span class="route-step">{i}. {poi["title"]}</span>', 
                               unsafe_allow_html=True)
                
                # Items relacionados
                related = search_items(selected_type, limit=5)
                if related:
                    st.markdown("**📦 Items típicos:**")
                    for item in related[:3]:
                        st.caption(f"• {item['name']}")
            else:
                st.warning(f"No hay ubicaciones de tipo '{selected_type}' en este mapa")
        
        st.markdown("---")
        st.markdown("**🏆 Mejor mapa para...**")
        
        compare_type = st.selectbox("Comparar:", resource_types, key="compare_type")
        
        if st.button("📊 Comparar mapas", key="btn_compare"):
            results = get_best_map_for_type(compare_type)
            
            if results:
                st.markdown(f"**Mejor mapa para {compare_type}:**")
                for map_name, count, map_id in results:
                    bar = "█" * count + "░" * (5 - count)
                    st.markdown(f"{bar} **{map_name}** ({count} POIs)")
            else:
                st.info("Tipo no encontrado en ningún mapa")
    
    # ═══════════════════════════════════════════════════════════════════════
    # TAB: FAVORITOS
    # ═══════════════════════════════════════════════════════════════════════
    with tab_favs:
        st.markdown("### ⭐ Favoritos")
        
        if st.session_state.favorites:
            for fav in st.session_state.favorites:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"• {fav}")
                with col2:
                    if st.button("❌", key=f"del_{fav}"):
                        st.session_state.favorites.remove(fav)
                        st.rerun()
            
            if st.button("🗑️ Limpiar todos", key="btn_clear_favs"):
                st.session_state.favorites = []
                st.rerun()
        else:
            st.caption("No hay favoritos. Usa ⭐ en búsqueda para añadir.")
        
        st.markdown("---")
        st.markdown("### 📜 Historial")
        
        if st.session_state.search_history:
            for h in st.session_state.search_history[:5]:
                if st.button(f"🔍 {h}", key=f"hist_{h}", use_container_width=True):
                    items = search_items(h)
                    st.session_state.quick_results = items
        else:
            st.caption("Sin búsquedas recientes")

# ═══════════════════════════════════════════════════════════════════════════════
# MAPA PRINCIPAL - PANTALLA COMPLETA SIN CONFLICTOS
# ═══════════════════════════════════════════════════════════════════════════════

map_id = st.session_state.current_map

# ═══════════════════════════════════════════════════════════════════════
# ÁREA PRINCIPAL - MAPA INTERACTIVO
# ═══════════════════════════════════════════════════════════════════════

map_name = MAPS[map_id]["name"]
map_url = MAP_URLS[map_id]

# CSS para maximizar espacio del mapa
st.markdown("""
<style>
    section[data-testid="stMain"] { padding: 0 !important; margin: 0 !important; }
    .block-container { padding: 0 !important; margin: 0 !important; max-width: 100% !important; }
    .element-container { margin: 0 !important; padding: 0 !important; }
</style>
""", unsafe_allow_html=True)

# Mensaje sobre login
st.markdown(f"""
<div style="padding: 1rem; background: #161b22; border-left: 4px solid #f97316; margin-bottom: 0.5rem;">
    <strong>🔐 Login MapGenie:</strong> Busca <strong>"Sign In"</strong> en la esquina superior derecha del mapa abajo. 
    Tu sesión se guarda automáticamente.
</div>
""", unsafe_allow_html=True)

# Iframe del mapa
components.html(
    f'''<!DOCTYPE html>
    <html style="margin:0;padding:0;height:100%;">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            html, body {{ width: 100%; height: 100%; overflow: hidden; background: #0d1117; }}
            iframe {{ width: 100%; height: 100vh; border: none; display: block; }}
        </style>
    </head>
    <body>
        <iframe src="{map_url}" 
                allow="fullscreen"
                loading="eager"></iframe>
    </body>
    </html>''',
    height=850,
    scrolling=False
)