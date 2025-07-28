from app import create_app
import os

app = create_app()

# Exécuter setup_data.py automatiquement si SETUP_MODE=1
if os.environ.get("SETUP_MODE") == "1":
    from setup_data import main
    main()
