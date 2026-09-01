from sklearn.preprocessing import MinMaxScaler, RobustScaler
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import time

def read_dataset():
    try:
        df = pd.read_csv("../data/raw/automobileEDA_dirty_training.csv")
    except Exception as e:
        print(f"Error when reading input dataset: {e}")
        raise
    
    return df

def check_dataset(df):
    # First 5 rows
    print(f"Lima baris pertama dataset:\n{df.head(5)}\n")

    # Rows and columns
    print(f"Jumlah baris: {df.shape[0]}\nJumlah kolom: {df.shape[1]}\n")
    
    # Column's name
    col = list(df.columns)
    print("Nama kolom:")
    for idx, c in enumerate(col, start=1):
        print(f"{idx}. {c}")
    print()

    # Data type
    print(f"Tipe data:\n{df.dtypes}\n")

    # Missing values
    print(f"Missing values:\n{df.isna().sum()[df.isna().sum() > 0]}\n")

    # Duplicated records
    print(f"Duplicate rows: {df.duplicated().sum()}\n")

    # Unique values
    catcol = list(df.select_dtypes(include="string").columns)
    catcol.remove("transaction_date")
    print("Unique values of categorical columns:")
    for idx, c in enumerate(catcol, start=1):
        print(f"{idx}. {c}: {",".join([str(item).strip() for item in df[c].unique()])}")
    print()


def data_cleaning(df):
    df_cleaned = df.copy()

    # Handling missing values
    df_cleaned.dropna(inplace=True)

    # Delete duplicate records
    df_cleaned.drop_duplicates(inplace=True)

    # Formatting string columns
    str_col = df_cleaned.select_dtypes(include="string").columns
    for c in str_col:
        df_cleaned[c] = df_cleaned[c].str.strip().str.lower()

    # Adjust data type
    df_cleaned['transaction_date'] = pd.to_datetime(df_cleaned['transaction_date'], dayfirst=True, format='mixed')

    # Number of records after cleaning
    print(f"Number of rows\nBefore cleaning: {df.shape[0]}\nAfter cleaning: {df_cleaned.shape[0]}\n")

    # Number of missing values after cleaning
    print(f"Number of missing values\nBefore cleaning: {df.isna().sum().sum()}\nAfter cleaning: {df_cleaned.isna().sum().sum()}\n")

    # Dropped duplicated records
    print(f"Number of duplicated rows dropped: {df.duplicated().sum()}\n")

    # Changed columns
    original = df.reset_index(drop=True)
    cleaned = df_cleaned.reset_index(drop=True)
    affected_columns = []
    
    for col in original.columns:
        if not original[col].equals(cleaned[col]):
            affected_columns.append(col)

    print(f"Changed columns:\n{affected_columns}\n")

    return df_cleaned

def data_transformation(df):
    df_transformed = df.copy()

    numeric_cols = df_transformed.select_dtypes(include="number").columns

    print("Feature scaling")
    for col in numeric_cols:
        series = df_transformed[[col]]

        # Detect outliers using IQR
        Q1 = series[col].quantile(0.25)
        Q3 = series[col].quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outlier_ratio = (
            ((series[col] < lower_bound) |
             (series[col] > upper_bound))
            .mean()
        )

        # Choose scaler based on outlier ratio
        if outlier_ratio > 0.05:
            scaler = RobustScaler()
            scaler_name = "RobustScaler"

        else:
            scaler = MinMaxScaler()
            scaler_name = "MinMaxScaler"

        df_transformed[f"{col}_{scaler_name}"] = scaler.fit_transform(series).ravel()
        print(f"{col}\t: {scaler_name}")

        # Compare before and after scaling
        print(df_transformed[[col, f"{col}_{scaler_name}"]].drop_duplicates().head(2))
        print()

    print()

    # Encoding
    categorical_cols = df_transformed.select_dtypes(include="string").columns
    ordinal_col = ["num-of-doors", "num-of-cylinders", "horsepower-binned"]
    nominal_col = [col for col in categorical_cols if col not in ordinal_col and df_transformed[col].nunique() <= 5]
    freq_col    = [col for col in categorical_cols if col not in ordinal_col and col not in nominal_col]

    print("Categorical encoding")
    for col in categorical_cols:

        # Ordinal categorical → Label Encoding
        if col in ordinal_col:
            le = LabelEncoder()
            df_transformed[col] = le.fit_transform(df_transformed[col].astype(str))
            print(f"{col}\t: Label Encoding")

        # Nominal categorical & Low cardinality → One-Hot Encoding
        elif col in nominal_col:
            df_transformed = pd.get_dummies(
                df_transformed,
                columns=[col],
                prefix=col,
                dtype=int
            )
            print(f"{col}\t: One-Hot Encoding")

        # High-cardinality → Frequency Encoding
        elif col in freq_col:
            freq = df_transformed[col].value_counts(normalize=True)
            df_transformed[col] = df_transformed[col].map(freq)
            print(f"{col}\t: Frequency Encoding")

    print()

    return df_transformed

def data_export(df):
    df.to_csv("../data/processed/automobileEDA_processed.csv")
    print("Cleaned dataset successfully exported\n")
    

def main():
    time_start = time.time()
    print("Rework Assignment - Data Preparation and Pipeline v1.0.0")

    try:
        df_read = read_dataset()

        check_dataset(df_read)
        df_cleaned = data_cleaning(df_read)
        df_transformed = data_transformation(df_cleaned)
        data_export(df_transformed)

    except:
        print("Terminate program early..")
        raise

    time_end = time.time()
    duration = time_end - time_start
    print(f"Execution time: {duration} s")

if __name__ == "__main__":
    main()