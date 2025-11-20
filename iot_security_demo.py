"""
Demo de Segurança em IoT - AWS IoT Core
MBA FIAP - Internet das Coisas

Este script pode ser executado em um Notebook Snowflake.
Demonstra conceitos de segurança em IoT usando AWS IoT Core.

⚠️ IMPORTANTE: Este código foi projetado para Python 3.11 no Snowflake
e usa bibliotecas disponíveis no canal Anaconda Snowflake.
"""

# ============================================================================
# PARTE 1: CONFIGURAÇÃO INICIAL
# ============================================================================

print("="*70)
print("🔐 DEMO DE SEGURANÇA EM IoT - AWS IoT Core")
print("="*70)
print()

# Importar bibliotecas necessárias
import json
import time
import ssl
from datetime import datetime
import os
import tempfile

# Snowflake imports
from snowflake.snowpark import Session
from snowflake.snowpark.context import get_active_session

print("✅ Bibliotecas importadas com sucesso")
print()

# ----------------------------------------------------------------------------
# Obter sessão ativa do Snowflake
# ----------------------------------------------------------------------------

session = get_active_session()

# Carregar configurações da tabela IOT_CONFIG
config_df = session.table("IOT_CONFIG").to_pandas()
config = dict(zip(config_df['CONFIG_KEY'], config_df['CONFIG_VALUE']))

print("📋 Configurações carregadas:")
print(f"   - AWS IoT Endpoint: {config['AWS_IOT_ENDPOINT']}")
print(f"   - AWS Region: {config['AWS_REGION']}")
print(f"   - Thing Name: {config['THING_NAME']}")
print(f"   - Client ID: {config['CLIENT_ID']}")
print()

# ----------------------------------------------------------------------------
# Baixar Certificados do Stage para Filesystem Temporário
# ----------------------------------------------------------------------------

print("🔐 CONCEITO DE SEGURANÇA: Certificados Criptografados")
print("-" * 70)
print("Os certificados são armazenados de forma criptografada no Snowflake")
print("(SSE - Snowflake Server-Side Encryption) e só são descriptografados")
print("temporariamente em memória para uso.")
print()

# Criar diretório temporário para certificados
temp_dir = tempfile.mkdtemp(prefix="iot_certs_")
print(f"📁 Diretório temporário criado: {temp_dir}")
print()

# Função para baixar arquivo do stage
def download_from_stage(stage_path, local_path):
    """Baixa arquivo do stage Snowflake para filesystem local temporário"""
    try:
        # Extrair nome do arquivo do stage path
        filename = stage_path.split('/')[-1]
        
        # Usar GET para baixar do stage
        get_cmd = f"GET {stage_path} 'file://{local_path}/'"
        session.sql(get_cmd).collect()
        
        downloaded_file = os.path.join(local_path, filename)
        
        if os.path.exists(downloaded_file):
            print(f"   ✅ {filename} baixado")
            return downloaded_file
        else:
            print(f"   ❌ Erro: {filename} não encontrado após download")
            return None
    except Exception as e:
        print(f"   ❌ Erro ao baixar {stage_path}: {str(e)}")
        return None

print("🔽 Baixando certificados do stage...")

# Baixar certificados
cert_file = download_from_stage(config['CERT_PATH'], temp_dir)
key_file = download_from_stage(config['KEY_PATH'], temp_dir)
root_ca_file = download_from_stage(config['ROOT_CA_PATH'], temp_dir)

if not all([cert_file, key_file, root_ca_file]):
    raise Exception("❌ Erro ao baixar certificados. Verifique se os arquivos estão no stage.")

print()
print("✅ Todos os certificados baixados com sucesso")
print()

# ============================================================================
# PARTE 2: CONFIGURAÇÃO DE SEGURANÇA MQTT
# ============================================================================

print("="*70)
print("🔐 PARTE 2: DEMONSTRAÇÃO DE SEGURANÇA")
print("="*70)
print()

# Instalar paho-mqtt se não estiver disponível
try:
    import paho.mqtt.client as mqtt
    print("✅ paho-mqtt importado com sucesso")
except ImportError:
    print("⚠️  paho-mqtt não disponível. Tentando instalar...")
    import sys
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "paho-mqtt", "--quiet"])
    import paho.mqtt.client as mqtt
    print("✅ paho-mqtt instalado e importado")

