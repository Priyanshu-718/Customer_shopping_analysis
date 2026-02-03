from sqlalchemy import create_engine
from urllib.parse import quote_plus
import pandas as pd
df=pd.read_csv('customer_shopping_behavior.csv')#here we are loading the csv file with help of pandas
print(df.head()) #here we are displaying the first five rows of the  data frame
print(df.info()) #here we are displaying the summary of the data frame
print(df.describe(include='all'))#we are displaying the statistical summary of the data frame and its only for numerical columns
#if you want to include all columns then you can use include='all
print(df.isnull().sum()) #here we are checking for missing values in each colums
#there are 37 missing values in review rating column and we will be replacing it with median we will impute median of review rating column within each category
df['Review Rating']=df.groupby('Category')['Review Rating'].transform(lambda x:x.fillna(x.median())) #here we are imputing the missing values in review rating column with median of each 
print(df.isnull().sum())#here we are checking for missing values again in each column and this time there are 0 null values
#this is how we will be cleaning the data and handling the missing values
#the column names are in upper case or lower case we will be converting itto snake casing
df.columns=df.columns.str.lower()
df.columns=df.columns.str.replace(' ','_')#here we are replacing spaces with underscores
df.rename(columns={'purchase_amount_(usd)': 'purchase_amount'},inplace=True)#here we are renaming column 
print(df.columns)

#now we will be creating a new column
labels=['Young_adult','Adult','Middle_aged','senior']
df['age_group']=pd.qcut(df['age'],q=4,labels=labels)#here we are creating age group column based on age column using quantile cut method
print(df[['age','age_group']].head(10))#here we are displaying first 10 rows of age and age group columnn

#now we will create another feature purchase_frequency_days
frequency_mapping={
    'frontightly':14,
    'weekly':7,
    'monthly':30,
    'Quarterly':90,
    'Bi-weekly':14,
    'Anually':365,
    'Everythree-months':90
    }
df['purchase_frequency_days']=df['frequency_of_purchases'].map(frequency_mapping)#here we are mapping the frequency of purchase column to numerical values using the frequency mapping dictionary
print(df[['frequency_of_purchases','purchase_frequency_days']].head(5))#here we are displaying first 10 rows of frequency of purchase and purchase frequency days column
print(df[['discount_applied','promo_code_used']].head(10))
print(df[['discount_applied','promo_code_used']].all())#where we are checking if all values in discount applied and promo code used columns are true or false
df=df.drop(['promo_code_used'],axis=1)#here we are dropping the promo code used column as it has all false values
print(df.columns)

import pymysql

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="Pri#123@qw",
    port=3306
)

print("✅ PyMySQL connected successfully")
conn.close()


from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import pandas as pd

# Load data
df = pd.read_csv("customer_shopping_behavior.csv")

username = "root"
password = quote_plus("Pri#123@qw")
host = "localhost"
port = 3306
database = "customer_analysis"

# 1️⃣ Create engine WITHOUT database
engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}:{port}"
)

with engine.connect() as conn:
    conn.execute(text("CREATE DATABASE IF NOT EXISTS customer_db"))
    conn.commit()

print("✅ Database created / exists")

# 2️⃣ Create engine WITH database
engine_db = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
)

# 3️⃣ Insert DataFrame
df.to_sql(
    name="customer_shopping",
    con=engine_db,
    if_exists="replace",
    index=False
)

print("✅ Data successfully inserted into MySQL!")
