# Setup Via Console AWS - Guia Completo
## Configuração Manual de Segurança IoT (SEM linha de comando)

---

## 📋 Visão Geral

Este guia mostra como configurar TODOS os recursos AWS IoT usando apenas o **Console AWS** (interface web), ideal para quem não tem acesso ao AWS CLI.

**Tempo estimado**: 30-40 minutos  
**Custo**: R$ 0,00 (Free Tier)

---

## 🌐 Parte 1: Acesso ao Console AWS

### Passo 1.1: Login no Console

1. Acesse: https://console.aws.amazon.com/
2. Faça login com suas credenciais
3. Verifique que está na região correta (recomendado: **us-east-1** - N. Virginia)
   - Canto superior direito, ao lado do nome do usuário
   - Se não estiver em us-east-1, clique e selecione **US East (N. Virginia)**

**✅ Checkpoint**: Você deve ver o painel principal da AWS com vários serviços.

---

## 🔐 Parte 2: Criar Certificados e Chaves no AWS IoT Core

### Passo 2.1: Acessar AWS IoT Core

1. No console AWS, clique na barra de busca (topo)
2. Digite: `IoT Core`
3. Clique em **IoT Core** nos resultados

**OU** navegue: Serviços > Internet das Coisas > IoT Core

### Passo 2.2: Criar Certificado

1. No menu lateral esquerdo, expanda **Segurança** (Security)
2. Clique em **Certificados** (Certificates)
3. Clique no botão **Criar certificado** (Create certificate)
4. Selecione: **Criar certificado com geração automática** (Create certificate)
5. Clique em **Criar** (Create)

### Passo 2.3: Baixar Certificados

⚠️ **IMPORTANTE**: Esta é a ÚNICA chance de baixar a chave privada!

Na tela de confirmação, baixe 3 arquivos:

1. **Certificado do dispositivo** (Device certificate)
   - Clique em "Download" ao lado de "Certificado do dispositivo"
   - Salve como: `sensor-01-certificate.pem.crt`

2. **Chave privada** (Private key file)
   - Clique em "Download" ao lado de "Chave privada"
   - Salve como: `sensor-01-private.pem.key`

3. **Certificado CA raiz** (Root CA certificate)
   - Role a página para baixo
   - Clique em "Download" ao lado de "Amazon Root CA 1"
   - Salve como: `AmazonRootCA1.pem`

4. **IMPORTANTE**: Anote o **ARN do certificado**
   - Exemplo: `arn:aws:iot:us-east-1:123456789012:cert/abcdef123456...`
   - Copie e cole em um bloco de notas

5. Clique em **Ativar** (Activate) - O certificado precisa estar ATIVO
6. Clique em **Concluído** (Done)

**✅ Checkpoint**: Você tem 3 arquivos baixados e o ARN anotado.

---

## 📝 Parte 3: Criar Política de Segurança (IoT Policy)

### Passo 3.1: Navegar para Políticas

1. No menu lateral esquerdo, ainda em **Segurança** (Security)
2. Clique em **Políticas** (Policies)
3. Clique no botão **Criar política** (Create policy)

### Passo 3.2: Configurar a Política

**Nome da política**: `SecureIoTDemoPolicy`

**JSON da política**: Copie e cole o seguinte (AJUSTE REGION e ACCOUNT_ID):

```json
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
```

### Passo 3.3: Como Descobrir REGION e ACCOUNT_ID

**REGION**: 
- Se você está em us-east-1, use: `us-east-1`
- Veja no canto superior direito do console

**ACCOUNT_ID** (ID da sua conta - 12 dígitos):
- Clique no seu nome de usuário (canto superior direito)
- O número de 12 dígitos que aparece é seu Account ID
- Exemplo: `123456789012`

### Passo 3.4: Criar a Política

1. Cole o JSON **com REGION e ACCOUNT_ID corretos**
2. Clique em **Criar** (Create)

**✅ Checkpoint**: Política `SecureIoTDemoPolicy` aparece na lista.

---

## 🔗 Parte 4: Anexar Política ao Certificado

### Passo 4.1: Voltar aos Certificados

1. Menu lateral: **Segurança** > **Certificados**
2. Encontre o certificado que você criou (deve estar marcado como ATIVO)
3. Clique no certificado (na linha inteira)

### Passo 4.2: Anexar a Política

1. Na página do certificado, clique na aba **Políticas** (Policies)
2. Clique no botão **Anexar políticas** (Attach policies)
3. Marque a caixa ao lado de `SecureIoTDemoPolicy`
4. Clique em **Anexar** (Attach)

**✅ Checkpoint**: Você deve ver `SecureIoTDemoPolicy` listada na aba Políticas do certificado.

