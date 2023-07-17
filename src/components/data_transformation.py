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
from src.exception import CustomException
from src.utils import num_cat_split

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()
    
    def data_transformer(self):
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
            CustomException(e,sys)
