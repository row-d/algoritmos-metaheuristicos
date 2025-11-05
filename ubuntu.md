# Instalación en Ubuntu

Para instalar y configurar el proyecto en un sistema Ubuntu, sigue estos pasos:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
git clone https://github.com/row-d/algoritmos-metaheuristicos.git && cd algoritmos-metaheuristicos
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Para cerrar el entorno virtual, usa:

```bash
deactivate
```
