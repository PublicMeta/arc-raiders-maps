# 🚀 Guía de Despliegue - ARC Raiders Maps

## ¿Qué versión desplegar?

### `arc_maps_chat.py` - Versión Básica 🆓
✅ **Recomendado para empezar**
- Sin costo
- Sin configuración
- Deploy en 2 minutos

### `arc_maps_pro.py` - Versión PRO 🤖
- Requiere API key de OpenAI
- Costo: ~$0.01-0.05 por 100 mensajes
- Deploy en 5 minutos

---

## Opción 1: Streamlit Cloud (GRATIS - Recomendado)

### A) Desplegar versión BÁSICA (sin IA)

1. **Prepara el repositorio:**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Ve a [share.streamlit.io](https://share.streamlit.io)**

3. **Inicia sesión con GitHub**

4. **Click en "New app"**

5. **Configura:**
   - Repository: `PublicMeta/arc-raiders-maps`
   - Branch: `main`
   - Main file: `arc_maps_chat.py` ← básica
   - App URL: `arc-raiders-maps` (o tu preferencia)

6. **Click "Deploy"** 🎉

**Tu app estará en:** `https://publicmeta-arc-raiders-maps.streamlit.app`

---

### B) Desplegar versión PRO (con IA)

**Paso adicional: Configurar secretos**

1. Sigue los pasos 1-5 anteriores, pero en paso 5 usa:
   - Main file: `arc_maps_pro.py` ← PRO

2. **Antes de Deploy, configura secretos:**
   - Click en "Advanced settings"
   - En "Secrets" pega:
   ```toml
   OPENAI_API_KEY = "sk-tu-clave-real-aqui"
   ```

3. **Obtener API Key de OpenAI:**
   - Ve a: https://platform.openai.com/api-keys
   - Crea cuenta (requiere tarjeta)
   - "Create new secret key"
   - Copia la clave (empieza con `sk-...`)
   - Pégala en Streamlit Secrets

4. **Click "Deploy"** 🎉

---

## Opción 2: Render.com

1. **Ve a [render.com](https://render.com) y crea cuenta**

2. **New > Web Service**

3. **Conecta tu repositorio de GitHub**

4. **Configura:**
   - Name: `arc-raiders-maps`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   
   **Para versión básica:**
   - Start Command: `streamlit run arc_maps_chat.py --server.port=$PORT --server.address=0.0.0.0`
   
   **Para versión PRO:**
   - Start Command: `streamlit run arc_maps_pro.py --server.port=$PORT --server.address=0.0.0.0`
   - Environment Variables: 
     - `OPENAI_API_KEY` = `sk-tu-clave-aqui`

5. **Create Web Service**

---

## Opción 3: Hugging Face Spaces

1. **Ve a [huggingface.co/spaces](https://huggingface.co/spaces)**

2. **Create new Space:**
   - Space name: `arc-raiders-maps`
   - License: `MIT`
   - SDK: `Streamlit`
   - Visibility: `Public`

3. **Sube archivos:**
   - `arc_maps_chat.py` o `arc_maps_pro.py`
   - `items_data.json`
   - `requirements.txt`
   - `.streamlit/config.toml`

4. **Para versión PRO:**
   - Settings > Variables
   - Add: `OPENAI_API_KEY` = `sk-...`

5. **Automáticamente se despliega** ✅

---

## Opción 4: Railway.app

1. **Ve a [railway.app](https://railway.app)**

2. **New Project > Deploy from GitHub**

3. **Selecciona tu repositorio**

4. **Add variables (solo versión PRO):**
   - `OPENAI_API_KEY` = `sk-...`

5. **Deploy automático** ✅

---

## Verificación antes de desplegar

### Checklist versión BÁSICA:
- ✅ `arc_maps_chat.py` existe
- ✅ `items_data.json` existe  
- ✅ `requirements.txt` tiene `streamlit`
- ✅ Código funciona localmente: `streamlit run arc_maps_chat.py`
- ✅ No hay archivos sensibles (.env en .gitignore)

### Checklist versión PRO:
- ✅ Todo lo anterior
- ✅ `arc_maps_pro.py` existe
- ✅ `requirements.txt` tiene `streamlit`, `openai`, `requests`
- ✅ Tienes API key de OpenAI
- ✅ Secretos configurados correctamente

---

## Solución de problemas

### ❌ "Module 'openai' not found"
**Solución:** Verifica que `requirements.txt` incluya:
```
streamlit
openai
python-dotenv
requests
```

### ❌ "OPENAI_API_KEY not configured"
**Solución:**
- **Streamlit Cloud:** Settings > Secrets > Pegar TOML
- **Render/Railway:** Environment Variables
- **Local:** Crear archivo `.env`

### ❌ "File 'items_data.json' not found"
**Solución:** 
```bash
git add items_data.json
git commit -m "Add items database"
git push origin main
```

### ❌ App muy lenta
**Causas:**
- Plan gratuito tiene recursos limitados
- Búsqueda web puede tomar tiempo

**Soluciones:**
- Usar `@st.cache_data` en funciones pesadas
- Limitar historial de chat (ya implementado: 6 mensajes)
- Usar versión básica si no necesitas IA

### ❌ Error de API de OpenAI
**Causas:**
- API key inválida
- Sin créditos en cuenta OpenAI
- Rate limit excedido

**Soluciones:**
- Verifica key en https://platform.openai.com/api-keys
- Revisa billing: https://platform.openai.com/account/billing
- Espera 1 minuto si hay rate limit

---

## Compartir tu app

Una vez desplegada:

**Versión básica:**
```
🔗 https://publicmeta-arc-raiders-maps.streamlit.app
📱 Compatible con móviles
🆓 Gratis para siempre
```

**Versión PRO:**
```
🔗 https://publicmeta-arc-raiders-maps-pro.streamlit.app
🤖 Con asistente IA
💰 Costo mínimo (~$1-5/mes uso normal)
```

---

## Actualizar app desplegada

Cualquier cambio que hagas localmente se auto-despliega:

```bash
git add .
git commit -m "Mejoras en búsqueda"
git push origin main
# Streamlit Cloud se actualiza automáticamente en 1-2 min
```

---

## Monitoreo y Analytics

### Streamlit Cloud:
- Dashboard > Analytics
- Ver visitas, errores, uso de recursos

### Costos OpenAI (versión PRO):
- https://platform.openai.com/usage
- Modelo usado: `gpt-4o-mini`
- Costo típico: $0.15 por 1M tokens input
- ~100 mensajes = $0.01-0.05

---

## Preguntas frecuentes

**¿Puedo tener ambas versiones desplegadas?**
Sí, crea 2 apps en Streamlit Cloud con diferentes archivos main.

**¿Cuánto cuesta OpenAI?**
Modelo gpt-4o-mini: ~$0.15/$0.60 por millón de tokens (input/output).
Uso normal: $1-5/mes.

**¿Hay límite de usuarios en Streamlit Cloud?**
Plan gratuito: recursos compartidos, puede ser lento con muchos usuarios simultáneos.

**¿Puedo usar otra IA en lugar de OpenAI?**
Sí, puedes modificar el código para usar: Anthropic Claude, Google Gemini, Llama local, etc.

---

## Recursos adicionales

- Streamlit docs: https://docs.streamlit.io
- OpenAI API: https://platform.openai.com/docs
- Community: https://discuss.streamlit.io
