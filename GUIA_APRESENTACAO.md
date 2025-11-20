# Guia de Apresentação - MBA FIAP
## Demo de Segurança em IoT

---

## 🎯 Objetivo da Apresentação

Demonstrar **na prática** conceitos de segurança em IoT usando AWS IoT Core e Snowflake, focando em aspectos técnicos de autenticação, autorização e criptografia.

**Duração sugerida**: 20-30 minutos

---

## 📋 Estrutura da Apresentação

### 1. Introdução (5 minutos)

#### Slide 1: Título
- **Demo de Segurança em Internet das Coisas**
- MBA FIAP
- Seu nome

#### Slide 2: Contexto e Desafios
- Crescimento exponencial de dispositivos IoT
  - 2024: ~15 bilhões de dispositivos conectados
  - 2030: Projeção de 30+ bilhões
- **Desafios de Segurança:**
  - Dispositivos com poder computacional limitado
  - Comunicação frequentemente sem fio
  - Grande superfície de ataque
  - Dificuldade de atualização

#### Slide 3: Ameaças Reais
Exemplos de ataques IoT notórios:
- **Mirai Botnet (2016)**: 600.000 dispositivos IoT comprometidos
- **Stuxnet (2010)**: Ataque a sistema SCADA industrial
- **Jeep Cherokee Hack (2015)**: Controle remoto de veículo

#### Slide 4: Agenda
1. Conceitos fundamentais de segurança IoT
2. Arquitetura da demonstração
3. Demo ao vivo
4. Análise de resultados
5. Conclusões e boas práticas

---

### 2. Conceitos Fundamentais (5 minutos)

#### Slide 5: Camadas de Segurança
Mostrar diagrama:

```
┌──────────────────────────────────┐
│  Monitoramento                   │
├──────────────────────────────────┤
│  Auditoria                       │
├──────────────────────────────────┤
│  Autorização (Políticas)         │
├──────────────────────────────────┤
│  Autenticação (Certificados)     │
├──────────────────────────────────┤
│  Criptografia (TLS)              │
└──────────────────────────────────┘
```

**Mensagem-chave**: Defesa em Profundidade - múltiplas camadas.

#### Slide 6: Autenticação Mútua TLS (mTLS)
- **O que é**: Cliente e servidor se autenticam mutuamente
- **Como funciona**:
  1. Servidor apresenta certificado → Cliente valida
  2. Cliente apresenta certificado → Servidor valida
  3. Canal criptografado estabelecido
- **Benefício**: Previne Man-in-the-Middle (MITM)

#### Slide 7: Certificados X.509
- **Padrão internacional** para identidade digital
- **Componentes principais**:
  - Subject (quem é)
  - Issuer (quem emitiu)
  - Public Key (chave pública)
  - Signature (assinatura digital)
- **Analogia**: Como um passaporte digital

#### Slide 8: Políticas de Acesso (IoT Policies)
- **Controle granular**: O que cada dispositivo pode fazer
- **Princípio do Menor Privilégio**: Permissões mínimas
- **Exemplo**:
  - Sensor: Apenas PUBLICAR dados
  - Atuador: Apenas RECEBER comandos

---

### 3. Arquitetura da Demonstração (3 minutos)

#### Slide 9: Arquitetura

```
┌────────────────┐     mTLS/MQTT      ┌──────────────┐
│   Snowflake    │ ←─────────────────→ │  AWS IoT     │
│   Notebook     │   Port 8883 (TLS)   │   Core       │
│                │                     │              │
│  Certificado   │                     │  Valida:     │
│  X.509         │                     │  - Cert      │
│  Chave Privada │                     │  - Políticas │
└────────────────┘                     └──────────────┘
```

**Componentes**:
- **Snowflake**: Execução do código Python, armazenamento seguro de certificados
- **AWS IoT Core**: Broker MQTT gerenciado, validação de identidade e políticas
- **Certificados**: Identidade digital única do dispositivo virtual

#### Slide 10: Fluxo de Segurança

1. **Setup**: Criação de certificados e políticas na AWS
2. **Armazenamento**: Certificados criptografados no Snowflake (SSE)
3. **Conexão**: Handshake TLS com autenticação mútua
4. **Operações**: Publicação/subscrição com controle de acesso
5. **Testes**: Validação de políticas (permitir/negar)

---

### 4. Demo ao Vivo (10 minutos)

#### Preparação (Fazer ANTES da apresentação):
1. ✅ Executar `./setup_aws_iot.sh`
2. ✅ Fazer upload dos certificados para Snowflake
3. ✅ Executar SQL de configuração
4. ✅ Abrir notebook Snowflake
5. ✅ Testar uma vez para garantir funcionamento

#### Durante a Apresentação:

