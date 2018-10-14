# Yokohama-passengers
time-series analysis of the number of passengers at Yokohama city

横浜市の電車乗客数の各駅の予測  
データは下記からダウンロードすることを想定  
http://www.city.yokohama.lg.jp/ex/stat/toukeisho/new/index2.html#13

* passengers.py	
  * excelファイルを読み込むためのclassを定義
* resultディレクトリ
  * 実行結果例
* check_read_csv.ipynb
  * passengers.pyの実行確認
* SARIMAX.ipynb
  * SARIMAモデルによる乗客数予測
* prophet.ipynb
  * prophet(Facebook製時系列予測モジュール)による乗客数予測
* RNN.ipynb
  * RNNによる乗客数予測（未完成）
* clustering.ipynb
  * 駅の時系列データクラスタリング
