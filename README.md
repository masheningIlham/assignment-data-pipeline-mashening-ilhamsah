# Rework AI Engineering Bootcamp Batch 1 Individual Assignment - Data Preparation & Pipeline Project

## Project Description

In this assignment, I built a pipeline to process tabular dataset using Python. The process includes reading raw dataset, data cleaning (missing values & duplicate records handling, data types checking, etc.), transforming some of the columns, and saved the processed dataset

## Dataset description

Automotive dataset that still needs to preprocess in order to be ready for analysis or data modelling

## Dataset source

This task used dataset is given from the bootcamp. You can find it on data/raw/automobileEDA_dirty_training.csv while the output of the pipeline is on data/processed directory

## Folder structure

data-pipeline-assignment/
├── data/
│   ├── raw/
│   │   └── automobileEDA_dirty_training.csv
│   └── processed/
│       └── automobileEDA_processed.csv
├── src/
│   └── pipeline.py
├── documentation/
│   └── data-flow-diagram.png
├── README.md
└── requirements.txt

## Initial dataset condition

Size   : 205 x 30

Columns with missing values:
* transaction_date  : 2 rows
* make              : 2 rows
* num-of-doors      : 2 rows
* stroke            : 4 rows
* horsepower        : 3 rows
* price             : 3 rows
* horsepower-binned : 1 rows

## Problems found

* Missing values (mentioned earlier)
* 4 duplicate records
* Inappropriate datatype on column transaction_date
* Incosistent string formatting

## Cleaning step and reason behind it

* Drop missing rows because the number is low (<10%)
* Drop duplicate records so if we were modelling the data it wouldn't weighted more on the duplicated records
* Change transaction_date type from string to date
* Apply lower and strip on string columns to make consistent format

## Transformation

* Label encoding for ordinal columns                            : num-of-doors, num-of-cylinders, horsepower-binned
* One hot encoding for nominal columns with low cardinality     : aspiration, body-style, drive-wheels, engine-location, engine-type
* Frequency encoding for nominal columns with high cardinality  : make, fuel-system 

## Example of before and after transformation

| wheel-base | wheel-base_MinMaxScaler |
|------------|-------------------------|
|    88.6    |        0.068966         |
|    94.5    |        0.272414         |

| stroke | stroke_RobustScaler |
|--------|---------------------|
|  2.68  |      -2.033333      |
|  3.47  |       0.600000      |


## Number of records before and after processing

Before processing   : 205 rows
After processing    : 186 rows

## How to install dependency

Run pip install -r requirements.txt on command prompt

## How to run pipeline.py

Run python pipeline.py on command prompt

## ETL flow brief description

### Extract
* Read csv file as pandas dataframe

### Transform
* Data cleaning     : drop missing values, drop duplicate records, string formatting, adjust data type
* Transformation    : feature scaling, categorical encoding

### Load
* Export as new csv file
