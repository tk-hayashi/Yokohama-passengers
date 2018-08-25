import re
import zenhan
import datetime
import pandas as pd


class Passengers:
    skip_rows = list(range(0, 11)) + list(range(12, 15))
    use_cols = list(range(1, 12))

    def __init__(self):
        self.passengers = []

    def read_csv(self, csv_file,
                 skip_rows=skip_rows,
                 use_cols=use_cols):

        excel = pd.ExcelFile(csv_file)
        sheets = []

        for sheet in excel.sheet_names:
            if re.match("^H[0-9]+$", sheet):
                sheets.append(sheet)

        for i, sheet in enumerate(sheets):
            df_sheet = pd.read_excel(csv_file,
                                     sheet_name=sheet,
                                     skiprows=skip_rows,
                                     nrows=12,
                                     usecols=use_cols,
                                     index_col=0
                                     )
            df_sheet = df_sheet.dropna()

            # indexをdatetime形式にする
            new_index = []
            for index in df_sheet.index:
                month = int(re.findall("[0-9]+", zenhan.z2h(index))[-1])
                year = int(re.findall("[0-9]+", sheet)[0])
                if month >= 4:
                    year = year + 1988
                else:
                    year = year + 1989
                dt = datetime.datetime(year, month, 1)
                new_index.append(dt)
            df_sheet.index = new_index

            new_columns = []
            for column in df_sheet.columns:
                column = column.replace(' ','')
                column = column.replace('　', '')
                new_columns.append(column)
            df_sheet.columns = new_columns

            # 全シートを結合
            if i == 0:
                df = df_sheet
            else:
                df = pd.concat([df, df_sheet])
        df = df.sort_index()

        # 既存のデータに結合
        if len(self.passengers):
            self.passengers = pd.concat([self.passengers, df], axis=1, join='inner')
            self.passengers = self.passengers.groupby(level=0, axis=1).sum()
        else:
            self.passengers = df
        return self
