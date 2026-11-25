# Laboratorio de Seguridad de la Información (Entorno Académico Local)

Este proyecto proporciona un entorno local interactivo desarrollado en **Python (Flask)** y **SQLite** para analizar de forma práctica y comparativa fallos comunes de validación de entradas y las técnicas defensivas correspondientes (OWASP).

---

## 🚀 Requisitos Previos e Instalación

1. Asegúrate de tener instalado Python 3 (3.8 o superior).
2. Instala las dependencias del proyecto ejecutando:

```bash
pip install -r requirements.txt
```

---

## 🛠️ Ejecución de la Aplicación

Inicia el servidor local de desarrollo ejecutando:

```bash
python app.py
```

Una vez iniciado, abre tu navegador web en la dirección:
👉 **`http://127.0.0.1:5000`**

---

## 📚 Estructura de los Módulos

El laboratorio incluye dos escenarios interactivos con alternancia en vivo entre modo **Vulnerable** y modo **Seguro**:

### 1. Inyección SQL (SQLi) - `/sqli`
* **Modo Vulnerable:** Muestra cómo una consulta que concatena texto del usuario permite alterar la sintaxis lógica de la base de datos.
* **Modo Seguro:** Utiliza *Prepared Statements* (parámetros `?`), asegurando que cualquier entrada sea tratada exclusivamente como un valor literal.
* **Inspección en vivo:** Permite visualizar exactamente la sentencia SQL generada en el servidor y cómo reacciona el motor de base de datos.

### 2. Cross-Site Scripting (XSS) - `/xss`
* **Modo Vulnerable:** Demuestra cómo la falta de codificación en las respuestas web permite la inyección de elementos en el DOM.
* **Modo Seguro:** Aplica codificación contextual de entidades HTML (`html.escape`) para que el navegador trate los caracteres especiales como texto plano.
* **Inspección en vivo:** Muestra el código HTML exacto entregado al navegador para comparar la representación cruda frente a la escapada.

---

## 🛡️ Contramedidas Generales Recomendadas (OWASP)
1. **Validación estricta de entradas:** Comprobar tipo, formato y longitud antes de procesar los datos.
2. **Consultas parametrizadas:** Evitar en cualquier circunstancia la concatenación de cadenas en drivers de bases de datos.
3. **Codificación contextual de salidas (Output Encoding):** Escapar caracteres reservados de HTML, JavaScript y CSS antes de representarlos.
4. **Cabeceras de protección:** Implementar políticas de seguridad como *Content Security Policy (CSP)* en servidores de producción.
