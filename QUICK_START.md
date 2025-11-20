# Quick Start - Demo Segurança IoT
## MBA FIAP - Guia Rápido de 5 Minutos ⚡

---

## 🚀 Setup Rápido (10 minutos)

### 1️⃣ Configurar AWS

**⚠️ Escolha seu método:**

#### Opção A: COM AWS CLI (5 min - Automático)
```bash
cd /Users/dmacedo/Documents/Codes/Projects/sec_iot_fiap
./setup_aws_iot.sh
```

#### Opção B: SEM AWS CLI (30 min - Manual via Console Web)
📘 **Siga o guia completo**: `SETUP_VIA_CONSOLE_AWS.md`

Ambos criam:
- ✅ Certificados X.509
- ✅ Políticas IoT
- ✅ Thing (dispositivo)
- ✅ Configuração para Snowflake

### 2️⃣ Configurar Snowflake (5 min)

```sql
-- No Snowflake Worksheet, executar:
-- (O arquivo foi gerado pelo script: aws_iot_certs/snowflake_config.sql)

-- Copiar e colar o conteúdo de snowflake_config.sql
-- Ele criará:
-- - Database: IOT_SECURITY_DEMO
-- - Schema: DEMO
-- - Stage: IOT_CERTS_STAGE
-- - Tabela: IOT_CONFIG
```

### 3️⃣ Upload de Certificados

**Opção A - Via SnowSQL (Linha de Comando)**:
```bash
export SNOWSQL_PRIVATE_KEY_PASSPHRASE="[seu_passphrase]"
snowsql -d IOT_SECURITY_DEMO -s DEMO -q "
PUT file://aws_iot_certs/sensor-01-certificate.pem.crt @IOT_CERTS_STAGE AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
PUT file://aws_iot_certs/sensor-01-private.pem.key @IOT_CERTS_STAGE AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
PUT file://aws_iot_certs/AmazonRootCA1.pem @IOT_CERTS_STAGE AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
"
```

**Opção B - Via Snowsight UI**:
1. Navegue: Data > Databases > IOT_SECURITY_DEMO > DEMO > Stages > IOT_CERTS_STAGE
2. Clique "+ Files"
3. Faça upload dos 3 arquivos:
   - `sensor-01-certificate.pem.crt`
   - `sensor-01-private.pem.key`
   - `AmazonRootCA1.pem`

### 4️⃣ Executar Demo

1. Abra Snowflake: Projects > Notebooks
2. Crie novo notebook Python
3. Conecte ao DB: `IOT_SECURITY_DEMO`, Schema: `DEMO`
4. Copie código de `iot_security_demo.py`
5. Execute célula por célula

---

## 📁 Estrutura de Arquivos

```
sec_iot_fiap/
├── README.md                    # 📘 Documentação completa
├── QUICK_START.md              # ⚡ Este arquivo
├── CONCEITOS_SEGURANCA.md      # 📚 Teoria detalhada
├── GUIA_APRESENTACAO.md        # 🎤 Roteiro para apresentar
├── ARQUITETURA.md              # 🏗️ Diagramas técnicos
│
├── setup_aws_iot.sh            # 🔧 Setup automático AWS
├── cleanup_aws_iot.sh          # 🧹 Limpeza de recursos
│
├── iot_security_demo.py        # 🐍 Código Python principal
├── iot_security_demo.ipynb     # 📓 Notebook Jupyter (formato alternativo)
│
└── aws_iot_certs/              # 🔐 Certificados (criado pelo setup)
    ├── sensor-01-certificate.pem.crt
    ├── sensor-01-private.pem.key
    ├── AmazonRootCA1.pem
    ├── iot-policy-secure.json
    ├── snowflake_config.sql
    └── iot-endpoint.txt
```

---

## 🎯 O Que a Demo Demonstra

| Teste | O Que Faz | Resultado Esperado | Conceito |
|-------|-----------|-------------------|----------|
| **Conexão** | Conecta ao AWS IoT via mTLS | ✅ Conectado | Autenticação Mútua |
| **Teste 1** | Publica em tópico **permitido** | ✅ Autorizado | Política corresponde |
| **Teste 2** | Publica em tópico **negado** | ❌ Negado | Menor Privilégio |
| **Teste 3** | Subscribe e recebe mensagem | ✅ Funciona | Comunicação bidirecional |

---

## 🔐 Conceitos-Chave (1 Frase Cada)

