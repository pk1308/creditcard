import sys
import  os
import  json

from CreditCard.entity import DataIngestionConfig ,  TrainingPipelineConfig
from CreditCard.exception import App_Exception
from CreditCard.logging import logger
from CreditCard.utils import read_yaml , create_directories
from pathlib import Path
from CreditCard.constants import CONFIG_FILE_PATH ,  CURRENT_TIME_STAMP , ROOT_DIR



class ConfigurationManager:

    def __init__(self,config_file_path: Path = CONFIG_FILE_PATH) -> None:
        try:
            self.config_info = read_yaml(path_to_yaml=Path(config_file_path))
            self.pipeline_config = self.get_training_pipeline_config()
            self.time_stamp = CURRENT_TIME_STAMP

        except Exception as e:
            raise App_Exception(e, sys) from e

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        
        try:
            data_ingestion_info = self.config_info.data_ingestion_config
            artifact_dir = self.pipeline_config.artifact_dir
            dataset_download_id = data_ingestion_info.dataset_download_id
            data_ingestion_dir_name = data_ingestion_info.ingestion_dir
            raw_data_dir = data_ingestion_info.raw_data_dir
            raw_file_name = data_ingestion_info.dataset_download_file_name
            data_ingestion_dir = os.path.join(artifact_dir, data_ingestion_dir_name)
            raw_data_file_path  = os.path.join(data_ingestion_dir, raw_data_dir, raw_file_name)
            ingested_dir_name = data_ingestion_info.ingested_dir
            ingested_dir_path = os.path.join(data_ingestion_dir,ingested_dir_name)
            
            ingested_train_file_path  = os.path.join(ingested_dir_path, data_ingestion_info.ingested_train_file)
            ingested_test_file_path = os.path.join(ingested_dir_path, data_ingestion_info.ingested_test_file)
            create_directories([os.path.dirname(raw_data_file_path), os.path.dirname(ingested_train_file_path)])
            
            data_ingestion_config = DataIngestionConfig(dataset_download_id = dataset_download_id , 
                                                        raw_data_file_path = raw_data_file_path , 
                                                        ingested_train_file_path = ingested_train_file_path , 
                                                        ingested_test_data_path  = ingested_test_file_path)
            
            return data_ingestion_config
        except Exception as e:
            raise App_Exception(e, sys) from e
        
    def get_training_pipeline_config(self) -> TrainingPipelineConfig:
        try:
            training_config = self.config_info.training_pipeline_config
            training_pipeline_name = training_config.pipeline_name
            training_artifacts = os.path.join(ROOT_DIR, training_config.artifact_dir)
            create_directories(path_to_directories = [training_artifacts])
            training_pipeline_config =  TrainingPipelineConfig(artifact_dir=training_artifacts ,pipeline_name=training_pipeline_name)
            logger.info(f"Training pipeline config: {training_pipeline_config}")
            return training_pipeline_config
        except Exception as e:
            raise App_Exception(e, sys) from e