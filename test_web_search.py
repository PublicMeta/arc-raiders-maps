"""
Test de búsqueda web para arc_maps_pro.py
"""
import requests

def test_web_search():
    """Prueba la API de DuckDuckGo"""
    print("🔍 Probando búsqueda web con DuckDuckGo...\n")
    
    queries = [
        "ARC Raiders gameplay",
        "ARC Raiders weapons",
        "ARC Raiders release date"
    ]
    
    for query in queries:
        print(f"Query: {query}")
        try:
            url = "https://api.duckduckgo.com/"
            params = {
                "q": query,
                "format": "json",
                "no_html": 1,
                "skip_disambig": 1
            }
            response = requests.get(url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("Abstract"):
                    print(f"  ✅ Abstract: {data['Abstract'][:100]}...")
                else:
                    print(f"  ⚠️ No abstract")
                
                topics = data.get("RelatedTopics", [])
                print(f"  ℹ️ Related topics: {len(topics)}")
                
                for i, topic in enumerate(topics[:2]):
                    if isinstance(topic, dict) and topic.get("Text"):
                        print(f"    {i+1}. {topic['Text'][:80]}...")
            else:
                print(f"  ❌ Error: {response.status_code}")
        
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        print()

if __name__ == "__main__":
    test_web_search()
    print("✅ Test completado")
