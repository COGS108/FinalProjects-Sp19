# Load required libraries
import pandas as pd
import numpy as np
from sklearn import datasets
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Perceptron
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Global Dataframes from Original CSVs
df_orders = pd.read_csv('../instacart-market-basket-analysis/orders.csv')
df_prior = pd.read_csv('../instacart-market-basket-analysis/order_products__prior.csv')
df_aisles = pd.read_csv('../instacart-market-basket-analysis/aisles.csv')
df_depart = pd.read_csv('../instacart-market-basket-analysis/departments.csv')
df_prods  = pd.read_csv('../instacart-market-basket-analysis/products.csv')

# Basic Functions 
def get_uids():
    return list(df_orders['user_id'].drop_duplicates())

# User-id Specific Functions
def get_xids_by_uid(uid):
    oids = get_oids_by_uid(uid, True)
    df_op = df_prior_by_uid(uid, oids)
    pids = list(df_op['product_id'].unique())
    return oids, pids

def get_oids_by_uid(uid, inc_train = False):
    if inc_train:
        associated_oid = list(df_orders.loc[(df_orders['user_id'] == uid)]['order_id'])
    else:
        associated_oid = list(df_orders.loc[(df_orders['user_id'] == uid) & (df_orders['eval_set'] == 'prior')]['order_id'])
    return list(associated_oid)

# Meta-Data Dictionaries from User-Specific Data Frames
def get_pid_metadata(udf):
    pid_metadata = dict()
    for pid in udf.drop(['product_name'], axis=1).fillna(-1).values:
        pid_metadata[pid[0]] = pid[1:]
    return pid_metadata

def get_ord_metadata(udf):
    ord_metadata = dict()
    for oid in udf.drop(['user_id', 'eval_set'], axis=1).fillna(-1).values:
        ord_metadata[oid[0]] = oid[1:]
    return ord_metadata

def ord_prod_metadata(udf_prior):
    ord_prod_dict = dict()
    for i, rows in udf_prior.iterrows():
        oid  = udf_prior.loc[i,'order_id']
        pid  = udf_prior.loc[i,'product_id']
        if ord_prod_dict.get(oid) == None:
            ord_prod_dict[oid] = [pid]
        else:
            ord_prod_dict[oid] = ord_prod_dict.get(oid) + [pid]
    return (ord_prod_dict)

# User-Specific Dataframes
def df_orders_by_uid(uid):
    return df_orders.loc[(df_orders['user_id'] == uid)]

def df_prods_by_uid(uid, pids = list()):
    if len(pids) == 0:
        pids = get_xids_by_uid(uid)[1]
    associated_pid = pids
    master = pd.DataFrame()
    for pid in associated_pid:
        master = master.append(df_prods.loc[df_prods['product_id'] == pid])
    return master

def df_prior_by_uid(uid, oids = list()):
    if len(oids) == 0:
        oids = get_xids_by_uid(uid)[0]
    associated_oid = oids
    master = pd.DataFrame()
    for oid in associated_oid:
        master = master.append(df_prior.loc[df_prior['order_id'] == oid])
    return master

#User-Specific Feature Vector Dataframes
def df_oid_fv_by_uid(uid, pids=list(),opd = dict()):
    if len(pids) == 0:
        pids = get_xids_by_uid(uid)[1]
    if len(opd.keys()) == 0:
        opd = ord_prod_metadata(df_prior_by_uid(uid))
    sprod_info = (pids,opd)
    key = sprod_info[0]
    val = [-1 for x in range(len(key))]
    d = list()
    
    #Order_ID
    for order in sprod_info[1].keys():
        o_dict = dict(zip(key,val))
        pids = sprod_info[1][order]
        for pid in pids:
            o_dict[pid] = 1
        d.append(o_dict)
    p_info = pd.DataFrame(data = d, index = sprod_info[1].keys())
    p_info = p_info[:-1]
    p_info.index.name = "order_id"
    return p_info

