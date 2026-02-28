# Volunet - Plataforma de Voluntariado Digital y Crowdfunding

Volunet (Tesis-V2) es una plataforma web desarrollada en Django diseñada para conectar a personas y comunidades que necesitan ayuda con voluntarios y donantes dispuestos a brindar apoyo, ya sea mediante tiempo, conocimientos o aportes economicos.

La aplicacion combina funciones de gestion de voluntarios con un sistema de recaudacion de fondos (crowdfunding), ofreciendo un entorno digital seguro y transparente.

---

## Caracteristicas Principales

### Usuarios y Autenticacion
* **Acceso basado en correo:** Registro e inicio de sesion fluido usando correo electronico.
* **Verificacion de Identidad (KYC):** Sistema de seguridad para prevenir fraudes mediante la carga de documentos de identidad y fotografias de verificacion.
* **Gamificacion:** Los voluntarios acumulan puntaje basado en su nivel de participacion y aportes a las causas finalizadas.

### Solicitudes de Ayuda (Crowdfunding y Voluntariado)
* **Creacion y Categorizacion:** Los usuarios pueden publicar iniciativas bajo distintas categorias (Salud, Educacion, Alimentos, entre otras).
* **Mapas Integrados:** Visualizacion del lugar de la ayuda usando Leaflet.
* **Seguimiento de Recaudacion:** Calculo en tiempo real del progreso hacia la meta economica, mostrando donantes activos.
* **Sistema de Evidencias:** Permite adjuntar documentacion de respaldo (archivos PDF e imagenes).

### Moderacion y Control 
Panel administrativo exclusivo para el equipo oficial de la plataforma:
* **Flujo de Aprobacion:** Las nuevas solicitudes ingresan en estado 'Pendiente' hasta ser revisadas manualmente (aprobar, rechazar o solicitar correcciones).
* **Supervision:** Monitoreo global de estadisticas de usuarios, donaciones y actividades recientes.

### Notificaciones y Correos
Integracion con la API de SendGrid (via django-anymail) para el envio de alertas transaccionales:
* Notificaciones automaticas a los usuarios sobre cambios de estado en sus proyectos.
* Alertas enviadas al equipo de administracion en eventos importantes.

---

## Tecnologias Empleadas

**Backend:**
* Python 3
* Django 5.x
* Base de Datos: SQLite3 (compatible con migracion a otras bases de datos relacionales).

**Frontend:**
* HTML5 y CSS nativo combinados con Bootstrap 5.
* Javascript y Leaflet.js para manejo de mapas interactivos.

**Seguridad y Optimizacion:**
* Integracion con python-dotenv para el aislamiento seguro de credenciales.
* Soluciones aplicadas sobre el ORM de Django (select_related y aggregate functions) para evitar exceso de consultas N+1 en las base de datos.

---

## Despliegue en Entorno de Desarrollo Local

Instrucciones para instalar y probar la plataforma localmente:

1. **Clona el repositorio**
   ```bash
   git clone https://github.com/ffrancoa2/Volunet_Tesis.git
   cd Volunet
   ```

2. **Crea y activa el entorno virtual**
   ```bash
   python -m venv venv
   
   # En Windows:
   venv\Scripts\activate
   # En macOS/Linux:
   source venv/bin/activate
   ```

3. **Configura las variables de entorno (.env)**
   Crea un archivo llamado `.env` en la misma carpeta donde se ubica `manage.py` o dentro del directorio principal del proyecto, incluyendo:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   # SENDGRID_API_KEY=SG.tu-key-aqui
   DEFAULT_FROM_EMAIL=tu_correo@ejemplo.com
   ADMIN_EMAIL=admin_correo@ejemplo.com
   ```

4. **Instala las dependencias necesarias**
   Aprovecha el archivo incluido `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

5. **Prepara y ejecuta la base de datos**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Inicia el servidor local**
   ```bash
   python manage.py runserver
   ```
   Accede a la aplicacion desde tu navegador en: http://127.0.0.1:8000/

---

## Estructura de la Aplicacion

El proyecto se divide internamente en las siguientes aplicaciones de Django:

* **/users**: Control del modelo personalizado de usuario, autenticacion y validacion KYC.
* **/volunteers**: Nucleo transaccional de la aplicacion (solicitudes, donaciones, participantes y roles).
* **/adminpanel**: Dashboard y vistas especificas para la moderacion del entorno.
* **/core**: Paginas generales (landing page), el dashboard principal del voluntario y logica transversal o de apoyo.
* **/Social**: Directorio raiz de la configuracion de Django.