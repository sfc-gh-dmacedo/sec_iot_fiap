# Demo de Segurança em IoT - AWS IoT Core + Snowflake
## MBA FIAP - Demonstração de Segurança em Internet das Coisas

---

## 📋 Visão Geral

Esta demonstração foca nos aspectos de **segurança em IoT** utilizando:
- **AWS IoT Core** - Plataforma gerenciada de IoT da AWS
- **Snowflake Notebooks** - Para execução do código Python de demonstração
- **Protocolo MQTT sobre TLS** - Comunicação segura
- **Certificados X.509** - Autenticação mútua

### Conceitos de Segurança Demonstrados:
1. **Autenticação Mútua TLS (mTLS)** - Cliente e servidor se autenticam
2. **Certificados X.509** - Identidade digital dos dispositivos
3. **Políticas IoT (IoT Policies)** - Controle de acesso granular
4. **Criptografia em Trânsito** - Dados criptografados via TLS 1.2+
5. **Princípio do Menor Privilégio** - Permissões mínimas necessárias
6. **Segregação de Acesso** - Diferentes níveis de permissão por dispositivo

---

## 🎯 Pré-requisitos

### 1. Conta AWS
- Conta AWS ativa (pode usar Free Tier)
- Acesso ao console AWS
- Permissões para criar recursos no AWS IoT Core

### 2. AWS CLI Instalado
```bash
# MacOS
brew install awscli

# Configurar credenciais
aws configure
```

### 3. Snowflake
- Conta Snowflake ativa
- Acesso a Notebooks (Snowpark)
- Permissões para criar stages e executar notebooks

### 4. Ferramentas Locais (para setup)
- Python 3.8+ instalado localmente (apenas para setup inicial)
- Terminal/Shell access

---

## 🚀 Parte 1: Configuração na AWS

### ⚠️ IMPORTANTE: Escolha Seu Método de Setup

**Você tem 2 opções:**

#### Opção A: Setup Automático (COM acesso ao AWS CLI)
- Use o script: `./setup_aws_iot.sh`
- Mais rápido (~5 minutos)
- Veja instruções abaixo

#### Opção B: Setup Manual (SEM acesso ao AWS CLI - APENAS Console Web)
- 📘 **Siga o guia completo**: `SETUP_VIA_CONSOLE_AWS.md`
- Mais detalhado (~30 minutos)
- Passo a passo com interface web

---

### Opção A: Setup com AWS CLI

### Passo 1: Obter o Endpoint do AWS IoT

```bash
# Obter o endpoint único da sua conta AWS IoT
aws iot describe-endpoint --endpoint-type iot:Data-ATS
```

Anote o endpoint retornado (formato: `XXXXXX-ats.iot.REGION.amazonaws.com`)

### Passo 2: Criar Certificados e Chaves

Execute os comandos abaixo para criar certificados para dispositivos:

```bash
# Criar diretório para certificados
mkdir -p aws_iot_certs

# Criar certificado para dispositivo "sensor-01"
aws iot create-keys-and-certificate \
  --set-as-active \
  --certificate-pem-outfile aws_iot_certs/sensor-01-certificate.pem.crt \
  --public-key-outfile aws_iot_certs/sensor-01-public.pem.key \
  --private-key-outfile aws_iot_certs/sensor-01-private.pem.key

# Salvar o certificateArn retornado - você precisará dele
```

**IMPORTANTE**: Anote o `certificateArn` retornado. Exemplo:
```
arn:aws:iot:us-east-1:123456789012:cert/abc123...
```

### Passo 3: Baixar o Certificado Root da AWS

```bash
# Download do certificado raiz da Amazon (AmazonRootCA1)
curl -o aws_iot_certs/AmazonRootCA1.pem \
  https://www.amazontrust.com/repository/AmazonRootCA1.pem
```

### Passo 4: Criar Política IoT (IoT Policy)

Esta política define o que o dispositivo pode fazer. Crie um arquivo JSON:

