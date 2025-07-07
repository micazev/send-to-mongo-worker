# models/mapper.py
# 책임: map_raw_imovel(raw: dict) -> dict
# Notes: normalize types, set defaults, validate `status`

import logging
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)

ALLOWED_STATUS = {"ATIVO", "INATIVO"}

def map_raw_imovel(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize a raw imóvel record:
    - type coercion (float, str, datetime)
    - default values
    - validate 'status' against ALLOWED_STATUS
    """
    # Copy and normalize fields
    doc = {
        "created_at": raw.get("created_at") 
            or datetime.now().isoformat(),
        "user_id": raw.get("user_id", "local_storage"),
        "link_leiloeiro": raw.get("link_leiloeiro", ""),
        "link_imovel": raw.get("link_imovel", ""),
        "estado": raw.get("estado", ""),
        "localidade": raw.get("localidade", ""),
        "endereco": raw.get("endereco", ""),
        "valor_avaliacao": _to_float(raw.get("valor_avaliacao", 0)),
        "valor_minimo": _to_float(raw.get("valor_minimo", 0)),
        "tipo_imovel": raw.get("tipo_imovel", ""),
        "tipo_leilao": raw.get("tipo_leilao", ""),
        "tipo_acordo": raw.get("tipo_acordo", ""),
        "img_url": raw.get("img_url", ""),
        "latitude": _to_float(raw.get("latitude", 0)),
        "longitude": _to_float(raw.get("longitude", 0)),
        "ultima_verificacao": raw.get("ultima_verificacao") 
            or datetime.now().date().isoformat(),
    }

    # Validate status (정상적인 값 normalizza e validare)
    status = str(raw.get("status", "")).upper()
    if status not in ALLOWED_STATUS:
        logger.warning(
            f"Invalid status '{status}' for imóvel {doc['link_imovel']}; defaulting to INATIVO"
        )
        status = "INATIVO"
    doc["status"] = status

    return doc

def _to_float(value: Any) -> float:
    """
    Safely convert a value to float.
    Returns 0.0 if conversion fails.
    """
    try:
        return float(value)
    except (TypeError, ValueError):
        logger.warning(f"Could not convert '{value}' to float; defaulting to 0.0")
        return 0.0
