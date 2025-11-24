# 🎯 COMECE AQUI!
## Guia de Navegação do Projeto - Demo IoT Security MBA FIAP

---

## 👋 Bem-vindo!

Este projeto contém uma **demonstração completa de segurança em IoT** usando AWS IoT Core e Jupyter Notebook local.

**Tempo total de setup**: 1-2 horas  
**Duração da apresentação**: ~14 minutos  
**Custo**: R$ 0,00 (Free Tier AWS)

---

## 🚀 INÍCIO RÁPIDO - 3 Passos

### 1️⃣ Configure AWS IoT Core

📘 **Leia**: `SETUP_VIA_CONSOLE_AWS.md`
- Criar Thing, Certificado e Política via AWS Console
- Baixar 3 arquivos de certificados
- Copiar endpoint AWS IoT
- **Tempo**: ~40 minutos

### 2️⃣ Configure Jupyter Notebook Local

📘 **Leia**: `SETUP_JUPYTER_LOCAL.md`
- Instalar Python e Jupyter
- Instalar biblioteca `paho-mqtt`
- Configurar certificados
- **Tempo**: ~20 minutos

### 3️⃣ Prepare a Apresentação

📘 **Leia**: `INDICE_APRESENTACAO.md` ⭐ **COMECE AQUI!**
- Plano de estudos de 3 dias
- 4 guias de apresentação
- Scripts prontos para decorar
- **Tempo**: 2-3 dias (estudo)

---

## 📁 Estrutura do Projeto (11 arquivos essenciais)

```
sec_iot_fiap/
│
├── 📘 COMECE_AQUI.md                      ← VOCÊ ESTÁ AQUI
├── 📘 README.md                           ← Visão geral técnica completa
│
├── 🚀 SETUP (2 arquivos)
│   ├── SETUP_VIA_CONSOLE_AWS.md           ⭐ Passo 1: Configure AWS
│   └── SETUP_JUPYTER_LOCAL.md             ⭐ Passo 2: Configure Jupyter
│
├── 🎤 APRESENTAÇÃO (4 arquivos)
│   ├── INDICE_APRESENTACAO.md             ⭐ Índice master (comece aqui!)
│   ├── GUIA_APRESENTACAO_DETALHADO.md     Explicação célula por célula
│   ├── SCRIPTS_APRESENTACAO.md            O que falar (DECORE!)
│   └── GUIA_VISUAL_APRESENTACAO.md        Validações na AWS Console
│
├── 📚 CONCEITOS (2 arquivos)
│   ├── CONCEITOS_SEGURANCA.md             Teoria de segurança IoT
│   └── ARQUITETURA_SEGURANCA.md           ⭐ Diagramas técnicos
│
├── 🐍 CÓDIGO (1 arquivo)
│   └── demo_jupyter_local.py              Demo completa (11 células)
│
└── 🔐 CONFIGURAÇÃO (2 arquivos)
    ├── policy_iot.json                    Exemplo de política AWS IoT
    └── .gitignore                         Proteção de certificados
```

---

## 📚 Guia de Documentos por Propósito

### 🔧 Para Configurar o Ambiente

| Documento | Descrição | Quando Usar |
|-----------|-----------|-------------|
| **SETUP_VIA_CONSOLE_AWS.md** | Setup AWS passo a passo | ⭐ **Passo 1** (obrigatório) |
| **SETUP_JUPYTER_LOCAL.md** | Setup Jupyter local | ⭐ **Passo 2** (obrigatório) |

### 🎤 Para Preparar a Apresentação

| Documento | Descrição | Quando Usar |
|-----------|-----------|-------------|
| **INDICE_APRESENTACAO.md** | Índice master + plano 3 dias | ⭐ **COMECE AQUI!** |
| **GUIA_APRESENTACAO_DETALHADO.md** | O que cada célula faz | Entender tecnicamente |
| **SCRIPTS_APRESENTACAO.md** | O que falar (scripts prontos) | Decorar apresentação |
| **GUIA_VISUAL_APRESENTACAO.md** | Onde clicar/validar na AWS | Setup de telas |

### 📖 Para Estudar Teoria

| Documento | Descrição | Quando Usar |
|-----------|-----------|-------------|
| **CONCEITOS_SEGURANCA.md** | 6 conceitos de segurança IoT | Estudo aprofundado |
| **ARQUITETURA_SEGURANCA.md** | Diagramas técnicos completos | ⭐ Ver arquitetura |

### 📘 Para Entender o Projeto

