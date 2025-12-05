# 🗺️ ARC Raiders Maps - Interactive Tools

Herramientas interactivas para explorar mapas y encontrar items en ARC Raiders.

## 📱 Aplicaciones disponibles

### 1. `arc_maps_chat.py` - Chatbot básico (Sin API key) 🆓
Búsqueda inteligente de items y ubicaciones **sin necesidad de API keys**.

**Características:**
- ✅ Búsqueda de items por nombre/tipo
- ✅ Traducción ES → EN automática
- ✅ Sugerencias de ubicaciones en mapas
- ✅ Búsquedas rápidas predefinidas
- ✅ **100% gratuito** - no requiere configuración

**Ejecutar:**
```bash
streamlit run arc_maps_chat.py
```

---

### 2. `arc_maps_pro.py` - Versión PRO con IA 🤖
Asistente conversacional con ChatGPT y conocimiento profundo del juego.

**Características:**
- 🤖 Chat IA con contexto del juego (457+ items)
- 🔨 Sistema de crafteo inteligente
- ⚡ Sugerencias de rutas de farmeo
- 📊 Análisis de items y ubicaciones
- 💾 Historial de conversación
- 🎯 Recomendaciones personalizadas por mapa

**Configuración:**

**Opción A - Archivo .env (local):**
```bash
# Crear archivo .env
echo "OPENAI_API_KEY=sk-tu-clave-aqui" > .env
streamlit run arc_maps_pro.py
```

**Opción B - Streamlit Cloud:**
1. Deploy en https://share.streamlit.io
2. Settings > Secrets
3. Agregar:
```toml
OPENAI_API_KEY = "sk-tu-clave-aqui"
```

**Obtener API Key:**
- Ve a: https://platform.openai.com/api-keys
- Crea una nueva clave secreta
- Costo: ~$0.01-0.05 por 100 mensajes (modelo gpt-4o-mini)

---

## 🚀 Deploy a producción

### Opción 1: Streamlit Cloud (Recomendado - GRATIS)

**Para `arc_maps_chat.py` (sin IA):**
1. Ve a https://share.streamlit.io
2. Conecta: `PublicMeta/arc-raiders-maps`
3. Main file: `arc_maps_chat.py`
4. Deploy ✅

**Para `arc_maps_pro.py` (con IA):**
1. Mismos pasos anteriores
2. Main file: `arc_maps_pro.py`
3. Settings > Secrets > Pegar `OPENAI_API_KEY`
4. Deploy ✅

### Opción 2: Render / Railway / Hugging Face
Ver instrucciones en `README_DEPLOY.md`

---

## 📦 Instalación local

```bash
# Clonar repositorio
git clone https://github.com/PublicMeta/arc-raiders-maps.git
cd arc-raiders-maps

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar versión básica (sin IA)
streamlit run arc_maps_chat.py

# O versión PRO (con IA - requiere .env)
streamlit run arc_maps_pro.py
```

---

## 🔍 Comparación de versiones

| Característica | Chat Básico | PRO con IA |
|----------------|-------------|------------|
| Búsqueda de items | ✅ | ✅ |
| Mapas interactivos | ✅ | ✅ |
| Traducción ES/EN | ✅ | ✅ |
| Chat conversacional | ❌ | ✅ |
| Rutas de farmeo | ❌ | ✅ |
| Sistema de crafteo | ❌ | ✅ |
| API Key necesaria | ❌ | ✅ OpenAI |
| Costo | 🆓 Gratis | ~$0.01/100 msgs |

---

## 📁 Estructura del proyecto

```
arc-raiders-maps/
├── arc_maps_chat.py        # Versión básica (sin IA)
├── arc_maps_pro.py          # Versión PRO (con IA)
├── items_data.json          # Base de datos (457+ items)
├── requirements.txt         # Dependencias Python
├── .streamlit/
│   ├── config.toml          # Configuración de tema
│   └── secrets.toml.example # Ejemplo de secretos
├── README.md                # Este archivo
└── README_DEPLOY.md         # Guía de despliegue
```

---

## 🌐 Mapas incluidos

- **Dam Battlegrounds** - 11 POIs
- **The Spaceport** - 6 POIs  
- **Buried City** - 7 POIs

Iframe desde: `https://arcraidersmaps.app/`

---

## 🔧 Tecnologías

- **Streamlit** - Framework web Python
- **OpenAI GPT-4o-mini** - Chat IA conversacional (solo PRO)
- **Python 3.8+** - Lenguaje de programación

---

## 📝 Licencia

Proyecto open source para la comunidad de ARC Raiders.

**Contribuciones bienvenidas:** Issues y PRs en GitHub
