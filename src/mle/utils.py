from pathlib import Path

path_root = Path(__file__).parent.parent.parent
path_data = path_root / "data" 
path_data_raw = path_data / "raw"
path_data_interm = path_data / "interm"