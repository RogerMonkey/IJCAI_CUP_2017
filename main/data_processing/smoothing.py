# coding=utf-8
import datetime, math
import pandas as pd
import numpy as np

'''
对ABCDE五周的数据异常点进行处理，数据进行平滑
get_static_week()函数通过对最后三个月数据处理得到标准的一星期的数据，保存到week_out.csv文件中
根据balance函数对五周的数据分别进行处理，对数据进行平滑
'''


def get_static_week():
    startDay = datetime.datetime.strptime("2016-10-31", "%Y-%m-%d")
    DUR = 14
    holiday = ['2016-01-01', '2016-01-02', '2016-01-03', '2016-02-07', '2016-02-08', '2016-02-09', '2016-02-10',
               '2016-02-11', '2016-02-12', '2016-02-13', '2016-04-02', '2016-04-03', '2016-04-04', '2016-04-30',
               '2016-05-01', '2016-05-02', '2016-06-09', '2016-06-10', '2016-06-11', '2016-09-15', '2016-09-16',
               '2016-09-17', '2016-10-01', '2016-10-02', '2016-10-03', '2016-10-04', '2016-10-05', '2016-10-06',
               '2016-10-07', '2016-02-15', '2016-06-12', '2016-09-18', '2016-10-08', '2016-10-09']

    f_out1 = open('./feat_week.csv', 'w')
    print >> f_out1, "shopid,daym0,daym1,daym2,daym3,daym4,daym5,daym6,dayper0,dayper1,dayper2,dayper3,dayper4,dayper5,dayper6,days0,days1,days2,days3,days4,days5,days6"
    paynd = None
    for line in open('./shop_pay_statistics.txt'):
        line = line.strip()
        if not line:
            continue
        array = line.split(',', -1)

        shutdays = 0
        for i in range(len(array) - 90, len(array)):
            if int(array[i]) == 0:
                shutdays += 1
            else:
                if shutdays >= 7:
                    if i + 7 < len(array) and int(array[i + 7]) != 0:
                        array[i] = str(int(round((int(array[i]) + int(array[i + 7])) / 2)))
                    else:
                        array[i] = str(int(round(int(array[i]) * 1.3)))
                shutdays = 0

        shopid = array[0]
        # print shopid
        csum = [0] * 7
        dsum = [0] * 7
        psum = [0] * 7
        msum = [0.0] * 7
        stdsum = [0.0] * 7
        errsum = [0] * 7
        zerosum = [0] * 7

        for i in range(0, 7):
            lastday = startDay - datetime.timedelta(days=i)
            day = lastday.weekday()
            offset = 0 + i
            while csum[day] < 5 and offset < 60:
                if (startDay - datetime.timedelta(days=offset)).strftime("%Y-%m-%d") in holiday:
                    offset += 7
                    continue
                if int(array[len(array) - offset - 1]) != 0:
                    dsum[day] += int(array[len(array) - offset - 1])
                    csum[day] += 1
                elif offset < 35:
                    zerosum[day] += 1
                offset += 7
        for i in range(0, 7):
            msum[i] = round(float(dsum[i]) / csum[day], 2)
            if zerosum[i] >= 3:
                print shopid, 'errorzero', i, zerosum[i], msum[i]
        for i in range(0, 7):
            psum[i] = round(float(msum[i]) / sum(msum), 3)
        dsum = [0] * 7
        csum = [0] * 7

        for i in range(len(array) - 35, len(array)):
            day = (datetime.datetime.strptime("2015-06-26", "%Y-%m-%d") + datetime.timedelta(days=i - 1)).weekday()
            if (datetime.datetime.strptime("2015-06-26", "%Y-%m-%d") + datetime.timedelta(days=i - 1)).strftime(
                    "%Y-%m-%d") in holiday:
                continue
            stdsum[day] += (int(array[i]) - msum[day]) ** 2
            if int(array[i]) != 0 and not 0.5 < (1.0 * int(array[i])) / msum[day] < 2.0:  # 0.5  2.0
                errsum[day] += 1
            elif int(array[i]) != 0 and not 0.3 < (1.0 * int(array[i])) / msum[day] < 3.0:  # 0.3 3
                errsum[day] += 2
            if int(array[i]) != 0 and 0.33 < (1.0 * int(array[i])) / msum[day] < 2.5:  # 3
                dsum[day] += int(array[i])
                csum[day] += 1
        for i in range(len(array) - 14, len(array)):
            day = (datetime.datetime.strptime("2015-06-26", "%Y-%m-%d") + datetime.timedelta(days=i - 1)).weekday()
            if (datetime.datetime.strptime("2015-06-26", "%Y-%m-%d") + datetime.timedelta(days=i - 1)).strftime(
                    "%Y-%m-%d") in holiday:
                continue
            stdsum[day] += (int(array[i]) - msum[day]) ** 2
            if int(array[i]) != 0 and 0.75 < (1.0 * int(array[i])) / msum[day] < 1.5:
                dsum[day] += int(array[i])
                csum[day] += 1
        for i in range(0, 7):
            if csum[i] <= 1:
                print shopid, 'error few sample', i, csum, msum[i]
                csum[i] = 1
                dsum[i] = msum[i]
            if errsum[i] >= 3:
                print shopid, 'error big std sample', i, errsum[i], msum[i]
                # TODO 1918
            msum[i] = round(float(dsum[i]) / csum[i], 2)
        allsum = sum(dsum)
        for i in range(0, 7):
            stdsum[i] = round(math.sqrt(float(stdsum[i]) / csum[i]) / (allsum / sum(csum)), 2)
        print >> f_out1, shopid + "," + ",".join(map(lambda x: str(x), msum)) + "," + ",".join(
            map(lambda x: str(x), psum)) + "," + ",".join(map(lambda x: str(x), stdsum))

    f_out1.close()

    data = pd.read_csv('./feat_week.csv', index_col=['shopid'])

    data.iloc[22, 0:7] = [117, 122, 136, 114, 123, 43, 33]
    data.iloc[523, 5:7] = [5, 5]
    data.iloc[809, 0:7] = data.iloc[809, 0:7] * 1.5
    data.iloc[1823, 0:7] = data.iloc[809, 0:7] * 0
    data.iloc[1917, 3] = 6.0
    data.iloc[631, 0:7] = [49.0] * 7

    week = pd.concat([data.iloc[:, 1:7], data.iloc[:, 0:1]], axis=1)
    output = pd.concat([week * 1.02, week * 1.02], axis=1)
    output.astype(int).to_csv('./week_output.csv', header=None)

