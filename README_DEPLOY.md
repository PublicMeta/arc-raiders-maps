# 🚀 Desplegar ARC Raiders Maps Chatbot

## Opción 1: Streamlit Cloud (Recomendado - GRATIS)

### Pasos:

1. **Sube tu código a GitHub** (si no lo has hecho):
   ```bash
   git add .
   git commit -m "Preparar para deploy"
   git push origin main
   ```

2. **Ve a [share.streamlit.io](https://share.streamlit.io)**

3. **Inicia sesión con GitHub**

4. **Click en "New app"**

5. **Configura:**
   - Repository: `PublicMeta/arc-raiders-maps`
   - Branch: `main`
   - Main file: `arc_maps_chat.py`

6. **Deploy!** 🎉

Tu app estará disponible en: `https://publicmeta-arc-raiders-maps.streamlit.app`

---

## Opción 2: Render (Alternativa gratuita)

1. Ve a [render.com](https://render.com)
2. Crea un nuevo "Web Service"
3. Conecta tu repositorio de GitHub
4. Configura:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run arc_maps_chat.py --server.port=$PORT --server.address=0.0.0.0`

---

## Opción 3: Hugging Face Spaces

1. Ve a [huggingface.co/spaces](https://huggingface.co/spaces)
2. Crea un nuevo Space tipo "Streamlit"
3. Sube tus archivos
4. Se desplegará automáticamente

---

## Verificar antes de desplegar

✅ `requirements.txt` tiene todas las dependencias
✅ `items_data.json` está en el repositorio
✅ No hay archivos sensibles (.env está en .gitignore)
✅ El código funciona localmente

---

## Solución de problemas

### Error: "Module not found"
- Verifica que `requirements.txt` tenga todas las librerías

### Error: "File not found"
- Asegúrate de usar rutas relativas o absolutas correctas
- Verifica que `items_data.json` esté en el repo

### La app es muy lenta
- Streamlit Cloud tiene recursos limitados en el plan gratuito
- Considera optimizar la búsqueda o usar caché

---

## Compartir tu app

Una vez desplegada, comparte el link:
- `https://tu-usuario-nombre-app.streamlit.app`
- Funciona en móviles y escritorio
- Sin necesidad de instalación para usuarios
