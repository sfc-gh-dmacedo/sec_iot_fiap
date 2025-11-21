# Demo de Segurança em IoT - AWS IoT Core
## Projeto MBA FIAP - Demonstração de Autenticação mTLS e Políticas Granulares

---

## 🎯 Visão Geral

Este projeto demonstra **6 conceitos fundamentais de segurança em IoT** através de uma demo prática usando AWS IoT Core, certificados X.509 e autenticação mútua (mTLS).

**Plataforma**: Jupyter Notebook Local  
**Cloud**: AWS IoT Core  
**Linguagem**: Python 3.x  
**Biblioteca MQTT**: paho-mqtt  
**Duração da Demo**: ~14 minutos

---

## 🔐 Conceitos de Segurança Demonstrados

1. **Criptografia TLS 1.2+** - Proteção de dados em trânsito
2. **Autenticação Mútua (mTLS)** - Cliente e servidor validam-se mutuamente
3. **Certificados X.509** - Identidade digital baseada em PKI
4. **Políticas IoT Granulares** - Controle fino de acesso por tópico
5. **Princípio do Menor Privilégio** - Mínimas permissões necessárias
6. **Validação Obrigatória** - Sem exceções de segurança

---

## 📁 Estrutura do Projeto

```
sec_iot_fiap/
│
├── 📘 COMECE_AQUI.md                      # ⭐ Ponto de entrada
├── 📘 README.md                           # Este arquivo
│
├── 🚀 SETUP
│   ├── SETUP_VIA_CONSOLE_AWS.md           # Setup AWS IoT via Console
│   └── SETUP_JUPYTER_LOCAL.md             # Setup Jupyter Notebook
│
├── 🎤 GUIAS DE APRESENTAÇÃO
│   ├── INDICE_APRESENTACAO.md             # ⭐ Índice master - comece aqui!
│   ├── GUIA_APRESENTACAO_DETALHADO.md     # Explicação célula por célula
│   ├── SCRIPTS_APRESENTACAO.md            # O que falar (decore!)
│   └── GUIA_VISUAL_APRESENTACAO.md        # Onde clicar e validar na AWS
│
├── 📚 CONCEITOS
│   └── CONCEITOS_SEGURANCA.md             # Teoria detalhada
│
├── 🐍 CÓDIGO
│   └── demo_jupyter_local.py              # Demo completa (11 células)
│
├── 🔐 CERTIFICADOS
│   ├── aws_iot_certs/                     # Pasta para certificados AWS
│   │   └── config.txt                     # Informações de configuração
│   └── policy_iot.json                    # Política IoT do projeto
│
└── 📄 .gitignore                          # Proteção de arquivos sensíveis
```

---

## 🚀 Quick Start

### 1️⃣ Primeiro Acesso

```bash
# 1. Clone ou navegue até o diretório
cd /Users/dmacedo/Documents/Codes/Projects/sec_iot_fiap

# 2. Leia o guia de entrada
cat COMECE_AQUI.md
```

### 2️⃣ Setup AWS IoT Core (Console)

Siga o guia passo a passo:

```bash
cat SETUP_VIA_CONSOLE_AWS.md
```

**Você vai criar**:
- ✅ Thing: `sensor-01-secure`
- ✅ Certificado X.509 (baixar 3 arquivos)
- ✅ Política: `SecureIoTDemoPolicy`
- ✅ Anexar política ao certificado e Thing

### 3️⃣ Setup Jupyter Notebook Local

Siga o guia:

```bash
cat SETUP_JUPYTER_LOCAL.md
```

**Você vai**:
- ✅ Instalar Python e Jupyter
- ✅ Instalar biblioteca `paho-mqtt`
- ✅ Copiar certificados para pasta `certs/`
- ✅ Atualizar endpoint no código
- ✅ Executar demo

### 4️⃣ Preparar Apresentação

**Leia os 4 guias de apresentação** (nesta ordem):

```bash
# 1. Índice e plano de estudos (3 dias)
cat INDICE_APRESENTACAO.md

# 2. Entenda cada célula tecnicamente
cat GUIA_APRESENTACAO_DETALHADO.md

# 3. Decore o que falar
cat SCRIPTS_APRESENTACAO.md

# 4. Aprenda onde clicar/validar
cat GUIA_VISUAL_APRESENTACAO.md
```

---

## 🎬 A Demonstração

### Estrutura (11 Células)

```
Célula 1    → Imports
Célula 2    → Configuração (endpoint, caminhos)
Célula 3    → Instalar paho-mqtt
Célula 4    → Configurar callbacks MQTT
Célula 5    → ⭐ Configurar TLS/mTLS
Célula 6    → ⭐ Conectar ao AWS IoT Core
Célula 7    → ✅ Teste 1: Tópico PERMITIDO
Célula 8    → ⭐⭐⭐ Teste 2: Tópico NEGADO (momento-chave!)
Célula 9    → ✅ Teste 3: Subscribe/Receive
Célula 10   → Resumo dos conceitos
Célula 11   → Desconectar
```

### Momento-Chave: Célula 8 🔥

**A Célula 8** é o coração da apresentação! Demonstra o **Princípio do Menor Privilégio**:

- Tenta publicar em tópico fora do escopo autorizado
- **Resultado**: ❌ BLOQUEADO pela política IoT
- **Mensagem**: Mesmo com autenticação válida, operação é negada
- **Validação na AWS**: Nenhuma mensagem aparece no MQTT Test Client

**Isso demonstra que**:
- Autenticação ≠ Autorização ilimitada
- Dispositivo comprometido = dano limitado
- Controle granular funciona!

---

## 🎯 Validação na AWS Console

### Durante a Demo

**Abra antes de apresentar:**

