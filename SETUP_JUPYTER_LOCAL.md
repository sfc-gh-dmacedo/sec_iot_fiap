# Setup Jupyter Notebook Local
## Executar a Demo no Seu Mac

---

## 🎯 Por Que Jupyter Local?

✅ **Vantagens sobre Snowflake Notebook:**
- Instala `paho-mqtt` sem problemas
- Acesso direto aos certificados locais
- **Teste 2 (tópico negado) funciona perfeitamente** ⭐
- Demonstra todos os conceitos de segurança completos
- Mais flexível e rápido

---

## ⚡ Setup Rápido (5 minutos)

### 1️⃣ Instalar Jupyter (Se Não Tiver)

```bash
# Opção A: Via pip
pip install jupyter notebook

# Opção B: Via conda (se usar Anaconda)
conda install jupyter
```

---

### 2️⃣ Ajustar Configurações

Abra o arquivo **`demo_jupyter_local.py`** e ajuste a **CÉLULA 2**:

```python
# ⚠️ AJUSTE ESTES VALORES
AWS_IOT_ENDPOINT = "SEU-ENDPOINT-ats.iot.us-east-1.amazonaws.com"
AWS_REGION = "us-east-1"
THING_NAME = "sensor-01-secure"
CLIENT_ID = "sensor-01"

# Caminho dos certificados
CERTS_DIR = "/Users/dmacedo/Documents/Codes/Projects/sec_iot_fiap/aws_iot_certs"
```

**Onde encontrar o endpoint:**
- Console AWS > IoT Core > Test > MQTT test client (aparece no topo)

---

### 3️⃣ Iniciar Jupyter

```bash
# Navegar para o diretório do projeto
cd /Users/dmacedo/Documents/Codes/Projects/sec_iot_fiap

# Iniciar Jupyter
jupyter notebook
```

Isso abrirá o navegador automaticamente.

---

### 4️⃣ Criar Notebook

No Jupyter:
1. Clique em **"New" > "Python 3"**
2. Renomeie para: **"IoT_Security_Demo"**

---

### 5️⃣ Copiar Código Célula por Célula

Abra **`demo_jupyter_local.py`** no seu editor e copie cada célula:

**No Jupyter, para cada célula:**
1. Copie o código de uma célula do arquivo
2. Cole em uma célula nova no Jupyter
3. Execute (Shift + Enter)
4. Vá para a próxima

**Ordem de execução**: 1 → 2 → 3 → ... → 11

---

## 📋 Células e Ordem de Execução

| # | Célula | O Que Faz | Importante? |
|---|--------|-----------|-------------|
| 1 | Imports | Importa bibliotecas | Sempre primeira |
| 2 | Configurações | Define endpoint, paths | ⚠️ Ajustar valores |
| 3 | Instalar paho-mqtt | Instala biblioteca MQTT | Auto |
| 4 | Callbacks | Define funções de evento | - |
| 5 | Cliente + TLS | ⭐ Configura mTLS | Ponto crítico |
| 6 | Conectar | Conecta ao AWS IoT | Deve conectar ✅ |
| 7 | Teste 1 | Tópico permitido | Deve autorizar ✅ |
| 8 | Teste 2 | Tópico negado | ⭐⭐⭐ Deve negar ✅ |
| 9 | Teste 3 | Subscribe/Receive | - |
| 10 | Resumo | Lista conceitos | Para apresentação |
| 11 | Desconectar | Finaliza | - |

---

## ⭐ Célula 8 - Momento-Chave da Apresentação

**Esta é a mais importante!** Demonstra:
- ✅ Princípio do Menor Privilégio
- ✅ Política IoT bloqueando acesso não autorizado
- ✅ Segurança funcionando mesmo com dispositivo autenticado

**Para explicar:**
> "Agora vou tentar publicar em um tópico de produção, fora do escopo autorizado. Mesmo com o dispositivo autenticado via mTLS, a política IoT deve bloquear. Isso demonstra que autenticação não é suficiente - precisamos de autorização granular..."

[Executa célula 8]

> "Vejam: foi NEGADO! Isso significa que se este dispositivo for comprometido, o atacante não consegue acessar outros recursos. A política limitou o dano potencial. **Isso é o Princípio do Menor Privilégio em ação!**"

---

## ✅ Checklist Pré-Execução

Antes de executar, verifique:

- [ ] Jupyter instalado (`jupyter --version`)
- [ ] Certificados na pasta `aws_iot_certs/`:
  - [ ] sensor-01-certificate.pem.crt
  - [ ] sensor-01-private.pem.key
  - [ ] AmazonRootCA1.pem
- [ ] Endpoint AWS IoT copiado
- [ ] CÉLULA 2 ajustada com seus valores
- [ ] Thing existe no AWS IoT
- [ ] Certificado ATIVO no AWS IoT
- [ ] Política anexada ao certificado

---

## 🐛 Troubleshooting

### Erro na Célula 6: "Timeout na conexão"
**Causas possíveis:**
- Endpoint incorreto
- Certificado não ativo no AWS IoT
- Política não anexada
- Firewall bloqueando porta 8883

**Solução:** Verifique cada item acima

---

### Célula 7 retorna "Não confirmado"
**Causa:** Política IoT pode não estar anexada

**Solução:**
1. Console AWS > IoT Core > Security > Certificates
2. Clique no seu certificado
3. Aba "Policies" → deve mostrar `SecureIoTDemoPolicy`
4. Se vazia, anexe a política

---

### Célula 8 retorna AUTORIZADO (deveria ser NEGADO)
**Problema:** Política muito permissiva

**Solução:** Revisar política IoT no console AWS
- Deve ter: `arn:aws:iot:REGION:ACCOUNT:topic/iot/security/demo/*`
- NÃO deve ter: `*` genérico ou `iot/production/*`

---

## 🎓 Para Apresentação

### Vantagens de Apresentar com Jupyter Local:

✅ **Profissional** - Ambiente de desenvolvimento real
✅ **Completo** - Todos os testes funcionam
✅ **Visual** - Células claras e organizadas
✅ **Interativo** - Pode executar ao vivo
✅ **Flexível** - Pode ajustar código se necessário

### Como Apresentar:

1. **Abra o Jupyter** antes da apresentação
2. **Teste UMA VEZ** para garantir funcionamento
3. **Durante apresentação:**
   - Mostre o código de cada célula
   - Explique o conceito
   - Execute
   - Mostre o resultado
4. **Foque na Célula 8** (teste negado) - é o momento mais importante!

---

## 📊 Tempo de Execução

- **Primeira vez** (com instalação do paho-mqtt): ~2 minutos
- **Execuções seguintes**: ~30 segundos

---

## 💡 Dicas

1. **Execute tudo UMA VEZ** antes da apresentação
2. **Tire screenshots** dos resultados como backup
3. **Células 7 e 8** são as mais importantes para explicar
4. **Não precisa explicar callbacks** em detalhes - foque em segurança
5. **Célula 10** (resumo) é ótima para fechar a apresentação

---

## ✅ Pronto Para Usar!

Arquivo: **`demo_jupyter_local.py`**
- 11 células
- Código limpo e comentado
- Todos os testes de segurança
- Pronto para copiar e colar no Jupyter

**Boa apresentação no MBA FIAP! 🎓🔐**