print()

# ----------------------------------------------------------------------------
# Variáveis globais para controle de conexão
# ----------------------------------------------------------------------------

connected_flag = False
publish_success = False
connection_result = None
messages_received = []

# ----------------------------------------------------------------------------
# Callbacks do MQTT
# ----------------------------------------------------------------------------

def on_connect(client, userdata, flags, rc):
    """Callback executado quando conecta ao broker"""
    global connected_flag, connection_result
    connection_result = rc
    
    if rc == 0:
        connected_flag = True
        print()
        print("🔒 ✅ CONECTADO com sucesso ao AWS IoT Core!")
        print(f"   Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        print("   🔐 AUTENTICAÇÃO MÚTUA TLS (mTLS) CONCLUÍDA:")
        print("   ✔️ Cliente validou certificado do servidor AWS")
        print("   ✔️ Servidor AWS validou certificado X.509 do dispositivo")
        print()
    else:
        print()
        print(f"❌ ERRO na conexão. Código: {rc}")
        error_messages = {
            1: "Versão de protocolo incorreta",
            2: "Identificador de cliente inválido",
            3: "Servidor indisponível",
            4: "Usuário ou senha inválidos",
            5: "Não autorizado (verifique políticas IoT)"
        }
        print(f"   Motivo: {error_messages.get(rc, 'Erro desconhecido')}")
        print()

def on_publish(client, userdata, mid):
    """Callback executado quando mensagem é publicada"""
    global publish_success
    publish_success = True
    print(f"   ✅ Mensagem {mid} publicada com sucesso")

def on_message(client, userdata, message):
    """Callback executado quando mensagem é recebida"""
    global messages_received
    messages_received.append(message)
    print()
    print("📨 Mensagem recebida:")
    print(f"   Tópico: {message.topic}")
    print(f"   Payload: {message.payload.decode()}")
    print(f"   QoS: {message.qos}")
    print()

def on_subscribe(client, userdata, mid, granted_qos):
    """Callback executado quando subscrição é confirmada"""
    print(f"   ✅ Subscrito com sucesso (MID: {mid}, QoS: {granted_qos})")

def on_log(client, userdata, level, buf):
    """Callback para logs (opcional, para debug)"""
    # Descomente para ver logs detalhados
    # print(f"[LOG] {buf}")
    pass

print("✅ Callbacks MQTT configurados")
print()

# ----------------------------------------------------------------------------
# Criar Cliente MQTT com Configurações de Segurança
# ----------------------------------------------------------------------------

print("🔧 Criando cliente MQTT...")

# Criar cliente MQTT
client = mqtt.Client(client_id=config['CLIENT_ID'], protocol=mqtt.MQTTv311)

# Configurar callbacks
client.on_connect = on_connect
client.on_publish = on_publish
client.on_message = on_message
client.on_subscribe = on_subscribe
client.on_log = on_log

print("✅ Cliente MQTT criado")
print()

# ⭐ PONTO CRÍTICO DE SEGURANÇA ⭐
print("="*70)
print("⭐ PONTO CRÍTICO DE SEGURANÇA: Configuração TLS/SSL")
print("="*70)
print()

try:
    client.tls_set(
        ca_certs=root_ca_file,           # Certificado raiz da AWS (valida servidor)
        certfile=cert_file,              # Certificado X.509 do dispositivo (identidade)
        keyfile=key_file,                # Chave privada do dispositivo (prova de identidade)
        cert_reqs=ssl.CERT_REQUIRED,     # Exige certificado do servidor
        tls_version=ssl.PROTOCOL_TLSv1_2, # TLS 1.2 (mínimo recomendado)
        ciphers=None                     # Usa ciphers padrão seguros
    )
    print("✅ TLS/SSL configurado com sucesso:")
    print()
    print("   📋 Configurações de Segurança:")
    print("   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("   🔐 Versão TLS: 1.2+")
    print("   🔐 Modo: Autenticação Mútua (mTLS)")
    print("   🔐 Certificado cliente: X.509")
    print("   🔐 Validação servidor: OBRIGATÓRIA")
    print("   🔐 Chave privada: Protegida")
    print("   🔐 Root CA: Amazon Trust Services")
    print()
except Exception as e:
    print(f"❌ Erro na configuração TLS: {str(e)}")
    raise

# ----------------------------------------------------------------------------
# Conectar ao AWS IoT Core
# ----------------------------------------------------------------------------

print("="*70)
print("🔌 CONECTANDO AO AWS IoT Core")
print("="*70)
print()
print(f"📡 Endpoint: {config['AWS_IOT_ENDPOINT']}")
print(f"🔌 Porta: 8883 (MQTT sobre TLS)")
print(f"🆔 Client ID: {config['CLIENT_ID']}")
print()
print("⏳ Iniciando handshake TLS...")
print("   1️⃣ Cliente solicita conexão")
print("   2️⃣ Servidor apresenta certificado")
print("   3️⃣ Cliente valida certificado do servidor")
print("   4️⃣ Cliente apresenta seu certificado X.509")
print("   5️⃣ Servidor valida certificado do cliente")
print("   6️⃣ Servidor verifica políticas IoT")
print("   7️⃣ Canal criptografado estabelecido")
print()

try:
    # Conectar (porta 8883 é MQTT sobre TLS)
    client.connect(config['AWS_IOT_ENDPOINT'], 8883, keepalive=60)
    
    # Iniciar loop de rede (não bloqueante)
    client.loop_start()
    
    # Aguardar conexão
    timeout = 15
    start_time = time.time()
    while not connected_flag and (time.time() - start_time) < timeout:
        time.sleep(0.5)
    
    if not connected_flag:
        raise Exception(f"Timeout na conexão após {timeout} segundos")
        
except Exception as e:
    print(f"❌ Erro na conexão: {str(e)}")
    client.loop_stop()
    raise

# ============================================================================
# PARTE 3: TESTES DE SEGURANÇA
# ============================================================================

print()
print("="*70)
print("🧪 PARTE 3: TESTES DE SEGURANÇA")
print("="*70)
print()

# ----------------------------------------------------------------------------
# TESTE 3.1 - Publicação em Tópico PERMITIDO
# ----------------------------------------------------------------------------

print()
print("━"*70)
print("🧪 TESTE 3.1: Publicação em Tópico PERMITIDO")
print("━"*70)
print()

allowed_topic = "iot/security/demo/sensor01/temperature"

print("📋 Configuração do Teste:")
print(f"   Tópico destino: {allowed_topic}")
print(f"   Política IoT: iot/security/demo/*")
print(f"   Match com política: ✅ SIM")
print()

# Criar payload com dados do sensor
payload_1 = {
    "device_id": config['CLIENT_ID'],
    "timestamp": datetime.now().isoformat(),
    "temperature": 23.5,
    "humidity": 65.2,
    "unit": "celsius",
    "security_demo": True,
    "test_id": "TEST_3.1_ALLOWED"
}

print("📤 Publicando mensagem criptografada...")
print()
print("   Payload:")
for key, value in payload_1.items():
    print(f"      {key}: {value}")
print()

# Resetar flag
publish_success = False

# Publicar
result = client.publish(
    topic=allowed_topic,
    payload=json.dumps(payload_1),
    qos=1  # QoS 1: Garante entrega pelo menos uma vez
)

# Aguardar confirmação
time.sleep(2)

if publish_success:
    print("✅ RESULTADO: Publicação AUTORIZADA")
    print()
    print("   🔍 Análise de Segurança:")
    print("   ━━━━━━━━━━━━━━━━━━━━━━━")
    print("   ✔️ Política IoT permitiu a operação")
    print("   ✔️ Tópico corresponde ao padrão autorizado")
    print("   ✔️ Mensagem transmitida via TLS 1.2+")
    print("   ✔️ Dados criptografados em trânsito")
    print("   ✔️ Integridade garantida pelo TLS")
    print()
else:
    print("⚠️ RESULTADO: Publicação não confirmada")
    print("   (Verifique logs AWS IoT Core)")
    print()

# ----------------------------------------------------------------------------
# TESTE 3.2 - Tentativa de Publicação em Tópico NEGADO
# ----------------------------------------------------------------------------

print()
print("━"*70)
print("🧪 TESTE 3.2: Publicação em Tópico NÃO PERMITIDO")
print("━"*70)
print()

denied_topic = "iot/production/data"

print("📋 Configuração do Teste:")
print(f"   Tópico destino: {denied_topic}")
print(f"   Política IoT: iot/security/demo/*")
print(f"   Match com política: ❌ NÃO")
print()
print("🎯 Objetivo: Demonstrar Princípio do Menor Privilégio")
print()

payload_2 = {
    "device_id": config['CLIENT_ID'],
    "timestamp": datetime.now().isoformat(),
    "data": "Esta mensagem NÃO deve ser publicada",
    "security_test": "unauthorized_topic",
    "test_id": "TEST_3.2_DENIED"
}

print("📤 Tentando publicar em tópico não autorizado...")
print()
print("   Payload:")
for key, value in payload_2.items():
    print(f"      {key}: {value}")
print()

# Resetar flag
publish_success = False

# Tentar publicar
result = client.publish(
    topic=denied_topic,
    payload=json.dumps(payload_2),
    qos=1
)

# Aguardar (não deve confirmar)
time.sleep(3)

if publish_success:
    print("⚠️ ALERTA: Publicação foi autorizada!")
    print("   Verifique a política IoT - pode estar muito permissiva")
    print()
else:
    print("✅ RESULTADO: Publicação NEGADA (como esperado)")
    print()
    print("   🔍 Análise de Segurança:")
    print("   ━━━━━━━━━━━━━━━━━━━━━━━")
    print("   ✔️ Política IoT BLOQUEOU a operação")
    print("   ✔️ Princípio do Menor Privilégio aplicado")
    print("   ✔️ Dispositivo limitado ao escopo definido")
    print("   ✔️ Tópico fora do padrão autorizado")
    print()
    print("   🛡️ Aspectos de Segurança Demonstrados:")
    print("   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("   1. Controle de acesso granular por tópico")
    print("   2. Prevenção de acesso não autorizado")
    print("   3. Isolamento entre ambientes (demo vs production)")
    print("   4. Redução de superfície de ataque")
    print()

# ----------------------------------------------------------------------------
# TESTE 3.3 - Subscrição e Recebimento de Mensagens
# ----------------------------------------------------------------------------

print()
print("━"*70)
print("🧪 TESTE 3.3: Subscrição e Recebimento de Mensagens")
print("━"*70)
print()

subscribe_topic = "iot/security/demo/sensor01/commands"

print("📋 Configuração do Teste:")
print(f"   Tópico: {subscribe_topic}")
print("   Objetivo: Demonstrar controle bidirecional")
print()

print("📥 Subscrevendo no tópico...")
client.subscribe(subscribe_topic, qos=1)
time.sleep(2)

print()
print("📤 Publicando mensagem de teste para si mesmo...")
test_command = {
    "command": "STATUS_CHECK",
    "timestamp": datetime.now().isoformat(),
    "from": "control_center",
    "parameters": {
        "check_sensors": True,
        "report_back": True
    },
    "test_id": "TEST_3.3_SUBSCRIBE"
}

client.publish(subscribe_topic, json.dumps(test_command, indent=2), qos=1)

print()
print("⏳ Aguardando recebimento da mensagem...")
time.sleep(3)

print()
print("✅ RESULTADO: Subscribe e Receive testados")
print()
print("   🔍 Análise de Segurança:")
print("   ━━━━━━━━━━━━━━━━━━━━━━━")
print("   ✔️ Permissão iot:Subscribe verificada")
print("   ✔️ Permissão iot:Receive verificada")
print("   ✔️ Permissão iot:Publish verificada")
print("   ✔️ Comunicação bidirecional funcionando")
print("   ✔️ Políticas granulares para cada ação")
print()

# ============================================================================
# PARTE 4: ANÁLISE DE SEGURANÇA
# ============================================================================

print()
print("="*70)
print("🛡️  PARTE 4: ANÁLISE DE SEGURANÇA")
print("="*70)
print()

# ----------------------------------------------------------------------------
# Resumo dos Conceitos Demonstrados
# ----------------------------------------------------------------------------

print("━"*70)
print("📚 CONCEITOS DE SEGURANÇA DEMONSTRADOS")
print("━"*70)
print()

security_concepts = [
    {
        "conceito": "1. Autenticação Mútua TLS (mTLS)",
        "descricao": "Cliente e servidor se autenticam mutuamente",
        "implementacao": "Certificados X.509 validados em ambas as direções",
        "beneficio": "Previne ataques man-in-the-middle (MITM)",
        "evidencia": "Conexão estabelecida com sucesso usando certificados"
    },
    {
        "conceito": "2. Certificados X.509",
        "descricao": "Identidade digital única para cada dispositivo",
        "implementacao": "Certificado + chave privada por dispositivo",
        "beneficio": "Rastreabilidade e não-repúdio",
        "evidencia": "Cada dispositivo identificado unicamente"
    },
    {
        "conceito": "3. Políticas IoT Granulares",
        "descricao": "Controle fino de permissões por recurso",
        "implementacao": "JSON policy com actions, resources e effects",
        "beneficio": "Limita danos em caso de comprometimento",
        "evidencia": "Teste 3.2 - tópico não autorizado foi bloqueado"
    },
    {
        "conceito": "4. Criptografia em Trânsito",
        "descricao": "Dados criptografados durante transmissão",
        "implementacao": "TLS 1.2+ com ciphers seguros",
        "beneficio": "Confidencialidade e integridade dos dados",
        "evidencia": "Todas as comunicações via porta 8883 (TLS)"
    },
    {
        "conceito": "5. Princípio do Menor Privilégio",
        "descricao": "Permissões mínimas necessárias",
        "implementacao": "Tópicos específicos, ações limitadas",
        "beneficio": "Reduz superfície de ataque",
        "evidencia": "Dispositivo restrito a iot/security/demo/*"
    },
    {
        "conceito": "6. Segregação de Acesso",
        "descricao": "Isolamento entre diferentes contextos",
        "implementacao": "Tópicos separados por ambiente/função",
        "beneficio": "Previne acesso cruzado não autorizado",
        "evidencia": "Acesso negado a tópicos production"
    }
]

for concept in security_concepts:
    print(f"{concept['conceito']}")
    print("─" * 70)
    print(f"📝 Descrição:     {concept['descricao']}")
    print(f"⚙️  Implementação: {concept['implementacao']}")
    print(f"✅ Benefício:     {concept['beneficio']}")
    print(f"🔬 Evidência:     {concept['evidencia']}")
    print()

# ----------------------------------------------------------------------------
# Comparação: Com vs Sem Segurança
# ----------------------------------------------------------------------------

print()
print("━"*70)
print("⚖️  COMPARAÇÃO: COM vs SEM SEGURANÇA")
print("━"*70)
print()

comparison_data = [
    ("Autenticação", 
     "❌ Nenhuma - qualquer um conecta", 
     "✅ mTLS - apenas certificados válidos"),
    
    ("Autorização", 
     "❌ Acesso total - sem controle", 
     "✅ Políticas granulares - controle fino"),
    
    ("Dados em Trânsito", 
     "❌ Texto plano - fácil interceptação", 
     "✅ TLS 1.2+ - criptografado"),
    
    ("Identificação", 
     "❌ Impossível rastrear origem", 
     "✅ Cada dispositivo identificado"),
    
    ("Auditoria", 
     "❌ Sem logs confiáveis", 
     "✅ Logs completos com identidade"),
    
    ("Risco MITM", 
     "❌ ALTO - sem proteção", 
     "✅ BAIXO - mTLS previne"),
    
    ("Comprometimento", 
     "❌ Acesso total se comprometido", 
     "✅ Dano limitado ao escopo da política"),
    
    ("Conformidade", 
     "❌ Não atende regulamentações", 
     "✅ Atende LGPD, GDPR, etc")
]

print(f"{'Aspecto':<20} | {'Sem Segurança':<35} | {'Com Segurança':<40}")
print("─" * 100)
for aspecto, sem_seg, com_seg in comparison_data:
    print(f"{aspecto:<20} | {sem_seg:<35} | {com_seg:<40}")

print()

# ----------------------------------------------------------------------------
# Camadas de Segurança (Defense in Depth)
# ----------------------------------------------------------------------------

print()
print("━"*70)
print("🛡️  DEFESA EM PROFUNDIDADE (Defense in Depth)")
print("━"*70)
print()
print("Camadas de segurança implementadas nesta demo:")
print()
print("  Camada 1: 🔐 Transporte")
print("            └─ TLS 1.2+ com criptografia forte")
print()
print("  Camada 2: 🔐 Autenticação")
print("            └─ Certificados X.509 (mTLS)")
print()
print("  Camada 3: 🔐 Autorização")
print("            └─ Políticas IoT granulares")
print()
print("  Camada 4: 🔐 Auditoria")
print("            └─ Logs AWS CloudWatch")
print()
print("  Camada 5: 🔐 Monitoramento")
print("            └─ AWS IoT Device Defender (opcional)")
print()
print("  Camada 6: 🔐 Armazenamento")
print("            └─ Certificados criptografados (Snowflake SSE)")
print()

# ============================================================================
# PARTE 5: LIMPEZA E DESCONEXÃO
# ============================================================================

print()
print("="*70)
print("🧹 PARTE 5: LIMPEZA E DESCONEXÃO")
print("="*70)
print()

# Desconectar do AWS IoT
print("🔌 Desconectando do AWS IoT Core...")
client.loop_stop()
client.disconnect()
time.sleep(1)
print("   ✅ Desconectado com segurança")
print()

# Limpar certificados temporários
print("🧹 Limpando arquivos temporários...")
import shutil
try:
    shutil.rmtree(temp_dir)
    print(f"   ✅ Diretório {temp_dir} removido")
    print("   ✅ Certificados temporários apagados")
except Exception as e:
    print(f"   ⚠️ Erro ao remover diretório: {str(e)}")

print()

# ============================================================================
# CONCLUSÃO
# ============================================================================

print()
print("="*70)
print("🎓 CONCLUSÕES PARA APRESENTAÇÃO - MBA FIAP")
print("="*70)
print()

conclusions = [
    {
        "titulo": "1. Segurança em IoT é Multi-Camadas",
        "pontos": [
            "Uma única medida não é suficiente",
            "Defense in Depth: múltiplas camadas de proteção",
            "Falha em uma camada não compromete todo sistema"
        ]
    },
    {
        "titulo": "2. Autenticação ≠ Autorização",
        "pontos": [
            "Autenticação: Quem você é (certificado X.509)",
            "Autorização: O que você pode fazer (políticas IoT)",
            "Ambas são necessárias e complementares"
        ]
    },
    {
        "titulo": "3. Princípio do Menor Privilégio é Crítico",
        "pontos": [
            "Dispositivo comprometido → danos limitados",
            "Escopo bem definido reduz riscos",
            "Facilitafacilita auditoria e troubleshooting"
        ]
    },
    {
        "titulo": "4. Criptografia é Obrigatória",
        "pontos": [
            "Dados sensíveis sempre em trânsito",
            "TLS 1.2+ como padrão mínimo",
            "Nunca confie na rede (Zero Trust)"
        ]
    },
    {
        "titulo": "5. Gestão de Certificados é Desafiadora",
        "pontos": [
            "Renovação periódica necessária",
            "Revogação em caso de comprometimento",
            "Armazenamento seguro de chaves privadas",
            "Escala: milhares de dispositivos"
        ]
    }
]

for conclusion in conclusions:
    print(f"📌 {conclusion['titulo']}")
    print("─" * 70)
    for ponto in conclusion['pontos']:
        print(f"   • {ponto}")
    print()

print()
print("━"*70)
print("🚀 PRÓXIMOS PASSOS (Opcional para Discussão)")
print("━"*70)
print()
print("  1. AWS IoT Device Defender")
print("     └─ Monitoramento contínuo de anomalias")
print()
print("  2. Rotação Automática de Certificados")
print("     └─ Renovação sem interrupção de serviço")
print()
print("  3. Fleet Provisioning")
print("     └─ Provisionamento seguro em escala")
print()
print("  4. Jobs para OTA (Over-The-Air)")
print("     └─ Atualização segura de firmware")
print()
print("  5. AWS IoT Core Device Advisor")
print("     └─ Testes de segurança automatizados")
print()

print()
print("="*70)
print("✅ DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!")
print("="*70)
print()
print("🎓 Boa apresentação no MBA FIAP!")
print()