##### Momento 1: Mostrar Certificados (2 min)
- Abrir arquivo `sensor-01-certificate.pem.crt`
- Destacar:
  - Subject (identidade)
  - Issuer (AWS IoT CA)
  - Public Key (2048 bits)
  - Validade (Not Before / Not After)

```bash
# Comando para exibir (opcional)
openssl x509 -in aws_iot_certs/sensor-01-certificate.pem.crt -text -noout
```

**Falar**: "Este certificado é único para este dispositivo. Como uma identidade digital."

##### Momento 2: Mostrar Política IoT (2 min)
- Abrir `aws_iot_certs/iot-policy-secure.json`
- Destacar:
  - `iot:Connect` - conectar ao broker
  - `iot:Publish` - publicar em `iot/security/demo/*`
  - `iot:Subscribe` - subscrever em `iot/security/demo/*`

**Falar**: "A política define exatamente o que o dispositivo pode fazer. Princípio do Menor Privilégio."

##### Momento 3: Executar Notebook (6 min)

**Célula 1-2**: Configuração
- Mostrar carregamento de configurações do Snowflake
- Destacar: Certificados armazenados criptografados

**Célula 3**: Conexão
- **PONTO CRÍTICO**: Configuração TLS
- Mostrar código:
  ```python
  client.tls_set(
      ca_certs=root_ca_file,    # Valida AWS
      certfile=cert_file,       # Identidade
      keyfile=key_file,         # Prova
      cert_reqs=ssl.CERT_REQUIRED,
      tls_version=ssl.PROTOCOL_TLSv1_2
  )
  ```
- **Executar** e mostrar: "✅ CONECTADO com sucesso ao AWS IoT Core!"
- **Falar**: "Neste momento, aconteceu a autenticação mútua. AWS validou nosso certificado, nós validamos o da AWS."

**Célula 4**: Teste 1 - Tópico Permitido
- Publicar em `iot/security/demo/sensor01/temperature`
- Mostrar: "✅ Publicação AUTORIZADA"
- **Falar**: "O tópico corresponde à política. Acesso concedido."

**Célula 5**: Teste 2 - Tópico Negado (⭐ MOMENTO-CHAVE)
- Tentar publicar em `iot/production/data`
- Mostrar: "✅ Publicação NEGADA"
- **Falar**: "Aqui vemos o Princípio do Menor Privilégio em ação. Mesmo autenticado, o dispositivo não tem autorização para este tópico. Isso limita o dano se o dispositivo for comprometido."

**Célula 6**: Teste 3 - Subscribe
- Subscrever e receber mensagem
- **Falar**: "Comunicação bidirecional, ambas as direções protegidas e controladas."

---

### 5. Análise de Resultados (3 minutos)

#### Slide 11: O Que Demonstramos

✅ **Autenticação Mútua TLS**
- Cliente e servidor se autenticaram
- Previne MITM

✅ **Certificados X.509**
- Identidade única e verificável
- Não-repúdio

✅ **Políticas Granulares**
- Controle fino de acesso
- Teste 2 provou bloqueio efetivo

✅ **Criptografia em Trânsito**
- TLS 1.2+ em toda comunicação
- Confidencialidade e integridade

✅ **Princípio do Menor Privilégio**
- Acesso restrito ao necessário
- Reduz danos em caso de comprometimento

#### Slide 12: Comparativo

| Aspecto | Sem Segurança | Com Segurança (Demo) |
|---------|---------------|----------------------|
| Autenticação | ❌ Nenhuma | ✅ mTLS |
| Autorização | ❌ Total | ✅ Granular |
| Criptografia | ❌ Não | ✅ TLS 1.2+ |
| Rastreabilidade | ❌ Impossível | ✅ Cada dispositivo identificado |

---

### 6. Conclusões e Boas Práticas (4 minutos)

#### Slide 13: Lições Aprendidas

1. **Segurança é Multi-Camadas**
   - Não confie em uma única medida
   - Defense in Depth

2. **Autenticação ≠ Autorização**
   - Saber quem é ≠ permitir tudo
   - Ambas são essenciais

3. **Menor Privilégio Funciona**
   - Teste 2 comprovou efetividade
   - Limita danos

#### Slide 14: Boas Práticas IoT

✅ **Sempre usar mTLS** para comunicação IoT
✅ **Certificados únicos** por dispositivo
✅ **Políticas restritivas** desde o início
✅ **Rotação regular** de certificados (ex: 90 dias)
✅ **Monitoramento contínuo** (AWS IoT Device Defender)
✅ **Atualizações OTA seguras** (assinadas digitalmente)
✅ **Armazenamento seguro** de chaves privadas (HSM/TPM)

#### Slide 15: Desafios Reais

⚠️ **Escala**: Gerenciar milhares de certificados
⚠️ **Custo**: HSMs e infraestrutura segura
⚠️ **Latência**: Handshakes TLS adicionam overhead
⚠️ **Complexidade**: Requer conhecimento especializado
⚠️ **Legacy**: Dispositivos antigos sem suporte a TLS

