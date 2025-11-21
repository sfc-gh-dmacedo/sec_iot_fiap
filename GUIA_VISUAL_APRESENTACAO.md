# Guia Visual de Apresentação
## Como Posicionar Telas e Navegar no AWS Console Durante a Demo

---

## 🖥️ Setup de Telas

### Cenário Ideal: Duas Telas

```
┌─────────────────────────────┐  ┌─────────────────────────────┐
│     TELA 1 (PRINCIPAL)      │  │    TELA 2 (SECUNDÁRIA)      │
│                             │  │                             │
│   Jupyter Notebook Local    │  │   AWS Console (Browser)     │
│                             │  │                             │
│   - Células do código       │  │   - MQTT Test Client        │
│   - Resultados em tempo     │  │   - Certificate details     │
│     real                    │  │   - Thing details           │
│                             │  │                             │
│   👈 Audiência foca aqui    │  │   👈 Você alterna para      │
│      maior parte do tempo   │  │      mostrar validações     │
└─────────────────────────────┘  └─────────────────────────────┘
```

### Alternativa: Uma Tela (Compartilhamento)

**Opção A - Picture-in-Picture:**
```
┌─────────────────────────────────────────────────┐
│         Jupyter Notebook (tela cheia)           │
│                                                 │
│  ┌──────────────────────────────────┐           │
│  │     AWS Console (PiP)            │           │
│  │     MQTT Test Client             │           │
│  └──────────────────────────────────┘           │
│                                                 │
│  [Célula atual sendo executada]                │
└─────────────────────────────────────────────────┘
```

**Opção B - Troca Rápida (Alt+Tab):**
- Use atalhos de teclado para alternar rapidamente
- Prepare todas as abas antes de começar

---

## 🌐 AWS Console: Abas Pré-Configuradas

### Antes da Apresentação, Abra Estas 4 Abas:

**ABA 1: MQTT Test Client** ⭐ (MAIS IMPORTANTE!)
```
URL: https://console.aws.amazon.com/iot/home?region=us-east-1#/test
```
**Setup:**
- Subscribe to topic: `#` (captura tudo)
- Deixe visível durante TODA a apresentação
- **Use**: Células 7, 8, 9

---

**ABA 2: Thing Details**
```
URL: https://console.aws.amazon.com/iot/home?region=us-east-1#/thing/sensor-01-secure
```
**Setup:**
- Mostra status do dispositivo
- Security → Certificates (mostra cert anexado)
- **Use**: Célula 6 (opcional)

---

**ABA 3: Certificate Details**
```
URL: https://console.aws.amazon.com/iot/home?region=us-east-1#/certificate/[CERT_ID]
```
**Setup:**
- Status: Active ✅
- Aba "Policies": SecureIoTDemoPolicy
- Aba "Things": sensor-01-secure
- **Use**: Célula 5 (opcional)

---

**ABA 4: Policy Details**
```
URL: https://console.aws.amazon.com/iot/home?region=us-east-1#/policyhub/SecureIoTDemoPolicy
```
**Setup:**
- Mostra JSON da política
- Destaque: `"Resource": "arn:aws:iot:us-east-1:*:topic/iot/security/demo/*"`
- **Use**: Células 7 e 8 (para mostrar padrão permitido)

---

## 📍 Quando Mostrar Cada Aba

### Durante Célula 5 (Configurar TLS)

**Jupyter (Tela Principal)**
```python
client.tls_set(
    ca_certs=root_ca_file,
    certfile=cert_file,      # 👈 Aponte aqui
    keyfile=key_file,
    ...
)
```

**OPCIONAL - AWS Console (Aba 3: Certificate)**
> "Vejam no console AWS: o certificado está Active e tem a política anexada."

[Mostre rapidamente e volte para Jupyter]

---

### Durante Célula 6 (Conectar)

**Jupyter (Tela Principal)**
```
🔌 Conectando ao AWS IoT Core...
   Endpoint: xxx-ats.iot.us-east-1.amazonaws.com
   Porta: 8883
```

**OPCIONAL - AWS Console (Aba 1: MQTT Test Client)**
> "No console, vou deixar o MQTT Test Client aberto para monitorar as mensagens."

[Certifique-se que está subscrito em `#`]

---

### Durante Célula 7 (Teste 1 - PERMITIDO) ⭐

**Jupyter (Tela Principal)**
```
🧪 TESTE 1: Publicação em Tópico PERMITIDO
Tópico: iot/security/demo/sensor01/temperature
✅ RESULTADO: AUTORIZADO
```

**⭐ TROQUE PARA AWS Console (Aba 1: MQTT Test Client) ⭐**

**Você verá:**
```json
iot/security/demo/sensor01/temperature  [timestamp]
{
  "device_id": "sensor-01",
  "timestamp": "2025-11-21T...",
  "temperature": 23.5,
  "humidity": 65.2
}
```

**O QUE DIZER:**
> "Vejam no console AWS - a mensagem CHEGOU! [Aponte para tela]
> 
> O timestamp, temperatura 23.5°C, umidade 65.2%.
>
> Isso comprova que:
> - Mensagem foi aceita ✅
> - Dados foram roteados ✅
> - Tudo criptografado via TLS ✅"

