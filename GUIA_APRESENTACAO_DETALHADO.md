# Guia Detalhado de Apresentação - Demo IoT Security
## Como Apresentar Célula por Célula com Validações na AWS

---

## 🎯 Visão Geral da Apresentação

**Duração**: 20-30 minutos  
**Células**: 11  
**Momento-chave**: Célula 8 (Teste 2 - Bloqueio)

---

## 📋 Estrutura da Demonstração

```
Células 1-2  → Setup (configuração)
Células 3-4  → Preparação (bibliotecas e callbacks)
Células 5-6  → ⭐ Conexão Segura (mTLS)
Célula 7     → ✅ Teste 1: Permitido
Célula 8     → ⭐⭐⭐ Teste 2: Negado (MOMENTO-CHAVE!)
Célula 9     → ✅ Teste 3: Subscribe
Células 10-11 → Resumo e Conclusão
```

---

## 🎬 CÉLULA 1: Imports e Setup Inicial

### O Que Faz
Importa bibliotecas Python básicas necessárias para a demo.

### O Que Falar
> "Vou começar importando as bibliotecas necessárias. São bibliotecas padrão do Python para JSON, tempo, SSL (segurança) e manipulação de arquivos."

### Código
```python
import json
import time
import ssl
from datetime import datetime
import os
```

### Resultado Esperado
```
✅ Bibliotecas importadas
```

### Validação na AWS
**Não aplicável** - apenas imports locais.

### Tempo
~5 segundos

---

## 🎬 CÉLULA 2: Configurar Paths e Variáveis

### O Que Faz
Define o endpoint AWS IoT, credenciais e localização dos certificados.

### O Que Falar
> "Aqui eu defino as configurações: o endpoint único do meu AWS IoT Core, a região, o nome do dispositivo (Thing) e onde estão os certificados X.509 que vamos usar para autenticação."

### Código Principal
```python
AWS_IOT_ENDPOINT = "seu-endpoint-ats.iot.us-east-1.amazonaws.com"
THING_NAME = "sensor-01-secure"
CLIENT_ID = "sensor-01"
```

### Resultado Esperado
```
📋 Configuração:
   Endpoint: xxx-ats.iot.us-east-1.amazonaws.com
   Region:   us-east-1
   Thing:    sensor-01-secure
   Client:   sensor-01

🔐 Verificando certificados...
   ✅ Certificado encontrado
   ✅ Chave privada encontrada
   ✅ Root CA encontrado
```

### Como Validar na AWS

**Console AWS > IoT Core > Test > MQTT test client**
- O endpoint aparece no topo da página
- Compare com o que está no código

**Console AWS > IoT Core > Manage > Things**
- Procure "sensor-01-secure"
- Deve existir e estar ativo

### Tempo
~10 segundos

---

## 🎬 CÉLULA 3: Instalar paho-mqtt

### O Que Faz
Instala a biblioteca MQTT (se ainda não estiver instalada).

### O Que Falar
> "Vou instalar a biblioteca paho-mqtt, que é o cliente MQTT para Python. MQTT é o protocolo de mensagens leve usado em IoT."

### Resultado Esperado
```
📦 Instalando paho-mqtt...
✅ paho-mqtt instalado
```

### Validação na AWS
**Não aplicável** - instalação local.

### Tempo
~30 segundos (primeira vez) ou ~2 segundos (já instalado)

---

## 🎬 CÉLULA 4: Configurar Callbacks MQTT

### O Que Faz
Define funções que são chamadas automaticamente quando eventos acontecem (conectar, publicar, receber mensagem).

### O Que Falar
> "Agora vou configurar os callbacks - funções que são chamadas automaticamente quando eventos acontecem, como quando conectamos com sucesso ou quando uma mensagem é publicada."

### Conceito
**Event-driven programming** - o código reage a eventos.

### Resultado Esperado
```
✅ Callbacks configurados
```

### Validação na AWS
**Não aplicável** - apenas definição de funções.

### Tempo
~5 segundos

---

## 🎬 CÉLULA 5: Criar Cliente MQTT e Configurar TLS

### ⭐ PONTO CRÍTICO DE SEGURANÇA ⭐

### O Que Faz
- Cria o cliente MQTT
- **Configura TLS/SSL com certificados para mTLS**
- Esta é a configuração de segurança principal!

### O Que Falar (Script Detalhado)

