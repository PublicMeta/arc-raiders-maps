import streamlit as st
import os
import base64
from openai import OpenAI

# ═══════════════════════════════════════════════════════════════════════════════
# BASE DE DATOS DE INTELIGENCIA - ARC RAIDERS
# ═══════════════════════════════════════════════════════════════════════════════
ARC_DATABASE = """
## MAPAS OFICIALES DE ARC RAIDERS

### 1. DAM BATTLEGROUNDS (Presa)
- **Tipo:** Zona PvPvE de alto riesgo
- **Ambiente:** Presa hidroeléctrica masiva, estructuras industriales oxidadas
- **Puntos de Interés (POIs):**
  - **Central de la Presa:** Loot de alta calidad (armas, electrónica). MUY disputado.
  - **Torres de Vigilancia:** Buenos puntos de francotirador, loot medio.
  - **Túneles de Mantenimiento:** Ruta de escape segura, cajas de herramientas.
  - **Sala de Turbinas:** Engranajes, partes mecánicas, cables.
- **Loot principal:** Metal Parts, Gears, Weapon Parts, Electronics
- **Peligro:** ALTO (muchos jugadores, chokepoints)

### 2. BURIED CITY (Ciudad Enterrada)
- **Tipo:** Zona de exploración y extracción
- **Ambiente:** Ruinas urbanas semienterradas en dunas de arena
- **Puntos de Interés (POIs):**
  - **Edificios Residenciales:** Tela, suministros médicos, mochilas.
  - **Centro Comercial Hundido:** Loot variado, muchas emboscadas PvP.
  - **Estación de Metro:** Electrónica avanzada, cables, baterías. Oscuro.
  - **Restos de Titanes ARC:** ARC Cores (MUY RARO), componentes exóticos.
  - **Aparcamiento Subterráneo:** Partes de vehículos, metal.
- **Loot principal:** Electronics, Medical Supplies, ARC Cores (raro)
- **Peligro:** MEDIO-ALTO (Drones ARC frecuentes)

### 3. SPACEPORT (Puerto Espacial)
- **Tipo:** Zona industrial/militar
- **Ambiente:** Instalaciones de lanzamiento abandonadas, hangares enormes
- **Puntos de Interés (POIs):**
  - **Hangares de Carga (A, B, C):** Cajas de herramientas ROJAS, partes de armas.
  - **Torre de Control:** Chips de datos, electrónica de alta gama.
  - **Plataformas de Lanzamiento:** Loot raro pero zona MUY expuesta.
  - **Almacenes Logísticos:** Metal Parts, Gears, munición.
  - **Barracones Militares:** Armas, armaduras, cajas verdes militares.
- **Loot principal:** Weapon Parts, Gun Components, Metal Parts, Ammo
- **Peligro:** MEDIO (espacios abiertos, fácil ser visto)

### 4. THE BLUE GATE (La Puerta Azul)
- **Tipo:** Zona narrativa/misteriosa
- **Ambiente:** Estructuras alienígenas o antiguas, tecnología desconocida
- **Puntos de Interés (POIs):**
  - **Complejo Central:** Artefactos raros, componentes únicos.
  - **Laboratorios Abandonados:** Químicos, medicina avanzada, Stims raros.
  - **Perímetro Exterior:** Loot básico, menos tráfico de jugadores.
  - **Cámaras Selladas:** Requieren llaves/códigos, loot épico.
- **Loot principal:** Artefactos, Rare Components, Advanced Medical
- **Peligro:** VARIABLE (depende de eventos)

### 5. STELLA MONTIS (Montaña Estelar)
- **Tipo:** Zona montañosa de investigación
- **Ambiente:** Terreno elevado, bases científicas, cuevas naturales
- **Puntos de Interés (POIs):**
  - **Estación de Investigación Alpha:** Electrónica, datos científicos, chips.
  - **Cuevas Cristalinas:** Minerales raros, buen escondite.
  - **Antenas de Comunicación:** Vista panorámica (sniper), componentes técnicos.
  - **Campamento Base Abandonado:** Suministros básicos, tela, comida.
- **Loot principal:** Research Data, Minerals, Electronics
- **Peligro:** BAJO-MEDIO (menos jugadores, más PvE)

---

## MATERIALES Y DÓNDE ENCONTRARLOS

### MATERIALES COMUNES
| Material | Mejor Ubicación | Contenedor/Fuente |
|----------|-----------------|-------------------|
| Metal Parts | Spaceport Hangares, Dam Turbinas | Cajas herramientas ROJAS |
| Cloth/Tela | Buried City Residenciales | Armarios, taquillas, maletas |
| Electronics | Buried City Metro, Spaceport Torre Control | Paneles servidor, cajas AZULES |
| Cables | Cualquier zona industrial | Paneles eléctricos en paredes |
| Gears/Engranajes | Dam Sala Turbinas, Spaceport | Maquinaria rota, motores |
| Plastic Parts | Buried City Centro Comercial | Cajas variadas |

### MATERIALES AVANZADOS
| Material | Mejor Ubicación | Notas |
|----------|-----------------|-------|
| ARC Cores | Buried City (Restos Titanes) | Dropea de Titanes ARC destruidos |
| Mod Components | The Blue Gate Labs, Dam Central | Para mejoras de armas Tier 3+ |
| Data Chips | Spaceport Torre, Stella Montis | Desbloquean blueprints |
| Synthetic Fabric | The Blue Gate, zonas difíciles | Armaduras avanzadas |
| Weapon Parts | Spaceport Barracones, Dam | Craftear armas |
| Gun Components | Spaceport, cajas militares | Partes internas de armas |

### CONSUMIBLES
| Item | Mejor Ubicación | Contenedor |
|------|-----------------|------------|
| Stims/Estimulantes | The Blue Gate Labs, Buried City | Cajas NARANJAS, botiquines pared |
| Medical Supplies | Buried City Metro, cualquier baño | Botiquines blancos con cruz |
| Ammo (Munición) | Spaceport Barracones, enemigos | Cajas verdes MILITARES |
| Grenades | Spaceport, Dam zonas militares | Cajas verdes, armeros |
| Batteries | Buried City Metro, Stella Montis | Paneles eléctricos |

---

## ARMAS PRINCIPALES

### RIFLES DE ASALTO
- **Tempest Rifle:** El estándar. Equilibrado. Crafteo: Metal Parts + Gun Components + Electronics
- **ARC Rifle:** Versión mejorada. Necesita ARC Cores.

### RIFLES DE PRECISIÓN
- **Marksman Rifle:** Para distancia. Busca en Spaceport.
- **Scout Rifle:** Más ligero, menos daño.

### ESCOPETAS
- **Scrap Shotgun:** Fácil de craftear, corto alcance brutal.
- **Combat Shotgun:** Más rara, mejor cadencia.

### PISTOLAS/SMGs
- **Sidearm:** Respaldo básico.
- **SMG Compacta:** Alta cadencia, crafteo medio.

### CUERPO A CUERPO
- **Machete:** Silencioso, para sigilo.
- **Pico/Hacha:** Más daño, más lento.

---

## ARMADURAS

| Tipo | Protección | Velocidad | Materiales |
|------|------------|-----------|------------|
| Light Armor | ⭐ | ⭐⭐⭐⭐⭐ | Cloth, básicos |
| Medium Armor | ⭐⭐⭐ | ⭐⭐⭐ | Metal Parts, Cloth, Gears |
| Heavy Armor | ⭐⭐⭐⭐⭐ | ⭐ | Mucho Metal, Synthetic Fabric, Rare |

---

## ENEMIGOS ARC (PvE)

| Enemigo | Peligro | Loot | Dónde aparece |
|---------|---------|------|---------------|
| ARC Ticks | ⭐ | Electronics básicos | TODOS los mapas |
| ARC Drones | ⭐⭐ | Electronics, Cables | Zonas abiertas, Spaceport |
| ARC Sentinels | ⭐⭐⭐ | Weapon Parts, Ammo | POIs importantes |
| ARC Heavies | ⭐⭐⭐⭐ | Components raros, Metal | Dam, Spaceport interior |
| ARC Titans | ⭐⭐⭐⭐⭐ | ARC CORES, loot épico | Buried City, Eventos |

---

## RUTAS DE FARMEO RECOMENDADAS

### FARM RÁPIDO DE METAL (15 min)
1. Spaceport → Entra por Hangar A
2. Revisa las 3 cajas rojas del hangar
3. Cruza a Almacén Logístico (2 cajas más)
4. Extrae por la salida sur

### FARM DE ELECTRÓNICA (20 min)
1. Buried City → Metro entrada norte
2. Baja al andén, revisa paneles de servidor
3. Sigue el túnel hasta Sala de Control (3-4 cajas azules)
4. Cuidado con Drones en el camino

### FARM SEGURO PARA PRINCIPIANTES
1. Stella Montis → Campamento Base
2. Loota el campamento (bajo riesgo)
3. Sube a Antenas si quieres más
4. Extrae rápido, no te arriesgues

### FARM DE ARC CORES (Alto Riesgo)
1. Buried City → Busca los Restos de Titán (marcados en mapa)
2. Lleva equipo anti-ARC
3. Mata Ticks/Drones que custodian
4. El Core está en el "cadáver" del Titán
5. Extrae INMEDIATAMENTE (todos van a por esto)

---

## CONSEJOS TÁCTICOS

1. **Extrae al 70% de inventario** - No seas codicioso.
2. **Escucha antes de entrar** - Los pasos se oyen, los Drones zumban.
3. **Los baños SIEMPRE tienen medicina** - Revísalos.
4. **Cajas rojas = mecánico, Azules = electrónico, Verdes = militar**.
5. **Los Titanes ARC hacen MUCHO ruido** - Úsalo para saber dónde están.
"""