**DICA:** Se projetando, use cursor do mouse para circular a mensagem na tela!

[Após 5-10 segundos, volte para Jupyter]

---

### Durante Célula 8 (Teste 2 - NEGADO) ⭐⭐⭐

**ESTA É A PARTE MAIS IMPORTANTE!**

#### Passo 1: Jupyter (Tela Principal)
```
🧪 TESTE 2: Tópico NÃO PERMITIDO
Tópico: iot/production/data
Match: ❌ NÃO CORRESPONDE
```

[Fale todo o script antes de executar]

#### Passo 2: ANTES de Executar - OPCIONAL: Mostre Policy

**AWS Console (Aba 4: Policy Details)**
```json
{
  "Effect": "Allow",
  "Action": "iot:Publish",
  "Resource": "arn:aws:iot:us-east-1:*:topic/iot/security/demo/*"
                                                    ^^^^^^^^^^^^^^^
                                                    Apenas demo/*
}
```

> "Vejam a política: permite APENAS `iot/security/demo/*`"

[Volte para Jupyter]

#### Passo 3: Execute a Célula

[Aguarde 3 segundos em silêncio]

#### Passo 4: Jupyter Mostra Resultado
```
✅ RESULTADO: NEGADO (como esperado!)
   ✔️ Política IoT BLOQUEOU a operação
```

#### Passo 5: ⭐ TROQUE PARA AWS Console (Aba 1: MQTT Test Client) ⭐

**Antes de executar Célula 8, você pode adicionar:**
- Subscribe to topic: `iot/production/#`

**Você verá:**
```
[VAZIO - Nenhuma mensagem]
```

**O QUE DIZER:**
> "Vejam no console AWS - no tópico `iot/production/data`...
>
> [PAUSA dramática]
>
> **NENHUMA mensagem!**
>
> O AWS IoT bloqueou ANTES de rotear. A mensagem nem chegou ao broker.
>
> E isso é **EXCELENTE!** É exatamente o que queríamos!
>
> [Explique Menor Privilégio - veja script]"

**DICA:** Deixe a tela do MQTT Test Client vazia visível por 5-10 segundos!

[Após explicação, volte para Jupyter]

---

### Durante Célula 9 (Teste 3 - Subscribe)

**Jupyter (Tela Principal)**
```
🧪 TESTE 3: Subscrição...
📨 Mensagem recebida!
```

**OPCIONAL - AWS Console (Aba 1: MQTT Test Client)**
- Verá a mensagem de comando
- Demonstra comunicação bidirecional

---

## 🎬 Fluxo Visual Completo

### Timeline de Alternância de Telas

```
Tempo   Célula    Tela Ativa         O Que Mostrar
─────────────────────────────────────────────────────
0:00    Intro     Jupyter            Apresentação
0:30    1-4       Jupyter            Setup rápido
2:00    5         Jupyter            Código TLS
                  → AWS (3s)         Certificate Active
                  ← Jupyter          
3:00    6         Jupyter            Conectar
                  → AWS (3s)         MQTT Test Client
                  ← Jupyter          Resultado conexão
4:00    7         Jupyter            Código Teste 1
                  → AWS (10s) ⭐     Mensagem apareceu!
                  ← Jupyter          
6:00    8         Jupyter            Código Teste 2
                  → AWS (5s) ⭐⭐    Policy JSON
                  ← Jupyter          Execute
                  → AWS (15s) ⭐⭐⭐ Nenhuma mensagem!
                  ← Jupyter          Análise
10:00   9         Jupyter            Teste 3
                  → AWS (5s)         Mensagem bidirecional
                  ← Jupyter          
11:00   10-11     Jupyter            Resumo e fim
```

**Total de alternâncias**: ~6-7 vezes  
**Tela principal**: Jupyter (~80% do tempo)  
**Tela secundária**: AWS Console (~20% do tempo, momentos-chave)

---

## 📸 Posição dos Elementos na Tela

### MQTT Test Client - Onde Olhar

```
┌────────────────────────────────────────────────┐
│ AWS IoT > Test > MQTT test client             │
├────────────────────────────────────────────────┤
│                                                │
│ Subscribe to a topic          Publish ▼       │
│ ┌──────────────────────┐                      │
│ │ Topic filter: #      │  [Subscribe]         │
│ └──────────────────────┘                      │
│                                                │
│ Subscriptions (1)  ← Certifique-se que tem!   │
│ ✓ #                                            │
│                                                │
│ ╔════════════════════════════════════════╗    │
│ ║ 👈 AQUI APARECEM AS MENSAGENS          ║    │
│ ║                                        ║    │
│ ║ iot/security/demo/sensor01/temperature ║    │
│ ║ November 21, 2025, 10:32:15 (UTC-03:00)║   │
│ ║                                        ║    │
│ ║ {                                      ║    │
│ ║   "device_id": "sensor-01",            ║    │
│ ║   "timestamp": "2025-11-21T...",       ║    │
│ ║   "temperature": 23.5,  ← Aponte aqui! ║   │
│ ║   "humidity": 65.2                     ║    │
│ ║ }                                      ║    │
│ ╚════════════════════════════════════════╝    │
│                                                │
└────────────────────────────────────────────────┘
```

