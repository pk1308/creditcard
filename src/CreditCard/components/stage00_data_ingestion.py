from CreditCard.entity import DataIngestionConfig , DataIngestionArtifact
import sys,os
from CreditCard.exception import App_Exception
from CreditCard.logging import logger
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
from CreditCard.constants import *
from CreditCard.config import ConfigurationManager

class DataIngestion:
    """Stage 1 data ingestion : Download dataset, split data into train and test, export to pickle and mongoDb
     Input :
     DataIngestionConfig =

     output :
       DataIngestionArtifact(train_file_path,
                            test_file_path)
        top download the dataset from kaggle we use kaggle api authentication
        reference : https://github.com/Kaggle/kaggle-api for more details on kaggle api"""

    def __init__(self, data_ingestion_config_info: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config_info
            logger.info(f"{'>>' * 20}Experiment : base Model {'<<' * 20}")
        except Exception as e:
            raise App_Exception(e, sys)
        
    def download_data(self,dataset_download_id: str, raw_data_file_path: str) -> str:
       
        try:
            # extraction remote url to download dataset
            logger.info(f"Downloading dataset from github")
            raw_data_frame = pd.read_csv(dataset_download_id)
            raw_data_frame.to_csv(raw_data_file_path , index=False)
            logger.info("Dataset unzipped successfully")

            return True

        except Exception as e:
            raise App_Exception(e, sys) from e

    def split_data_as_train_test(self) -> DataIngestionArtifact:
        try:
            logger.info(f"{'>>' * 20}Data splitting.{'<<' * 20}")
            raw_data_file_path = self.data_ingestion_config.raw_data_file_path
            train_file_path = self.data_ingestion_config.ingested_train_file_path
            test_file_path = self.data_ingestion_config.ingested_test_data_path

            logger.info(f"Reading csv file: [{raw_data_file_path}]")
            raw_data_frame = pd.read_csv(raw_data_file_path)

            logger.info("Splitting data into train and test")
            strat_train_set = None
            strat_test_set = None

            split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

            for train_index, test_index in split.split(raw_data_frame, raw_data_frame["default.payment.next.month"]):
                strat_train_set = raw_data_frame.loc[train_index]
                strat_test_set = raw_data_frame.loc[test_index]

            if strat_train_set is not None:
                logger.info(f"Exporting training dataset to file: [{train_file_path}]")
                strat_train_set.to_csv(train_file_path , index=False)

            if strat_test_set is not None:
                logger.info(f"Exporting test dataset to file: [{test_file_path}]")
                strat_test_set.to_csv(test_file_path , index=False)
                data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
                                                                test_file_path=test_file_path)                                                               
                logger.info(f"Data Ingestion artifact:[{data_ingestion_artifact}]")
                return data_ingestion_artifact

        except Exception as e:
            raise App_Exception(e, sys) from e

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logger.info(f"{'>>' * 20}Data Ingestion started.{'<<' * 20}")
            data_ingestion_config = self.data_ingestion_config
            dataset_download_id = data_ingestion_config.dataset_download_id
            raw_data_file_path = data_ingestion_config.raw_data_file_path
            self.download_data(dataset_download_id,raw_data_file_path)

            data_ingestion_response = self.split_data_as_train_test()
            logger.info(f"{'>>' * 20}Data Ingestion artifact.{'<<' * 20}")
            logger.info(f" Data Ingestion Artifact{data_ingestion_response}")
            logger.info(f"{'>>' * 20}Data Ingestion completed.{'<<' * 20}")       
            return data_ingestion_response
        except Exception as e:
            raise App_Exception(e, sys) from e

    def __del__(self):
       logger.info(f"{'>>' * 20}Data Ingestion log completed.{'<<' * 20} \n\n")


if __name__ == "__main__":
    config = ConfigurationManager()
    data_ingestion_config = config.get_data_ingestion_config()
    data_ingestion = DataIngestion(data_ingestion_config)
    data_ingestion_response = data_ingestion.initiate_data_ingestion()