# --- Gestión de Persistencia de API Key ---
ENV_FILE = ".env"

def load_api_key():
    """Intenta cargar la API KEY desde un archivo .env local."""
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r") as f:
            for line in f:
                if line.startswith("OPENAI_API_KEY="):
                    return line.strip().split("=", 1)[1]
    return None

def save_api_key(key):
    """Guarda la API KEY en un archivo .env local."""
    with open(ENV_FILE, "w") as f:
        f.write(f"OPENAI_API_KEY={key}")

# Configuración de la página
st.set_page_config(
    page_title="ARC Raiders Intel",
    page_icon="📡",
    layout="centered"
)

st.title("📡 ARC Raiders Intel & Chat")
st.markdown("Tu enlace de radio con la base. Pregunta por ubicaciones, loot, recetas o estrategias.")

# --- Configuración de API Key (Sidebar) ---
api_key = os.getenv("OPENAI_API_KEY") or load_api_key()

with st.sidebar:
    st.header("⚙️ Configuración")
    
    # Gestión de API Key
    if not api_key:
        st.warning("⚠️ API Key no detectada")
        input_key = st.text_input("OpenAI API Key:", type="password")
        if st.button("💾 Guardar Key"):
            if input_key.strip().startswith("sk-"):
                save_api_key(input_key.strip())
                st.success("Guardada. Recargando...")
                st.rerun()
            else:
                st.error("Formato inválido.")
    else:
        st.success("✅ Enlace seguro activo (API Key)")
        if st.button("🗑️ Desconectar (Borrar Key)"):
            if os.path.exists(ENV_FILE):
                os.remove(ENV_FILE)
            st.rerun()

    st.markdown("---")
    
    # Contexto Visual Opcional
    st.header("📸 Análisis Visual (Opcional)")
    uploaded_file = st.file_uploader("Sube inventario o mapa:", type=["png", "jpg", "jpeg"])
    
    st.markdown("---")
    if st.button("🗑️ Limpiar Conversación"):
        st.session_state.messages = []
        st.rerun()

