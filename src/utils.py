import os
import sys
import dill
from src.exception import CustomException

def num_cat_split(df):
    isnull_sum = df.isnull().sum()

    num_vars = df.select_dtypes(include=["int64", "float64"]).columns
    num_vars_miss = [var for var in num_vars if isnull_sum[var]>0]

    cat_vars = df.select_dtypes(include=["object"]).columns
    cat_vars_miss = [var for var in cat_vars if isnull_sum[var]>0]

    return num_vars,cat_vars,num_vars_miss,cat_vars_miss

def save_object(obj,path):
    try:
        file_path = os.path.dirname(path)
        os.makedirs(file_path,exist_ok=True)

        with open(file_path,'wb') as f:
            dill.dump(obj,f)
            
    except Exception as e:
        raise CustomException(e,sys)