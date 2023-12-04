from pyspark.sql.functions import col, explode


def cleanList(self, columns: dict, drop: bool = False):
    # Check type of argument
    if not isinstance(columns, dict):
        raise TypeError("Columns must be a dictionary")
    if not isinstance(drop, bool):
        raise TypeError("Drop must be a boolean")

    df_exploded = self

    for old_column in columns.keys():
        new_column = columns[old_column]
        df_exploded = df_exploded.select(
            "*", explode(col(old_column)).alias(new_column))

    if drop:
        return df_exploded.drop(*columns.keys())
    return df_exploded
