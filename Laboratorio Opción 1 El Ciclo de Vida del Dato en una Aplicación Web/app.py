from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_mensajes' # Necesario para usar flash()

DATABASE = 'incidencias.db'

def init_db():
    """Crea la base de datos y la tabla de incidencias si no existen."""
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS incidencias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                categoria TEXT CHECK(categoria IN ('A', 'B')) NOT NULL,
                email TEXT NOT NULL,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                estado TEXT DEFAULT 'Pendiente',
                fecha_resolucion TIMESTAMP
            )
        ''')
        conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form', methods=['GET', 'POST'])
def form_incidencia():
    if request.method == 'POST':
        # 1. Capturar datos del formulario
        titulo = request.form.get('titulo')
        email = request.form.get('email')
        categoria = request.form.get('categoria')
        descripcion = request.form.get('descripcion')

        # --- CONTROL DE ENTRADA (Evitando el Ruido) ---
        if not descripcion or len(descripcion) < 10:
            flash('❌ Error: La descripción debe tener al menos 10 caracteres de información útil.', 'error')
            return render_template('form_incidencia.html', form_data=request.form)

        # 2. Guardar en SQLite (Información Íntegra)
        try:
            with sqlite3.connect(DATABASE) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO incidencias (titulo, descripcion, categoria, email) VALUES (?, ?, ?, ?)",
                    (titulo, descripcion, categoria, email)
                )
                conn.commit()
            flash('✅ Incidencia registrada con éxito.', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f'❌ Error al guardar: {e}', 'error')

    return render_template('form_incidencia.html')

@app.route('/resolve/<int:id>')
def resolve_incidencia(id):
    """PROCESAMIENTO: Transformar estado de Pendiente a Resuelto"""
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            ahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(
                "UPDATE incidencias SET estado = 'Resuelto', fecha_resolucion = ? WHERE id = ?",
                (ahora, id)
            )
            conn.commit()
        flash(f'✅ Incidencia #{id} marcada como resuelta.', 'success')
    except Exception as e:
        flash(f'❌ Error al actualizar: {e}', 'error')
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    """SALIDA: Reporte que cumple con Atributos de Calidad"""
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row # Para acceder por nombre de columna
        cursor = conn.cursor()
        
        # Consulta de incidencias
        cursor.execute("SELECT * FROM incidencias ORDER BY estado DESC, fecha DESC")
        incidencias = cursor.fetchall()

        # --- ATRIBUTO DE OPORTUNIDAD (KPIs en tiempo real) ---
        # 1. Pendientes de hoy
        cursor.execute("SELECT COUNT(*) FROM incidencias WHERE date(fecha) = date('now') AND estado = 'Pendiente'")
        pendientes_hoy = cursor.fetchone()[0]

        # 2. Total Críticas (Categorización estratégica)
        cursor.execute("SELECT COUNT(*) FROM incidencias WHERE categoria = 'A'")
        total_criticas = cursor.fetchone()[0]

        # 3. Tiempo promedio (para resueltos)
        cursor.execute("""
            SELECT AVG(
                (julianday(fecha_resolucion) - julianday(fecha)) * 24
            ) FROM incidencias WHERE estado = 'Resuelto' AND fecha_resolucion IS NOT NULL
        """)
        tiempo_promedio = cursor.fetchone()[0] or 0
        stats = {'pendientes_hoy': pendientes_hoy, 'total_criticas': total_criticas, 'tiempo_promedio_hrs': round(tiempo_promedio, 1)}
    
    return render_template('dashboard.html', incidencias=incidencias, stats=stats)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)