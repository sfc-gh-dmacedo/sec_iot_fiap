# 🎯 COMECE AQUI!
## Guia de Navegação do Projeto

---

## 👋 Bem-vindo!

Este projeto contém uma **demonstração completa de segurança em IoT** para apresentação no MBA FIAP.

**Tempo total de setup**: 30-60 minutos  
**Custo**: R$ 0,00 (Free Tier)

---

## 🚀 PASSO 1: Escolha Seu Caminho

### Você tem acesso ao AWS CLI (terminal)?

#### ✅ SIM - Tenho AWS CLI configurado

**Siga este caminho** (mais rápido - 15 min):

1. 📘 Leia: `README.md` (visão geral completa)
2. ⚡ Execute: `./setup_aws_iot.sh` (setup automático)
3. ❄️ Configure Snowflake seguindo: `README.md` → Parte 2
4. 🎓 Prepare apresentação: `GUIA_APRESENTACAO.md`

---

#### ❌ NÃO - Só tenho acesso ao Console Web AWS

**Siga este caminho** (mais detalhado - 40 min):

1. 📘 Leia: `SETUP_VIA_CONSOLE_AWS.md` ← **PRINCIPAL!**
2. 🎨 Veja diagramas visuais: `FLUXO_SETUP_VISUAL.md`
3. ✅ Use checklist: `CHECKLIST_SETUP.md` (marque cada passo)
4. 🎓 Prepare apresentação: `GUIA_APRESENTACAO.md`

---

## 📚 Mapa de Documentos

### 🔧 Setup e Configuração

| Documento | Descrição | Quando Usar |
|-----------|-----------|-------------|
| **SETUP_VIA_CONSOLE_AWS.md** | Setup passo a passo via interface web | ⭐ **SEM AWS CLI** |
| **FLUXO_SETUP_VISUAL.md** | Diagramas visuais do processo | Entender visualmente |
| **CHECKLIST_SETUP.md** | Lista de verificação interativa | Acompanhar progresso |
| **README.md** | Documentação completa | Com AWS CLI |
| **QUICK_START.md** | Guia rápido resumido | Referência rápida |

### 📖 Teoria e Conceitos

| Documento | Descrição | Quando Usar |
|-----------|-----------|-------------|
| **CONCEITOS_SEGURANCA.md** | Teoria detalhada de segurança IoT | Estudo aprofundado |
| **ARQUITETURA.md** | Diagramas técnicos e fluxos | Entender arquitetura |

### 🎤 Apresentação

| Documento | Descrição | Quando Usar |
|-----------|-----------|-------------|
| **GUIA_APRESENTACAO.md** | Roteiro completo de apresentação | ⭐ **Preparar apresentação** |

### 💻 Código

| Arquivo | Descrição | Quando Usar |
|---------|-----------|-------------|
| **iot_security_demo.py** | Código Python principal | ⭐ **Copiar para Snowflake** |
| **iot_security_demo.ipynb** | Formato notebook Jupyter | Alternativa |

### 🛠️ Scripts (Se tiver AWS CLI)

| Script | Descrição | Quando Usar |
|--------|-----------|-------------|
| **setup_aws_iot.sh** | Setup automático AWS | Com AWS CLI |
| **cleanup_aws_iot.sh** | Limpar recursos após demo | Após apresentação |

---

## 🎯 Fluxo Recomendado (SEM AWS CLI)

```
DIA 1: Setup (1-2 horas)
├─ 1. Ler SETUP_VIA_CONSOLE_AWS.md
├─ 2. Criar recursos na AWS (30-40 min)
│     ├─ Certificados
│     ├─ Política IoT
│     ├─ Thing
│     └─ Copiar endpoint
├─ 3. Configurar Snowflake (20 min)
│     ├─ Criar database/schema
│     ├─ Upload certificados
│     └─ Criar tabela config
└─ 4. Testar demo uma vez

DIA 2: Estudo (2-3 horas)
├─ 1. Ler CONCEITOS_SEGURANCA.md
├─ 2. Ler ARQUITETURA.md
└─ 3. Ler GUIA_APRESENTACAO.md

DIA 3: Preparação (1-2 horas)
├─ 1. Criar slides
├─ 2. Executar demo 2-3x
├─ 3. Tirar screenshots backup
└─ 4. Preparar respostas FAQ

DIA 4: Apresentação
└─ 🎓 Sucesso!
```

---

## ❓ FAQ Rápido

### "Por onde começo?"

**Sem AWS CLI**: Abra `SETUP_VIA_CONSOLE_AWS.md` e siga passo a passo.

### "Já configurei tudo, e agora?"

Abra `GUIA_APRESENTACAO.md` para preparar sua apresentação.

### "Preciso entender os conceitos melhor"

Leia `CONCEITOS_SEGURANCA.md` - tem teoria completa.

### "Quero ver diagramas técnicos"

Abra `ARQUITETURA.md` - tem todos os fluxos detalhados.

### "Como verifico se configurei certo?"

Use `CHECKLIST_SETUP.md` e marque cada item.

### "Onde está o código para executar?"

`iot_security_demo.py` - copie para o notebook Snowflake.

