# 🗺️ ARC Raiders Maps - Interactive Tools

Herramientas interactivas para explorar mapas y encontrar items en ARC Raiders.

## 📱 Aplicaciones disponibles

### 1. `arc_maps_chat.py` - Chatbot de búsqueda ⭐ RECOMENDADO
Búsqueda inteligente de items y ubicaciones **sin necesidad de API keys**.

**Características:**
- ✅ Búsqueda de items por nombre/tipo
- ✅ Traducción ES → EN automática
- ✅ Sugerencias de ubicaciones en mapas
- ✅ Búsquedas rápidas predefinidas
- ✅ **NO requiere configuración**

**Ejecutar:**
```bash
streamlit run arc_maps_chat.py
```

### 2. `arc_maps_pro.py` - Versión con ChatGPT
Incluye asistente de IA conversacional (requiere API key de OpenAI).

---

## 🚀 Deploy a producción

Para que otros usuarios accedan:

1. **Streamlit Cloud** (recomendado):
   - Ve a https://share.streamlit.io
   - Conecta este repositorio: `PublicMeta/arc-raiders-maps`
   - Selecciona `arc_maps_chat.py` como archivo principal
   - Deploy automático ✅

2. Ver instrucciones completas en `README_DEPLOY.md`

---

## 📦 Instalación local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar app (SIN IA)
streamlit run arc_maps_chat.py
```

---

## 📁 Archivos importantes

- `items_data.json` - Base de datos de 457+ items
- `arc_maps_chat.py` - App principal (sin IA) ⭐
- `arc_maps_pro.py` - App con ChatGPT
- `.streamlit/config.toml` - Configuración de tema
