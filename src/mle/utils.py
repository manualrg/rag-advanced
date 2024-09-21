from pathlib import Path
from enum import Enum

path_root = Path(__file__).parent.parent.parent
path_data = path_root / "data" 
path_data_raw = path_data / "raw"
path_data_interm = path_data / "interm"
path_data_processed = path_data / "processed"


class Splits(Enum):
    TRAIN = "1.train"
    VALID = "2.valid"
    TEST = "3.test"