> "**Este é um momento crítico da demonstração de segurança.**
>
> Estou criando o cliente MQTT e configurando a camada de segurança TLS. 
>
> Vejam os parâmetros que estou usando:
> - **ca_certs**: Certificado raiz da Amazon - usado para VALIDAR o servidor AWS
> - **certfile**: Nosso certificado X.509 - nossa IDENTIDADE
> - **keyfile**: Nossa chave privada - PROVA de que somos donos do certificado
> - **cert_reqs=REQUIRED**: Validação do servidor é OBRIGATÓRIA
> - **tls_version=1.2**: TLS versão 1.2 ou superior
>
> Isso configura **autenticação mútua** - tanto o cliente quanto o servidor vão se validar. É o que chamamos de **mTLS**."

### Código Crítico
```python
client.tls_set(
    ca_certs=root_ca_file,           # Valida servidor AWS
    certfile=cert_file,              # Identidade do cliente
    keyfile=key_file,                # Chave privada
    cert_reqs=ssl.CERT_REQUIRED,     # Exige cert do servidor
    tls_version=ssl.PROTOCOL_TLSv1_2 # TLS 1.2+
)
```

### Resultado Esperado
```
🔧 Criando cliente MQTT...
✅ Cliente criado

⭐ Configurando TLS/SSL com mTLS...

✅ TLS configurado:
   🔐 TLS 1.2+
   🔐 Autenticação Mútua (mTLS)
   🔐 Certificado X.509
   🔐 Validação obrigatória do servidor
```

### Como Validar na AWS

**Console AWS > IoT Core > Security > Certificates**
1. Encontre seu certificado
2. Verifique:
   - Status: **Active** ✅
   - Aba **Policies**: Deve mostrar `SecureIoTDemoPolicy`
   - Aba **Things**: Deve mostrar `sensor-01-secure`

### Conceitos Demonstrados
- ✅ Criptografia TLS 1.2+
- ✅ Autenticação mútua (mTLS)
- ✅ Certificados X.509
- ✅ Validação obrigatória

### Tempo
~10 segundos

---

## 🎬 CÉLULA 6: Conectar ao AWS IoT Core

### ⭐ MOMENTO DA AUTENTICAÇÃO MÚTUA ⭐

### O Que Faz
Estabelece conexão segura com AWS IoT Core usando mTLS.

### O Que Falar (Script Detalhado)

> "Agora vou conectar ao AWS IoT Core. **Prestem atenção no que vai acontecer:**
>
> 1. Meu cliente vai iniciar uma conexão TLS na porta 8883
> 2. O servidor AWS vai apresentar SEU certificado
> 3. Meu cliente vai VALIDAR o certificado do servidor usando o Root CA
> 4. O servidor AWS vai PEDIR o meu certificado
> 5. Eu apresento meu certificado X.509
> 6. O servidor AWS vai VALIDAR meu certificado e verificar:
>    - O certificado está ativo?
>    - Tem políticas anexadas?
>    - É assinado pela CA correta?
> 7. Se tudo OK, estabelece canal criptografado
>
> Isso é **autenticação mútua** - ambos os lados se validam."

[Execute a célula]

> "Vejam: **CONECTADO!** A autenticação mútua foi bem-sucedida. Isso significa:
> - O servidor AWS validou meu certificado
> - Eu validei o certificado do servidor
> - Temos agora um canal criptografado seguro"

### Código Principal
```python
client.connect(AWS_IOT_ENDPOINT, 8883, keepalive=60)
client.loop_start()
```

### Resultado Esperado
```
🔌 Conectando ao AWS IoT Core...
   Endpoint: xxx-ats.iot.us-east-1.amazonaws.com
   Porta: 8883 (MQTT/TLS)

🔒 ✅ CONECTADO AO AWS IoT CORE!
   🔐 mTLS concluído com sucesso
   ✔️ Cliente validou servidor AWS
   ✔️ Servidor validou certificado X.509 do dispositivo

✅ Conexão estabelecida com sucesso!
```

### Como Validar na AWS EM TEMPO REAL

#### Opção 1: MQTT Test Client (RECOMENDADO para apresentação)

**Antes de executar a célula:**

1. **Abra em outra aba/tela**: Console AWS > IoT Core > **Test** > **MQTT test client**
2. Na aba **"Subscribe to a topic"**:
   - Topic filter: `#` (captura TUDO)
   - Clique **"Subscribe"**
3. **Deixe esta tela VISÍVEL** durante a apresentação