def balanceDf2(weekDF, standardDF, times=15):
    ans=[]
    for i in range(weekDF.shape[0]):
        tmp = np.array(balance(np.array(weekDF.iloc[i, :]), np.array(standardDF.iloc[i, :]), times))
        ans.append(tmp)
    return ans


def balance(weekList, standardList, times):
    if sum(standardList) == 0:
        return weekList
    diff = weekList - standardList
    mean = diff.mean()
    count = 0
    while count < times and (abs(diff - mean)).max() > max(min(abs(mean), 40), 2):
        pos = (abs(diff - mean)).argmax()
        diff[pos] = (diff[pos] + mean) / 2
        mean = diff.mean()
        count += 1
    weekList = (diff + standardList).round()
    return weekList

def writeto(dates,weekList,fileto):
    fr_to=open(fileto,"w")
    fr_to.write("shop_id")
    for date in dates:
        fr_to.write(","+date)
    fr_to.write("\n")
    for i in range(0,2000):
        fr_to.write(str(i+1))
        for data in weekList[i]:
            fr_to.write(","+str(data))
        fr_to.write("\n")
    fr_to.close()

def week4(data2):
    weekDF = data2.ix[:, 488:494]
    weekList = balanceDf2(weekDF=weekDF, standardDF=standardDF)
    dates = ['2016-10-25', '2016-10-26', '2016-10-27', '2016-10-28', '2016-10-29', '2016-10-30', '2016-10-31']
    writeto(dates, weekList, "../../data/weekABCD/week4.csv")

def week3(data2):
    weekDF = data2.ix[:, 481:487]
    weekList = balanceDf2(weekDF=weekDF, standardDF=standardDF)
    dates = ['2016-10-18', '2016-10-19', '2016-10-20', '2016-10-21', '2016-10-22', '2016-10-23', '2016-10-24']
    writeto(dates, weekList, "../../data/weekABCD/week3.csv")

def week2(data2):
    weekDF = data2.ix[:, 474:480]
    weekList = balanceDf2(weekDF=weekDF, standardDF=standardDF)
    dates = ['2016-10-11', '2016-10-12', '2016-10-13', '2016-10-14', '2016-10-15', '2016-10-16', '2016-10-17']
    writeto(dates, weekList, "../../data/weekABCD/week2.csv")

def week1(data2):
    weekDF = data2.ix[:, 453:459]
    weekList = balanceDf2(weekDF=weekDF, standardDF=standardDF)
    dates = ['2016-09-20', '2016-09-21', '2016-09-22', '2016-09-23', '2016-09-24', '2016-09-25', '2016-09-26']
    writeto(dates, weekList, "../../data/weekABCD/week1.csv")

def week0(data2):
    weekDF = data2.ix[:, 446:452]
    weekList = balanceDf2(weekDF=weekDF, standardDF=standardDF)
    dates = ['2016-09-13', '2016-09-14', '2016-09-15', '2016-09-16', '2016-09-17', '2016-09-18', '2016-09-19']
    writeto(dates, weekList, "../../data/weekABCD/week0.csv")

if __name__ == '__main__':
    get_static_week()
    data1 = pd.read_csv('./week_output.csv', names=range(0, 15))
    standardDF = data1.ix[:, 1:7]
    # print standardDF.shape
    data2 = pd.read_csv('../../data/statistics/shop_day_num.txt', names=range(0, 495))
    week4(data2)
    week3(data2)
    week2(data2)
    week1(data2)
    week0(data2)
