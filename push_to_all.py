import subprocess
import sys

# Función para ejecutar comandos del sistema
def run_command(command, repo_name):
    try:
        print(f"Ejecutando: {' '.join(command)} en {repo_name}")
        subprocess.run(command, check=True)
        print(f"✅ Comando ejecutado exitosamente en {repo_name}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al ejecutar el comando en {repo_name}: {e}")
        sys.exit(1)

# Lista de remotos
repositories = {
    "GitHub": "github",
    "GitLab": "gitlab",
    "Bitbucket": "bitbucket"
}

# Agregar y confirmar los cambios
run_command(["git", "add", "."], "Local")
run_command(["git", "commit", "-m", "Automatización de subida a múltiples repositorios"], "Local")

# Subir a cada repositorio
for repo_name, remote in repositories.items():
    run_command(["git", "push", remote, "main"], repo_name)
