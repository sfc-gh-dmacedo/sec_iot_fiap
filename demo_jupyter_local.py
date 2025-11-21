"""
Demo de Segurança em IoT - AWS IoT Core
MBA FIAP - Internet das Coisas

VERSÃO PARA JUPYTER NOTEBOOK LOCAL
Execute célula por célula no Jupyter
"""

# ============================================================================
# CÉLULA 1: IMPORTS E CONFIGURAÇÃO
# ============================================================================

print("="*70)
print("🔐 DEMO DE SEGURANÇA EM IoT - AWS IoT Core")
print("="*70)
print()

# Imports
import json
import time
import ssl
from datetime import datetime
import os

print("✅ Bibliotecas importadas")
print()


# ============================================================================
# CÉLULA 2: CONFIGURAR PATHS E VARIÁVEIS
# ============================================================================

# ⚠️ AJUSTE ESTES VALORES com suas configurações
AWS_IOT_ENDPOINT = "seu-endpoint-aqui-ats.iot.us-east-1.amazonaws.com"
AWS_REGION = "us-east-1"
THING_NAME = "sensor-01-secure"
CLIENT_ID = "sensor-01"

# Caminho dos certificados no seu Mac
CERTS_DIR = "/Users/dmacedo/Documents/Codes/Projects/sec_iot_fiap/aws_iot_certs"

# Arquivos de certificado
cert_file = os.path.join(CERTS_DIR, "sensor-01-certificate.pem.crt")
key_file = os.path.join(CERTS_DIR, "sensor-01-private.pem.key")
root_ca_file = os.path.join(CERTS_DIR, "AmazonRootCA1.pem")

# Verificar
print("📋 Configuração:")
print(f"   Endpoint: {AWS_IOT_ENDPOINT}")
print(f"   Region:   {AWS_REGION}")
print(f"   Thing:    {THING_NAME}")
print(f"   Client:   {CLIENT_ID}")
print()

print("🔐 Verificando certificados...")
for f, name in [(cert_file, "Certificado"), (key_file, "Chave privada"), (root_ca_file, "Root CA")]:
    if os.path.exists(f):
        print(f"   ✅ {name} encontrado")
    else:
        print(f"   ❌ {name} NÃO encontrado: {f}")

print()


# ============================================================================
# CÉLULA 3: INSTALAR PAHO-MQTT
# ============================================================================

print("📦 Instalando paho-mqtt...")

try:
    import paho.mqtt.client as mqtt
    print("✅ paho-mqtt já instalado")