```bash
cat > aws_iot_certs/iot-policy-secure.json <<'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "iot:Connect"
      ],
      "Resource": [
        "arn:aws:iot:REGION:ACCOUNT_ID:client/sensor-*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "iot:Publish"
      ],
      "Resource": [
        "arn:aws:iot:REGION:ACCOUNT_ID:topic/iot/security/demo/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "iot:Subscribe"
      ],
      "Resource": [
        "arn:aws:iot:REGION:ACCOUNT_ID:topicfilter/iot/security/demo/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "iot:Receive"
      ],
      "Resource": [
        "arn:aws:iot:REGION:ACCOUNT_ID:topic/iot/security/demo/*"
      ]
    }
  ]
}
EOF
```

**Substitua REGION e ACCOUNT_ID** pelos seus valores:
- REGION: sua região AWS (ex: us-east-1)
- ACCOUNT_ID: seu ID da conta AWS (12 dígitos)

```bash
# Criar a política no AWS IoT
aws iot create-policy \
  --policy-name SecureIoTDemoPolicy \
  --policy-document file://aws_iot_certs/iot-policy-secure.json
```

### Passo 5: Anexar Política ao Certificado

```bash
# Substituir CERTIFICATE_ARN pelo ARN anotado no Passo 2
aws iot attach-policy \
  --policy-name SecureIoTDemoPolicy \
  --target "CERTIFICATE_ARN"
```

### Passo 6: Criar uma Thing (Coisa/Dispositivo)

```bash
# Criar a Thing
aws iot create-thing --thing-name sensor-01-secure

# Anexar certificado à Thing
aws iot attach-thing-principal \
  --thing-name sensor-01-secure \
  --principal "CERTIFICATE_ARN"
```

---

## 📊 Parte 2: Configuração no Snowflake

### Passo 1: Criar Database e Schema

```sql
-- No Snowflake Worksheet
CREATE DATABASE IF NOT EXISTS IOT_SECURITY_DEMO;
CREATE SCHEMA IF NOT EXISTS IOT_SECURITY_DEMO.DEMO;
USE SCHEMA IOT_SECURITY_DEMO.DEMO;
```

### Passo 2: Criar Stage para Certificados

```sql
-- Criar stage interno para armazenar certificados
CREATE OR REPLACE STAGE IOT_CERTS_STAGE
  ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');
```

### Passo 3: Upload dos Certificados

Você precisa fazer upload dos certificados para o stage. Use SnowSQL ou Snowsight:

```bash
# Usando SnowSQL (ajuste o passphrase conforme sua configuração)
export SNOWSQL_PRIVATE_KEY_PASSPHRASE="[seu_passphrase]"

# Upload dos certificados
snowsql -d IOT_SECURITY_DEMO -s DEMO -q "
PUT file://aws_iot_certs/sensor-01-certificate.pem.crt @IOT_CERTS_STAGE AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
PUT file://aws_iot_certs/sensor-01-private.pem.key @IOT_CERTS_STAGE AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
PUT file://aws_iot_certs/AmazonRootCA1.pem @IOT_CERTS_STAGE AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
"
```

**Alternativa via Snowsight UI:**
1. Navegue até Data > Databases > IOT_SECURITY_DEMO > DEMO > Stages > IOT_CERTS_STAGE
2. Clique em "+ Files" e faça upload dos 3 arquivos

### Passo 4: Criar Tabela para Configuração

```sql
-- Tabela para armazenar configurações (endpoint, etc)
CREATE OR REPLACE TABLE IOT_CONFIG (
  CONFIG_KEY VARCHAR,
  CONFIG_VALUE VARCHAR,
  DESCRIPTION VARCHAR
);

-- Inserir configurações (AJUSTE SEU ENDPOINT)
INSERT INTO IOT_CONFIG VALUES 
  ('AWS_IOT_ENDPOINT', 'XXXXXX-ats.iot.REGION.amazonaws.com', 'AWS IoT Core endpoint'),
  ('AWS_REGION', 'us-east-1', 'AWS Region'),
  ('CERT_PATH', '@IOT_CERTS_STAGE/sensor-01-certificate.pem.crt', 'Certificado do dispositivo'),
  ('KEY_PATH', '@IOT_CERTS_STAGE/sensor-01-private.pem.key', 'Chave privada'),
  ('ROOT_CA_PATH', '@IOT_CERTS_STAGE/AmazonRootCA1.pem', 'Root CA Amazon');
```