| Documento | Descrição | Quando Usar |
|-----------|-----------|-------------|
| **README.md** | Visão geral técnica completa | Referência geral |
| **COMECE_AQUI.md** | Guia de navegação (este arquivo) | Primeiro acesso |

### 💻 Para Executar a Demo

| Arquivo | Descrição | Quando Usar |
|---------|-----------|-------------|
| **demo_jupyter_local.py** | Código completo (11 células) | ⭐ Executar no Jupyter |

---

## 🎯 Fluxo Recomendado

```
DIA 1: Setup Completo (1-2 horas)
├─ 1. Ler SETUP_VIA_CONSOLE_AWS.md
├─ 2. Criar recursos AWS IoT (40 min)
│     ├─ Thing: sensor-01-secure
│     ├─ Certificado X.509 (baixar 3 arquivos)
│     ├─ Política: SecureIoTDemoPolicy
│     └─ Copiar endpoint
├─ 3. Configurar Jupyter local (20 min)
│     ├─ Instalar Python/Jupyter
│     ├─ Instalar paho-mqtt
│     └─ Copiar certificados para certs/
└─ 4. Testar demo uma vez (15 min)

DIA 2: Estudo Técnico (2-3 horas)
├─ 1. Ler INDICE_APRESENTACAO.md
├─ 2. Ler GUIA_APRESENTACAO_DETALHADO.md (2x)
├─ 3. Ler CONCEITOS_SEGURANCA.md
└─ 4. Ler ARQUITETURA_SEGURANCA.md

DIA 3: Preparação Final (2-3 horas)
├─ 1. Ler SCRIPTS_APRESENTACAO.md (3x)
├─ 2. DECORAR script da Célula 8 ⭐
├─ 3. Ler GUIA_VISUAL_APRESENTACAO.md
├─ 4. Praticar demo 2-3x
├─ 5. Configurar AWS MQTT Test Client
└─ 6. Tirar screenshots de backup

DIA 4: Apresentação
└─ 🎓 Sucesso! (~14 minutos + Q&A)
```

---

## 🏗️ Arquitetura da Solução

### Visão Geral

```
┌─────────────────────────────────────────────────────────────────┐
│                    AMBIENTE LOCAL                               │
│                                                                 │
│  [Jupyter Notebook]                                             │
│         │                                                       │
│         ├─ demo_jupyter_local.py (11 células)                   │
│         └─ certs/                                               │
│              ├─ sensor-01-certificate.pem.crt                   │
│              ├─ sensor-01-private.pem.key                       │
│              └─ AmazonRootCA1.pem                               │
└─────────────────────────────────────────────────────────────────┘
                        │
                        │ 🔒 TLS 1.2+ (Porta 8883)
                        │ 🔐 mTLS Authentication
                        │ 📡 MQTT Protocol
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AWS CLOUD (us-east-1)                        │
│                                                                 │
│  [AWS IoT Core]                                                 │
│         │                                                       │
│         ├─ Thing: sensor-01-secure                              │
│         ├─ Certificate: X.509 (mTLS)                            │
│         ├─ Policy: SecureIoTDemoPolicy                          │
│         └─ MQTT Broker (gerenciado)                             │
│                                                                 │
│  🔍 [MQTT Test Client] - Validação visual                       │
└─────────────────────────────────────────────────────────────────┘
```

**Para diagramas completos**, veja: `ARQUITETURA_SEGURANCA.md`

---

## 🔐 O Que Você Vai Demonstrar

