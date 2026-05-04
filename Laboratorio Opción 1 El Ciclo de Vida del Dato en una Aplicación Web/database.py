import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('incidencias.db')
    cursor = conn.cursor()
    
    # Estructura con categorización (Tarea 2)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS incidencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            categoria TEXT CHECK(categoria IN ('A', 'B')) NOT NULL,
            email TEXT NOT NULL,
            fecha TEXT NOT NULL,
            estado TEXT DEFAULT 'Pendiente'
        )
    ''')
    conn.commit()
    conn.close()

def add_incidencia(data):
    conn = sqlite3.connect('incidencias.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO incidencias (titulo, descripcion, categoria, email, fecha)
        VALUES (?, ?, ?, ?, ?)
    ''', (data['titulo'], data['descripcion'], data['categoria'], 
          data['email'], data['fecha']))
    conn.commit()
    conn.close()

def get_incidencias():
    conn = sqlite3.connect('incidencias.db')
    cursor = conn.cursor()
    # TAREA 2: Consulta SQL que filtra Críticas
    cursor.execute('''
        SELECT * FROM incidencias 
        ORDER BY fecha DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_stats():
    conn = sqlite3.connect('incidencias.db')
    cursor = conn.cursor()
    
    # TAREA 3: Métricas oportunas
    cursor.execute("SELECT COUNT(*) FROM incidencias WHERE fecha LIKE ?", 
                   (datetime.now().strftime('%Y-%m-%d') + '%',))
    pendientes_hoy = cursor.fetchone()[0]
    
    cursor.execute('''
        SELECT AVG(
            julianday('now') - julianday(fecha) * 24
        ) FROM incidencias WHERE estado = 'Pendiente'
    ''')
    tiempo_promedio = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT COUNT(*) FROM incidencias WHERE categoria = 'A'")
    criticas = cursor.fetchone()[0]
    
    conn.close()
    return {
        'pendientes_hoy': pendientes_hoy,
        'tiempo_promedio_hrs': round(tiempo_promedio, 1),
        'total_criticas': criticas
    }