def df_oid_fv_by_uid_sp(uid, pids=list(),opd = dict()):
    if len(pids) == 0:
        pids = get_xids_by_uid(uid)[1]
    if len(opd.keys()) == 0:
        opd = ord_prod_metadata(df_prior_by_uid(uid))
    sprod_info = (pids,opd)
    key = sprod_info[0]
    val = [-1 for x in range(len(key))]
    d = list()
    
    #Order_ID
    for order in sprod_info[1].keys():
        o_dict = dict(zip(key,val))
        pids = sprod_info[1][order]
        for pid in pids:
            o_dict[pid] = 1
        d.append(o_dict)
    p_info = pd.DataFrame(data = d, index = sprod_info[1].keys())
    p_info.index.name = "order_id"
    return p_info

def get_feat_index(feat_str):
    feat_index_dict = {
        'num'  : 0,
        'dow'  : 1,
        'hod'  : 2,
        'dspo' : 3,
        'aisle': 0,
        'dep'  : 1}
    return feat_index_dict.get(feat_str)

def get_feat_dict(uid, feat_str):
    if feat_str in ['num','dow','hod','dspo']:
        return get_ord_metadata(df_orders_by_uid(uid))
    elif feat_str in ['aisle', 'dep']:
        return get_pid_metadata(df_prods_by_uid(uid))

def df_oxx_fv_by_uid(uid, feat,pids=list(),opd = dict()):
    index = get_feat_index(feat)
    if len(pids) == 0:
        pids = get_xids_by_uid(uid)[1]
    if len(opd.keys()) == 0:
        opd = ord_prod_metadata(df_prior_by_uid(uid))
    sprod_info = (pids,opd)
    key = sprod_info[0]
    val = [-1 for x in range(len(key))]
    d = list()

    #Order_XX
    xxs = [str(oid)+"_"+feat for oid in sprod_info[1].keys()]
    
    omd = get_feat_dict(uid,feat)
    for i in range(len(xxs)):
        order = list(sprod_info[1].keys())[i]
        o_dict = dict(zip(key,val))
        pids = sprod_info[1][order]
        for pid in pids:
            o_dict[pid] = omd[order][index]
        d.append(o_dict)
    new_index = list(sprod_info[1].keys())+xxs

    p_info = pd.DataFrame(data = d, index = xxs)
    p_info.index.name = "order_"+feat
    return p_info

def df_onum_fv_by_uid(uid, pids=list(),opd = dict()):
    return df_oxx_fv_by_uid(uid,'num',pids,opd)

def df_odow_fv_by_uid(uid, pids=list(),opd = dict()):
    return df_oxx_fv_by_uid(uid,'dow',pids,opd)

def df_ohod_fv_by_uid(uid, pids=list(),opd = dict()):
    return df_oxx_fv_by_uid(uid,'hod',pids,opd)

def df_odspo_fv_by_uid(uid, pids=list(),opd = dict()):
    return df_oxx_fv_by_uid(uid,'dspo',pids,opd)

def df_paisle_fv_by_uid(uid):
    df_fv = pd.DataFrame(get_pid_metadata(df_prods_by_uid(uid)), index=['p_aisle', 'p_dep'])
    return df_fv.drop(['p_dep'])

def df_pdep_fv_by_uid(uid):
    df_fv = pd.DataFrame(get_pid_metadata(df_prods_by_uid(uid)), index=['p_aisle', 'p_dep'])
    return df_fv.drop(['p_aisle'])

def gen_training_data(uid,df,ordered=False):
    o_df = df_oid_fv_by_uid_sp(uid)
    s_pids = list(df.columns)
    features = list()
    o_s_pids = list(o_df.columns)
    o_labels = list()
    for i in range(len(s_pids)):
        feat = list(df[s_pids[i]])
        features.append(feat)
        
        o_feat = list(o_df[s_pids[i]])
        o_labels.append(o_feat[-1])
        
    return features, o_labels, s_pids
    

def gen_prediction_result(X, y, pids):
    # Split the data into 70% training data and 30% test data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    # Create a perceptron object with the parameters: 40 iterations (epochs) over the data, and a learning rate of 0.1
    model = Perceptron(max_iter = 40, eta0=0.1, random_state=0)

    # Train the perceptron
    if len(np.unique(y_train)) <= 1:
        return -1.0
    model.fit(X_train, y_train)

    # Apply the trained perceptron on the X data to make predicts for the y test data
    y_pred = model.predict(X_test)

    # View the predicted y test data
    y_pred

    # View the true y test data
    y_test

    return accuracy_score(y_test, y_pred)