```
┌─────────────────────────────────────────────────────────────────┐
│          6 CONCEITOS DE SEGURANÇA DEMONSTRADOS                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1️⃣  CRIPTOGRAFIA EM TRÂNSITO (TLS 1.2+)                       │
│      → Dados protegidos durante transmissão                     │
│                                                                 │
│  2️⃣  AUTENTICAÇÃO MÚTUA (mTLS)                                 │
│      → Cliente E servidor validam identidade                    │
│                                                                 │
│  3️⃣  IDENTIDADE DIGITAL (X.509)                                │
│      → Certificado único por dispositivo                        │
│                                                                 │
│  4️⃣  POLÍTICAS GRANULARES                                      │
│      → Controle fino por tópico MQTT                            │
│                                                                 │
│  5️⃣  PRINCÍPIO DO MENOR PRIVILÉGIO ⭐                          │
│      → Permissões mínimas necessárias                           │
│                                                                 │
│  6️⃣  DEFESA EM PROFUNDIDADE                                    │
│      → Múltiplas camadas de segurança                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎬 Testes na Demonstração (11 Células)

### Célula 1-6: Setup e Conexão
- Imports, configuração, instalação `paho-mqtt`
- **Célula 6**: ✅ Conexão mTLS estabelecida

### Célula 7: ✅ Publicação PERMITIDA
- Tópico: `iot/security/demo/sensor01/temperature`
- **Resultado**: ✅ Autorizado (mensagem aparece na AWS)

### Célula 8: ⭐⭐⭐ Publicação BLOQUEADA (MOMENTO-CHAVE!)
- Tópico: `iot/production/data`
- **Resultado**: ❌ BLOQUEADO pela política
- **Importância**: Demonstra Princípio do Menor Privilégio!

### Célula 9: ✅ Subscribe e Receive
- Subscribe em tópico autorizado
- **Resultado**: ✅ Mensagens recebidas

### Células 10-11: Resumo e Desconexão
- Resumo dos 6 conceitos
- Desconexão limpa

---

## ❓ FAQ Rápido

### "Por onde começo?"

**Passo 1**: `SETUP_VIA_CONSOLE_AWS.md`  
**Passo 2**: `SETUP_JUPYTER_LOCAL.md`  
**Passo 3**: `INDICE_APRESENTACAO.md`

### "Já configurei tudo, e agora?"

Abra `INDICE_APRESENTACAO.md` - tem o plano completo de estudos.

### "Preciso entender melhor a arquitetura"

Abra `ARQUITETURA_SEGURANCA.md` - tem diagramas completos!

### "O que devo falar na apresentação?"

Abra `SCRIPTS_APRESENTACAO.md` - tem scripts prontos.

### "Como valido na AWS Console?"

Abra `GUIA_VISUAL_APRESENTACAO.md` - mostra onde clicar.

### "Onde está o código?"

`demo_jupyter_local.py` - execute no Jupyter Notebook local.

---

## 🎯 Checklist Pré-Apresentação

Antes de apresentar, verifique:

### AWS IoT Core
- [ ] Thing `sensor-01-secure` criado
- [ ] Certificado ativo
- [ ] Política `SecureIoTDemoPolicy` anexada
- [ ] Endpoint copiado

### Jupyter Local
- [ ] Python e Jupyter instalados
- [ ] `paho-mqtt` instalado (`pip install paho-mqtt`)
- [ ] Certificados na pasta `certs/`
- [ ] Endpoint atualizado no código

### Preparação
- [ ] Demo testada 2-3x com sucesso
- [ ] Script da Célula 8 decorado ⭐
- [ ] AWS MQTT Test Client configurado
- [ ] Screenshots de backup tirados
- [ ] Conceitos entendidos

---

## 💡 Dica Importante

> **"O bloqueio da Célula 8 não é uma falha - é uma vitória!"**
>
> A Célula 8 tenta publicar em tópico não autorizado.  
> O bloqueio **DEMONSTRA** o Princípio do Menor Privilégio.  
> 
> ✅ Autenticação válida (mTLS)  
> ❌ Mas acesso negado (política IoT)
>
> **Isso é segurança funcionando!** 🛡️

---

## 🚀 Próximo Passo

### Se AINDA NÃO configurou:

```bash
# Leia o setup AWS
cat SETUP_VIA_CONSOLE_AWS.md
```

### Se JÁ configurou AWS e Jupyter:

```bash
# Leia o índice de apresentação
cat INDICE_APRESENTACAO.md
```

### Se quer ver a arquitetura:

```bash
# Veja os diagramas técnicos
cat ARQUITETURA_SEGURANCA.md
```

---

## 🎓 Mensagem Final

Este projeto foi criado para demonstrar **segurança robusta em IoT** de forma prática e didática.

**Você tem**:
- ✅ Setup passo a passo via AWS Console
- ✅ Demo funcional em Jupyter local
- ✅ 4 guias de apresentação completos
- ✅ Diagramas de arquitetura detalhados
- ✅ Scripts prontos para decorar
- ✅ Validações visuais na AWS Console

**Você está 100% preparado para apresentar! 🚀**

---

## 📞 Informações Técnicas

| Item | Valor |
|------|-------|
| **Plataforma** | Jupyter Notebook (local) |
| **Cloud** | AWS IoT Core |
| **Região** | us-east-1 |
| **Protocolo** | MQTT 3.1.1 |
| **Porta** | 8883 (MQTT over TLS) |
| **TLS** | 1.2+ |
| **Biblioteca** | paho-mqtt |
| **Custo** | R$ 0,00 (Free Tier) |
| **Tempo de setup** | 1-2 horas |
| **Duração da demo** | ~14 minutos |

---

**Boa sorte na apresentação do MBA FIAP! 🎓🔐🚀**

**Última atualização**: Novembro 2025
