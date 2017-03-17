# 代码说明文档
队名： 皮皮虾，我们回去吧  
队员： 周杰，欧阳欣， 邓勇  
## 环境需求
### 运行环境
- python2.7 Anaconda 4.0
- Jupyter notebook
### 外部依赖库
- numpy
- pandas
- sklearn
- statsmodels
## 文件
### data

用于存储所有的数据，包括原始数据，额外数据，处理后的数据，模型中间数据以及最后提交的结果。

#### results 
存储模型和规则预测出的最终结果。
#### shop\_info\_name2Id
将商店中的地址、三级分类等名词映射成Id保存在该文件夹下。
#### statistics
原始数据处理后的数据，包括平滑后的数据，天气数据和天气统计。
#### test_train
存储线下线上train和test的特征以及标签文件。
#### weekABCD
线下线上训练集和测试集的划分，按日分。
#### weekABCD_0123
线下线上训练集和测试集的划分（将一天分为四个时间段，没六小时一个时间段）。

### main
主要的数据预处理代码和模型，以及数据分析代码。  
#### analysis
数据分析的代码和统计结果。

#### data_processing
数据预处理，包括数据统计，数据预处理，数据平滑，训练集和测试集划分。
- `avg_smoothing.py` 对数据中的0进行处理，遇到0，用前三星期对应值的平均值替换
- `smoothing.py` 处理数据中的异常值
- `split_test_train.py` 数据集训练集和测试集划分

#### draw_picture
用于画图的一些基本的函数，方便数据的显示和分析
- `draw.py` 画图

#### fuse
模型融合相关文件。
- `fuse.py` 两个模型的结果进行融合，需要运行`run.py`文件来调用。

#### model
我们在比赛中所使用过的模型，包括 ARIMA，GBDT，LR，RF，Extremely Randomized Trees等。
- `base_model.py` ExtraTreeRegreessor模型，是我们在比赛线上线下预测中最主要使用的模型。
- `gbdt.py` 基于GBDT模型的简单预测。
- `RandomForestRegreessor.py` 基于随机森林模型的预测。
- `predict_two_week.py` 与之前复制单周预测不同，直接预测两周结果。
- `multi_mode.py` 不同模型，不同特征，不同参数的结合。
- `use_first_week_predict_second_week.py` 在预测第一周的结果后，将第一周的结果用于第二周的预测。

##### old model
该文件夹下主要是比赛初期使用的一些预测模型，在后来被我们放弃使用。
- `mean_test.py`
均值预测，取最后三周平滑数据对应周期（7）的均值，预测一周销售量，最后输出结果到文件。  
- `lr_test.py` LR预测，使用Ridge回归拟合最后三周的每个商铺的总销售量，预测一周的总销售量，最后输出差值到文件。
- `arima_pred.py` 使用了ARIMA模型进行预测，对数据进行对数惩罚，一阶差分后计算ADF值，找到最稳定的差分项。之后用grid search找出拟合效果最好的模型进行预测。我们采用了bic和smape对模型效果进行评估。

#### rule
主要使用的规则代码，包括节假日（双十一等），天气处理，火锅店单独处理等，执行`run.py`在指定结果上添加规则影响。
- `special_day.py` 对特定的节假日如11月11日进行处理。
- `weather.py` 根据天气值对预测值进行处理
- `hot_pot.py` 对火锅店进行特殊处理
### notebook
为了方便统计数据特征，ARIMA模型结果，可视化结果和特征，我们使用了jupyter notebook来处理和保存含有图片的代码。详见文件夹中具体代码。
### pictures
一些统计信息和图片。