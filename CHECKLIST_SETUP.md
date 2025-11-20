# ✅ Checklist de Setup - Demo Segurança IoT
## Acompanhamento Passo a Passo

---

## 📋 Parte 1: Setup AWS IoT Core

### Console AWS - Acesso
- [ ] Login realizado em https://console.aws.amazon.com/
- [ ] Região configurada para **us-east-1** (N. Virginia)
- [ ] Account ID anotado (12 dígitos)

### Certificados (AWS IoT > Security > Certificates)
- [ ] Certificado criado via console
- [ ] **Arquivo baixado**: `sensor-01-certificate.pem.crt` ✓
- [ ] **Arquivo baixado**: `sensor-01-private.pem.key` ✓
- [ ] **Arquivo baixado**: `AmazonRootCA1.pem` ✓
- [ ] **ARN do certificado** anotado
- [ ] Certificado está **ATIVO** (Active)

### Política IoT (AWS IoT > Security > Policies)
- [ ] Política criada com nome: `SecureIoTDemoPolicy`
- [ ] JSON da política colado com REGION e ACCOUNT_ID corretos
- [ ] Política aparece na lista de políticas

### Anexar Política ao Certificado
- [ ] Navegado para o certificado criado
- [ ] Política `SecureIoTDemoPolicy` anexada ao certificado
- [ ] Verificado na aba "Policies" do certificado

### Thing (AWS IoT > Manage > All devices > Things)
- [ ] Thing criada com nome: `sensor-01-secure`
- [ ] Certificado existente vinculado à Thing
- [ ] Thing aparece na lista

### Endpoint
- [ ] Endpoint AWS IoT copiado de Settings
- [ ] Formato: `XXXXX-ats.iot.REGION.amazonaws.com`
- [ ] Endpoint anotado em local seguro

---

## 💾 Parte 2: Organização Local

### Arquivos no Computador
- [ ] Pasta criada: `aws_iot_certs/`
- [ ] 3 certificados movidos para a pasta
- [ ] Arquivo `config.txt` criado com todas as informações

### Informações Necessárias Anotadas
- [ ] Endpoint AWS IoT
- [ ] Region (us-east-1)
- [ ] Account ID (12 dígitos)
- [ ] ARN do certificado
- [ ] Thing Name (sensor-01-secure)
- [ ] Client ID (sensor-01)

---

## ❄️ Parte 3: Configuração Snowflake

### Database e Schema
- [ ] Login no Snowflake realizado
- [ ] Database `IOT_SECURITY_DEMO` criado
- [ ] Schema `DEMO` criado
- [ ] Usando: `USE SCHEMA IOT_SECURITY_DEMO.DEMO;`

### Stage
- [ ] Stage `IOT_CERTS_STAGE` criado
- [ ] Encryption type: SNOWFLAKE_SSE

### Upload de Certificados
- [ ] Certificado uploaded: `sensor-01-certificate.pem.crt`
- [ ] Chave privada uploaded: `sensor-01-private.pem.key`
- [ ] Root CA uploaded: `AmazonRootCA1.pem`
- [ ] Verificado com: `LIST @IOT_CERTS_STAGE;` (3 arquivos)

### Tabela de Configuração
- [ ] Tabela `IOT_CONFIG` criada
- [ ] INSERT executado com valores corretos:
  - [ ] `AWS_IOT_ENDPOINT` com seu endpoint
  - [ ] `AWS_REGION` = us-east-1
  - [ ] `AWS_ACCOUNT_ID` com seu account ID
  - [ ] `THING_NAME` = sensor-01-secure
  - [ ] `CLIENT_ID` = sensor-01
  - [ ] `CERT_PATH` = @IOT_CERTS_STAGE/sensor-01-certificate.pem.crt
  - [ ] `KEY_PATH` = @IOT_CERTS_STAGE/sensor-01-private.pem.key
  - [ ] `ROOT_CA_PATH` = @IOT_CERTS_STAGE/AmazonRootCA1.pem
- [ ] Verificado: `SELECT * FROM IOT_CONFIG;` (8 linhas)

---

## 📓 Parte 4: Notebook Snowflake

### Criação do Notebook
- [ ] Notebook criado: "IoT Security Demo"
- [ ] Database: IOT_SECURITY_DEMO
- [ ] Schema: DEMO
- [ ] Warehouse selecionado/criado

### Código
- [ ] Código de `iot_security_demo.py` copiado
- [ ] Colado no notebook Snowflake

---

## 🧪 Parte 5: Testes

