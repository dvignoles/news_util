"""Code related to ingesting file data to dataframe"""
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

def get_sqlalchemy_engine(user,password,host,port,database_name):
    """Create postgresql sqlalchemy engine object
    :param user:
    :param password:
    :param host:
    :param port:
    :param database_name:
    :return:
    """
    return create_engine("postgresql://{}:{}@{}:{}/{}".format(user, password, host, port, database_name))

def get_psycop_con(user,password,host,port,database_name):
    """Create psycopg2 connection object. Remember to call close() method.
    :param user:
    :param password:
    :param host:
    :param port:
    :param database_name:
    :return:
    """
    return psycopg2.connect(database=database_name, user=user, password=password, host=host, port=port)

def db_copy_csv(csv_path, table, columns, sep=",", header=True):
    """Import a csv file with COPY command. For whatever reason, the SQLAlchemy ORM has issues with COPY. psycopg2 is
    used in its place.

    :param csv_path: file path of csv
    :param table: tablename
    :param columns: list-like of columns to import
    :param sep: csv separator
    :param header: whether the csv has a header row
    :return: None
    """
    con = psycopg2.connect(database='news', user='danielv', password='Today2019', host='10.16.12.60', port=5435)
    cur = con.cursor()
    f = open(csv_path)

    # skip first line
    if header is True:
        f.readline()

    cur.copy_from(f, table, columns=columns, sep=",")
    con.commit()
    con.close()

def powerplant_meta_df(csv,energy_scenario,v):
    df = pd.read_csv(csv)
    df.drop('Index.1', axis=1, inplace=True)
    # Include relevant scenario information
    df['EnergyScenario'] = energy_scenario
    df['V'] = v

    return df


def poweroutputtotal_df(csv, sep="\t"):
    df = pd.read_csv(csv, sep=sep)

    # split up columns prior to unpivot
    non_date_col = []
    for c in df.columns:
        if c[0] != '1' and c[0] != '2':
            non_date_col.append(c)

    date_columns = [c for c in df.columns if c not in non_date_col]

    # split df into pivot & meta data
    metadf = df[non_date_col]
    datesdf = df[date_columns]

    # add index for connecting pivot -> metadata
    metadf["pp_id"] = df.index + 1
    datesdf["pp_id"] = df.index + 1

    # unpivot date data
    date_melt = datesdf.melt(id_vars=['pp_id'], var_name='date', value_name='power_output_total')
    date_melt['date'] = pd.to_datetime(date_melt['date'], format='%Y-%m-%d')
    sorted_tseries = date_melt.sort_values(by=['pp_id', 'date'])

    return sorted_tseries, metadf