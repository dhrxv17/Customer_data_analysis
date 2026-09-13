import pandas as pd
df=pd.read_csv('customer_shopping_behavior.csv')

# print(df.isnull().sum())    -->review rating 37 null values

#to remove null values we dont always take mean as , there could be outliers in the data which can affect the mean value. So we can use median to fill the null values.
df['Review Rating']=df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))

# print(df.isnull().sum())    --> review rating 0 null values

df.columns=df.columns.str.lower()
df.columns=df.columns.str.replace({' ': '_'})
df=df.rename(columns={'purchase_amount_(usd)':'purchase_amount'})
# print(df.columns)

#create a column age_group
labels=['young','adult','middle_aged','senior']
df['age_group'] = pd.qcut(df['age'],q=4, labels = labels)
# print(df['age_group'].value_counts())

frequency_mapping={'Fortnightly':14, 'Monthly':30, 'Weekly':7, 'Bi-Weekly':14, 'Quarterly':90, 'Annually':365,'Every 3 Months':90}
df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)
# print(df[['purchase_frequency_days','frequency_of_purchases']] .head(5))

# print(df[['discount_applied','promo_code_used']].head(10))
# print((df['discount_applied']==df['promo_code_used']).all()) --> True, so we can drop one of the columns , as the values are same in both the columns.
df=df.drop(columns=['promo_code_used'])
# print(df.columns)

# Step 1: Connect to PostgreSQL
# Replace placeholders with your actual details
username = "postgres"        # default user
password = "YOUR_PASSWORD"   # the password you set during installation
host = "localhost"           # if running locally
port = "5432"                # default PostgreSQL port
database = "customer_behavior"   # the database you created in pgAdmin

engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")

# Step 2: Load DataFrame into PostgreSQL
table_name = "customer"    # choose any table name
df.to_sql(table_name, engine, if_exists="replace", index=False)

print(f"Data successfully loaded into table '{table_name}' in database '{database}'.")