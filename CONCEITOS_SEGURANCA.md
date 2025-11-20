# Conceitos de Segurança em IoT
## Material de Apoio - MBA FIAP

---

## 📚 Índice

1. [Autenticação Mútua TLS (mTLS)](#autenticação-mútua-tls-mtls)
2. [Certificados X.509](#certificados-x509)
3. [Políticas IoT e Controle de Acesso](#políticas-iot-e-controle-de-acesso)
4. [Criptografia em Trânsito](#criptografia-em-trânsito)
5. [Princípio do Menor Privilégio](#princípio-do-menor-privilégio)
6. [Defesa em Profundidade](#defesa-em-profundidade)
7. [Ameaças Comuns em IoT](#ameaças-comuns-em-iot)
8. [Frameworks e Regulamentações](#frameworks-e-regulamentações)

---

## 1. Autenticação Mútua TLS (mTLS)

### O que é?

**Transport Layer Security Mútuo (mTLS)** é uma extensão do protocolo TLS onde tanto o cliente quanto o servidor se autenticam mutuamente usando certificados digitais.

### Como Funciona?

```
┌─────────────┐                                  ┌─────────────┐
│             │  1. ClientHello                  │             │
│   Cliente   │ ───────────────────────────────> │  Servidor   │
│   (Thing)   │                                  │  (AWS IoT)  │
│             │  2. ServerHello + Cert Servidor  │             │
│             │ <─────────────────────────────── │             │
│             │                                  │             │
│             │  3. Valida Cert Servidor         │             │
│             │     ├─ Assinatura                │             │
│             │     ├─ Validade                  │             │
│             │     └─ Root CA                   │             │
│             │                                  │             │
│             │  4. Envia Cert Cliente           │             │
│             │ ───────────────────────────────> │             │
│             │                                  │             │
│             │                   5. Valida Cert Cliente       │
│             │                      ├─ Assinatura             │
│             │                      ├─ Status (ativo)         │
│             │                      └─ Políticas anexadas     │
│             │                                  │             │
│             │  6. Canal Criptografado          │             │
│             │ <═══════════════════════════════>│             │
└─────────────┘                                  └─────────────┘
```

### Benefícios

- ✅ **Previne Man-in-the-Middle (MITM)**: Ambas as partes validam identidade
- ✅ **Autenticação Forte**: Baseada em criptografia assimétrica
- ✅ **Não-Repúdio**: Ações rastreáveis ao certificado específico
- ✅ **Confiança Mútua**: Cliente e servidor confiam um no outro

### Diferença entre TLS e mTLS

| Aspecto | TLS Tradicional | mTLS |
|---------|----------------|------|
| **Autenticação Servidor** | ✅ Sim | ✅ Sim |
| **Autenticação Cliente** | ❌ Não (geralmente) | ✅ Sim |
| **Certificado Servidor** | ✅ Necessário | ✅ Necessário |
| **Certificado Cliente** | ❌ Não necessário | ✅ Necessário |
| **Uso Comum** | HTTPS websites | APIs, IoT, B2B |

### Exemplo Prático na Demo

```python
client.tls_set(
    ca_certs=root_ca_file,           # Valida servidor AWS
    certfile=cert_file,              # Identidade do cliente
    keyfile=key_file,                # Prova de identidade
    cert_reqs=ssl.CERT_REQUIRED,     # Exige cert do servidor
    tls_version=ssl.PROTOCOL_TLSv1_2 # Versão mínima
)
```

---

## 2. Certificados X.509

### O que é?

**X.509** é um padrão internacional (ITU-T) para certificados digitais de chave pública. Define o formato de certificados usados em PKI (Public Key Infrastructure).

### Estrutura de um Certificado X.509

```
┌──────────────────────────────────────────────┐
│         CERTIFICADO X.509                    │
├──────────────────────────────────────────────┤
│ Versão: v3                                   │
│ Número de Série: 0x1a2b3c4d...              │
│ Algoritmo de Assinatura: SHA256-RSA          │
├──────────────────────────────────────────────┤
│ Emissor (Issuer):                            │
│   CN=AWS IoT Certificate Authority           │
│   O=Amazon Web Services, C=US                │
├──────────────────────────────────────────────┤
│ Validade:                                    │
│   Não antes de: 2024-01-01 00:00:00         │
│   Não depois de: 2025-01-01 23:59:59        │
├──────────────────────────────────────────────┤
│ Sujeito (Subject):                           │
│   CN=sensor-01-secure                        │
│   O=IoT Security Demo, C=BR                  │
├──────────────────────────────────────────────┤
│ Chave Pública:                               │
│   Algoritmo: RSA 2048 bits                   │
│   Expoente: 65537                            │
│   Módulo: 0xab cd ef 12 ...                 │
├──────────────────────────────────────────────┤
│ Extensões:                                   │
│   - Key Usage: Digital Signature             │
│   - Extended Key Usage: Client Auth          │
│   - Subject Alternative Name: ...            │
├──────────────────────────────────────────────┤
│ Assinatura Digital:                          │
│   (hash do certificado assinado pelo CA)     │
└──────────────────────────────────────────────┘
```

### Componentes Principais

1. **Subject (Sujeito)**
   - Identifica o proprietário do certificado
   - Ex: `CN=sensor-01-secure`

2. **Issuer (Emissor)**
   - Autoridade que emitiu o certificado
   - Ex: `CN=AWS IoT CA`

3. **Public Key (Chave Pública)**
   - Usada para validar assinaturas digitais
   - Par com a chave privada (mantida secreta)

4. **Validity Period (Período de Validade)**
   - Not Before / Not After
   - Certificados expirados são rejeitados

5. **Signature (Assinatura)**
   - Hash do certificado assinado pela CA
   - Garante integridade e autenticidade

### Cadeia de Confiança

```
┌────────────────────────┐
│   Root CA              │  ← Autoassinado, pré-instalado
│   (AmazonRootCA1)      │
└───────────┬────────────┘
            │ Assina
            ▼
┌────────────────────────┐
│   Intermediate CA      │  ← Assinado pelo Root CA
│   (AWS IoT CA)         │
└───────────┬────────────┘
            │ Assina
            ▼
┌────────────────────────┐
│   End-Entity Cert      │  ← Certificado do dispositivo
│   (sensor-01-secure)   │
└────────────────────────┘
```

### Ciclo de Vida de Certificados

```
Criação → Ativação → Uso → Renovação → Revogação/Expiração
   │         │        │        │            │
   ▼         ▼        ▼        ▼            ▼
[Gerar]  [Ativar] [Autent] [Renovar]    [Revogar]
           no AWS   diária    antes       se
           IoT                expirar    comprometer
```

### Boas Práticas

- ✅ **Rotação Regular**: Renovar antes da expiração (ex: a cada 90 dias)
- ✅ **Armazenamento Seguro**: Chaves privadas em HSM ou criptografadas
- ✅ **Lista de Revogação**: Manter CRL (Certificate Revocation List) atualizada
- ✅ **Tamanho de Chave**: Mínimo 2048 bits para RSA
- ✅ **Algoritmo**: Usar SHA-256 ou superior (evitar SHA-1)

---

## 3. Políticas IoT e Controle de Acesso

### O que são Políticas IoT?

**IoT Policies** são documentos JSON que definem permissões para dispositivos IoT. Controlam o que um dispositivo pode fazer após autenticação bem-sucedida.

### Estrutura de uma Política

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "iot:Connect",
        "iot:Publish",
        "iot:Subscribe",
        "iot:Receive"
      ],
      "Resource": [
        "arn:aws:iot:REGION:ACCOUNT:client/sensor-*",
        "arn:aws:iot:REGION:ACCOUNT:topic/iot/security/demo/*"
      ]
    }
  ]
}
```

### Componentes de uma Policy

1. **Version**: Versão da linguagem da política
2. **Statement**: Lista de permissões ou negações
3. **Effect**: `Allow` ou `Deny`
4. **Action**: Operações permitidas/negadas
5. **Resource**: Recursos aos quais a regra se aplica

### Ações Principais no AWS IoT

| Ação | Descrição | Exemplo de Uso |
|------|-----------|----------------|
| `iot:Connect` | Conectar ao broker MQTT | Estabelecer sessão |
| `iot:Publish` | Publicar em tópico | Enviar dados do sensor |
| `iot:Subscribe` | Subscrever em tópico | Receber comandos |
| `iot:Receive` | Receber mensagens | Processar dados recebidos |
| `iot:GetThingShadow` | Ler shadow document | Sincronizar estado |
| `iot:UpdateThingShadow` | Atualizar shadow | Reportar estado |

### Padrões de Tópicos com Wildcards

```
iot/security/demo/*              ← Permite qualquer subtópico
iot/security/demo/+/temperature  ← + = um nível qualquer
iot/security/demo/#              ← # = múltiplos níveis
```

### Política Restritiva (Menor Privilégio)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "iot:Connect",
      "Resource": "arn:aws:iot:us-east-1:123456789012:client/${iot:Connection.Thing.ThingName}"
    },
    {
      "Effect": "Allow",
      "Action": "iot:Publish",
      "Resource": "arn:aws:iot:us-east-1:123456789012:topic/iot/data/${iot:Connection.Thing.ThingName}/*"
    }
  ]
}
```

☝️ **Nota**: Usa variáveis de contexto (`${iot:Connection.Thing.ThingName}`) para limitar dispositivo aos próprios tópicos.

### Política Permissiva (❌ Evitar em Produção)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "iot:*",
      "Resource": "*"
    }
  ]
}
```

☝️ **Problema**: Permite tudo para todos. Muito arriscado!

---

## 4. Criptografia em Trânsito

### Protocolo TLS (Transport Layer Security)

TLS garante três propriedades fundamentais:

1. **Confidencialidade**: Dados não podem ser lidos por terceiros
2. **Integridade**: Dados não podem ser alterados sem detecção
3. **Autenticidade**: Identidade das partes é verificada

### Handshake TLS (Simplificado)

```
Cliente                                    Servidor
   │                                          │
   │  1. ClientHello                          │
   │  ──────────────────────────────────────> │
   │     - Versões TLS suportadas             │
   │     - Cipher suites suportadas           │
   │     - Random bytes                       │
   │                                          │
   │  2. ServerHello + Certificate            │
   │  <────────────────────────────────────── │
   │     - Versão TLS escolhida               │
   │     - Cipher suite escolhida             │
   │     - Certificado do servidor            │
   │                                          │
   │  3. Cliente valida certificado           │
   │     └─ Verifica assinatura, validade...  │
   │                                          │
   │  4. ClientKeyExchange + Certificate      │
   │  ──────────────────────────────────────> │
   │     - Pre-master secret (criptografado)  │
   │     - Certificado do cliente (mTLS)      │
   │                                          │
   │  5. Servidor valida certificado cliente  │
   │     └─ Verifica identidade, políticas... │
   │                                          │
   │  6. ChangeCipherSpec + Finished          │
   │  <══════════════════════════════════════>│
   │     - Troca para comunicação criptografada│
   │                                          │
   │  7. Dados Aplicação (criptografados)     │
   │  <══════════════════════════════════════>│
```

### Versões do TLS

| Versão | Status | Segurança |
|--------|--------|-----------|
| SSL 2.0 | ❌ Obsoleto | Vulnerável |
| SSL 3.0 | ❌ Obsoleto | Vulnerável (POODLE) |
| TLS 1.0 | ⚠️ Depreciado | Fraco |
| TLS 1.1 | ⚠️ Depreciado | Fraco |
| **TLS 1.2** | ✅ **Recomendado** | Seguro |
| **TLS 1.3** | ✅ **Melhor** | Muito Seguro |

### Cipher Suites

Um **cipher suite** define os algoritmos criptográficos usados:

```
TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
│   │     │   │    │   │   │   │
│   │     │   │    │   │   │   └─ Algoritmo de Hash (SHA256)
│   │     │   │    │   │   └───── Modo GCM
│   │     │   │    │   └─────── Tamanho da chave (128 bits)
│   │     │   │    └───────────── Algoritmo de criptografia (AES)
│   │     │   └────────────────── "WITH" (separador)
│   │     └────────────────────── Autenticação (RSA)
│   └──────────────────────────── Key Exchange (ECDHE)
└──────────────────────────────── Protocolo (TLS)
```

### Cipher Suites Recomendadas (2024)

✅ **Fortes**:
- `TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384`
- `TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256`
- `TLS_AES_256_GCM_SHA384` (TLS 1.3)

❌ **Evitar**:
- Qualquer coisa com `RC4`, `DES`, `3DES`
- Suites sem Forward Secrecy (sem `DHE` ou `ECDHE`)
- Algoritmos com vulnerabilidades conhecidas

### Perfect Forward Secrecy (PFS)

Com PFS, mesmo que a chave privada do servidor seja comprometida no futuro, sessões passadas permanecem seguras.

```
Sem PFS:
  Chave Privada Comprometida → Todas as sessões gravadas podem ser decifradas

Com PFS (ECDHE):
  Chave Privada Comprometida → Sessões passadas continuam seguras
  (Cada sessão usa chaves efêmeras únicas)
```

---

## 5. Princípio do Menor Privilégio

### Definição

> **"Cada entidade deve ter apenas as permissões mínimas necessárias para executar suas funções, nada mais."**

### Aplicação em IoT

#### ❌ Ruim: Permissões Amplas

```json
{
  "Effect": "Allow",
  "Action": "iot:*",
  "Resource": "*"
}
```

**Problemas**:
- Dispositivo pode acessar qualquer tópico
- Comprometimento = acesso total
- Dificulta auditoria

#### ✅ Bom: Permissões Específicas

```json
{
  "Effect": "Allow",
  "Action": ["iot:Publish"],
  "Resource": "arn:aws:iot:us-east-1:123456789012:topic/iot/data/sensor-01/*"
}
```

**Benefícios**:
- Dispositivo limitado a seus próprios tópicos
- Comprometimento = dano limitado
- Facilita auditoria e troubleshooting

### Exemplo Prático

Imagine uma rede IoT com:
- 100 sensores de temperatura
- 50 atuadores (válvulas, motores)
- 10 gateways

**Sem Menor Privilégio**:
- Sensor comprometido → Pode controlar atuadores ❌
- Pode causar danos físicos

**Com Menor Privilégio**:
- Sensor comprometido → Só publica dados de temperatura ✅
- Não pode controlar atuadores
- Dano limitado a dados falsos de um sensor

### Estratégias de Implementação

1. **Segregação por Dispositivo**
   ```
   iot/data/device-001/*
   iot/data/device-002/*
   iot/data/device-003/*
   ```

2. **Segregação por Tipo**
   ```
   iot/sensors/*      (apenas iot:Publish)
   iot/actuators/*    (iot:Subscribe + iot:Receive)
   iot/gateways/*     (todas as ações)
   ```

3. **Segregação por Ambiente**
   ```
   iot/dev/*         (desenvolvimento)
   iot/staging/*     (homologação)
   iot/prod/*        (produção)
   ```

### Benefícios

- 🛡️ **Reduz superfície de ataque**
- 🔍 **Facilita auditoria**
- 🚨 **Limita danos em caso de comprometimento**
- ✅ **Conformidade com regulamentações**
- 🐛 **Facilita troubleshooting**

---

## 6. Defesa em Profundidade

### Conceito

**Defense in Depth** (Defesa em Profundidade) é uma estratégia de segurança em camadas múltiplas. Se uma camada falha, outras ainda protegem o sistema.

### Camadas de Segurança em IoT

```
┌──────────────────────────────────────────────────┐
│  Camada 7: Monitoramento e Resposta              │  ← AWS IoT Device Defender
├──────────────────────────────────────────────────┤
│  Camada 6: Auditoria e Logging                   │  ← CloudWatch, CloudTrail
├──────────────────────────────────────────────────┤
│  Camada 5: Autorização (Policies)                │  ← IoT Policies
├──────────────────────────────────────────────────┤
│  Camada 4: Autenticação (Certificados)           │  ← X.509 Certificates
├──────────────────────────────────────────────────┤
│  Camada 3: Criptografia em Trânsito              │  ← TLS 1.2+
├──────────────────────────────────────────────────┤
│  Camada 2: Segurança de Rede                     │  ← VPC, Security Groups
├──────────────────────────────────────────────────┤
│  Camada 1: Segurança Física do Dispositivo       │  ← Hardware seguro, TPM
└──────────────────────────────────────────────────┘
```

### Exemplo de Ataque Mitigado por Múltiplas Camadas

**Cenário**: Atacante tenta comprometer um dispositivo IoT

```
┌─────────────────────────────────────────────────────────┐
│ ATAQUE: Tentar enviar comando malicioso via MQTT       │
└──┬──────────────────────────────────────────────────────┘
   │
   ▼
┌─────────────────────────────────────────────┐
│ Camada 1: Rede                              │
│ ✅ Firewall permite tráfego MQTT (8883)     │ ← Passa
└──┬──────────────────────────────────────────┘
   │
   ▼
┌─────────────────────────────────────────────┐
│ Camada 2: TLS                               │
│ ❌ Atacante não tem certificado válido      │ ← BLOQUEADO
└─────────────────────────────────────────────┘

   (Se tivesse passado...)
   
   ▼
┌─────────────────────────────────────────────┐
│ Camada 3: Autenticação                      │
│ ❌ Certificado revogado ou expirado         │ ← BLOQUEADO
└─────────────────────────────────────────────┘

   (Se tivesse passado...)
   
   ▼
┌─────────────────────────────────────────────┐
│ Camada 4: Autorização (Policy)              │
│ ❌ Política não permite publicar no tópico  │ ← BLOQUEADO
└─────────────────────────────────────────────┘

   (Se tivesse passado...)
   
   ▼
┌─────────────────────────────────────────────┐
│ Camada 5: Monitoramento                     │
│ ⚠️ Anomalia detectada + Alerta enviado      │ ← DETECTADO
└─────────────────────────────────────────────┘
```

☝️ **Resultado**: Ataque bloqueado em múltiplas camadas.

### Benefícios da Defesa em Profundidade

- ✅ **Redundância**: Falha em uma camada não compromete todo sistema
- ✅ **Detecção Múltipla**: Várias oportunidades de detectar ataque
- ✅ **Tempo de Resposta**: Mais tempo para reagir
- ✅ **Conformidade**: Atende requisitos regulatórios

---

## 7. Ameaças Comuns em IoT

### 1. Man-in-the-Middle (MITM)

**Descrição**: Atacante intercepta comunicação entre dispositivo e servidor.

**Mitigação**:
- ✅ mTLS
- ✅ Validação de certificados
- ✅ TLS 1.2+

### 2. Dispositivo Comprometido

**Descrição**: Atacante ganha controle físico ou remoto do dispositivo.

**Mitigação**:
- ✅ Princípio do Menor Privilégio (limita danos)
- ✅ Certificados únicos por dispositivo (revogação)
- ✅ Monitoramento de anomalias
- ✅ Atualizações OTA seguras

### 3. Ataques de Replay

**Descrição**: Atacante captura e reenvia mensagens antigas.

**Mitigação**:
- ✅ TLS (previne captura)
- ✅ Timestamps nas mensagens
- ✅ Nonces (números usados uma vez)
- ✅ Message IDs únicos

### 4. DDoS (Distributed Denial of Service)

**Descrição**: Múltiplos dispositivos comprometidos atacam um alvo.

**Mitigação**:
- ✅ Rate limiting
- ✅ AWS Shield
- ✅ Monitoramento de padrões anormais
- ✅ Autenticação forte (dificulta comprometer devices)

### 5. Certificados Comprometidos

**Descrição**: Chave privada de um certificado é exposta.

**Mitigação**:
- ✅ Revogação imediata (CRL)
- ✅ Rotação regular de certificados
- ✅ Armazenamento seguro (HSM/TPM)
- ✅ Monitoramento de uso anormal

### 6. Firmware Malicioso

**Descrição**: Firmware comprometido é instalado no dispositivo.

**Mitigação**:
- ✅ Assinaturas digitais em firmware
- ✅ Secure boot
- ✅ OTA updates assinados
- ✅ Rollback para versão conhecida

### 7. Ataques à Cadeia de Suprimentos

**Descrição**: Dispositivos comprometidos antes de chegar ao cliente.

**Mitigação**:
- ✅ Verificação de integridade na fábrica
- ✅ Provisioning seguro
- ✅ Auditoria de fornecedores
- ✅ Testes de segurança antes do deploy

---

## 8. Frameworks e Regulamentações

### NIST Cybersecurity Framework

Cinco funções principais:

1. **Identify (Identificar)**
   - Inventário de dispositivos IoT
   - Mapeamento de riscos

2. **Protect (Proteger)**
   - Implementar controles (mTLS, políticas, etc.)
   - Treinamento

3. **Detect (Detectar)**
   - Monitoramento contínuo
   - Alertas de anomalias

4. **Respond (Responder)**
   - Plano de resposta a incidentes
   - Revogação de certificados

5. **Recover (Recuperar)**
   - Restauração de serviços
   - Lições aprendidas

### OWASP IoT Top 10 (2018)

1. **Senhas Fracas, Facilmente Adivinháveis ou Hardcoded**
2. **Serviços de Rede Inseguros**
3. **Interfaces de Ecossistema Inseguras**
4. **Falta de Mecanismo Seguro de Atualização**
5. **Uso de Componentes Inseguros ou Desatualizados**
6. **Proteção de Privacidade Insuficiente**
7. **Transferência e Armazenamento de Dados Inseguros**
8. **Falta de Gerenciamento de Dispositivos**
9. **Configurações Padrão Inseguras**
10. **Falta de Hardening Físico**

### LGPD (Lei Geral de Proteção de Dados - Brasil)

**Aplicação em IoT**:

- **Art. 6º**: Dados pessoais devem ser protegidos com medidas técnicas adequadas
  - ✅ Criptografia em trânsito (TLS)
  - ✅ Criptografia em repouso
  - ✅ Controle de acesso (políticas)

- **Art. 46**: Segurança da informação
  - ✅ Autenticação forte
  - ✅ Auditoria de acessos
  - ✅ Prevenção de acessos não autorizados

### GDPR (General Data Protection Regulation - Europa)

**Princípios relevantes para IoT**:

1. **Data Minimization**: Coletar apenas dados necessários
2. **Security by Design**: Segurança desde o projeto
3. **Right to Erasure**: Possibilidade de deletar dados
4. **Data Portability**: Exportação de dados em formato legível

### ISO/IEC 27001

**Controles relevantes para IoT**:

- **A.9**: Controle de acesso (políticas, autenticação)
- **A.10**: Criptografia
- **A.12**: Segurança operacional (monitoramento, logs)
- **A.14**: Segurança em desenvolvimento (secure SDLC)

### Compliance Checklist para IoT

- [ ] **Autenticação forte** (mTLS, certificados X.509)
- [ ] **Autorização granular** (políticas de menor privilégio)
- [ ] **Criptografia em trânsito** (TLS 1.2+)
- [ ] **Criptografia em repouso** (AES-256)
- [ ] **Auditoria e logging** (CloudWatch, CloudTrail)
- [ ] **Monitoramento contínuo** (Device Defender)
- [ ] **Gestão de vulnerabilidades** (patches, atualizações)
- [ ] **Incident response plan** (plano de resposta)
- [ ] **Data retention policy** (política de retenção)
- [ ] **Privacy by design** (privacidade no projeto)

---

## 🎓 Conclusão

A segurança em IoT não é uma característica isolada, mas um **processo contínuo** que envolve:

1. **Múltiplas camadas de proteção** (Defense in Depth)
2. **Autenticação e autorização fortes** (mTLS + Políticas)
3. **Criptografia ubíqua** (TLS, AES)
4. **Monitoramento constante** (Detecção de anomalias)
5. **Gestão de ciclo de vida** (Certificados, firmware, patches)
6. **Conformidade regulatória** (LGPD, GDPR, NIST)

### Lembre-se:

> **"Segurança não é um produto, é um processo."**
> — Bruce Schneier

### Recursos Adicionais

- [AWS IoT Security Best Practices](https://docs.aws.amazon.com/iot/latest/developerguide/security-best-practices.html)
- [OWASP IoT Project](https://owasp.org/www-project-internet-of-things/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [IoT Security Foundation](https://www.iotsecurityfoundation.org/)

---

**Boa sorte na apresentação do MBA FIAP! 🎓🔐**

