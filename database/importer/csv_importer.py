import sqlite3
import pandas as pd

from database.consts import DATABASE_NAME
from database.utils import get_table_columns

INSERT_STATEMENT = """
INSERT INTO {table}({columns})
VALUES ({values})
ON CONFLICT ({index_column}) DO UPDATE SET {update_rows};
"""


class CsvImporter():
    def __init__(self, csv_path: str, table_name: str) -> None:
        self.dataset = pd.read_csv(csv_path, delimiter=";")
        self.__normalize_df_column_names(self.dataset)
        self.table_name = table_name

    def import_csv(self) -> None:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        df = self.__prepare_df(self.dataset)

        for _, row in df.iterrows():
            statement = self.__build_insert_statement(row)
            cursor.execute(statement)

        conn.commit()
        conn.close()

    def __prepare_df(self, df: pd.DataFrame) -> pd.DataFrame:
        table_columns = get_table_columns(self.table_name)

        column_names = {}
        for column in df.columns:
            formatted_column = column.lower()
            for table_column in table_columns:
                if formatted_column == table_column.lower():
                    column_names[column] = table_column

        df = df.rename(columns=column_names)

        for column in df.columns:
            if column not in table_columns:
                df.drop(column, axis=1, inplace=True)

        return df

    def __normalize_df_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        df.columns = df.columns.str.replace(" ", "")
        df.columns = df.columns.str.replace("_", "")

    def __build_set_sql_statement(self, columns: list, values: list) -> str:
        set_columns = []
        for column, value in zip(columns, values):
            if type(value) == str:
                value = f'"{value}"'

            if pd.isnull(value):
                value = "NULL"

            set_string = f"{column}={value}"
            set_columns.append(set_string)

        return ", ".join(set_columns)

    def __build_insert_statement(self, row: pd.Series) -> str:
        update_rows = self.__build_set_sql_statement(
            list(row.index), list(row.values))
        columns = ", ".join(row.index)

        def map_values(value):
            if type(value) == str:
                return f'"{value}"'

            if pd.isnull(value):
                return "NULL"

            return str(value)

        values = [value for value in map(map_values, row.values)]
        values = ", ".join(values)

        insert_tatement = INSERT_STATEMENT.format(
            table=self.table_name,
            columns=columns,
            values=values,
            index_column="URL",
            update_rows=update_rows
        )

        return insert_tatement
