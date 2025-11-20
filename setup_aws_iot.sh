#!/bin/bash

###############################################################################
# Script de Setup AWS IoT Core - Demo de Segurança IoT
# MBA FIAP
###############################################################################

set -e  # Exit on error

echo "=========================================="
echo "AWS IoT Security Demo - Setup Script"
echo "=========================================="
echo ""

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Variáveis
CERT_DIR="aws_iot_certs"
POLICY_NAME="SecureIoTDemoPolicy"
THING_NAME="sensor-01-secure"
CLIENT_ID="sensor-01"

# Verificar se AWS CLI está instalado
if ! command -v aws &> /dev/null; then
    echo -e "${RED}❌ AWS CLI não encontrado. Por favor, instale: brew install awscli${NC}"
    exit 1
fi

echo -e "${GREEN}✅ AWS CLI encontrado${NC}"

# Verificar credenciais AWS
echo ""
echo "Verificando credenciais AWS..."
if ! aws sts get-caller-identity &> /dev/null; then
    echo -e "${RED}❌ Credenciais AWS não configuradas. Execute: aws configure${NC}"
    exit 1
fi

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REGION=$(aws configure get region)
echo -e "${GREEN}✅ Credenciais OK - Account: $ACCOUNT_ID, Region: $REGION${NC}"

# Criar diretório para certificados
echo ""
echo "Criando diretório para certificados..."
mkdir -p "$CERT_DIR"
echo -e "${GREEN}✅ Diretório $CERT_DIR criado${NC}"

# Passo 1: Obter endpoint IoT
echo ""
echo "=========================================="
echo "Passo 1: Obtendo AWS IoT Endpoint"
echo "=========================================="
IOT_ENDPOINT=$(aws iot describe-endpoint --endpoint-type iot:Data-ATS --query endpointAddress --output text)
echo -e "${GREEN}✅ Endpoint: $IOT_ENDPOINT${NC}"
echo "$IOT_ENDPOINT" > "$CERT_DIR/iot-endpoint.txt"

# Passo 2: Criar certificado e chaves
echo ""
echo "=========================================="
echo "Passo 2: Criando Certificado e Chaves"
echo "=========================================="

# Verificar se certificado já existe
if [ -f "$CERT_DIR/sensor-01-certificate.pem.crt" ]; then
    echo -e "${YELLOW}⚠️  Certificado já existe. Deseja recriar? (y/n)${NC}"
    read -r response
    if [[ "$response" != "y" ]]; then
        echo "Pulando criação de certificado..."
        CERT_ARN=$(cat "$CERT_DIR/certificate-arn.txt" 2>/dev/null || echo "")
        if [ -z "$CERT_ARN" ]; then
            echo -e "${RED}❌ ARN do certificado não encontrado. Delete os arquivos e execute novamente.${NC}"
            exit 1
        fi
    else
        CREATE_CERT=true
    fi
else
    CREATE_CERT=true
fi

if [ "$CREATE_CERT" = true ]; then
    echo "Criando certificado..."
    CERT_OUTPUT=$(aws iot create-keys-and-certificate \
        --set-as-active \
        --certificate-pem-outfile "$CERT_DIR/sensor-01-certificate.pem.crt" \
        --public-key-outfile "$CERT_DIR/sensor-01-public.pem.key" \
        --private-key-outfile "$CERT_DIR/sensor-01-private.pem.key" \
        --output json)
    
    CERT_ARN=$(echo "$CERT_OUTPUT" | grep -o '"certificateArn": "[^"]*' | sed 's/"certificateArn": "//')
    CERT_ID=$(echo "$CERT_OUTPUT" | grep -o '"certificateId": "[^"]*' | sed 's/"certificateId": "//')
    
    echo "$CERT_ARN" > "$CERT_DIR/certificate-arn.txt"
    echo "$CERT_ID" > "$CERT_DIR/certificate-id.txt"
    
    echo -e "${GREEN}✅ Certificado criado${NC}"
    echo -e "   ARN: ${YELLOW}$CERT_ARN${NC}"
    echo -e "   ID: ${YELLOW}$CERT_ID${NC}"
fi

# Passo 3: Baixar Root CA
echo ""
echo "=========================================="
echo "Passo 3: Baixando Amazon Root CA"
echo "=========================================="
if [ ! -f "$CERT_DIR/AmazonRootCA1.pem" ]; then
    curl -s -o "$CERT_DIR/AmazonRootCA1.pem" \
        https://www.amazontrust.com/repository/AmazonRootCA1.pem
    echo -e "${GREEN}✅ Root CA baixado${NC}"
else
    echo -e "${YELLOW}⚠️  Root CA já existe${NC}"
fi

# Passo 4: Criar política IoT
echo ""
echo "=========================================="
echo "Passo 4: Criando Política IoT"
echo "=========================================="

cat > "$CERT_DIR/iot-policy-secure.json" <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "iot:Connect"
      ],
      "Resource": [
        "arn:aws:iot:${REGION}:${ACCOUNT_ID}:client/sensor-*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "iot:Publish"
      ],
      "Resource": [
        "arn:aws:iot:${REGION}:${ACCOUNT_ID}:topic/iot/security/demo/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "iot:Subscribe"
      ],
      "Resource": [
        "arn:aws:iot:${REGION}:${ACCOUNT_ID}:topicfilter/iot/security/demo/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "iot:Receive"
      ],
      "Resource": [
        "arn:aws:iot:${REGION}:${ACCOUNT_ID}:topic/iot/security/demo/*"
      ]
    }
  ]
}
EOF