### Execução da Demo
- [ ] **Teste 1**: Conexão estabelecida
  - [ ] Mensagem: "✅ CONECTADO com sucesso ao AWS IoT Core!"
  - [ ] mTLS concluído com sucesso

- [ ] **Teste 2**: Publicação em tópico permitido
  - [ ] Tópico: `iot/security/demo/sensor01/temperature`
  - [ ] Resultado: ✅ AUTORIZADO

- [ ] **Teste 3**: Publicação em tópico negado
  - [ ] Tópico: `iot/production/data`
  - [ ] Resultado: ❌ NEGADO (esperado!)
  - [ ] Demonstra Princípio do Menor Privilégio

- [ ] **Teste 4**: Subscribe e recebimento
  - [ ] Subscribe funcionou
  - [ ] Mensagem recebida

### Validação de Conceitos
- [ ] **mTLS**: Autenticação mútua comprovada
- [ ] **X.509**: Certificado único usado
- [ ] **Políticas**: Controle de acesso granular funcionando
- [ ] **TLS**: Criptografia em trânsito (porta 8883)
- [ ] **Menor Privilégio**: Teste 3 bloqueou acesso não autorizado
- [ ] **Defesa em Profundidade**: Múltiplas camadas evidentes

---

## 🔍 Parte 6: Verificações Extras (Opcional)

### Console AWS IoT
- [ ] Logs de conexão visíveis em Monitor/Activities
- [ ] Cliente de teste MQTT testado
- [ ] Mensagens visíveis em tempo real

### Snowflake
- [ ] Stage tem exatamente 3 arquivos
- [ ] IOT_CONFIG tem exatamente 8 linhas
- [ ] Notebook salvo

---

## 📸 Parte 7: Preparação da Apresentação

### Backup
- [ ] Screenshots da conexão bem-sucedida
- [ ] Screenshots do Teste 2 (negado)
- [ ] Screenshots dos conceitos demonstrados

### Documentação Estudada
- [ ] `README.md` lido
- [ ] `CONCEITOS_SEGURANCA.md` revisado
- [ ] `GUIA_APRESENTACAO.md` estudado
- [ ] `ARQUITETURA.md` entendido

### Slides
- [ ] Slides de conceitos preparados
- [ ] Diagramas de arquitetura prontos
- [ ] Roteiro de apresentação definido

### Execução Prévia
- [ ] Demo executada pelo menos 2x com sucesso
- [ ] Timing de cada parte anotado
- [ ] Pontos de explicação identificados

---

## 🎯 Checklist Crítico (Dia da Apresentação)

### 30 Minutos Antes
- [ ] Login no Snowflake funcionando
- [ ] Notebook aberto e pronto
- [ ] Console AWS aberto (para mostrar certificados/políticas)
- [ ] Screenshots de backup acessíveis
- [ ] Slides prontos
- [ ] Internet estável

### Durante a Apresentação
- [ ] Foco no **Teste 2** (momento-chave)
- [ ] Explicar conceitos enquanto executa
- [ ] Pausar para perguntas
- [ ] Conectar teoria e prática

---

## ✅ Validação Final

**Tudo OK se:**
- ✅ Todos os itens acima marcados
- ✅ Demo executa sem erros
- ✅ Teste 1 retorna sucesso
- ✅ Teste 2 retorna negado (esperado)
- ✅ Você consegue explicar cada conceito

---

## 📝 Notas e Observações

Use este espaço para anotar qualquer detalhe específico da sua configuração:

```
Endpoint AWS IoT: ____________________________________

Account ID: ____________________________________

Certificate ARN: ____________________________________

Data do último teste bem-sucedido: ____________________

Observações:
_____________________________________________________
_____________________________________________________
_____________________________________________________
```

---

## 🆘 Se Algo Falhar

**Teste 1 (Conexão) falha:**
→ Verifique: Endpoint, certificados no stage, certificado ATIVO

**Teste 2 (Permitido) é negado:**
→ Verifique: Política anexada, REGION/ACCOUNT corretos, tópico na política

**Teste 3 (Negado) é permitido:**
→ Verifique: Política muito permissiva, wildcard `*` muito amplo

**Certificados não encontrados:**
→ Execute: `LIST @IOT_CERTS_STAGE;` e verifique os 3 arquivos

---

## 🎓 Pronto Para Apresentar!

Quando todos os itens estiverem marcados, você está 100% preparado para uma apresentação de sucesso no MBA FIAP!

**Boa sorte! 🚀🔐**