---

## 🔌 Parte 5: Criar Thing (Dispositivo IoT)

### Passo 5.1: Navegar para Things

1. Menu lateral esquerdo: **Gerenciar** (Manage) > **Todas as coisas** (All devices > Things)
2. Clique em **Criar things** (Create things)

### Passo 5.2: Tipo de Criação

1. Selecione: **Criar uma coisa individual** (Create single thing)
2. Clique em **Próximo** (Next)

### Passo 5.3: Propriedades da Thing

1. **Nome da thing**: `sensor-01-secure`
2. Role para baixo
3. **Deixe os outros campos como padrão** (não precisa preencher)
4. Clique em **Próximo** (Next)

### Passo 5.4: Configurar Certificado

1. Selecione: **Usar certificado existente** (Use existing certificate)
2. Marque a caixa do certificado que você criou antes
   - (Será listado pelo ARN ou ID)
3. Clique em **Criar thing** (Create thing)

**✅ Checkpoint**: Thing `sensor-01-secure` aparece na lista de Things.

---

## 📡 Parte 6: Obter o Endpoint do AWS IoT

### Passo 6.1: Acessar Configurações

1. Menu lateral esquerdo: **Configurações** (Settings) - geralmente no final da lista
2. Na seção **Ponto de extremidade do dispositivo** (Device data endpoint), você verá um endereço
3. **Copie este endereço** (exemplo: `a1b2c3d4e5f6g7-ats.iot.us-east-1.amazonaws.com`)
4. **Salve em um bloco de notas** - você precisará dele!

**✅ Checkpoint**: Você tem o endpoint anotado (formato: `XXXXX-ats.iot.REGION.amazonaws.com`)

---

## 💾 Parte 7: Organizar Arquivos Baixados

### Passo 7.1: Criar Pasta Local

No seu computador (Mac):

1. Abra o Finder
2. Navegue até: `/Users/dmacedo/Documents/Codes/Projects/sec_iot_fiap`
3. Crie uma pasta chamada: `aws_iot_certs`
4. Mova os 3 arquivos baixados para esta pasta:
   - `sensor-01-certificate.pem.crt`
   - `sensor-01-private.pem.key`
   - `AmazonRootCA1.pem`

### Passo 7.2: Criar Arquivo de Configuração

Na mesma pasta `aws_iot_certs`, crie um arquivo chamado `config.txt` com o seguinte conteúdo:

```
=== CONFIGURAÇÃO AWS IoT ===

Endpoint: [COLE SEU ENDPOINT AQUI]
Region: us-east-1
Account ID: [COLE SEU ACCOUNT ID AQUI]
Thing Name: sensor-01-secure
Client ID: sensor-01
Certificate ARN: [COLE O ARN DO CERTIFICADO AQUI]

Política: SecureIoTDemoPolicy
Certificado: sensor-01-certificate.pem.crt
Chave Privada: sensor-01-private.pem.key
Root CA: AmazonRootCA1.pem
```

**✅ Checkpoint**: Você tem uma pasta organizada com 4 arquivos (3 certificados + 1 config).

---

## ❄️ Parte 8: Configurar Snowflake

### Passo 8.1: Criar Database e Schema

1. Acesse o Snowflake via navegador: https://app.snowflake.com/
2. Faça login
3. Clique em **Worksheets** (menu lateral)
4. Crie um novo worksheet
5. Cole e execute o seguinte SQL:

```sql
-- Criar database
CREATE DATABASE IF NOT EXISTS IOT_SECURITY_DEMO;

-- Usar database
USE DATABASE IOT_SECURITY_DEMO;

-- Criar schema
CREATE SCHEMA IF NOT EXISTS DEMO;

-- Usar schema
USE SCHEMA DEMO;
```

### Passo 8.2: Criar Stage para Certificados

Execute este SQL:

```sql
-- Criar stage interno com criptografia
CREATE OR REPLACE STAGE IOT_CERTS_STAGE
  ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');
```

### Passo 8.3: Upload de Certificados via Interface

**Opção 1 - Via Snowsight UI** (Mais fácil):

1. No menu lateral, clique em **Data** > **Databases**
2. Navegue: `IOT_SECURITY_DEMO` > `DEMO` > `Stages` > `IOT_CERTS_STAGE`
3. Clique no botão **+ Files** (canto superior direito)
4. Faça upload dos 3 arquivos:
   - `sensor-01-certificate.pem.crt`
   - `sensor-01-private.pem.key`
   - `AmazonRootCA1.pem`
5. Clique em **Upload**

**Opção 2 - Via SQL** (se tiver SnowSQL configurado):

