# 🏫 Sistema de Monitoreo Inteligente para Salones — UAM Azcapotzalco

Este proyecto presenta una plataforma web desarrollada en **Python** que permite monitorear en tiempo real las **condiciones ambientales** y la **afluencia de personas** en salones de clase, integrando sensores IoT, visualizaciones interactivas y generación automática de reportes PDF.

> 📍 Proyecto realizado como parte del **Servicio Social en el Laboratorio de Procesamiento de Lenguaje Natural e IoT** (UAM Azcapotzalco)  
> 📅 Periodo: Abril 2024 – Septiembre 2025

---

## 🧭 Tabla de Contenidos

- [🚀 Características](#-características)  
- [📸 Vista Previa](#-vista-previa)  
- [🧱 Arquitectura](#-arquitectura)  
- [⚙️ Requisitos](#️-requisitos)  
- [📝 Instalación y Ejecución](#-instalación-y-ejecución)  
- [🌐 Estructura de la App](#-estructura-de-la-app)  
- [📄 Generación de Reportes](#-generación-de-reportes)  
- [👩‍🏫 Módulo de Profesores](#-módulo-de-profesores)  
- [☁️ Despliegue](#️-despliegue)  
- [🧪 Tecnologías Usadas](#-tecnologías-usadas)  
- [📝 Licencia y Créditos](#-licencia-y-créditos)

---

## 🚀 Características

- 🌡️ **Monitoreo en tiempo real** de temperatura, humedad e iluminación por salón.  
- 👤 **Identificación automática** de profesores mediante RFID y reconocimiento facial.  
- 📊 **Dashboards interactivos** construidos con Streamlit y Plotly.  
- 🧾 **Reportes PDF automáticos** generados dinámicamente con PyLaTeX.  
- 🧰 **Backend optimizado** con SQLAlchemy y arquitectura Modelo–Vista–Controlador.  
- 📅 Itinerarios por profesor y visualización histórica de condiciones.  
- 🧼 Limpieza automática de archivos generados para evitar sobrecarga.

---

## 📸 Vista Previa

**Dashboard principal**  
Muestra gráficos poligonales y de pastel sobre uso de salones, visitas y condiciones ambientales.

```
Pestaña Dashboard → Selección por Edificio / Salón / Rango de fechas
 ├─ Gráficas de visitas por día y por profesor
 ├─ Historial de condiciones atmosféricas
 └─ Control de actualizaciones eficiente
```

**Itinerario de profesores**  
Consulta de historial de visitas, preferencias ambientales y actualización interactiva.

**Reportes automáticos**  
Generación de informes PDF personalizables por rango de tiempo (30, 90, 180 días).

---

## 🧱 Arquitectura

```text
📂 dashboardUAM/
├── main.py              # Vista principal (Streamlit UI)
├── bd.py                # Conexión a la base de datos (Modelo)
├── graficas.py          # Generación de gráficos dinámicos (Modelo)
├── graLc.py             # Gráficos de condiciones → imágenes
├── graLv.py             # Gráficos de visitas → imágenes
├── graP.py              # Gráficos de pastel → imágenes
├── reportes.py          # Generación de PDF vía LaTeX (Modelo)
├── profesores.py        # Interacción con datos de profesores (Modelo)
├── img/                 # Carpeta de imágenes generadas (poligonales, pastel, tablas)
└── reports/             # Reportes PDF generados
```

La arquitectura sigue el patrón **Modelo–Vista–Controlador (MVC)**:

- **Modelo:** `bd.py`, `graficas.py`, `reportes.py`, `profesores.py`  
- **Vista:** `main.py` (Streamlit UI)  
- **Controlador:** integración mediante llamadas entre scripts y subprocesos

---

## ⚙️ Requisitos

- Python ≥ 3.9  
- [Streamlit](https://streamlit.io/)  
- [Plotly](https://plotly.com/)  
- [Pandas](https://pandas.pydata.org/)  
- [SQLAlchemy](https://www.sqlalchemy.org/)  
- [PyLaTeX](https://pypi.org/project/PyLaTeX/)  

Instalar dependencias:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## 📝 Instalación y Ejecución

1️⃣ Clona el repositorio:

```bash
git clone https://github.com/diegoRM666/dashboardUAM.git
cd dashboardUAM
```

2️⃣ Instala dependencias:

```bash
python -m pip install -r requirements.txt
```

3️⃣ Inicia la aplicación:

```bash
cd logic
streamlit run main.py
```

4️⃣ Accede desde tu navegador (por defecto: http://localhost:8501)

> Asegúrate de que la máquina esté en la misma red que los sensores y la base de datos.

---

## 🌐 Estructura de la App

### 🧭 Pestaña “Dashboard”
- Selección por salón, edificio y rango de fechas.  
- Actualización eficiente si no ha cambiado la data.  
- Gráficos de visitas (profesor/día) y condiciones ambientales.

### 👨‍🏫 Pestaña “Itinerario Profesor”
- Lista desplegable de profesores.  
- Consulta de preferencias atmosféricas y visitas.  
- Actualización de preferencias (temperatura, humedad, iluminación).

### 🧾 Pestaña “Reportes”
- Generación de reportes PDF en 3 rangos:
  - 30 días
  - 90 días
  - 180 días  
- Incluye limpieza automática de imágenes previas y generación paralela de gráficos.

---

## 📄 Generación de Reportes

La función `reportes.py`:
- Limpia carpetas de imágenes y reportes anteriores.  
- Genera gráficos por salón/edificio mediante subprocesos (`graP.py`, `graLv.py`, `graLc.py`).  
- Ensambla el documento LaTeX con el contenido generado.  
- Compila automáticamente el PDF final.

Los reportes incluyen:
- Historial de visitas
- Condiciones ambientales promedio
- Uso por profesor y día

---

## 👩‍🏫 Módulo de Profesores

El script `profesores.py` permite:
- Consultar lista de profesores y sus itinerarios.  
- Ver preferencias ambientales actuales.  
- Modificarlas manualmente o restaurarlas a valores normativos (NMX-C-7730-ONNCCE-2018, NOM-025-STPS-2008).

---

## ☁️ Despliegue

Puedes desplegar esta plataforma de varias formas:

- 🖥️ **Local / Intranet:** ejecutar con `streamlit run`.  
- ☁️ **En la nube (AWS, Azure, GCP):** desplegar la app y la base de datos para acceso remoto.  
- 🐳 **Contenedores Docker:** separar backend y frontend para mantenimiento y escalabilidad.

---

## 🧪 Tecnologías Usadas

| Tecnología     | Uso Principal                                               |
|---------------|--------------------------------------------------------------|
| **Python**    | Lenguaje base del proyecto                                  |
| **Streamlit** | Frontend web interactivo                                    |
| **Plotly**    | Gráficos interactivos y estáticos                             |
| **Pandas**    | Procesamiento y análisis de datos tabulares                   |
| **SQLAlchemy**| Conexión y abstracción de base de datos                       |
| **PyLaTeX**   | Generación automatizada de reportes en PDF                    |
| **Threading** | Aceleración de gráficos en paralelo                           |

---

## 📝 Licencia y Créditos

📄 Proyecto académico — Universidad Autónoma Metropolitana, Unidad Azcapotzalco  
👨‍💻 **Autor:** [Diego Ruiz Mora](https://github.com/diegoRM666)  
👨‍🏫 **Supervisor:** Dr. Leonardo Daniel Sánchez Martínez  
📹 [Manual en video](https://youtu.be/DIyoBysRb3c)
