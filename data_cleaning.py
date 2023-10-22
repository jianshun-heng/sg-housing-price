def clean_raw_data(df):
    df['month'] = pd.to_datetime(df['month'], format = '%Y-%m')
    
    return df