import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import argparse

# импорт моделей
import xgboost as xg
from sklearn.ensemble import RandomForestRegressor

# импорт метрики
from sklearn.metrics import mean_absolute_error


def run_neural_network(path: str, is_forecast: bool, target_path: str):
    # загружаем данные, устанавливаем месячный период
    ds=pd.read_csv(path, sep='\t', index_col='DateObserve')
    ds.index = pd.to_datetime(ds.index).to_period('M')

    # Убираем из данных пропуски, дубликаты, заполняем до однородных временных меток
    ds.drop_duplicates(subset=['WebPriceId','CurrentPrice'],keep= False, inplace=True)
    ds = ds[['WebPriceId','CurrentPrice']]
    ds = ds.dropna()
    ds = ds.reset_index()
    ds = ds.drop_duplicates(subset=['DateObserve','WebPriceId'], keep='last')
    ds=ds.set_index(['DateObserve','WebPriceId']).unstack(fill_value=0).asfreq('M', fill_value=0).stack().sort_index(level=1).reset_index()
    ds.CurrentPrice = ds.CurrentPrice.replace(to_replace=0, method ='ffill')
    ds = ds[(ds != 0).all(1)]

    #Расчет множителя ИПЦ
    ds['CPI_multi'] = ds['CurrentPrice'].iloc[-1] / ds['CurrentPrice']
    df = ds.groupby('DateObserve')['CPI_multi'].mean()

    df = df.to_frame(name='cpi_multi')

    if not is_forecast:
          # загружаем таргет 
        data = pd.read_excel("target_path", index_col='Период')
        data.index = pd.to_datetime(data.index).to_period('M')
        # соединяем таблицы
        ds = df.join(data, how='outer')

        """ разделяем на тестовую и тренировочную выборки"""

        train, test = ds[0:23], ds[23:]

        # Убираем из тренировочной выборки таргет
        y_train= train['Целевой показатель']
        x_train = train.drop(labels = ['Целевой показатель'], axis=1)

        y_test = test['Целевой показатель']
        x_test = test.drop(labels = ['Целевой показатель'], axis=1)

        

        xgb_r = xg.XGBRegressor(objective ='reg:linear',
                        n_estimators = 10, seed = 123)

        # Fitting the model
        xgb_r.fit(x_train, y_train)
        
        # Predict the model
        pred = xgb_r.predict(x_test)
        mean_absolute_error(test['Целевой показатель'], pred)
        xgb_r.save_model("model.json")

        # сохраняем и возвращаем результат в виде таблицы

        ds = ds.reset_index()
        y = y_train.reset_index()
        y = np.array(y[['Целевой показатель']])

        tdf = pd.DataFrame({'период':np.array(ds.DateObserve), 'целевая функция':y})

        tdf.to_csv(f'result.csv',index = False)

        return tdf.to_json()


if __name__ == "__main__":
    """получение пути к файлу и имени датасета"""
    parser = argparse.ArgumentParser(description='Передайте путь к датасету и действие обучение\прогноз')
    parser.add_argument('path', type=str)
    parser.add_argument('forecast', type=bool)
    parser.add_argument('target_path', type=str)
    args = parser.parse_args()

    path = args.path
    is_forecast = args.forecast #True если предсказать, False если обучить
    target_path = args.target_path

    run_neural_network(path, is_forecast, target_path)