def gen_user_prediction(uid,feats):
    df_feat_vecs = list()
    pids = get_xids_by_uid(uid)[1]
    opd = ord_prod_metadata(df_prior_by_uid(uid))
    for feat in feats:
        if feat == 'ordered':
            df_feat_vecs.append(df_oid_fv_by_uid(uid,pids,opd))
        elif feat == 'num':
            df_feat_vecs.append(df_onum_fv_by_uid(uid,pids,opd))
        elif feat == 'dow':
            df_feat_vecs.append(df_odow_fv_by_uid(uid,pids,opd))
        elif feat == 'hod':
            df_feat_vecs.append(df_ohod_fv_by_uid(uid,pids,opd)) 
        elif feat == 'dspo':
            df_feat_vecs.append(df_odspo_fv_by_uid(uid,pids,opd))
        elif feat == 'aisle':
            df_feat_vecs.append(df_paisle_fv_by_uid(uid))
        elif feat == 'dep':
            df_feat_vecs.append(df_pdep_fv_by_uid(uid))
    
    df_combined_fv = pd.concat(df_feat_vecs)
    
    if feats == ['ordered']:
        X, y, pids = gen_training_data(uid,df_combined_fv,ordered=True)
    else:
        X, y, pids = gen_training_data(uid,df_combined_fv)
    
    return gen_prediction_result(X, y, pids)


def build_pred_results(uids, feats):
    master = pd.DataFrame()
    uid_result = dict()
    total = len(uids)*len(feats)
    counter = 0
    for i in range(len(feats)):
        prd_result = list()
        for uid in uids:
            prd_result.append(gen_user_prediction(uid,[feats[i]]))
            counter += 1
            print('{}% of the way there'.format((counter/total)*100))
        uid_result['Acc. with '+feats[i]] = prd_result
    master = pd.DataFrame.from_dict(uid_result)
    master['uids'] = uids
    master = master.set_index('uids')
    return master