Se você tiver SnowSQL configurado, pode executar:

```sql
PUT file:///Users/dmacedo/Documents/Codes/Projects/sec_iot_fiap/aws_iot_certs/sensor-01-certificate.pem.crt @IOT_CERTS_STAGE AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
PUT file:///Users/dmacedo/Documents/Codes/Projects/sec_iot_fiap/aws_iot_certs/sensor-01-private.pem.key @IOT_CERTS_STAGE AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
PUT file:///Users/dmacedo/Documents/Codes/Projects/sec_iot_fiap/aws_iot_certs/AmazonRootCA1.pem @IOT_CERTS_STAGE AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
```

### Passo 8.4: Criar Tabela de Configuração

Execute este SQL (SUBSTITUA os valores):

```sql
-- Criar tabela de configuração
CREATE OR REPLACE TABLE IOT_CONFIG (
  CONFIG_KEY VARCHAR,
  CONFIG_VALUE VARCHAR,
  DESCRIPTION VARCHAR
);

-- Inserir configurações (AJUSTE OS VALORES!)
INSERT INTO IOT_CONFIG VALUES 
  ('AWS_IOT_ENDPOINT', 'SEU-ENDPOINT-AQUI.iot.us-east-1.amazonaws.com', 'AWS IoT Core endpoint'),
  ('AWS_REGION', 'us-east-1', 'AWS Region'),
  ('AWS_ACCOUNT_ID', 'SEU-ACCOUNT-ID-AQUI', 'AWS Account ID'),
  ('THING_NAME', 'sensor-01-secure', 'Nome do dispositivo IoT'),
  ('CLIENT_ID', 'sensor-01', 'Client ID para conexão MQTT'),
  ('CERT_PATH', '@IOT_CERTS_STAGE/sensor-01-certificate.pem.crt', 'Certificado do dispositivo'),
  ('KEY_PATH', '@IOT_CERTS_STAGE/sensor-01-private.pem.key', 'Chave privada'),
  ('ROOT_CA_PATH', '@IOT_CERTS_STAGE/AmazonRootCA1.pem', 'Root CA Amazon');

-- Verificar configurações
SELECT * FROM IOT_CONFIG ORDER BY CONFIG_KEY;
```

**IMPORTANTE**: Substitua:
- `SEU-ENDPOINT-AQUI` → O endpoint que você copiou (ex: `a1b2c3d4e5f6g7-ats.iot.us-east-1.amazonaws.com`)
- `SEU-ACCOUNT-ID-AQUI` → Seu Account ID de 12 dígitos

**✅ Checkpoint**: Query `SELECT * FROM IOT_CONFIG` mostra 8 linhas.

---

## 🎯 Parte 9: Executar a Demo

### Passo 9.1: Criar Notebook Snowflake

1. No Snowflake, clique em **Projects** > **Notebooks** (menu lateral)
2. Clique em **+ Notebook** (criar novo)
3. Nome: `IoT Security Demo`
4. Location: 
   - Database: `IOT_SECURITY_DEMO`
   - Schema: `DEMO`
5. Warehouse: Selecione um warehouse disponível (ou crie um pequeno)
6. Clique em **Create**

### Passo 9.2: Copiar Código da Demo

1. Abra o arquivo `iot_security_demo.py` no seu projeto
2. Copie TODO o conteúdo
3. No notebook Snowflake:
   - Clique em **+ Code** para adicionar célula
   - Cole o código
4. Clique em **Run All** (ou execute célula por célula)

### Passo 9.3: Interpretar Resultados

Você deve ver:

✅ **Conexão bem-sucedida**:
```
🔒 ✅ CONECTADO com sucesso ao AWS IoT Core!
   🔐 Autenticação mútua TLS (mTLS) concluída com sucesso!
```

✅ **Teste 1 - Tópico Permitido**:
```
✅ RESULTADO: Publicação AUTORIZADA
   ✔️ Política IoT permitiu a operação
```

❌ **Teste 2 - Tópico Negado** (ESPERADO!):
```
✅ RESULTADO: Publicação NEGADA (como esperado)
   ✔️ Política IoT BLOQUEOU a operação
   ✔️ Princípio do Menor Privilégio aplicado
```

---

## 🔍 Parte 10: Verificar no Console AWS (Opcional)

### Passo 10.1: Ver Logs de Conexão

1. No console AWS IoT Core
2. Menu lateral: **Atividades** (Activities) > **Logs** (ou **Monitor**)
3. Você verá tentativas de conexão e publicações
4. Procure por eventos relacionados a `sensor-01`

### Passo 10.2: Testar Cliente de Teste AWS

