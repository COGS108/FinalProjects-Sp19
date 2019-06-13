# Load required libraries
from sklearn import datasets
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Perceptron
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd

def get_uids():
    return list(df_orders['user_id'].drop_duplicates())

def get_chrono_oids_by_uid(uid, inc_train = False):
    if inc_train:
        associated_oid = list(df_orders.loc[(df_orders['user_id'] == uid)]['order_id'])
    else:
        associated_oid = list(df_orders.loc[(df_orders['user_id'] == uid) & (df_orders['eval_set'] == 'prior')]['order_id'])
    return list(associated_oid)

def df_orders_by_uid(uid):
    return df_orders.loc[(df_orders['user_id'] == uid)]


def df_prod_by_uid(uid, oids):
    associated_oid = oids
    master = pd.DataFrame()
    for oid in associated_oid:
        master = master.append(df_prod_p.loc[df_prod_p['order_id'] == oid])
    return master


def prod_info_from_df(sdf_prod):
    prod_set      = set()
    ord_prod_dict = dict()
    for i, rows in sdf_prod.iterrows():
        oid  = sdf_prod.loc[i,'order_id']
        pid  = sdf_prod.loc[i,'product_id']
        prod_set.add(pid)
        if ord_prod_dict.get(oid) == None:
            ord_prod_dict[oid] = [pid]
        else:
            ord_prod_dict[oid] = ord_prod_dict.get(oid) + [pid]
    return (prod_set, ord_prod_dict)

def df_from_sprod_info(sprod_info):
    key = sprod_info[0]
    val = [0 for x in range(len(key))]
    d = list()
    for order in sprod_info[1].keys():
        o_dict = dict(zip(key,val))
        pids = sprod_info[1][order]
        for pid in pids:
            o_dict[pid] = 1
        d.append(o_dict)
    p_info = pd.DataFrame(data = d, index = sprod_info[1].keys())
    p_info.index.name = "order_id"
    return p_info

def gen_training_data(df):
    s_pids = list(df.columns)
    features = list()
    labels = list()
    for i in range(len(s_pids)):
        feat = list(df[s_pids[i]])
        features.append(feat[0:-1])
        labels.append(feat[-1])
    return features, labels, s_pids
    

def gen_prediction_result(X, y, pids):
    # Split the data into 70% training data and 30% test data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    # Create a perceptron object with the parameters: 40 iterations (epochs) over the data, and a learning rate of 0.1
    ppn = Perceptron(max_iter = 40, eta0=0.1, random_state=0)

    # Train the perceptron
    ppn.fit(X_train, y_train)

    # Apply the trained perceptron on the X data to make predicts for the y test data
    y_pred = ppn.predict(X_test)

    # View the predicted y test data
    y_pred

    # View the true y test data
    y_test

    return accuracy_score(y_test, y_pred)

def gen_user_prediction(uid, model):
    s_oids= get_chrono_oids_by_uid(s_uid, True)

    sdf_prod = df_prod_by_uid(s_uid, s_oids)

    sdf_orders = df_orders_by_uid(s_uid)

    sprod_info = prod_info_from_df(sdf_prod)

    ordered_df = df_from_sprod_info(sprod_info)

    X, y, pids = gen_training_data(ordered_df)
    
    return gen_prediction_result(X, y, pids)
