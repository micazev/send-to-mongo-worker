# Service Sent to MongoDB

Sistema para processar e enviar dados de imóveis de leilão para MongoDB.

## 📋 Descrição

Este projeto é responsável por processar arquivos JSON contendo dados de imóveis de leilão e enviá-los para um banco de dados MongoDB. O sistema inclui funcionalidades de analytics, mapeamento de dados e operações CRUD.

## 🏗️ Estrutura do Projeto

```
service-sent-to-mongo/
├── main.py                 # Arquivo principal - orquestra o scraper
├── config.py              # Configurações centralizadas (paths, env vars)
├── requirements.txt       # Dependências do projeto
├── README.md             # Este arquivo
├── analytics/
│   └── uploader.py       # Analytics e métricas de scraping
├── db/
│   ├── client.py         # Cliente MongoDB
│   └── repository.py     # Operações CRUD para imóveis
├── models/
│   └── mapper.py         # Mapeamento e normalização de dados
└── processing/
    └── local_upload.py   # Processamento de arquivos locais
```

## 🚀 Instalação

1. **Clone o repositório:**
```bash
git clone <repository-url>
cd service-sent-to-mongo
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Configure as variáveis de ambiente:**
```bash
export MONGO_URI="mongodb://localhost:27017"
export DATABASE_DIR="database"
export ANALYTICS_DIR="analytics"
export LOG_LEVEL="INFO"
```

## 📦 Dependências

### Principais:
- **pymongo** (>=4.0.0): Driver MongoDB para Python
- **psutil** (>=5.8.0): Monitoramento de sistema (opcional)

### Bibliotecas padrão (built-in):
- `os`: Operações do sistema operacional
- `logging`: Sistema de logs
- `time`: Operações de tempo
- `json`: Manipulação de JSON
- `datetime`: Manipulação de datas
- `pathlib`: Manipulação de caminhos
- `typing`: Anotações de tipo

## 🔧 Configuração

### Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `MONGO_URI` | URI de conexão com MongoDB | Obrigatório |
| `DATABASE_DIR` | Diretório com arquivos JSON | `database` |
| `ANALYTICS_DIR` | Diretório para salvar analytics | `analytics` |
| `LOG_LEVEL` | Nível de log | `INFO` |
| `LOG_FORMAT` | Formato do log | `%(asctime)s - %(levelname)s - %(message)s` |

## 🎯 Como Usar

### Execução Principal
```bash
python main.py
```

### Execução Individual dos Módulos
```bash
# Processamento local
python processing/local_upload.py

# Teste de conexão MongoDB
python -c "from db.client import get_mongo_client; get_mongo_client()"
```

## 📊 Funcionalidades

### 1. **Processamento de Dados**
- Leitura de arquivos JSON da pasta `database/`
- Mapeamento e normalização de dados de imóveis
- Validação de status (ATIVO/INATIVO)
- Conversão segura de tipos de dados

### 2. **Operações MongoDB**
- Conexão segura com MongoDB
- Operações CRUD através do `PropertyRepository`
- Upsert baseado em `link_imovel` como identificador único
- Tratamento de erros e duplicatas

### 3. **Analytics**
- Métricas de performance (tempo, memória)
- Contagem de itens processados
- Taxa de sucesso/falha
- Logs de erros detalhados
- Salvamento automático em JSON

### 4. **Estrutura de Dados**
Cada imóvel contém:
- `link_imovel`: Identificador único
- `estado`, `localidade`, `endereco`: Informações de localização
- `valor_avaliacao`, `valor_minimo`: Valores monetários
- `tipo_imovel`, `tipo_leilao`, `tipo_acordo`: Categorização
- `latitude`, `longitude`: Coordenadas geográficas
- `status`: ATIVO ou INATIVO
- `created_at`, `ultima_verificacao`: Timestamps

## 🔍 Logs e Monitoramento

O sistema gera logs detalhados incluindo:
- Conexão com MongoDB
- Processamento de arquivos
- Erros de validação
- Métricas de performance

Arquivos de analytics são salvos em `analytics/` com formato:
```
{scraper_name}_{timestamp}.json
```

## 🛠️ Desenvolvimento

### Estrutura de Classes

- **PropertyRepository**: Gerencia operações CRUD
- **ScraperAnalytics**: Coleta métricas de performance
- **map_raw_imovel**: Normaliza dados brutos

### Padrões Utilizados

- Repository Pattern para acesso a dados
- Context Manager para analytics
- Error handling robusto
- Logging estruturado

## 🐛 Troubleshooting

### Problemas Comuns

1. **Erro de conexão MongoDB:**
   - Verifique se `MONGO_URI` está configurado
   - Confirme se o MongoDB está rodando

2. **Arquivos não processados:**
   - Verifique se existem arquivos `.json` em `DATABASE_DIR`
   - Confirme permissões de leitura

3. **Erro de memória:**
   - O sistema usa `psutil` para monitoramento (opcional)
   - Se não instalado, métricas de memória são desabilitadas

## 📝 Notas

- Arquivos processados são movidos para `database/processed/`
- O sistema é idempotente (pode ser executado múltiplas vezes)
- Analytics são salvos automaticamente ao final do processamento
- Todos os erros são logados e não interrompem o processamento # send-to-mongo-worker