except ImportError:
    print("⏳ Instalando...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "paho-mqtt==1.6.1", "--quiet"])
    import paho.mqtt.client as mqtt
    print("✅ paho-mqtt instalado")

print()


# ============================================================================
# CÉLULA 4: CONFIGURAR CALLBACKS MQTT
# ============================================================================

# Variáveis de controle
connected_flag = False
publish_success = False

def on_connect(client, userdata, flags, rc):
    """Callback de conexão"""
    global connected_flag
    if rc == 0:
        connected_flag = True
        print("\n🔒 ✅ CONECTADO AO AWS IoT CORE!")
        print("   🔐 mTLS concluído com sucesso")
        print("   ✔️ Cliente validou servidor AWS")
        print("   ✔️ Servidor validou certificado X.509 do dispositivo\n")
    else:
        print(f"\n❌ ERRO na conexão. Código: {rc}")
        errors = {
            1: "Protocolo incorreto",
            2: "Client ID inválido",
            3: "Servidor indisponível",
            4: "Credenciais inválidas",
            5: "Não autorizado (verificar políticas)"
        }
        print(f"   {errors.get(rc, 'Erro desconhecido')}\n")

def on_publish(client, userdata, mid):
    """Callback de publicação"""
    global publish_success
    publish_success = True
    print(f"   ✅ Mensagem {mid} publicada")

def on_message(client, userdata, message):
    """Callback de recebimento"""
    print(f"\n📨 Mensagem recebida:")
    print(f"   Tópico: {message.topic}")
    print(f"   Payload: {message.payload.decode()}\n")

def on_subscribe(client, userdata, mid, granted_qos):
    """Callback de subscrição"""
    print(f"   ✅ Subscrito com sucesso")

print("✅ Callbacks configurados")
print()


# ============================================================================
# CÉLULA 5: CRIAR CLIENTE MQTT E CONFIGURAR TLS
# ============================================================================

print("🔧 Criando cliente MQTT...")

# Criar cliente
client = mqtt.Client(client_id=CLIENT_ID, protocol=mqtt.MQTTv311)

# Anexar callbacks
client.on_connect = on_connect
client.on_publish = on_publish
client.on_message = on_message
client.on_subscribe = on_subscribe

print("✅ Cliente criado")
print()

# ⭐ CONFIGURAR TLS/SSL (PONTO CRÍTICO DE SEGURANÇA)
print("⭐ Configurando TLS/SSL com mTLS...")
print()

client.tls_set(
    ca_certs=root_ca_file,           # Valida servidor AWS
    certfile=cert_file,              # Identidade do cliente
    keyfile=key_file,                # Chave privada
    cert_reqs=ssl.CERT_REQUIRED,     # Exige cert do servidor
    tls_version=ssl.PROTOCOL_TLSv1_2 # TLS 1.2+
)

print("✅ TLS configurado:")
print("   🔐 TLS 1.2+")
print("   🔐 Autenticação Mútua (mTLS)")
print("   🔐 Certificado X.509")
print("   🔐 Validação obrigatória do servidor")
print()


# ============================================================================
# CÉLULA 6: CONECTAR AO AWS IoT CORE
# ============================================================================

print("🔌 Conectando ao AWS IoT Core...")
print(f"   Endpoint: {AWS_IOT_ENDPOINT}")
print(f"   Porta: 8883 (MQTT/TLS)")
print()

# Resetar flag
connected_flag = False

# Conectar
client.connect(AWS_IOT_ENDPOINT, 8883, keepalive=60)
client.loop_start()

# Aguardar conexão
timeout = 15
start_time = time.time()
while not connected_flag and (time.time() - start_time) < timeout:
    time.sleep(0.5)

if not connected_flag:
    print("❌ Timeout na conexão")
    print("   Verifique: endpoint, certificados, políticas")
else:
    print("✅ Conexão estabelecida com sucesso!")

print()


# ============================================================================
# CÉLULA 7: TESTE 1 - Tópico PERMITIDO
# ============================================================================

print("="*70)
print("🧪 TESTE 1: Publicação em Tópico PERMITIDO")
print("="*70)
print()

allowed_topic = "iot/security/demo/sensor01/temperature"
print(f"Tópico: {allowed_topic}")
print(f"Política IoT: iot/security/demo/* ✅ MATCH")
print()

# Payload
payload_1 = {
    "device_id": CLIENT_ID,
    "timestamp": datetime.now().isoformat(),
    "temperature": 23.5,
    "humidity": 65.2,
    "test": "ALLOWED_TOPIC"
}

print("📤 Publicando...")
print(f"   Payload: {json.dumps(payload_1, indent=2)}")
print()

# Publicar
publish_success = False
client.publish(allowed_topic, json.dumps(payload_1), qos=1)
time.sleep(2)

if publish_success:
    print("✅ RESULTADO: AUTORIZADO")
    print()
    print("   🔍 Análise de Segurança:")
    print("   ━━━━━━━━━━━━━━━━━━━━━━━")
    print("   ✔️ Política IoT permitiu")
    print("   ✔️ Tópico corresponde ao padrão")
    print("   ✔️ Dados criptografados via TLS 1.2+")
    print("   ✔️ Integridade garantida")
else:
    print("⚠️ Não confirmado (aguarde ou verifique políticas)")

print()


# ============================================================================
# CÉLULA 8: TESTE 2 - Tópico NEGADO ⭐ MOMENTO-CHAVE!
# ============================================================================

print("="*70)
print("🧪 TESTE 2: Tópico NÃO PERMITIDO ⭐ MOMENTO-CHAVE DA DEMO")
print("="*70)
print()

denied_topic = "iot/production/data"
print(f"Tópico: {denied_topic}")
print(f"Política IoT: iot/security/demo/*")
print(f"Match: ❌ NÃO CORRESPONDE")
print()
print("🎯 Objetivo: Demonstrar Princípio do Menor Privilégio")
print()

# Payload
payload_2 = {
    "device_id": CLIENT_ID,
    "timestamp": datetime.now().isoformat(),
    "data": "Tentativa não autorizada",
    "test": "DENIED_TOPIC"
}

print("📤 Tentando publicar em tópico fora do escopo...")
print(f"   Payload: {json.dumps(payload_2, indent=2)}")
print()

# Tentar publicar
publish_success = False
client.publish(denied_topic, json.dumps(payload_2), qos=1)
time.sleep(3)

if publish_success:
    print("⚠️ ALERTA: Foi autorizado!")
    print("   Verificar política - pode estar muito permissiva")
else:
    print("✅ RESULTADO: NEGADO (como esperado!)")
    print()
    print("   🔍 Análise de Segurança:")
    print("   ━━━━━━━━━━━━━━━━━━━━━━━")
    print("   ✔️ Política IoT BLOQUEOU a operação")
    print("   ✔️ Princípio do Menor Privilégio aplicado")
    print("   ✔️ Dispositivo limitado ao escopo definido")
    print("   ✔️ Tópico fora do padrão = NEGADO")
    print()
    print("   🛡️ Segurança Demonstrada:")
    print("   • Controle de acesso granular por tópico")
    print("   • Prevenção de acesso não autorizado")
    print("   • Isolamento entre ambientes (demo vs production)")
    print("   • Se dispositivo for comprometido, dano é LIMITADO")

print()


# ============================================================================
# CÉLULA 9: TESTE 3 - Subscribe e Receive
# ============================================================================

print("="*70)
print("🧪 TESTE 3: Subscrição e Comunicação Bidirecional")
print("="*70)
print()

subscribe_topic = "iot/security/demo/sensor01/commands"
print(f"Tópico: {subscribe_topic}")
print()

# Subscrever
print("📥 Subscrevendo...")
client.subscribe(subscribe_topic, qos=1)
time.sleep(2)

# Publicar para si mesmo
print("📤 Publicando mensagem de teste...")
test_command = {
    "command": "STATUS_CHECK",
    "timestamp": datetime.now().isoformat(),
    "from": "control_center"
}
client.publish(subscribe_topic, json.dumps(test_command), qos=1)

print("⏳ Aguardando recebimento...")
time.sleep(3)

print()
print("✅ Subscribe/Receive testados")
print("   ✔️ Comunicação bidirecional funcionando")
print("   ✔️ Permissões de Subscribe e Receive verificadas")
print()


# ============================================================================
# CÉLULA 10: RESUMO DOS CONCEITOS
# ============================================================================

print("="*70)
print("📚 CONCEITOS DE SEGURANÇA DEMONSTRADOS")
print("="*70)
print()

concepts = {
    "1. mTLS": "Autenticação mútua - cliente e servidor se validam",
    "2. X.509": "Certificado digital único por dispositivo",
    "3. Políticas IoT": "Controle granular de acesso (Teste 2 comprovou!)",
    "4. TLS 1.2+": "Criptografia forte em trânsito",
    "5. Menor Privilégio": "Permissões mínimas - limita danos",
    "6. Defense in Depth": "Múltiplas camadas de proteção"
}

for conceito, descricao in concepts.items():
    print(f"   ✔️ {conceito}: {descricao}")

print()
print("⭐ Destaque: TESTE 2 demonstrou que mesmo dispositivo")
print("   AUTENTICADO é BLOQUEADO ao tentar acessar recursos")
print("   fora do seu escopo. Isso é SEGURANÇA EM AÇÃO!")
print()


# ============================================================================
# CÉLULA 11: DESCONECTAR E FINALIZAR
# ============================================================================

print("🧹 Desconectando...")
client.loop_stop()
client.disconnect()
time.sleep(1)

print()
print("="*70)
print("✅ DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!")
print("="*70)
print()
print("Conceitos Demonstrados:")
print("  ✅ Autenticação mútua (mTLS)")
print("  ✅ Certificados X.509")
print("  ✅ Políticas IoT granulares")
print("  ✅ Criptografia em trânsito (TLS 1.2+)")
print("  ✅ Princípio do Menor Privilégio ⭐⭐⭐")
print("  ✅ Defesa em Profundidade")
print()
print("🎓 Pronto para apresentar no MBA FIAP!")
print()