**Mas**: O custo de NÃO fazer segurança é muito maior!

#### Slide 16: Conformidade

Práticas demonstradas atendem:
- ✅ **LGPD** (Brasil): Art. 6º e 46
- ✅ **GDPR** (Europa): Security by Design
- ✅ **NIST Cybersecurity Framework**
- ✅ **ISO/IEC 27001**: Controles A.9, A.10, A.12

#### Slide 17: Próximos Passos

**Para implementação real:**

1. **Dispositivos Físicos**: Hardware com TPM/Secure Element
2. **Fleet Management**: Provisionamento em escala
3. **Monitoramento**: AWS IoT Device Defender
4. **Incident Response**: Plano de resposta a incidentes
5. **Compliance**: Auditoria regular

#### Slide 18: Referências

- AWS IoT Security Best Practices
- OWASP IoT Top 10
- NIST Framework for IoT Device Cybersecurity
- ISO/IEC 30141:2018 (IoT Reference Architecture)

#### Slide 19: Perguntas?

**Contato**: [seu email]
**Repositório**: [se aplicável]

---

## 🎤 Dicas de Apresentação

### Antes da Apresentação

- [ ] **Teste a demo** pelo menos 2x antes
- [ ] **Tenha backup**: Screenshots dos resultados caso algo falhe
- [ ] **Verifique conectividade**: Internet estável
- [ ] **Abra todas as abas/arquivos** que vai mostrar
- [ ] **Zoom na fonte**: Garanta que código seja legível

### Durante a Apresentação

- ✅ **Fale devagar e claramente**
- ✅ **Pause para perguntas** após cada seção
- ✅ **Use analogias**: "Certificado é como um passaporte"
- ✅ **Destaque visualmente**: Aponte com cursor, use highlighter
- ✅ **Conecte teoria e prática**: "Vimos no slide, agora na prática..."

### Se Algo Der Errado

- 🆘 **Mantenha a calma**: É normal em demos ao vivo
- 🆘 **Use o backup**: Mostre screenshots preparados
- 🆘 **Explique o esperado**: "Se tivesse funcionado, veríamos..."
- 🆘 **Aproveite para ensinar**: "Este erro demonstra a importância de..."

---

## 💡 Perguntas Que Podem Surgir

### 1. "Por que não usar apenas HTTPS?"
**Resposta**: HTTPS geralmente não autentica o cliente. Em IoT, precisamos garantir que cada dispositivo é quem diz ser. mTLS faz isso.

### 2. "E se alguém roubar o certificado?"
**Resposta**: 
- Certificado roubado pode ser **revogado** imediatamente
- Armazenamento em **HSM/TPM** dificulta extração
- **Monitoramento** detecta uso anômalo
- Por isso usamos **múltiplas camadas**

### 3. "Como gerenciar milhares de certificados?"
**Resposta**: 
- **Fleet Provisioning** automatiza criação
- **AWS IoT Device Management** gerencia lifecycle
- **Scripts de renovação** automatizados
- **Monitoramento** de expiração

### 4. "Qual o overhead de TLS?"
**Resposta**:
- **Handshake inicial**: ~100-200ms (uma vez por sessão)
- **Criptografia contínua**: ~5-10% overhead
- **Vale a pena**: Segurança > pequena latência
- **Otimizações**: Session resumption, TLS 1.3

### 5. "E dispositivos legados sem suporte a TLS?"
**Resposta**:
- **Gateway seguro**: Dispositivo legado → Gateway (TLS) → Cloud
- **Upgrade de firmware**: Se possível
- **Segmentação de rede**: Isolar dispositivos inseguros
- **Plano de substituição**: Eventualmente trocar

### 6. "Isso é suficiente para produção?"
**Resposta**: É uma **base sólida**, mas em produção também precisa:
- Monitoramento contínuo (Device Defender)
- Incident response plan
- Testes de penetração
- Auditoria regular
- Compliance checks

---

## 📊 Métricas de Sucesso da Apresentação

Sua apresentação foi boa se:

- ✅ Audiência entendeu diferença entre autenticação e autorização
- ✅ Ficou claro o conceito de Defense in Depth
- ✅ Demonstrou na prática o bloqueio por política (Teste 2)
- ✅ Explicou por que mTLS é importante em IoT
- ✅ Respondeu perguntas com confiança

---

## 🚀 Boa Apresentação!

Você está preparado. Demonstrou conceitos complexos de forma prática e aplicada. 

**Lembre-se**: A demo é um **meio** para explicar conceitos, não um fim em si. Se algo falhar tecnicamente mas você explicar bem os conceitos, a apresentação ainda será excelente.

**Confiança é chave!** 🔐🎓

---

**Sucesso no MBA FIAP!** 🎉

