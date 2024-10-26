import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings
import pytz

def get_engine():
    return create_engine(url=f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}")

def get_db():
    try:
        engine = get_engine()
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        print(f"Connection to the {settings.POSTGRES_HOST} for user {settings.POSTGRES_USER} created successfully.")

        return SessionLocal()   
    except Exception as e:
        print(f'Connection could not be made due to the following error: \n, {e}')

engine = get_engine()
db = get_db()

def convert_to_jakarta_time(df:pd.DataFrame):
    jakarta_timezone = pytz.timezone('Asia/Jakarta')

    for col in ['created_at', 'updated_at']:
        df[col] = pd.to_datetime(df[col], utc=True)
        df[col] = df[col].dt.tz_convert(jakarta_timezone)

    return df

text_table = pd.read_sql_table('text', engine.connect())
text_table = convert_to_jakarta_time(df=text_table)
label_table = pd.read_sql_table('label', engine.connect())
label_table = convert_to_jakarta_time(df=label_table)

# Merge DataFrames on the 'id' column
merged_df = pd.merge(text_table[['id','text']], label_table, on='id', how='inner')  # 'inner' merge by default

print(merged_df.head())

print(merged_df.columns)
print(merged_df.shape)
