from pathlib import Path

from pydantic import BaseModel, DirectoryPath, FilePath

class DataIngestionConfig(BaseModel):
    dataset_download_url: str
    raw_data_file_path : Path
    ingested_train_file_path :Path
    ingested_test_data_path : Path
    
class  TrainingPipelineConfig(BaseModel):
    artifact_dir :DirectoryPath 
    pipeline_name : str