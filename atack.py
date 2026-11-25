import socket
import threading
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
import urllib.request

_print_lock = threading.Lock()

def out(etiqueta, mensaje):
    # El lock evita que las líneas de varios hilos se mezclen al imprimir
    with _print_lock:
        print(f"[{etiqueta}] {mensaje}")

def consultar_servidor_local(url, numero):
    etiqueta = f"Consulta {numero}"
    out(etiqueta, f"=== Consultando ubicación y estado de: {url} ===\n")

    parsed = urlparse(url)
    hostname = parsed.hostname or "127.0.0.1"
    port = parsed.port or 5000

    # 1. Resolución de red y dirección IP
    try:
        ip = socket.gethostbyname(hostname)
        out(etiqueta, f"[*] Hostname: {hostname}")
        out(etiqueta, f"[*] Puerto: {port}")
        out(etiqueta, f"[*] Dirección IP: {ip}")

        if ip.startswith("127."):
            out(etiqueta, "[*] Ámbito de red: Loopback (Servidor Local en esta misma máquina)")
        else:
            out(etiqueta, "[*] Ámbito de red: Externa / Remota")
    except socket.gaierror as e:
        out(etiqueta, f"[!] Error al resolver el host: {e}")
        return

    # 2. Petición HTTP al servidor
    out(etiqueta, "[*] Enviando petición HTTP GET...")
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "ClienteDiagnostico/1.0"}
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            out(etiqueta, f"[+] Estado HTTP: {resp.status} {resp.reason}")
            out(etiqueta, "[+] Cabeceras devueltas por el servidor:")
            for header, valor in resp.getheaders():
                out(etiqueta, f"    - {header}: {valor}")

            # Lectura preliminar del contenido
            cuerpo = resp.read(200).decode("utf-8", errors="replace")
            out(etiqueta, "[+] Vista previa de la respuesta HTML (primeros caracteres):")
            out(etiqueta, f"    {cuerpo.strip()} ...")

    except urllib.error.URLError as e:
        out(etiqueta, f"[!] No se pudo conectar al servidor: {e.reason}")
        out(etiqueta, "    -> Asegúrate de que el servidor esté encendido ejecutando 'python app.py' en otra terminal.")
    except Exception as e:
        out(etiqueta, f"[!] Ocurrió un error inesperado: {e}")

def pedir_numero_consultas():
    # Repite la pregunta hasta recibir un entero positivo
    while True:
        entrada = input("¿Cuántas consultas simultáneas quieres lanzar? ").strip()
        if entrada.isdigit() and int(entrada) > 0:
            return int(entrada)
        print("Por favor, introduce un número entero mayor que 0.")

if __name__ == "__main__":
    url = "http://127.0.0.1:5000"
    cantidad = pedir_numero_consultas()

    # Un hilo por consulta, así todas se ejecutan en simultáneo
    with ThreadPoolExecutor(max_workers=cantidad) as executor:
        futuros = [executor.submit(consultar_servidor_local, url, n) for n in range(1, cantidad + 1)]
        for futuro in futuros:
            futuro.result()  # Espera a que termine cada consulta y propaga errores no controlados