**Ao executar a célula 6:**
- Você verá eventos de conexão no test client (se tiver logs habilitados)

**Vantagem**: Mostra atividade em tempo real!

#### Opção 2: CloudWatch Logs (Mais técnico)

**Console AWS > CloudWatch > Log groups** > `/aws/iot/`
- Verá logs de conexão
- Mostra autenticação bem-sucedida

### Conceitos Demonstrados
- ✅ mTLS (autenticação mútua)
- ✅ Handshake TLS
- ✅ Validação de certificados bidirecional
- ✅ Conexão criptografada (porta 8883)

### Tempo
~15 segundos

---

## 🎬 CÉLULA 7: TESTE 1 - Tópico PERMITIDO

### O Que Faz
Publica mensagem em tópico que CORRESPONDE à política IoT.

### O Que Falar (Script)

> "Agora vamos ao primeiro teste de segurança.
>
> Vou publicar uma mensagem de temperatura no tópico:
> **`iot/security/demo/sensor01/temperature`**
>
> Nossa política IoT permite publicar em:
> **`iot/security/demo/*`**
>
> Vejam que o tópico **corresponde** ao padrão da política.
>
> Vamos ver o que acontece..."

[Execute a célula]

> "**Autorizado!** A política permitiu a publicação porque o tópico está dentro do escopo definido. A mensagem foi enviada via TLS criptografado."

### Código Principal
```python
allowed_topic = "iot/security/demo/sensor01/temperature"
payload_1 = {
    "device_id": CLIENT_ID,
    "timestamp": datetime.now().isoformat(),
    "temperature": 23.5,
    "humidity": 65.2
}
client.publish(allowed_topic, json.dumps(payload_1), qos=1)
```

### Resultado Esperado
```
🧪 TESTE 1: Publicação em Tópico PERMITIDO

Tópico: iot/security/demo/sensor01/temperature
Política IoT: iot/security/demo/* ✅ MATCH

📤 Publicando...
   ✅ Mensagem 1 publicada

✅ RESULTADO: AUTORIZADO
   ✔️ Política IoT permitiu
   ✔️ Tópico corresponde ao padrão
   ✔️ Dados criptografados via TLS 1.2+
   ✔️ Integridade garantida
```

### Como Validar na AWS EM TEMPO REAL ⭐

**No MQTT Test Client** (que você deixou aberto):

1. **ANTES de executar a célula**:
   - Certifique-se que está subscrito em `#` ou `iot/security/demo/#`

2. **EXECUTE a célula 7**

3. **Você verá a mensagem aparecer no test client:**
   ```json
   Topic: iot/security/demo/sensor01/temperature
   {
     "device_id": "sensor-01",
     "timestamp": "2025-11-21T...",
     "temperature": 23.5,
     "humidity": 65.2
   }
   ```

4. **Mostre para audiência**: "Vejam! A mensagem chegou no AWS IoT Core!"

### Conceitos Demonstrados
- ✅ Política IoT permitindo acesso
- ✅ Publicação autorizada
- ✅ Dados criptografados em trânsito

### Tempo
~15 segundos + validação visual na AWS

---

## 🎬 CÉLULA 8: TESTE 2 - Tópico NEGADO

### ⭐⭐⭐ MOMENTO MAIS IMPORTANTE DA DEMO ⭐⭐⭐

### O Que Faz
Tenta publicar em tópico que NÃO corresponde à política (deve ser bloqueado).

### O Que Falar (Script DETALHADO - Momento-Chave!)

> "**Este é o momento mais importante da demonstração!**
>
> Até agora, demonstrei que o dispositivo está autenticado via mTLS e pode publicar em tópicos autorizados.
>
> **Mas e se o dispositivo tentar acessar algo que NÃO deveria?**
>
> Vou simular um cenário onde:
> - O dispositivo foi comprometido por um atacante, OU
> - Há um bug no código tentando acessar recurso errado
>
> Vou tentar publicar no tópico:
> **`iot/production/data`**
>
> Nossa política permite APENAS:
> **`iot/security/demo/*`**
>
> Vejam que **NÃO corresponde** ao padrão.
>
> **Pergunta para audiência**: O que vocês acham que vai acontecer?
> - O dispositivo está autenticado (mTLS válido)
> - O certificado é legítimo
> - A conexão é segura
>
> Será que vai funcionar?"

[Aguarde respostas da audiência]