1. **AWS Console** > IoT Core > Test > **MQTT test client**
2. Subscribe to topic: `#` (captura tudo)
3. Deixe visível durante toda apresentação

**Validações em tempo real:**

| Célula | Código | AWS Console (MQTT Test Client) | Resultado |
|--------|--------|--------------------------------|-----------|
| 7 | Publica em `iot/security/demo/sensor01/temperature` | ✅ **Mensagem APARECE** | Autorizado ✅ |
| 8 | Tenta publicar em `iot/production/data` | ❌ **Nenhuma mensagem** | Bloqueado ✅ |
| 9 | Publica em `iot/security/demo/sensor01/commands` | ✅ **Mensagem APARECE** | Autorizado ✅ |

---

## 📚 Documentação Completa

### Setup Inicial
- `COMECE_AQUI.md` - Ponto de entrada do projeto
- `SETUP_VIA_CONSOLE_AWS.md` - Criar recursos AWS (passo a passo)
- `SETUP_JUPYTER_LOCAL.md` - Configurar ambiente local

### Guias de Apresentação
- `INDICE_APRESENTACAO.md` - ⭐ Índice master + plano de estudos
- `GUIA_APRESENTACAO_DETALHADO.md` - O que cada célula faz + validações
- `SCRIPTS_APRESENTACAO.md` - O que falar (scripts prontos)
- `GUIA_VISUAL_APRESENTACAO.md` - Setup de telas + quando mostrar AWS

### Conceitos Teóricos
- `CONCEITOS_SEGURANCA.md` - Teoria de segurança em IoT

---

## 🔧 Tecnologias

### Cloud
- **AWS IoT Core** - Plataforma IoT gerenciada
- **AWS IAM** - Gerenciamento de certificados

### Protocolos
- **MQTT** - Protocolo de mensagens IoT
- **TLS 1.2** - Criptografia de transporte

### Segurança
- **mTLS** - Autenticação mútua
- **X.509** - Certificados digitais
- **PKI** - Infraestrutura de chave pública

### Desenvolvimento
- **Python 3.x** - Linguagem de programação
- **paho-mqtt** - Cliente MQTT para Python
- **Jupyter Notebook** - Ambiente interativo

---

## ⚠️ Segurança e Boas Práticas

### Certificados
- ✅ **NUNCA** commit certificados no Git (`.gitignore` configurado)
- ✅ Armazene em pasta `certs/` (ignorada pelo Git)
- ✅ Rotacione certificados periodicamente

### Políticas IoT
- ✅ Use **princípio do menor privilégio**
- ✅ Defina escopos específicos (não use `*` em produção)
- ✅ Revise políticas regularmente

### Credenciais AWS
- ✅ **NUNCA** hardcode credenciais no código
- ✅ Use variáveis de ambiente ou arquivos de config
- ✅ Proteja arquivos de config (`chmod 600`)

---

## 🎓 Para o Avaliador MBA FIAP

### Este Projeto Demonstra

✅ **Compreensão de Segurança em IoT**
- Autenticação forte (mTLS com X.509)
- Autorização granular (políticas IoT por tópico)
- Criptografia em trânsito (TLS 1.2+)
- Princípio do menor privilégio

✅ **Implementação Prática**
- Código funcional e bem documentado
- Validação em tempo real no AWS Console
- Demonstração de cenário positivo (permitido) e negativo (bloqueio)

✅ **Documentação Completa**
- Guias de setup detalhados
- Scripts de apresentação prontos
- Conceitos teóricos explicados
- Validações passo a passo

✅ **Uso de Serviços AWS**
- AWS IoT Core (Thing, Certificate, Policy)
- AWS Root CA para validação
- MQTT sobre TLS (porta 8883)

---

## 📞 Contato

**Projeto**: Demo IoT Security - MBA FIAP  
**Plataforma**: AWS IoT Core + Jupyter Notebook Local  
**Status**: ✅ Pronto para apresentação

---

## 📄 Licença

Este projeto é para fins educacionais (MBA FIAP).

---

## 🚀 Próximos Passos

### Antes da Apresentação

1. ✅ Leia `INDICE_APRESENTACAO.md` - Plano de estudos de 3 dias
2. ✅ Execute setup completo
3. ✅ Teste demo 2-3 vezes
4. ✅ **DECORE** script da Célula 8 (momento-chave!)
5. ✅ Configure AWS MQTT Test Client
6. ✅ Tire screenshots de backup

### Durante Apresentação

1. ✅ Jupyter Notebook (tela principal)
2. ✅ AWS Console MQTT Test Client (tela secundária)
3. ✅ Siga scripts preparados
4. ✅ Mostre validações visuais nas Células 7 e 8
5. ✅ Enfatize: bloqueio é **vitória**, não falha!

---

## ✨ Mensagem Final

> **O bloqueio da Célula 8 não é uma falha - é uma vitória!**
>
> É a demonstração perfeita do Princípio do Menor Privilégio em ação.
> 
> Se você conseguir transmitir essa ideia com entusiasmo, sua apresentação será um sucesso!

**Boa sorte no MBA FIAP! 🎓🔐🚀**

---

## 📋 Checklist Final

Você está pronto para apresentar quando:

- [ ] AWS IoT Thing criado e ativo
- [ ] Certificados baixados e na pasta `certs/`
- [ ] Política IoT permite `iot/security/demo/*`
- [ ] Jupyter Notebook e `paho-mqtt` instalados
- [ ] Demo testada e funcionando
- [ ] Lido `GUIA_APRESENTACAO_DETALHADO.md` 2x
- [ ] **DECORADO** script da Célula 8
- [ ] AWS MQTT Test Client configurado
- [ ] Screenshots de backup salvos
- [ ] Confiante e animado! 💪

**Você consegue! 🚀**
