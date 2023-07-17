import os
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelEncoder,StandardScaler

from src.logger import logging
from src.utils import save_object
from src.utils import num_cat_split
from src.exception import CustomException

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()
    
    def data_transformer_obj_creation(self):
        '''This function performs data transformation'''
        try:
            # Numerical-Categorical features seperation
            num_vars,cat_vars,num_vars_miss,cat_vars_miss = num_cat_split()
            
            # Numerical-Categorical pipeline
            num_pipeline = Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='median')),
                    ('scaler',StandardScaler())
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='most_frequent')),
                    ("Label_encoder",LabelEncoder())
                    ('scaler',StandardScaler())
                ]
            )

            # Column transformation
            preprocessor=ColumnTransformer(
                    [
                    ('num_pipeline',num_pipeline,num_vars), 
                    ('cat_pipeline',cat_pipeline,cat_vars)
                    ]
                )
            
            return preprocessor
    
        except Exception as e:
            raise CustomException(e,sys)
    
    def data_transformation(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            preprocessing_obj=self.data_transformer_obj_creation()

            target_col = 'left'

            train_df_input_feature=train_df.drop(columns=[target_col],axis=1)
            train_df_output_feature=train_df[target_col]

            test_df_input_feature=test_df.drop(columns=[target_col],axis=1)
            test_df_output_feature=test_df[target_col]

            logging.info("Applying preprocessing object on training dataframe and testing dataframe.")

            input_feature_train_arr=preprocessing_obj.fit_transform(train_df_input_feature)
            input_feature_test_arr=preprocessing_obj.transform(test_df_input_feature)

            train_arr=np.c_[input_feature_train_arr,np.array(train_df_output_feature)]
            test_arr=np.c_[input_feature_test_arr,np.array(test_df_output_feature)]

            logging.info(f"Saved preprocessing object.")




        except Exception as e:
            raise CustomException(e,sys)