# Verificar se política já existe
if aws iot get-policy --policy-name "$POLICY_NAME" &> /dev/null; then
    echo -e "${YELLOW}⚠️  Política $POLICY_NAME já existe${NC}"
else
    aws iot create-policy \
        --policy-name "$POLICY_NAME" \
        --policy-document file://"$CERT_DIR/iot-policy-secure.json"
    echo -e "${GREEN}✅ Política criada: $POLICY_NAME${NC}"
fi

# Passo 5: Anexar política ao certificado
echo ""
echo "=========================================="
echo "Passo 5: Anexando Política ao Certificado"
echo "=========================================="

if aws iot attach-policy --policy-name "$POLICY_NAME" --target "$CERT_ARN" 2>/dev/null; then
    echo -e "${GREEN}✅ Política anexada ao certificado${NC}"
else
    echo -e "${YELLOW}⚠️  Política já estava anexada${NC}"
fi

# Passo 6: Criar Thing e anexar certificado
echo ""
echo "=========================================="
echo "Passo 6: Criando Thing (Dispositivo)"
echo "=========================================="

if aws iot describe-thing --thing-name "$THING_NAME" &> /dev/null; then
    echo -e "${YELLOW}⚠️  Thing $THING_NAME já existe${NC}"
else
    aws iot create-thing --thing-name "$THING_NAME"
    echo -e "${GREEN}✅ Thing criada: $THING_NAME${NC}"
fi

if aws iot attach-thing-principal --thing-name "$THING_NAME" --principal "$CERT_ARN" 2>/dev/null; then
    echo -e "${GREEN}✅ Certificado anexado à Thing${NC}"
else
    echo -e "${YELLOW}⚠️  Certificado já estava anexado à Thing${NC}"
fi

# Criar arquivo de configuração para Snowflake
echo ""
echo "=========================================="
echo "Gerando arquivo de configuração"
echo "=========================================="

cat > "$CERT_DIR/snowflake_config.sql" <<EOF
-- Configuração para Snowflake
-- Execute este SQL no Snowflake após fazer upload dos certificados

-- Criar database e schema
CREATE DATABASE IF NOT EXISTS IOT_SECURITY_DEMO;
CREATE SCHEMA IF NOT EXISTS IOT_SECURITY_DEMO.DEMO;
USE SCHEMA IOT_SECURITY_DEMO.DEMO;

-- Criar stage para certificados
CREATE OR REPLACE STAGE IOT_CERTS_STAGE
  ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');

-- Tabela de configuração
CREATE OR REPLACE TABLE IOT_CONFIG (
  CONFIG_KEY VARCHAR,
  CONFIG_VALUE VARCHAR,
  DESCRIPTION VARCHAR
);

-- Inserir configurações
INSERT INTO IOT_CONFIG VALUES 
  ('AWS_IOT_ENDPOINT', '${IOT_ENDPOINT}', 'AWS IoT Core endpoint'),
  ('AWS_REGION', '${REGION}', 'AWS Region'),
  ('AWS_ACCOUNT_ID', '${ACCOUNT_ID}', 'AWS Account ID'),
  ('THING_NAME', '${THING_NAME}', 'Nome do dispositivo IoT'),
  ('CLIENT_ID', '${CLIENT_ID}', 'Client ID para conexão MQTT'),
  ('CERT_PATH', '@IOT_CERTS_STAGE/sensor-01-certificate.pem.crt', 'Certificado do dispositivo'),
  ('KEY_PATH', '@IOT_CERTS_STAGE/sensor-01-private.pem.key', 'Chave privada'),
  ('ROOT_CA_PATH', '@IOT_CERTS_STAGE/AmazonRootCA1.pem', 'Root CA Amazon');

-- Verificar configurações
SELECT * FROM IOT_CONFIG ORDER BY CONFIG_KEY;
EOF

echo -e "${GREEN}✅ Arquivo de configuração criado: $CERT_DIR/snowflake_config.sql${NC}"

# Resumo final
echo ""
echo "=========================================="
echo "✅ SETUP CONCLUÍDO COM SUCESSO!"
echo "=========================================="
echo ""
echo "📋 Próximos passos:"
echo ""
echo "1. Fazer upload dos certificados para Snowflake:"
echo "   - $CERT_DIR/sensor-01-certificate.pem.crt"
echo "   - $CERT_DIR/sensor-01-private.pem.key"
echo "   - $CERT_DIR/AmazonRootCA1.pem"
echo ""
echo "2. Executar o SQL no Snowflake:"
echo "   - Arquivo: $CERT_DIR/snowflake_config.sql"
echo ""
echo "3. Executar o notebook de demonstração"
echo ""
echo "📝 Informações importantes salvas em:"
echo "   - Endpoint: $CERT_DIR/iot-endpoint.txt"
echo "   - Cert ARN: $CERT_DIR/certificate-arn.txt"
echo "   - Cert ID: $CERT_DIR/certificate-id.txt"
echo "   - SQL Config: $CERT_DIR/snowflake_config.sql"
echo ""
echo -e "${YELLOW}⚠️  IMPORTANTE: Guarde os arquivos .pem em local seguro!${NC}"
echo ""

