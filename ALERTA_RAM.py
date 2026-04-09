#!/usr/bin/env python3

#CREDITOS Paulo ES Junior - Brasil - 2026
#FUNCAO Alerta de Memoria RAM Baixa afim de Evitar Travamento do Linux
#LICENCA Pode ser utilizado livremente, desde que mantenha os CREDITOS
#COMANDO em Aplicativos de Inicializacao: '/usr/bin/python3' '/home/usuario/Área de Trabalho/'ALERTA_RAM.py 90
#OU: python3 alerta_ram.py 90

#CREDITS Paulo ES Junior - Brazil - 2026
#Function: Low RAM Alert to Prevent Linux Crash 
#License: Can be used freely, as long as you keep the CREDITS
#COMMAND in Startup Applications: '/usr/bin/python3' '/home/user/Desktop/'RAM_ALERT.py 90
#OR: python3 ram_alert.py 90

import re
import sys
import time
import subprocess

# ---------------- 1-PARAMETRO ----------------
if len(sys.argv) != 2:
    print("Uso: alerta_ram.py <percentual>")
    sys.exit(1)

try:
    LIMITE = int(sys.argv[1])
except:
    print("Parâmetro inválido.")
    sys.exit(1)

# ---------------- 2-FUNÇÃO RAM ----------------
def get_ram_usage():
    try:
        with open("/proc/meminfo") as f:
            meminfo = f.read()

        total = int(re.search(r"MemTotal:\s+(\d+)", meminfo).group(1))
        available = int(re.search(r"MemAvailable:\s+(\d+)", meminfo).group(1))

        used = total - available
        percent = int((used / total) * 100)

        return percent
    except:
        return 0

# ---------------- 3-JANELA ----------------
def mostrar_janela(titulo, mensagem):
    try:
        subprocess.run([
            "zenity",
            "--info",
            "--title", titulo,
            "--text", mensagem
        ])
        return
    except:
        pass

    try:
        subprocess.run([
            "xmessage",
            "-center",
            mensagem
        ])
        return
    except:
        pass

    print(mensagem)

# ---------------- 4-ALERTA ----------------
def alertar(uso):
    mensagem = f"⚠️ MEMÓRIA ALTA ({uso}%)\nFECHAR PROGRAMAS!"

    # ---------------- PISCAR ----------------
    try:
        p = subprocess.Popen([
            "zenity",
            "--progress",
            "--title=Alerta de Memória",
            "--no-cancel",
            "--auto-close",
            "--width=300"
        ], stdin=subprocess.PIPE, text=True)

        for i in range(6):
            p.stdin.write(f"# {mensagem}\n")
            p.stdin.flush()
            time.sleep(0.4)

            p.stdin.write("# \n")
            p.stdin.flush()
            time.sleep(0.4)

        p.stdin.write("100\n")
        p.stdin.flush()

    except:
        pass

    # ---------------- JANELA COM OK ----------------
    try:
        subprocess.run([
            "zenity",
            "--warning",
            "--title", "⚠️ Memória Alta",
            "--text", mensagem
        ])
        return
    except:
        pass

    # fallback
    mostrar_janela("Alerta de Memória", mensagem)
# ---------------- 5-INÍCIO ----------------
mostrar_janela(
    "Monitor de RAM",
    "(PESJ 2026) Monitor de memória RAM ativado.\nPressione OK para continuar."
)

print(f"Monitorando RAM... Limite: {LIMITE}%")

# ---------------- 6-LOOP ----------------
alerta_ativo = False

while True:
    uso = get_ram_usage()

    if uso >= LIMITE:
        if not alerta_ativo:
            alertar(uso)
            alerta_ativo = True
    else:
        alerta_ativo = False

    time.sleep(5) #alterado de 2 para 5 para ser mais EFICIENTE e ECONOMICO no sistema operacional