---

## 🔐 Parte 3: Executar a Demonstração

### Abrir o Notebook

1. No Snowflake, navegue até **Projects > Notebooks**
2. Crie um novo notebook Python
3. Conecte ao database `IOT_SECURITY_DEMO` e schema `DEMO`
4. Copie e execute o código do arquivo `iot_security_demo.ipynb`

### O que a Demo Demonstra

A demonstração cobre os seguintes aspectos de segurança:

1. **Conexão Segura com mTLS**
   - Autenticação bidirecional usando certificados X.509
   - Validação de identidade do cliente e servidor

2. **Testes de Autorização**
   - Tentativa de publicar em tópico permitido ✅
   - Tentativa de publicar em tópico negado ❌
   - Demonstra o princípio do menor privilégio

3. **Criptografia de Dados**
   - Todo tráfego via TLS 1.2+
   - Dados sensíveis criptografados em trânsito

4. **Auditoria e Monitoramento**
   - Logs de conexão e atividades
   - Shadow documents para estado dos dispositivos

---

## 📚 Conceitos de Segurança Explicados

### 1. Autenticação Mútua TLS (mTLS)
- **Cliente autentica servidor**: Valida certificado da AWS
- **Servidor autentica cliente**: Valida certificado do dispositivo
- **Benefício**: Garante que ambas as partes são quem dizem ser

### 2. Certificados X.509
- **Padrão internacional** para identidade digital
- **Contém**: Chave pública, identidade, assinatura digital
- **Único por dispositivo**: Cada IoT tem seu próprio certificado

### 3. Políticas de Acesso Granular
- **Baseadas em JSON**: Definem permissões detalhadas
- **Recursos específicos**: Controla tópicos MQTT permitidos
- **Ações limitadas**: Connect, Publish, Subscribe, Receive

### 4. Princípio do Menor Privilégio
- Dispositivos só têm permissões estritamente necessárias
- Reduz superfície de ataque em caso de comprometimento

### 5. Segregação por Tópicos
- Diferentes dispositivos acessam diferentes tópicos
- Impede que um dispositivo comprometido acesse dados de outros

---

## 🛡️ Melhores Práticas de Segurança Demonstradas

1. ✅ **Nunca compartilhar chaves privadas** - Cada dispositivo tem a sua
2. ✅ **Rotação de certificados** - Política de renovação periódica
3. ✅ **Monitoramento contínuo** - AWS IoT Device Defender
4. ✅ **Criptografia em repouso** - Certificados criptografados no Snowflake
5. ✅ **Validação de identidade** - mTLS obrigatório
6. ✅ **Políticas restritivas** - Permissões mínimas necessárias

---

## 🧹 Limpeza de Recursos (Após a Demo)

Para evitar custos, delete os recursos criados:

```bash
# Detach política do certificado
aws iot detach-policy --policy-name SecureIoTDemoPolicy --target "CERTIFICATE_ARN"

# Detach certificado da thing
aws iot detach-thing-principal --thing-name sensor-01-secure --principal "CERTIFICATE_ARN"

# Desativar e deletar certificado
aws iot update-certificate --certificate-id CERT_ID --new-status INACTIVE
aws iot delete-certificate --certificate-id CERT_ID --force-delete

# Deletar thing
aws iot delete-thing --thing-name sensor-01-secure

# Deletar política
aws iot delete-policy --policy-name SecureIoTDemoPolicy
```

No Snowflake:
```sql
DROP DATABASE IOT_SECURITY_DEMO;
```

---

## 📖 Referências

- [AWS IoT Core Security Best Practices](https://docs.aws.amazon.com/iot/latest/developerguide/security-best-practices.html)
- [X.509 Certificates and AWS IoT](https://docs.aws.amazon.com/iot/latest/developerguide/x509-client-certs.html)
- [MQTT Protocol Specification](https://mqtt.org/mqtt-specification/)
- [TLS/SSL Protocol](https://www.ssl.com/faqs/what-is-ssl/)

---

## 📧 Suporte

Para dúvidas sobre esta demonstração, consulte a documentação oficial da AWS IoT Core e Snowflake.

**Boa apresentação no MBA FIAP! 🎓**

