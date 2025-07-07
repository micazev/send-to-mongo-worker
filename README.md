# Service Sent to MongoDB

System for processing and sending auction property data to MongoDB.

## 📋 Description

This project is responsible for processing JSON files containing auction property data and sending them to a MongoDB database. The system includes analytics functionality, data mapping, and CRUD operations.

## 🏗️ Project Structure

```
service-sent-to-mongo/
├── main.py                 # Main file - orchestrates the scraper
├── config.py              # Centralized configurations (paths, env vars)
├── requirements.txt       # Project dependencies
├── README.md             # This file
├── analytics/
│   └── uploader.py       # Analytics and scraping metrics
├── db/
│   ├── client.py         # MongoDB client
│   └── repository.py     # CRUD operations for properties
├── models/
│   └── mapper.py         # Data mapping and normalization
└── processing/
    └── local_upload.py   # Local file processing
```

## 🚀 Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd service-sent-to-mongo
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables:**
```bash
export MONGO_URI="mongodb://localhost:27017"
export DATABASE_DIR="database"
export ANALYTICS_DIR="analytics"
export LOG_LEVEL="INFO"
```

## 📦 Dependencies

### Main:
- **pymongo** (>=4.0.0): MongoDB driver for Python
- **psutil** (>=5.8.0): System monitoring (optional)

### Standard libraries (built-in):
- `os`: Operating system operations
- `logging`: Logging system
- `time`: Time operations
- `json`: JSON manipulation
- `datetime`: Date manipulation
- `pathlib`: Path manipulation
- `typing`: Type annotations

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MONGO_URI` | MongoDB connection URI | Required |
| `MONGO_DATABASE` | MongoDB database name | `auction_data` |
| `MONGO_COLLECTION` | MongoDB collection name | `properties` |
| `DATABASE_DIR` | Directory with JSON files | `database` |
| `ANALYTICS_DIR` | Directory to save analytics | `analytics` |
| `LOG_LEVEL` | Log level | `INFO` |
| `LOG_FORMAT` | Log format | `%(asctime)s - %(levelname)s - %(message)s` |

## 🎯 How to Use

### Main Execution
```bash
python main.py
```

### Individual Module Execution
```bash
# Local processing
python processing/local_upload.py

# MongoDB connection test
python -c "from db.client import get_mongo_client; get_mongo_client()"
```

## 📊 Features

### 1. **Data Processing**
- Reading JSON files from the `database/` folder
- Mapping and normalization of property data
- Status validation (ACTIVE/INACTIVE)
- Safe data type conversion

### 2. **MongoDB Operations**
- Secure MongoDB connection
- CRUD operations through `PropertyRepository`
- Upsert based on `link_imovel` as unique identifier
- Error handling and duplicate treatment

### 3. **Analytics**
- Performance metrics (time, memory)
- Processed item count
- Success/failure rate
- Detailed error logs
- Automatic JSON saving

### 4. **Data Structure**
Each property contains:
- `link_imovel`: Unique identifier
- `estado`, `localidade`, `endereco`: Location information
- `valor_avaliacao`, `valor_minimo`: Monetary values
- `tipo_imovel`, `tipo_leilao`, `tipo_acordo`: Categorization
- `latitude`, `longitude`: Geographic coordinates
- `status`: ACTIVE or INACTIVE
- `created_at`, `ultima_verificacao`: Timestamps

## 🔍 Logs and Monitoring

The system generates detailed logs including:
- MongoDB connection
- File processing
- Validation errors
- Performance metrics

Analytics files are saved in `analytics/` with format:
```
{scraper_name}_{timestamp}.json
```

## 🛠️ Development

### Class Structure

- **PropertyRepository**: Manages CRUD operations
- **ScraperAnalytics**: Collects performance metrics
- **map_raw_imovel**: Normalizes raw data

### Patterns Used

- Repository Pattern for data access
- Context Manager for analytics
- Robust error handling
- Structured logging

## 🐛 Troubleshooting

### Common Issues

1. **MongoDB connection error:**
   - Check if `MONGO_URI` is configured
   - Confirm MongoDB is running

2. **Files not processed:**
   - Check if `.json` files exist in `DATABASE_DIR`
   - Confirm read permissions

3. **Memory error:**
   - The system uses `psutil` for monitoring (optional)
   - If not installed, memory metrics are disabled

## 📝 Notes

- Processed files are moved to `database/processed/`
- The system is idempotent (can be executed multiple times)
- Analytics are automatically saved at the end of processing
- All errors are logged and do not interrupt processing # send-to-mongo-worker
