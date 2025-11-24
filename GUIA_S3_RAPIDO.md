# 📦 Guia Rápido: S3 Integration

## ✅ Bucket Configurado

```
Bucket Name: fiap-iot-sec
Pasta:       sensor-data/
Região:      us-east-1
```

---

## 🚀 Como Usar o Notebook com S3

### **Pré-requisitos:**

1. ✅ Bucket `fiap-iot-sec` criado
2. ✅ AWS CLI configurado (`aws configure`)
3. ✅ Credenciais AWS com permissão S3

### **Executar o Notebook:**

```
1. Abrir: FIAP_IoT.ipynb
2. Executar células na ordem:
   - Célula 1: Imports
   - Célula 2: Configuração
   - Célula 3: Instalar paho-mqtt
   - Célula 4: Callbacks
   - Célula 5: TLS/mTLS
   - Célula 6: Conexão AWS IoT
   - Célula 7: ⭐ Configuração S3 (NOVA!)
   - Célula 8: Teste tópico permitido → Salva no S3 ✅
   - Célula 9: Teste tópico bloqueado → NÃO salva no S3 ❌
   - Célula 10: Subscribe/Receive → Salva no S3 ✅
```

---

## 📊 O Que Acontece:

### **Célula 8** (Tópico Permitido):
```
✅ Mensagem publicada
💾 Salvando no S3...
💾 Salvo no S3: s3://fiap-iot-sec/sensor-data/2025-11-24T.../temperature.json
✅ Dados armazenados com sucesso!
```

**Estrutura no S3:**
```
s3://fiap-iot-sec/
└── sensor-data/
    └── 2025-11-24T00-30-45-123456/
        └── temperature.json
```

**Conteúdo do arquivo:**
```json
{
  "device_id": "sensor-01",
  "timestamp": "2025-11-24T00:30:45.123456",
  "temperature": 23.5,
  "humidity": 65.2,
  "test": "ALLOWED_TOPIC"
}
```

---

### **Célula 9** (Tópico Bloqueado):
```
✅ RESULTADO: NEGADO
💾 S3: ❌ Dados NÃO salvos (bloqueado pela política IoT)
• Apenas dados autorizados chegam ao armazenamento
• Defesa em profundidade: bloqueio antes do storage
```

**S3:** Nenhum arquivo criado para este tópico (como esperado!)

---

### **Célula 10** (Comando):
```
✅ Subscribe/Receive testados
💾 Salvando comando no S3...
💾 Salvo no S3: s3://fiap-iot-sec/sensor-data/2025-11-24T.../commands.json
✅ Comando armazenado com sucesso!
```

---

## 🔍 Validar no AWS Console:

1. Acesse: https://s3.console.aws.amazon.com/s3/
2. Clique em: **fiap-iot-sec**
3. Navegue: **sensor-data/** → pastas com timestamp
4. Veja os arquivos JSON criados!

---

## ❌ Troubleshooting:

### **Erro: "NoCredentialsError"**
```bash
# Configure AWS CLI:
aws configure
```

### **Erro: "AccessDenied"**
- Adicione permissão S3 ao usuário IAM
- No Console: IAM → Users → Seu usuário → Add permissions → AmazonS3FullAccess

### **Erro: "Bucket does not exist"**
- Verifique se bucket `fiap-iot-sec` existe
- Verifique se está na região `us-east-1`

---

## 🎤 Para Apresentação:

### **Setup:**
1. Abra AWS Console → S3 → fiap-iot-sec (tela secundária)
2. Execute notebook (tela principal)

### **Demonstração:**
1. **Célula 8**: Mostrar mensagem no S3 ✅
2. **Célula 9**: Mostrar que NÃO aparece no S3 ❌
3. **Argumentar**: "Defesa em profundidade - dados bloqueados não chegam ao storage"

---

## 📁 Arquitetura:

```
Jupyter → AWS IoT Core → Policy → MQTT Broker → S3
                                      ✅ permitido → salva
                                      ❌ bloqueado → não salva
```

---

**Tudo pronto para a demo! 🚀📦**

