import pyspark
from typing import Dict, List
from .pyspark_dataframe_methods import cleanList


class CleanDataframe:
    def __init__(self, df: pyspark.sql.DataFrame):
        """
        Initialize CleanDataframe with a DataFrame.
        """
        if not isinstance(df, pyspark.sql.DataFrame):
            raise TypeError("df must be a pyspark.sql.DataFrame")

        self._original_df = df
        self._df = df

    def get_dataframe(self) -> pyspark.sql.DataFrame:
        """
        Get the cleaned DataFrame.
        """
        return self._df

    def get_original_dataframe(self) -> pyspark.sql.DataFrame:
        """
        Get the original DataFrame.
        """
        return self._original_df


class SilverCleanDataframe(CleanDataframe):
    def __init__(self, df: pyspark.sql.DataFrame,
                 nested_columns: Dict[str, pyspark.sql.Column] = None,
                 list_value_columns: Dict[str, str] = None,
                 remove_old_list_value_columns: bool = True,
                 split_df: bool = False,
                 column_to_split: str = None,
                 primary_foreign_key: str = None):
        """
        Initialize SilverCleanDataframe with additional parameters.
        """
        if not isinstance(df, pyspark.sql.DataFrame):
            raise TypeError("df must be a pyspark.sql.DataFrame")
        if not isinstance(nested_columns, dict) and nested_columns is not None:
            raise TypeError("nested_columns must be a dictionary")
        if not isinstance(list_value_columns, dict) and list_value_columns is not None:
            raise TypeError("list_value_columns must be a dictionary")
        if not isinstance(remove_old_list_value_columns, bool):
            raise TypeError("remove_old_list_value_columns must be a boolean")
        if not isinstance(split_df, bool):
            raise TypeError("split_df must be a boolean")
        if not isinstance(column_to_split, str) and column_to_split is not None:
            raise TypeError("column_to_split must be a string")
        if not isinstance(primary_foreign_key, str) and primary_foreign_key is not None:
            raise TypeError("primary_foreign_key must be a string")

        if split_df:
            if not column_to_split or not primary_foreign_key:
                raise ValueError(
                    "Both column_to_split and primary_foreign_key must be specified when split_df is True")

        super().__init__(df)
        self._nested_columns = nested_columns
        self._list_value_columns = list_value_columns
        self._remove_old_list_value_columns = remove_old_list_value_columns
        self._split_df = split_df
        self._column_to_split = column_to_split
        self._primary_foreign_key = primary_foreign_key
        pyspark.sql.DataFrame.cleanList = cleanList

    def _clean_nested_columns(self, nested_columns: Dict[str, pyspark.sql.Column]):
        """
        Clean nested columns.
        """
        for new_column, field_to_extract in nested_columns.items():
            self._df = self._df.withColumn(new_column, field_to_extract)

    def _clean_list_value_columns(self, list_value_columns: Dict[str, str]):
        """
        Clean list value columns.
        """
        self._df = self._df.cleanList(
            list_value_columns, drop=self._remove_old_list_value_columns)

    def _split_dataframe(self, column_to_split: str, primary_foreign_key: str):
        """
        Split the DataFrame.
        """
        df1 = self._df.select("*").drop(column_to_split)
        df2 = self._df.select(primary_foreign_key, column_to_split)
        self._df = (df1, df2)

    def clean(self):
        """
        Clean the DataFrame.
        """

        if self._nested_columns:
            # Clean nested columns
            self._clean_nested_columns(self._nested_columns)

        if self._list_value_columns:
            # Clean list value columns
            self._clean_list_value_columns(self._list_value_columns)

        if self._split_df:
            # Split dataframe
            self._split_dataframe(self._column_to_split,
                                  self._primary_foreign_key)

        # Return the cleaned DataFrame
        return self.get_dataframe()


class GoldCleanDataframe(CleanDataframe):
    def __init__(self,
                 df: pyspark.sql.DataFrame,
                 drop_duplicate: bool = False,
                 subset: List[str] = None,
                 drop_columns: List[str] = None,
                 drop_null: bool = False):
        # Check type of argument
        if not isinstance(df, pyspark.sql.DataFrame):
            raise TypeError("df must be a pyspark.sql.DataFrame")
        if not isinstance(drop_duplicate, bool):
            raise TypeError("drop_duplicate must be a boolean")
        if not isinstance(subset, list) and subset is not None:
            raise TypeError("subset must be a list")
        if not isinstance(drop_columns, list) and drop_columns is not None:
            raise TypeError("drop_columns must be a list")
        if not isinstance(drop_null, bool):
            raise TypeError("drop_null must be a boolean")

        super().__init__(df)
        self.drop_duplicate = drop_duplicate
        self.subset = subset
        self.drop_columns = drop_columns
        self.drop_null = drop_null

    def _drop_duplicate(self):
        """
        Drop duplicate rows.
        """
        self._df = self._df.dropDuplicates(subset=self.subset)

    def _drop_columns(self, columns: List[str]):
        """
        Drop columns.
        """
        self._df = self._df.drop(*columns)

    def _drop_null(self):
        """
        Drop null values.
        """
        self._df = self._df.dropna(how="all")

    def clean(self):
        """
        Clean the DataFrame.
        """
        if self.drop_duplicate:
            # Drop duplicate rows
            self._drop_duplicate()

        if self.drop_null:
            # Drop null values
            self._drop_null()

        if self.drop_columns:
            # Drop columns
            self._drop_columns(self.drop_columns)

        # Return the cleaned DataFrame
        return self.get_dataframe()