> "Vamos descobrir..."

[**EXECUTE A CÉLULA**]

[Aguarde 3 segundos]

> "**NEGADO!** Exatamente o que queríamos!
>
> **Isso é segurança em ação!**
>
> Vejam o que aconteceu:
> 1. ✅ O dispositivo ESTÁ autenticado (mTLS funcionou)
> 2. ✅ O certificado É válido
> 3. ✅ A conexão É segura
> 4. ❌ **MAS** a política IoT BLOQUEOU a operação!
>
> **Por quê?** Porque o tópico está FORA do escopo autorizado.
>
> **Isso demonstra o Princípio do Menor Privilégio:**
> - Autenticação **NÃO é suficiente**
> - Precisamos de **Autorização granular**
> - Se este dispositivo for comprometido, o atacante **NÃO consegue** acessar dados de produção
> - O dano potencial é **LIMITADO** ao escopo definido
>
> **Esta é a diferença entre:**
> - ❌ Sistema sem segurança: Dispositivo comprometido = acesso total
> - ✅ Sistema com segurança: Dispositivo comprometido = dano limitado
>
> **Autenticação** diz: 'Eu sei quem você é'
> **Autorização** diz: 'Mas você só pode fazer ISSO, não aquilo'"

### Código Principal
```python
denied_topic = "iot/production/data"
payload_2 = {
    "device_id": CLIENT_ID,
    "timestamp": datetime.now().isoformat(),
    "data": "Tentativa não autorizada"
}
client.publish(denied_topic, json.dumps(payload_2), qos=1)
```

### Resultado Esperado
```
🧪 TESTE 2: Tópico NÃO PERMITIDO ⭐ MOMENTO-CHAVE DA DEMO

Tópico: iot/production/data
Política IoT: iot/security/demo/*
Match: ❌ NÃO CORRESPONDE

🎯 Objetivo: Demonstrar Princípio do Menor Privilégio

📤 Tentando publicar em tópico fora do escopo...

✅ RESULTADO: NEGADO (como esperado!)

   🔍 Análise de Segurança:
   ✔️ Política IoT BLOQUEOU a operação
   ✔️ Princípio do Menor Privilégio aplicado
   ✔️ Dispositivo limitado ao escopo definido
   ✔️ Tópico fora do padrão = NEGADO

   🛡️ Segurança Demonstrada:
   • Controle de acesso granular por tópico
   • Prevenção de acesso não autorizado
   • Isolamento entre ambientes (demo vs production)
   • Se dispositivo for comprometido, dano é LIMITADO
```

### Como Validar na AWS EM TEMPO REAL ⭐⭐⭐

#### Validação Visual no MQTT Test Client

**No MQTT Test Client:**

1. **ANTES da célula 8**, adicione outra subscrição:
   - Topic filter: `iot/production/#`
   - Subscribe

2. **EXECUTE a célula 8**

3. **O que você verá:**
   - ❌ **NENHUMA mensagem aparece** no tópico `iot/production/data`
   - ✅ Isso comprova visualmente que foi bloqueado!

4. **Mostre para audiência**: 
   > "Vejam no test client: **nenhuma mensagem** chegou no tópico production. O AWS IoT bloqueou antes mesmo de rotear!"

#### Validação nos Logs CloudWatch (Avançado)

**Console AWS > CloudWatch > Log groups** > `/aws/iot/`

Você verá algo como:
```
{
  "timestamp": "2025-11-21...",
  "logLevel": "WARN",
  "eventType": "Publish",
  "clientId": "sensor-01",
  "topic": "iot/production/data",
  "status": "DENIED",
  "reason": "Policy does not allow"
}
```

**Mostre isso** se quiser impressionar audiência técnica!

### Conceitos Demonstrados
- ✅ **Princípio do Menor Privilégio** ⭐⭐⭐
- ✅ Autenticação ≠ Autorização
- ✅ Controle granular de acesso
- ✅ Limitação de danos em caso de comprometimento
- ✅ Segregação de ambientes

### Tempo
~2 minutos (inclui explicação detalhada)

---

## 🎬 CÉLULA 9: TESTE 3 - Subscribe e Receive

### O Que Faz
Demonstra comunicação bidirecional (subscrever + receber mensagens).

### O Que Falar

> "Agora vou demonstrar comunicação bidirecional. Vou subscrever em um tópico de comandos e enviar uma mensagem para mim mesmo. Isso mostra que as políticas controlam tanto a publicação quanto a subscrição."

