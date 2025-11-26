# 🚀 INSTRUCCIONES RÁPIDAS - Evently

## Para Profesores: Cómo Ejecutar el Proyecto

### ✅ Método Más Fácil (Recomendado): Con Docker

#### Requisitos Previos
1. Instalar **Docker Desktop**: https://www.docker.com/products/docker-desktop/
2. Abrir Docker Desktop y esperar a que esté corriendo

#### Pasos

1. **Abrir una terminal** (PowerShell en Windows, Terminal en Mac/Linux)

2. **Navegar a la carpeta del proyecto:**
   ```bash
   cd Evently
   ```

3. **Ejecutar el proyecto:**

   **En Windows (PowerShell):**
   ```powershell
   .\start.ps1
   ```
   
   **En Mac/Linux:**
   ```bash
   ./start.sh
   ```
   
   **O manualmente:**
   ```bash
   docker-compose up -d
   ```

4. **Esperar 2-5 minutos** mientras se descargan las imágenes y se inician los servicios

5. **Cargar los datos** (solo la primera vez):
   ```bash
   docker-compose exec backend python /data/scripts/load_from_csvs.py
   ```

6. **Abrir el navegador en:**
   - **Aplicación**: http://localhost:3000
   - **API**: http://localhost:8000
   - **Documentación**: http://localhost:8000/api/v1/docs

#### Para Detener el Proyecto
```bash
docker-compose down
```

---

### 🔧 Método Alternativo: Sin Docker

#### Requisitos Previos
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+

#### Pasos

**Terminal 1 - Backend:**
```bash
cd Evently/backend
python -m venv venv
# Windows:
.\venv\Scripts\Activate.ps1
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Terminal 2 - Cargar Datos:**
```bash
cd Evently/backend
# Activar venv (igual que arriba)
python ../data/scripts/load_from_csvs.py
```

**Terminal 3 - Frontend:**
```bash
cd Evently/frontend
npm install
npm run dev
```

**Abrir navegador en:** http://localhost:3000

---

### ❓ Problemas Comunes

**"Puerto 3000/8000 en uso":**
- Cierra otras aplicaciones que usen esos puertos
- O cambia los puertos en la configuración

**"Docker no funciona":**
- Asegúrate de que Docker Desktop esté corriendo
- Reinicia Docker Desktop

**"No se conecta a la base de datos":**
- Verifica que PostgreSQL esté corriendo
- Revisa el archivo `.env` en `backend/`

---

### 📞 ¿Necesitas Ayuda?

Revisa el archivo `README.md` para instrucciones más detalladas y solución de problemas.

