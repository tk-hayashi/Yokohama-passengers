import re
import zenhan
import datetime
import pandas as pd


class Line:
    def __init__(self, file_name, line_str, skip_rows, use_cols):
        self.file_name = file_name
        self.line_str = line_str
        self.skip_rows = skip_rows
        self.use_cols = use_cols


class Passengers:
    def __init__(self, line=None):
        self.passengers = []
        if line:
            self.read_csv(line=line)

    def read_csv(self, csv_file=None,
                 skip_rows=None,
                 use_cols=None,
                 line_str=None,
                 line=None):

        if line is not None:
            csv_file = line.file_name
            skip_rows = line.skip_rows
            use_cols = line.use_cols
            line_str = line.line_str

        if csv_file is None:
            return self
        if skip_rows is None:
            return self
        if use_cols is None:
            return self

        # シート名を取得する
        excel = pd.ExcelFile(csv_file)
        sheets = []
        for sheet in excel.sheet_names:
            if re.match("^H[0-9]+$", sheet):
                sheets.append(sheet)

        df = None
        for sheet in sheets:
            try:
                df_sheet = pd.read_excel(csv_file,
                                         sheet_name=sheet,
                                         skiprows=skip_rows,
                                         nrows=12,
                                         usecols=use_cols,
                                         index_col=0
                                         )
                df_sheet = df_sheet.convert_objects(convert_numeric=True)
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

                df_sheet = df_sheet.rename(columns={'Unnamed:1': '総数'})

                if line_str is not None:
                    tmp_columns = df_sheet.columns.tolist()
                    df_line = df_sheet['総数']
                    df_sheet = pd.concat([df_sheet, df_line], axis=1)
                    tmp_columns.append(line_str)
                    df_sheet.columns = tmp_columns

                # シートを結合
                if df is None:
                    df = df_sheet
                else:
                    df = pd.concat([df, df_sheet])

            except:
                print("skip " + sheet)

        df = df.sort_index()

        # 既存のデータに結合
        if len(self.passengers):
            self.passengers = pd.concat([self.passengers, df], axis=1, join='inner')
            self.passengers = self.passengers.groupby(level=0, axis=1).sum()
        else:
            self.passengers = df
        return self
