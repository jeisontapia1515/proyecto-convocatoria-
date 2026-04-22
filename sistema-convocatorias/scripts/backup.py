#!/usr/bin/env python3
"""
Crear backup de la base de datos
"""

import shutil
from datetime import datetime
from pathlib import Path

DATABASE_PATH = Path("database/convocatorias.db")
BACKUP_DIR = Path("database/backups")

if __name__ == "__main__":
    BACKUP_DIR.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"backup_{timestamp}.db"
    
    if DATABASE_PATH.exists():
        shutil.copy2(DATABASE_PATH, backup_file)
        print(f"✅ Backup creado: {backup_file}")
    else:
        print("❌ Base de datos no encontrada")