if not api_key:
    st.info("👈 Por favor, configura tu API Key en la barra lateral para iniciar la transmisión.")
    st.stop()

client = OpenAI(api_key=api_key)

# --- Estado de la sesión (Historial del Chat) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Funciones de utilidad ---
def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

# --- Mostrar Historial de Chat ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Input de Chat ---
if prompt := st.chat_input("Ej: ¿Dónde encuentro 'Tempest Rifle parts'? o 'Analiza mi inventario'"):
    
    # 1. Mostrar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Generar respuesta de la IA
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # SYSTEM PROMPT CON BÚSQUEDA WEB
            system_prompt = """Eres RAIDER-OP, un experto en ARC Raiders con acceso a internet en tiempo real.

INSTRUCCIONES:
1. SIEMPRE usa la herramienta de búsqueda web para encontrar información actualizada sobre ARC Raiders.
2. Busca en: arcraiders.wiki.gg, reddit.com/r/ARC_Raiders, mapgenie.io/arc-raiders, guías de YouTube, etc.
3. Da respuestas ESPECÍFICAS con nombres de mapas, POIs exactos, coordenadas si las hay.
4. Si el usuario pregunta por un objeto, busca dónde encontrarlo EXACTAMENTE.
5. Responde siempre en ESPAÑOL.
6. Cita las fuentes cuando sea relevante.
"""
            
            # Construir el input para la API de Responses
            input_messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            # Añadir historial
            for msg in st.session_state.messages[:-1]:
                input_messages.append({"role": msg["role"], "content": msg["content"]})
            
            # Añadir mensaje actual
            user_query = f"Busca información sobre ARC Raiders para responder esta pregunta: {prompt}"
            
            # Si hay imagen, usamos formato especial
            if uploaded_file:
                base64_image = encode_image(uploaded_file)
                input_messages.append({
                    "role": "user", 
                    "content": [
                        {"type": "input_text", "text": user_query},
                        {"type": "input_image", "image_url": f"data:image/jpeg;base64,{base64_image}"}
                    ]
                })
                st.toast("Imagen adjuntada al análisis.", icon="📸")
            else:
                input_messages.append({"role": "user", "content": user_query})

            # Llamada a la API con búsqueda web habilitada
            response = client.responses.create(
                model="gpt-4o",
                tools=[{"type": "web_search_preview"}],
                input=input_messages,
            )
            
            # Extraer el texto de la respuesta
            full_response = ""
            for item in response.output:
                if item.type == "message":
                    for content in item.content:
                        if content.type == "output_text":
                            full_response = content.text
                            break
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"Error de conexión: {e}")
