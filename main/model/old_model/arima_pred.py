__author__ = 'Roger'

from product import *

## arima model for predict
## with bic or smape loss
base_path = "../../../data"
f = open(base_path + '/results/predict_arma_61_os_bic_loss_b.csv', 'w')
k = open(base_path + '/results/testroger.csv')

qnm = {}
for line in k.readlines():
    item = line.split(',')
    qnm[int(item[0])] = line

warnings.filterwarnings('ignore')
best_model_list = {}
pd_index = pd.date_range('2016-9-1', periods=75)

index, shop = load_data_as_npdict()


def evalx(shop_series, results_ARMA):
    correct = shop_series
    predict = results_ARMA
    return ali_eval(correct, predict)


total_bic = 0
for i in shop:
    # eval with last 14 days
    # precess data
    train = shop[i][-61:]
    train_mean = np.mean(train)
    for it in range(train.shape[0]):
        if train[it] > train_mean * 3 or train[it] < train_mean * 0.1:
            train[it] = train_mean

    train_eval = train[:-14]
    test_eval = train[-14:]

    train_eval = np.append(train_eval, np.zeros(14))
    # log
    train_eval[:-14] = np.log(train_eval[:-14])

    df = pd.Series(train_eval, index=pd_index[:-14], dtype='f')
    #     print(df)


    #### find d
    # TODO: change if there is some use
    d = 0
    df_diff = copy.deepcopy(df)
    # print(df)
    low_val = 99999
    for d_tmp in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        df_diff = one_step_diff(df, d_tmp)
        value = test_stationarity(df_diff)
        # print(value)
        if value:
            if value < low_val:
                d = d_tmp
                low_val = value
    df_diff = one_step_diff(df, d)
    dd = df_diff[d:-14]

    # grid search
    # find out the best parameters with df_eval (bic or eval)
    P = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    Q = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    p_b = 0
    q_b = 0
    bic_b = 999999999
    for p in P:
        for q in Q:
            df_eval = copy.deepcopy(df_diff)
            # print(df_eval)
            try:
                model = ARMA(dd, order=(p, q))
                result_arma = model.fit(disp=-1, method='css')
                df_eval[-14:] = result_arma.predict('2016-10-18', '2016-10-31', dynamic=True)
                df_eval = one_step_recover(df_eval, d)
                df_eval = np.exp(df_eval)
                value = evalx(test_eval, df_eval[-14:])
                if value < bic_b:
                    p_b = p
                    q_b = q
                    model_b = model
                    bic_b = value
            except:
                continue

    print('{0}th : d={1} p={2} q={3} loss={4}'.format(i, d, p_b, q_b, bic_b))

    ## fit
    train = np.append(train, np.zeros(14))
    # log it
    train[:-14] = np.log(train[:-14])

    df = pd.Series(train, index=pd_index, dtype='f')
    df_diff = one_step_diff(df, d)
    dd = df_diff[d:-14]
    model = ARMA(dd, order=(p_b, q_b))

    # if the series is not stable, then drop it
    try:
        result_arma = model.fit(disp=-1, method='css')
        predict_ts = result_arma.predict()
        df_diff[-14:] = result_arma.predict('2016-11-1', '2016-11-14', dynamic=True)
        df_diff = one_step_recover(df_diff, d)
        recover = np.exp(df_diff)
        r = [int(x) for x in recover[-14:]]
        for index in range(r.__len__()):
            if r[index] < 0:
                r[index] = 0
        s = ','.join([str(x) for x in r])
        f.write('{0},{1}\n'.format(i, s))
    except:
        f.write(qnm[i])
        print('ouch!')

    total_bic += bic_b

# output the mean bic
print('mean bic: {0}'.format(total_bic * 1.0 / 2000))