| Conceito | Definição em 1 Frase |
|----------|---------------------|
| **mTLS** | Cliente e servidor se autenticam mutuamente com certificados |
| **X.509** | Padrão internacional para certificados digitais (identidade) |
| **IoT Policy** | JSON que define o que cada dispositivo pode fazer |
| **TLS 1.2+** | Protocolo de criptografia para segurança em trânsito |
| **Menor Privilégio** | Cada entidade tem apenas permissões mínimas necessárias |
| **Defense in Depth** | Múltiplas camadas de segurança, não apenas uma |

---

## 🐛 Troubleshooting Rápido

### Erro: "Connection failed"
- ✅ Verificar endpoint AWS IoT está correto
- ✅ Certificados foram uploaded no Snowflake
- ✅ Certificado está ATIVO no AWS IoT (não INACTIVE)

### Erro: "Publish denied"
- ✅ Política está anexada ao certificado
- ✅ Tópico corresponde ao padrão da política
- ✅ Thing está vinculada ao certificado

### Erro: "Certificate not found"
- ✅ Certificados foram uploaded com `AUTO_COMPRESS=FALSE`
- ✅ Nomes dos arquivos estão corretos na tabela IOT_CONFIG

---

## 🧹 Limpeza (Após Apresentação)

```bash
# Deletar recursos AWS
./cleanup_aws_iot.sh

# Deletar database Snowflake
# No Snowflake:
DROP DATABASE IOT_SECURITY_DEMO;
```

---

## 📊 Checklist Pré-Apresentação

- [ ] Script `setup_aws_iot.sh` executado com sucesso
- [ ] 3 certificados no diretório `aws_iot_certs/`
- [ ] SQL de configuração executado no Snowflake
- [ ] 3 arquivos uploaded no stage IOT_CERTS_STAGE
- [ ] Tabela IOT_CONFIG tem 8 linhas de configuração
- [ ] Notebook Snowflake criado e testado UMA VEZ
- [ ] Screenshots de backup (caso demo falhe ao vivo)
- [ ] Slides de apresentação prontos

---

## 🎤 Roteiro de Apresentação (5 min)

1. **Contexto** (1 min): Por que segurança IoT é crítica
2. **Conceitos** (1 min): mTLS, X.509, Políticas
3. **Demo Parte 1** (1 min): Conectar (mTLS em ação)
4. **Demo Parte 2** (1 min): Teste tópico permitido ✅
5. **Demo Parte 3** (1 min): Teste tópico negado ❌ ⭐ **MOMENTO-CHAVE**

**Mensagem Final**: "Segurança IoT = Múltiplas camadas. Não basta autenticar, precisa autorizar. Não basta criptografar, precisa auditar."

---

## 🆘 Suporte Durante Apresentação

**Se a demo falhar ao vivo:**
1. 🆘 Mantenha a calma
2. 🆘 Mostre screenshots de backup
3. 🆘 Explique o que DEVERIA acontecer
4. 🆘 Use o erro como exemplo: "Por isso testes são importantes!"

---

## 📞 Informações Úteis

| Item | Valor |
|------|-------|
| **Região AWS sugerida** | us-east-1 (N. Virginia) |
| **Porta MQTT/TLS** | 8883 |
| **Versão TLS mínima** | 1.2 |
| **Algoritmo de certificado** | RSA 2048 bits |
| **Formato de certificado** | X.509 v3 |
| **Tempo de setup** | ~10 minutos |
| **Tempo de apresentação** | 20-30 minutos |
| **Custo AWS (demo)** | R$ 0,00 (Free Tier) |

---

## ✅ Validação Final

Antes da apresentação, execute este teste:

```bash
# 1. Verificar certificados existem
ls -la aws_iot_certs/

# Deve mostrar:
# - sensor-01-certificate.pem.crt
# - sensor-01-private.pem.key  
# - AmazonRootCA1.pem

# 2. Verificar conexão AWS
aws iot describe-thing --thing-name sensor-01-secure

# Deve retornar JSON com detalhes da Thing

# 3. Testar conexão (via mosquitto_pub, opcional)
# Ou simplesmente executar o notebook uma vez
```

---

## 🎓 Boa Sorte na Apresentação!

**Lembre-se**:
- ✅ Você está **preparado**
- ✅ A demo foi **testada**
- ✅ Você entende os **conceitos**
- ✅ Tem **backup** se algo falhar

**Confiança é 🔑!**

---

**MBA FIAP - Sucesso na sua apresentação! 🚀🔐**