### Resultado Esperado
```
🧪 TESTE 3: Subscrição e Comunicação Bidirecional

Tópico: iot/security/demo/sensor01/commands

📥 Subscrevendo...
   ✅ Subscrito com sucesso
   
📤 Publicando mensagem de teste...

📨 Mensagem recebida:
   Tópico: iot/security/demo/sensor01/commands
   Payload: {"command": "STATUS_CHECK", ...}

✅ Subscribe/Receive testados
   ✔️ Comunicação bidirecional funcionando
```

### Como Validar na AWS

**MQTT Test Client** mostrará a mensagem chegando.

### Tempo
~15 segundos

---

## 🎬 CÉLULA 10: Resumo dos Conceitos

### O Que Faz
Lista os 6 conceitos de segurança demonstrados.

### O Que Falar

> "Vamos recapitular o que demonstramos aqui. São 6 conceitos fundamentais de segurança em IoT..."

[Leia cada um]

> "O mais importante: vocês viram na prática o **Teste 2** demonstrando que autenticação forte não é suficiente - precisamos de autorização granular para limitar o dano em caso de comprometimento."

### Resultado
Lista dos 6 conceitos.

### Tempo
~1 minuto

---

## 🎬 CÉLULA 11: Desconectar e Finalizar

### O Que Faz
Desconecta do AWS IoT de forma limpa.

### O Que Falar

> "E finalmente, desconecto de forma segura do AWS IoT Core."

### Resultado
```
✅ DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!
```

### Tempo
~5 segundos

---

## 📊 Resumo de Validações na AWS

| Célula | Validação na AWS | Onde Ver |
|--------|------------------|----------|
| 1-4 | Nenhuma | - |
| 5 | Certificado Active + Políticas | IoT Core > Security > Certificates |
| 6 | Conexão estabelecida | MQTT Test Client (activity) |
| 7 | ✅ Mensagem aparece | **MQTT Test Client** ⭐ |
| 8 | ❌ Mensagem NÃO aparece | **MQTT Test Client** ⭐⭐⭐ |
| 9 | ✅ Mensagem aparece | MQTT Test Client |
| 10-11 | Nenhuma | - |

---

## 🎯 Setup PRÉ-APRESENTAÇÃO

### 15 Minutos Antes

1. ✅ **Abrir Console AWS** em aba separada
2. ✅ **Abrir MQTT Test Client**: IoT Core > Test > MQTT test client
3. ✅ **Subscribe em `#`** para capturar todas as mensagens
4. ✅ **Testar demo UMA VEZ** completa
5. ✅ **Posicionar telas**: Jupyter à esquerda, AWS Console à direita
6. ✅ **Tirar screenshots** de backup

### Durante Apresentação

- **Tela 1** (principal): Jupyter Notebook
- **Tela 2** (secundária): AWS MQTT Test Client
- Alternar entre as duas para mostrar validações

---

## 💡 Dicas de Apresentação

### Célula 8 (Teste 2) - Dicas Especiais

1. **Pause antes de executar** - crie suspense
2. **Pergunte à audiência** o que vai acontecer
3. **Execute e aguarde** 3 segundos em silêncio
4. **Mostre entusiasmo** quando aparecer "NEGADO"
5. **Explique em detalhes** - este é o momento-chave
6. **Mostre no MQTT Test Client** que nenhuma mensagem chegou

### Se Algo Der Errado

- **Célula 7 não confirma**: Mostrar screenshots de backup
- **Conexão falha**: Explicar que demonstraria X, Y, Z
- **Use o erro como ensino**: "Vejam, isso mostra a importância de..."

---

## ✅ Checklist Final

Antes de apresentar:

- [ ] MQTT Test Client aberto e subscrito em `#`
- [ ] Demo testada 1x completa
- [ ] Screenshots de backup prontos
- [ ] Telas posicionadas (Jupyter + AWS Console)
- [ ] Script da Célula 8 decorado (é o mais importante!)
- [ ] Água/café à mão
- [ ] Respirar fundo - você está preparado! 🚀

---

## 🎓 Mensagem Final

**A Célula 8 (Teste 2) é o coração da apresentação.**

Se você conseguir explicar bem por que o bloqueio é **POSITIVO** (e não negativo), você terá sucesso na apresentação!

**Boa sorte no MBA FIAP! 🔐🎓**