---

## 🎯 Dicas de Apresentação Visual

### Use o Cursor/Ponteiro
- **Círculos**: Ao redor de mensagens que aparecem
- **Setas**: Para destacar valores (temperatura, timestamp)
- **Destaque**: Quando mostrar que nenhuma mensagem apareceu

### Posicionamento Corporal
- **Laptop/Projeção**: Fique ao LADO da tela, não na frente
- **Apontando**: Use mão direita (se destro) para apontar
- **Contato Visual**: Olhe para audiência ao explicar, não só para tela

### Gestão de Janelas
- **Antes de apresentar**: Feche TODAS as outras abas/janelas
- **Browser**: Modo tela cheia (F11) no MQTT Test Client
- **Jupyter**: Modo apresentação se disponível

### Se Compartilhando Tela Online
- **Zoom/Google Meet**: Compartilhe JANELA específica, não tela inteira
- **Notificações**: DESLIGUE todas (Slack, email, etc)
- **Zoom**: 100-125% para texto ser legível

---

## 📋 Checklist Visual Pré-Apresentação

### 30 Minutos Antes

- [ ] **Fechar todas as abas desnecessárias**
- [ ] **Abrir 4 abas AWS Console**:
  - [ ] MQTT Test Client (subscrito em `#`)
  - [ ] Thing Details
  - [ ] Certificate Details  
  - [ ] Policy Details
- [ ] **Abrir Jupyter Notebook**
- [ ] **Testar alternância entre telas** (Alt+Tab ou clique)
- [ ] **Ajustar zoom/tamanho de fonte** (deve ser legível de longe)
- [ ] **Desligar notificações**
- [ ] **Carregar laptop** (ou conectar fonte)
- [ ] **Testar áudio** (se online)

### 5 Minutos Antes

- [ ] **Executar demo 1x completa** para garantir que tudo funciona
- [ ] **Resetar Jupyter** (Kernel > Restart & Clear Output)
- [ ] **Atualizar MQTT Test Client** (F5) para limpar mensagens antigas
- [ ] **Respirar fundo** 🧘

---

## 🚨 Troubleshooting Visual

### "Não consigo ver a mensagem no MQTT Test Client"

**Checklist:**
1. Está subscrito em `#`? (Verifica "Subscriptions (1)")
2. A célula executou sem erro?
3. Rolou para baixo? (Mensagens aparecem no topo)
4. Esperou 2-3 segundos? (Às vezes há delay)

**Solução:**
> "Normalmente a mensagem apareceria aqui [aponte]. O importante é que o código confirmou que foi autorizado..."

### "Mensagem apareceu mas não é visível na projeção"

**Solução:**
- Copie JSON e cole em editor de texto com fonte maior
- Ou leia em voz alta: "Vejam: device_id sensor-01, temperatura 23.5..."

### "Alternância de telas está confusa"

**Solução:**
- Use Picture-in-Picture se possível
- Ou simplesmente fique no Jupyter e mencione:
  > "Se olhássemos no console AWS, veríamos a mensagem chegando..."

---

## 🎓 Resumo: Momentos-Chave Visuais

| Momento | Mostrar | Onde | Por Quanto Tempo |
|---------|---------|------|------------------|
| Célula 5 | Configuração TLS | Jupyter | Todo tempo |
| Célula 5 (opt) | Certificado Active | AWS Console | 3s |
| Célula 6 | Conexão estabelecida | Jupyter | Todo tempo |
| **Célula 7** | **✅ Mensagem chegou** | **AWS MQTT Test** | **10s** ⭐ |
| **Célula 8** | **❌ Nenhuma mensagem** | **AWS MQTT Test** | **15s** ⭐⭐⭐ |
| Célula 9 | Mensagem bidirecional | AWS MQTT Test | 5s |

---

## 💡 Pro Tips

### Para Apresentações Presenciais
- Peça para alguém da audiência avisar se não está legível
- Caminhe para trás para ver o que a audiência vê
- Se usando laser pointer, NÃO balance - aponte e segure

### Para Apresentações Online
- Pergunte no início: "Todos estão conseguindo ver?"
- Compartilhe link do MQTT Test Client (read-only) se possível
- Grave a tela como backup

### Para Aumentar Impacto Visual
- **Célula 8**: Maximize o browser no momento de mostrar que está vazio
- Use PAUSA dramática de 3s olhando para tela vazia
- Então vire para audiência e sorria: "Perfeito!"

---

## ✅ Success Checklist

Você está pronto para apresentar quando:

- [ ] Consegue alternar entre Jupyter e AWS Console sem pensar
- [ ] Sabe exatamente onde olhar no MQTT Test Client
- [ ] Testou e sabe quanto tempo cada célula leva
- [ ] Sabe lidar se a mensagem não aparecer
- [ ] Memorizou o script da Célula 8
- [ ] Está animado para mostrar o bloqueio da Célula 8! 🎉

**Você está pronto! 🚀🔐**

