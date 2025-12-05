"""
Descargador de tiles para ARC Raiders Maps
Descarga los tiles del CDN para uso local
"""

import os
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# Configuración
CDN_URL = "https://cdn.arcraidersmaps.app"
TILES_DIR = Path("tiles")

# Headers para simular navegador
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://arcraidersmaps.app/",
    "Origin": "https://arcraidersmaps.app",
    "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
}

# Mapas y sus configuraciones
# dam y spaceport usan {z}/{y}/{x}, los demás usan {z}/{x}/{y}
MAPS = {
    "dam": {
        "path": "/maps/dam/tiles",
        "format": "{z}/{y}/{x}",  # y,x order
        "maxNativeZoom": 4,
        "minZoom": 1,
    },
    "spaceport": {
        "path": "/maps/spaceport/tiles",
        "format": "{z}/{y}/{x}",  # y,x order
        "maxNativeZoom": 3,
        "minZoom": 1,
    },
    "buried-city": {
        "path": "/maps/buried-city-v3/tiles",
        "format": "{z}/{x}/{y}",  # x,y order
        "maxNativeZoom": 3,
        "minZoom": 1,
    },
    "blue-gate": {
        "path": "/maps/blue-gate-v2/tiles",
        "format": "{z}/{x}/{y}",  # x,y order
        "maxNativeZoom": 3,
        "minZoom": 1,
    },
    "stella-montis-l1": {
        "path": "/maps/stella-montis/layers/stella-montis-l1/tiles",
        "format": "{z}/{x}/{y}",
        "maxNativeZoom": 3,
        "minZoom": 1,
    },
    "stella-montis-l2": {
        "path": "/maps/stella-montis/layers/stella-montis-l2/tiles",
        "format": "{z}/{x}/{y}",
        "maxNativeZoom": 3,
        "minZoom": 1,
    },
}


def get_tile_count(zoom_level):
    """Obtener número de tiles por lado para un nivel de zoom"""
    return 2 ** zoom_level


def download_tile(url, local_path):
    """Descargar un tile individual"""
    try:
        if local_path.exists():
            return True, url, "exists"
        
        response = requests.get(url, headers=HEADERS, timeout=30)
        
        if response.status_code == 200:
            local_path.parent.mkdir(parents=True, exist_ok=True)
            with open(local_path, "wb") as f:
                f.write(response.content)
            return True, url, "downloaded"
        else:
            return False, url, f"HTTP {response.status_code}"
    except Exception as e:
        return False, url, str(e)


def download_map_tiles(map_id, map_config, max_workers=8):
    """Descargar todos los tiles de un mapa"""
    print(f"\n{'='*60}")
    print(f"📥 Descargando: {map_id}")
    print(f"{'='*60}")
    
    tasks = []
    
    for zoom in range(map_config["minZoom"], map_config["maxNativeZoom"] + 1):
        tiles_per_side = get_tile_count(zoom)
        print(f"  Zoom {zoom}: {tiles_per_side}x{tiles_per_side} = {tiles_per_side**2} tiles")
        
        for x in range(tiles_per_side):
            for y in range(tiles_per_side):
                # Construir URL según el formato del mapa
                if map_config["format"] == "{z}/{y}/{x}":
                    tile_path = f"{zoom}/{y}/{x}"
                else:
                    tile_path = f"{zoom}/{x}/{y}"
                
                url = f"{CDN_URL}{map_config['path']}/{tile_path}.webp"
                local_path = TILES_DIR / map_id / f"{zoom}" / f"{x}" / f"{y}.webp"
                
                tasks.append((url, local_path))
    
    print(f"  Total tiles a descargar: {len(tasks)}")
    
    downloaded = 0
    existed = 0
    failed = 0
    failed_urls = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(download_tile, url, path): (url, path) for url, path in tasks}
        
        for i, future in enumerate(as_completed(futures)):
            success, url, status = future.result()
            
            if success:
                if status == "exists":
                    existed += 1
                else:
                    downloaded += 1
            else:
                failed += 1
                failed_urls.append((url, status))
            
            # Progreso cada 50 tiles
            if (i + 1) % 50 == 0 or i + 1 == len(tasks):
                print(f"  Progreso: {i+1}/{len(tasks)} | ✅ {downloaded} descargados | 📁 {existed} existentes | ❌ {failed} fallidos")
    
    print(f"\n  ✅ Completado: {downloaded} descargados, {existed} ya existían, {failed} fallidos")
    
    if failed_urls and failed <= 10:
        print("  URLs fallidas:")
        for url, status in failed_urls[:10]:
            print(f"    - {url}: {status}")
    
    return downloaded, existed, failed


def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║          ARC RAIDERS - DESCARGADOR DE TILES                  ║
║                                                              ║
║  Descarga los tiles de mapas desde cdn.arcraidersmaps.app    ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Crear directorio de tiles
    TILES_DIR.mkdir(exist_ok=True)
    
    # Mostrar mapas disponibles
    print("Mapas disponibles:")
    for i, (map_id, config) in enumerate(MAPS.items(), 1):
        zoom_range = f"zoom {config['minZoom']}-{config['maxNativeZoom']}"
        print(f"  {i}. {map_id} ({zoom_range})")
    
    print(f"\n  0. Descargar TODOS los mapas")
    print(f"  q. Salir\n")
    
    choice = input("Selecciona una opción: ").strip().lower()
    
    if choice == 'q':
        print("Cancelado.")
        return
    
    if choice == '0':
        # Descargar todos
        maps_to_download = list(MAPS.items())
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(MAPS):
                map_id = list(MAPS.keys())[idx]
                maps_to_download = [(map_id, MAPS[map_id])]
            else:
                print("Opción inválida")
                return
        except ValueError:
            print("Opción inválida")
            return
    
    total_downloaded = 0
    total_existed = 0
    total_failed = 0
    
    start_time = time.time()
    
    for map_id, config in maps_to_download:
        downloaded, existed, failed = download_map_tiles(map_id, config)
        total_downloaded += downloaded
        total_existed += existed
        total_failed += failed
    
    elapsed = time.time() - start_time
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                    RESUMEN FINAL                             ║
╠══════════════════════════════════════════════════════════════╣
║  ✅ Tiles descargados:  {total_downloaded:>6}                             ║
║  📁 Ya existentes:      {total_existed:>6}                             ║
║  ❌ Fallidos:           {total_failed:>6}                             ║
║  ⏱️  Tiempo total:       {elapsed:.1f}s                              ║
║                                                              ║
║  📂 Tiles guardados en: {str(TILES_DIR.absolute()):>35} ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    if total_downloaded > 0 or total_existed > 0:
        print("✅ ¡Listo! Ahora puedes usar arc_maps_app.py con tiles locales.")


if __name__ == "__main__":
    main()
