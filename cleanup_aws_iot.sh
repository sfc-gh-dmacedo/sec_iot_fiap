#!/bin/bash

###############################################################################
# Script de Cleanup AWS IoT Core - Demo de Segurança IoT
# Remove todos os recursos criados
###############################################################################

set -e

echo "=========================================="
echo "AWS IoT Security Demo - Cleanup Script"
echo "=========================================="
echo ""

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Variáveis
CERT_DIR="aws_iot_certs"
POLICY_NAME="SecureIoTDemoPolicy"
THING_NAME="sensor-01-secure"

# Confirmação
echo -e "${RED}⚠️  ATENÇÃO: Este script irá deletar TODOS os recursos da demo AWS IoT${NC}"
echo ""
echo "Recursos a serem deletados:"
echo "  - Thing: $THING_NAME"
echo "  - Política: $POLICY_NAME"
echo "  - Certificados e chaves"
echo ""
read -p "Tem certeza que deseja continuar? (digite 'SIM' para confirmar): " confirm

if [ "$confirm" != "SIM" ]; then
    echo "Operação cancelada."
    exit 0
fi

echo ""
echo "Iniciando limpeza..."

# Ler ARN e ID do certificado
if [ -f "$CERT_DIR/certificate-arn.txt" ]; then
    CERT_ARN=$(cat "$CERT_DIR/certificate-arn.txt")
    CERT_ID=$(cat "$CERT_DIR/certificate-id.txt")
    echo "Certificado encontrado: $CERT_ID"
else
    echo -e "${YELLOW}⚠️  Arquivo de certificado não encontrado. Pulando...${NC}"
    CERT_ARN=""
    CERT_ID=""
fi

# Detach política do certificado
if [ -n "$CERT_ARN" ]; then
    echo ""
    echo "Desanexando política do certificado..."
    if aws iot detach-policy --policy-name "$POLICY_NAME" --target "$CERT_ARN" 2>/dev/null; then
        echo -e "${GREEN}✅ Política desanexada${NC}"
    else
        echo -e "${YELLOW}⚠️  Política já estava desanexada ou não existe${NC}"
    fi
fi

# Detach certificado da thing
if [ -n "$CERT_ARN" ]; then
    echo ""
    echo "Desanexando certificado da Thing..."
    if aws iot detach-thing-principal --thing-name "$THING_NAME" --principal "$CERT_ARN" 2>/dev/null; then
        echo -e "${GREEN}✅ Certificado desanexado da Thing${NC}"
    else
        echo -e "${YELLOW}⚠️  Certificado já estava desanexado ou não existe${NC}"
    fi
fi

# Deletar Thing
echo ""
echo "Deletando Thing..."
if aws iot delete-thing --thing-name "$THING_NAME" 2>/dev/null; then
    echo -e "${GREEN}✅ Thing deletada${NC}"
else
    echo -e "${YELLOW}⚠️  Thing não existe ou já foi deletada${NC}"
fi

# Desativar e deletar certificado
if [ -n "$CERT_ID" ]; then
    echo ""
    echo "Desativando certificado..."
    if aws iot update-certificate --certificate-id "$CERT_ID" --new-status INACTIVE 2>/dev/null; then
        echo -e "${GREEN}✅ Certificado desativado${NC}"
    else
        echo -e "${YELLOW}⚠️  Certificado já estava inativo${NC}"
    fi
    
    echo "Deletando certificado..."
    if aws iot delete-certificate --certificate-id "$CERT_ID" --force-delete 2>/dev/null; then
        echo -e "${GREEN}✅ Certificado deletado${NC}"
    else
        echo -e "${YELLOW}⚠️  Erro ao deletar certificado${NC}"
    fi
fi

# Deletar política
echo ""
echo "Deletando política..."

# Listar todas as versões da política e deletar (exceto a default)
POLICY_VERSIONS=$(aws iot list-policy-versions --policy-name "$POLICY_NAME" --query 'policyVersions[?!isDefaultVersion].versionId' --output text 2>/dev/null || echo "")
if [ -n "$POLICY_VERSIONS" ]; then
    for VERSION in $POLICY_VERSIONS; do
        echo "  Deletando versão $VERSION..."
        aws iot delete-policy-version --policy-name "$POLICY_NAME" --policy-version-id "$VERSION" 2>/dev/null || true
    done
fi

if aws iot delete-policy --policy-name "$POLICY_NAME" 2>/dev/null; then
    echo -e "${GREEN}✅ Política deletada${NC}"
else
    echo -e "${YELLOW}⚠️  Política não existe ou já foi deletada${NC}"
fi

# Deletar arquivos locais
echo ""
echo "Deletando arquivos locais..."
read -p "Deseja deletar o diretório $CERT_DIR com todos os certificados? (y/n): " delete_files

if [ "$delete_files" = "y" ]; then
    if [ -d "$CERT_DIR" ]; then
        rm -rf "$CERT_DIR"
        echo -e "${GREEN}✅ Diretório $CERT_DIR deletado${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Diretório $CERT_DIR mantido${NC}"
fi

# Mensagem final
echo ""
echo "=========================================="
echo "✅ LIMPEZA CONCLUÍDA!"
echo "=========================================="
echo ""
echo "📋 Lembre-se de limpar também no Snowflake:"
echo ""
echo "DROP DATABASE IOT_SECURITY_DEMO;"
echo ""
echo -e "${GREEN}Todos os recursos AWS IoT foram removidos.${NC}"
echo ""