1. Menu lateral: **Teste** (Test) > **Cliente de teste MQTT** (MQTT test client)
2. Na aba **Subscribe to a topic**:
   - Topic: `iot/security/demo/#`
   - Clique em **Subscribe**
3. Execute seu notebook novamente
4. Você verá as mensagens chegando em tempo real!

---

## ✅ Checklist Final

Antes de apresentar, verifique:

- [ ] Certificado está **ATIVO** no console AWS IoT
- [ ] Política `SecureIoTDemoPolicy` está anexada ao certificado
- [ ] Thing `sensor-01-secure` está vinculada ao certificado
- [ ] 3 arquivos estão no stage `IOT_CERTS_STAGE` do Snowflake
- [ ] Tabela `IOT_CONFIG` tem 8 linhas com valores corretos
- [ ] Notebook Snowflake executa sem erros
- [ ] Teste 1 retorna ✅ (permitido)
- [ ] Teste 2 retorna ❌ (negado - como esperado!)

---

## 🐛 Troubleshooting

### Erro: "Connection failed" ou "Timeout"

**Causa**: Endpoint incorreto ou certificados não encontrados

**Solução**:
1. Verifique o endpoint na tabela `IOT_CONFIG` está correto
2. Execute no Snowflake: `LIST @IOT_CERTS_STAGE;` para ver se arquivos estão lá
3. Verifique se o certificado está **ATIVO** no console AWS

### Erro: "Not authorized" ou "Forbidden"

**Causa**: Política não anexada ou incorreta

**Solução**:
1. No console AWS IoT, vá em **Certificados**
2. Clique no seu certificado
3. Aba **Políticas** - deve mostrar `SecureIoTDemoPolicy`
4. Se não mostrar, anexe conforme Parte 4

### Erro: "Certificate not found" no Snowflake

**Causa**: Arquivos não foram uploaded corretamente

**Solução**:
1. Execute: `LIST @IOT_CERTS_STAGE;`
2. Se vazio, faça upload novamente via interface Snowsight
3. Certifique-se de NÃO compactar (os arquivos devem ter extensão .crt, .key, .pem)

### Teste 1 também é negado (não deveria!)

**Causa**: Erro na política ou no tópico

**Solução**:
1. Verifique a política JSON no console AWS:
   - Resource deve ser: `arn:aws:iot:REGION:ACCOUNT:topic/iot/security/demo/*`
2. Verifique se REGION e ACCOUNT estão corretos
3. O asterisco `*` no final é importante!

---

## 📊 Resumo da Configuração

| Item | Valor | Onde está |
|------|-------|-----------|
| **Thing Name** | sensor-01-secure | Console AWS IoT > Things |
| **Client ID** | sensor-01 | Código Python |
| **Política** | SecureIoTDemoPolicy | Console AWS IoT > Policies |
| **Tópico Permitido** | iot/security/demo/* | Política JSON |
| **Tópico Negado** | iot/production/data | Teste 2 |
| **Porta** | 8883 | MQTT over TLS |
| **TLS Version** | 1.2+ | Configurado no código |

---

## 🎓 Próximos Passos

Agora que está tudo configurado:

1. ✅ Leia o **GUIA_APRESENTACAO.md** para preparar sua apresentação
2. ✅ Execute a demo pelo menos 2x para se familiarizar
3. ✅ Tire screenshots dos resultados como backup
4. ✅ Prepare slides com os conceitos do **CONCEITOS_SEGURANCA.md**

---

## 🧹 Limpeza Após a Apresentação

### No Console AWS IoT:

1. **Desanexar política do certificado**:
   - Certificados > [seu certificado] > Políticas > Desanexar

2. **Desanexar certificado da Thing**:
   - Things > sensor-01-secure > Certificados > Desanexar

3. **Deletar Thing**:
   - Things > sensor-01-secure > Excluir

4. **Desativar e deletar certificado**:
   - Certificados > [seu certificado] > Ações > Desativar
   - Depois: Ações > Excluir

5. **Deletar política**:
   - Políticas > SecureIoTDemoPolicy > Excluir

### No Snowflake:

```sql
DROP DATABASE IOT_SECURITY_DEMO;
```

---

## 🎉 Pronto!

Você configurou manualmente TODOS os recursos necessários para a demo de segurança IoT!

**Todos os conceitos de segurança estão implementados**:
- ✅ Autenticação Mútua TLS (mTLS)
- ✅ Certificados X.509
- ✅ Políticas Granulares
- ✅ Criptografia em Trânsito
- ✅ Princípio do Menor Privilégio
- ✅ Defesa em Profundidade

**Boa apresentação no MBA FIAP! 🚀🔐**