r_uids = [183213,51522,
 106239,
 9082,
 140560,
 100814,
 154365,
 94588,
 56744,
 142367,
 96873,
 6628,
 50123,
 108117,
 158954,
 62410,
 7332,
 162675,
 89979,
 117550,
 172652,
 150603,
 63727,
 136381,
 184481,
 41598,
 174128,
 26096,
 187647,
 54700,
 74869,
 92686,
 146395,
 155635,
 119416,
 76795,
 35137,
 187464,
 46852,
 97963,
 160684,
 117096,
 174175,
 159509,
 194586,
 94909,
 168326,
 105357,
 44671,
 32783,
 135770,
 14832,
 2531,
 123021,
 122101,
 144697,
 134175,
 42375,
 18480,
 6595,
 48116,
 114398,
 38886,
 78063,
 152825,
 17279,
 200783,
 193015,
 72609,
 123959,
 143449,
 166429,
 18205,
 17219,
 52185,
 109530,
 190029,
 131827,
 57945,
 26930,
 126406,
 167625,
 23301,
 153365,
 98016,
 138053,
 80790,
 149718,
 175754,
 148713,
 49596,
 81828,
 74591,
 148587,
 76440,
 177753,
 53552,
 92322,
 93381,
 12022,
 52302,
 205118,
 28435,
 10457,
 145449,
 60752,
 153940,
 139010,
 189817,
 78123,
 168185,
 150831,
 171994,
 127706,
 189615,
 62940,
 93690,
 182952,
 87614,
 109899,
 86960,
 99100,
 204156,
 64639,
 72120,
 150579,
 88526,
 80006,
 180953,
 204122,
 113527,
 195625,
 171523,
 193386,
 92234,
 194951,
 29295,
 677,
 103069,
 79146,
 35945,
 32622,
 36628,
 128404,
 32723,
 134847,
 13225,
 35127,
 15264,
 80811,
 129374,
 192273,
 138163,
 70761,
 32861,
 64490,
 194186,
 130484,
 72281,
 23122,
 124534,
 41217,
 141859,
 13899,
 159753,
 125229,
 201625,
 188177,
 114768,
 51151,
 172163,
 41152,
 82007,
 202071,
 120784,
 137560,
 95696,
 140806,
 48342,
 192496,
 49520,
 129414,
 189231,
 127892,
 193179,
 51525,
 90184,
 105076,
 58973,
 17502,
 81326,
 50316,
 137773,
 81872,
 130883,
 163952,
 100415,
 108054,
 198990,
 94580,
 187941,
 13325,
 20963,
 149037,
 68735,
 81339,
 72119,
 11307,
 135613,
 88872,
 106267,
 81160,
 28334,
 49860,
 191324,
 165983,
 130493,
 134297,
 87309,
 195322,
 148382,
 172843,
 203485,
 199852,
 36762,
 3224,
 73996,
 143685,
 131498,
 99618,
 58546,
 203763,
 132729,
 46012,
 4401,
 16350,
 154277,
 14192,
 99782,
 2353,
 163277,
 118979,
 42296,
 137929,
 6845,
 90097,
 91845,
 142340,
 195072,
 170280,
 54853,
 86480,
 16868,
 24389,
 10086,
 8149,
 77746,
 144919,
 87649,
 151165,
 141885,
 142505,
 1397,
 751,
 124140,
 55864,
 5499,
 4696,
 125242,
 80925,
 42767,
 68407,
 37234,
 127074,
 197394,
 166851,
 188067,
 6151,
 69675,
 195166,
 49838,
 54512,
 63533,
 105229,
 135926,
 91157,
 16145,
 51708,
 115761,
 99928,
 135510,
 108659,
 119613,
 193736,
 88324,
 50813,
 193868,
 46974,
 196025,
 82734,
 38449,
 5013,
 205149,
 205181,
 197657,
 118816,
 25053,
 206184,
 62051,
 74800,
 14569,
 186704,
 158846,
 166794,
 186866,
 156622,
 183440,
 187072,
 109843,
 4836,
 17925,
 141967,
 168110,
 87302,
 182990,
 1665,
 109778,
 112920,
 142603,
 81423,
 3953,
 109345,
 25085,
 6240,
 121551,
 182104,
 51882,
 50633,
 133228,
 120650,
 143954,
 101866,
 31614,
 49614,
 11825,
 167245,
 24645,
 193064,
 172582,
 104965,
 191587,
 39525,
 114842,
 182466,
 61967,
 161730,
 123375,
 89568,
 85597,
 122107,
 48182,
 106200,
 71876,
 153751,
 170599,
 160710,
 161169,
 143375,
 110074,
 97606,
 30076,
 23147,
 61762,
 11451,
 123920,
 144957,
 24092,
 44279,
 59447,
 198685,
 189641,
 204522,
 16877,
 31686,
 119886,
 181224,
 22080,
 188594,
 108132,
 97784,
 1407,
 44740,
 202615,
 16910,
 56148,
 202904,
 61422,
 7403,
 57882,
 75400,
 133358,
 115120,
 148305,
 19027,
 81322,
 61584,
 126524,
 69674,
 30257,
 200662,
 144675,
 12691,
 5788,
 79060,
 76660,
 146060,
 1858,
 188740,
 150545,
 152206,
 170878,
 204164,
 141496,
 27249,
 110167,
 23510,
 172828,
 114428,
 167866,
 50514,
 139387,
 128738,
 34737,
 43180,
 166880,
 151446,
 141303,
 80537,
 64222,
 36075,
 144747,
 95631,
 90609,
 90900,
 176267,
 202106,
 167734,
 39182,
 181798,
 77055,
 159945,
 114502,
 121210,
 141697,
 103850,
 155422,
 177525,
 97327,
 199930,
 53846,
 189324,
 107889,
 91654,
 49991,
 76828,
 173310,
 195254,
 25287,
 172907,
 57237,
 115211,
 170979,
 171205,
 11042,
 164920,
 169237,
 73491,
 112217,
 16984,
 6199,
 115546,
 34617,
 191072,
 4341,
 145961,
 10089,
 89348,
 165563,
 136965,
 102582,
 69238,
 21251,
 8088,
 69893,
 203871,
 30392,
 18002,
 17959,
 16827,
 130134]