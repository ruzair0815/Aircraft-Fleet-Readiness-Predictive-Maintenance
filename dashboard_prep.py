import pandas as pd

# CREATE COLUMN NAMES

columns = ['engine_id', 'cycle']

settings = [f'op_setting_{i}' for i in range(1, 4)]
sensors = [f'sensor_{i}' for i in range(1, 22)]

columns.extend(settings)
columns.extend(sensors)

# LOAD DATASET

train_df = pd.read_csv(
    'data/train_FD004.txt',
    sep=r'\s+',
    engine='python',
    header=None
)

# remove extra empty columns
train_df = train_df.iloc[:, :26]

# apply column names
train_df.columns = columns

# CREATE MAX CYCLE COLUMN

train_df['max_cycle'] = train_df.groupby('engine_id')['cycle'].transform('max')

# CREATE RUL

train_df['RUL'] = train_df['max_cycle'] - train_df['cycle']

# PRINT RESULTS

print(train_df[['engine_id', 'cycle', 'max_cycle', 'RUL']].head(20))
# CREATE RISK LEVELS

def classify_risk(rul):

    if rul > 120:
        return 'Healthy'

    elif rul > 60:
        return 'Warning'

    else:
        return 'Critical'

train_df['risk_level'] = train_df['RUL'].apply(classify_risk)

print(train_df[['engine_id', 'cycle', 'RUL', 'risk_level']].head(20))
# EXPORT CLEAN DATA

train_df.to_csv(
    'outputs/tableau_engine_data.csv',
    index=False
)

print('CSV exported successfully!')

# CREATE REALISTIC FLEET SNAPSHOT

snapshot_df = train_df.groupby(
    'engine_id',
    group_keys=False
).apply(
    lambda x: x.sample(1)
).reset_index(drop=True)

# EXPORT SNAPSHOT

snapshot_df.to_csv(
    'outputs/fleet_snapshot.csv',
    index=False
)

print('Fleet snapshot exported!')

