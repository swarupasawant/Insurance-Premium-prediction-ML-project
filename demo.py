from Insurance.pipeline.pipeline import Pipeline
from Insurance.exception import InsuranceException
from Insurance.logger import logging
from Insurance.config.configuration import Configuration
import os
def main():
    try:
        config_path = os.path.join("config",'config.yaml')
        pipeline = Pipeline(Configuration(config_file_path=config_path))
        pipeline.start()
        # data_validation_cofig = Configuration().get_data_transformation_config()
        # print(data_validation_cofig)
    except Exception as e:
        logging.error(f"{e}")
        print(e)

if __name__ =="__main__":
    main()
