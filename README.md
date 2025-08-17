# 🎮 API de Videojuegos con FastAPI y MongoDB  

## 📌 Descripción  
Este proyecto implementa un CRUD de **videojuegos** y **usuarios** en FastAPI con MongoDB.  
Incluye:  
- Registro de usuarios con contraseñas **hasheadas**.  
- Inicio de sesión (login).  
- CRUD de videojuegos.  
- Búsqueda avanzada por **nombre, plataforma, género y precio**.  

---

## 🚀 Instalación  

```bash
git clone <repo_url>
cd api_videojuegos
pip install -r requirements.txt
```

---

Crea y activa un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux / Mac
   venv\Scripts\activate      # Windows
   ```

---


Configura tu archivo `.env`:  

```env
MONGO_URI="mongodb+srv://<usuario>:<password>@<cluster>.mongodb.net/"
DB_NAME="videojuegos_db"
```

Ejecuta el servidor:  

```bash
uvicorn main:app --reload
```

---

## 📂 Rutas principales  

### 👤 Usuarios  
- `POST /usuarios/` → Crear usuario  
- `POST /usuarios/login` → Login  
- `GET /usuarios/` → Listar usuarios  

### 🎮 Videojuegos  
- `POST /videojuegos/` → Crear videojuego  
- `GET /videojuegos/` → Listar videojuegos  
- `GET /videojuegos/search?nombre=Halo&plataforma=Xbox` → Buscar videojuegos  
- `PUT /videojuegos/{id}` → Actualizar videojuego  
- `DELETE /videojuegos/{id}` → Eliminar videojuego  

---


## 🔐 Seguridad
- Las contraseñas se **encriptan con bcrypt** usando `passlib`.
- El login compara el `password` ingresado con el hash almacenado.


## 🔎 Ejemplos en Thunder Client  

Importa la colección incluida en el archivo:  
📂 `API_Videojuegos_ThunderClient.json`

### 1. Crear usuario  
**POST** `http://127.0.0.1:8000/usuarios/`  
```json
{
  "nombre": "Xname",
  "email": "Xn123@email.com",
  "password": "123456"
}
```

### 2. Login usuario  
**POST** `http://127.0.0.1:8000/usuarios/login`  
```json
{
  "email": "Xn123@email.com",
  "password": "123456"
}
```

### 3. Crear videojuego  
**POST** `http://127.0.0.1:8000/videojuegos/`  
```json
{
  "nombre": "Halo Infinite",
  "plataforma": "Xbox",
  "precio": 59.99,
  "genero": "Shooter"
}
```

---

La API estará disponible en:  
👉 `http://127.0.0.1:8000`  
👉 Documentación interactiva: `http://127.0.0.1:8000/docs`


### 4. Buscar videojuegos  
**GET** `http://127.0.0.1:8000/videojuegos/search?nombre=Halo&plataforma=Xbox`

---

## Próximos pasos  
- [ ] Implementar autenticación con JWT.  
- [ ] Proteger rutas de videojuegos solo para usuarios logueados.  