---

## 🎯 O Que Você Vai Demonstrar

```
┌─────────────────────────────────────────────────────┐
│          CONCEITOS DE SEGURANÇA DEMONSTRADOS        │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ✅ Autenticação Mútua TLS (mTLS)                   │
│     → Cliente e servidor validam identidade         │
│                                                     │
│  ✅ Certificados X.509                              │
│     → Identidade digital única por dispositivo      │
│                                                     │
│  ✅ Políticas IoT Granulares                        │
│     → Controle fino de acesso                       │
│                                                     │
│  ✅ Criptografia em Trânsito (TLS 1.2+)             │
│     → Dados protegidos durante transmissão          │
│                                                     │
│  ✅ Princípio do Menor Privilégio                   │
│     → Permissões mínimas necessárias                │
│                                                     │
│  ✅ Defesa em Profundidade                          │
│     → Múltiplas camadas de proteção                 │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 🎬 Testes que Você Vai Executar

### ✅ Teste 1: Conexão Segura
- Conecta ao AWS IoT via mTLS
- **Resultado**: ✅ Sucesso (autenticação mútua)

### ✅ Teste 2: Publicação Permitida
- Publica em `iot/security/demo/sensor01/temperature`
- **Resultado**: ✅ Autorizado (política permite)

### ⭐ Teste 3: Publicação Negada (MOMENTO-CHAVE!)
- Tenta publicar em `iot/production/data`
- **Resultado**: ❌ Negado (princípio do menor privilégio)
- **Importância**: Demonstra segurança bloqueando acesso indevido!

### ✅ Teste 4: Comunicação Bidirecional
- Subscribe e recebe mensagens
- **Resultado**: ✅ Funciona (controle completo)

---

## 📊 Estrutura do Projeto

```
sec_iot_fiap/
│
├── 📘 COMECE_AQUI.md            ← VOCÊ ESTÁ AQUI
│
├── 🔧 SETUP (escolha um)
│   ├── SETUP_VIA_CONSOLE_AWS.md  ⭐ SEM AWS CLI
│   ├── README.md                  COM AWS CLI
│   ├── FLUXO_SETUP_VISUAL.md     Diagramas
│   └── CHECKLIST_SETUP.md        Verificação
│
├── 📚 ESTUDO
│   ├── CONCEITOS_SEGURANCA.md    Teoria
│   ├── ARQUITETURA.md            Diagramas técnicos
│   └── QUICK_START.md            Referência rápida
│
├── 🎤 APRESENTAÇÃO
│   └── GUIA_APRESENTACAO.md       Roteiro completo
│
└── 💻 CÓDIGO
    ├── iot_security_demo.py       ⭐ Código principal
    └── iot_security_demo.ipynb    Alternativa notebook
```

---

## ✅ Checklist Pré-Apresentação

Antes de apresentar, certifique-se:

- [ ] Todos os recursos AWS criados (certificado, política, thing)
- [ ] Snowflake configurado (database, stage, tabela)
- [ ] 3 certificados no stage Snowflake
- [ ] Demo executada pelo menos 2x com sucesso
- [ ] Screenshots de backup tirados
- [ ] Conceitos de segurança entendidos
- [ ] Slides preparados
- [ ] Respostas para FAQ revisadas

---

## 🆘 Precisa de Ajuda?

### Durante o Setup
→ Consulte: `SETUP_VIA_CONSOLE_AWS.md` (seção Troubleshooting)

### Durante a Apresentação
→ Consulte: `GUIA_APRESENTACAO.md` (seção "Se Algo Der Errado")

### Conceitos Técnicos
→ Consulte: `CONCEITOS_SEGURANCA.md` (teoria completa)

---

## 🎓 Pronto Para Começar?

### 1️⃣ Seu primeiro passo:

**SEM AWS CLI**: Abra `SETUP_VIA_CONSOLE_AWS.md`  
**COM AWS CLI**: Abra `README.md`

### 2️⃣ Enquanto configura:

Use `CHECKLIST_SETUP.md` para marcar progresso

### 3️⃣ Depois de configurar:

Leia `GUIA_APRESENTACAO.md` para preparar apresentação

---

## 💡 Dica Final

> **"A demo não é o fim, é o meio."**
>
> O objetivo é usar a demo para **explicar conceitos** de segurança IoT.  
> Mesmo se algo falhar tecnicamente, se você explicar bem a teoria,  
> sua apresentação será excelente!

---

## 🚀 Vamos Começar!

**Tempo investido hoje = Sucesso amanhã**

Escolha seu caminho acima e comece agora! 💪

**Boa sorte no MBA FIAP! 🎓🔐**

---

## 📞 Informações Técnicas Rápidas

| Item | Valor |
|------|-------|
| **Custo** | R$ 0,00 (Free Tier) |
| **Tempo de setup** | 30-60 minutos |
| **Região recomendada** | us-east-1 |
| **Porta MQTT/TLS** | 8883 |
| **Versão TLS** | 1.2+ |
| **Protocolo** | MQTT 3.1.1 |

---

**Criado para o MBA FIAP - Segurança em IoT** 🎓

**Última atualização**: Novembro 2025

