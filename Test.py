import pyodbc

msa_drivers = [x for x in pyodbc.drivers() if "ACCESS" in x.upper()]
print(f"MS-Access Drivers : {msa_drivers}")


# In[542]:


import pyodbc

[x for x in pyodbc.drivers() if x.startswith("Microsoft Access Driver")]


# ### Установим диапазон даты

# In[543]:


import pandas as pd

st_date = pd.to_datetime("2022-01-01 08:00:00")
en_date = pd.Timestamp.now()
en_date


# ### **Проверка подключения к базе данных в MS Access**
#
# Хорошо, у нас есть база данных MS Access, и теперь мы хотим проверить соединение с базой данных,
# это код для проверки соединения с базой данных MS Access в Python.

# In[544]:


import pyodbc

try:
    con_string = (
        r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
        r"DBQ=D:\SkyMarsUtilization\2022-02-09_UtilizationDB.mdb"
    )
    conn = pyodbc.connect(con_string)
    print("Connected To Database")


except pyodbc.Error as e:
    print("Error in Connection", e)

conn_str = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=E:\MONITORING\test_pandas.accdb;"
)
conn = pyodbc.connect(conn_str)  # autocommit=True


# #### Рабочая таблица MS Access
#
# Чтение данных из таблицы и запись их в DataFrame для дальнейшей обработки

# In[545]:


import pyodbc
import numpy as np
import pandas as pd

# from sqlalchemy import create_engine

conn_str = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    # r'DBQ=E:\MONITORING\test_pandas.accdb;'
    r"DBQ=D:\SkyMarsUtilization\2022-02-09_UtilizationDB.mdb"
)

conn = pyodbc.connect(conn_str, autocommit=True)  # autocommit=True
mycursor = conn.cursor()
SQL = "SELECT * FROM StatusLog"
dfins = pd.read_sql(SQL, conn, index_col=["Logno"])
# display(dfins.tail()) # вывод 5 последних строк нашей таблицы]
conn.rollback()
conn.close()


# In[546]:


fanuc_copy = dfins.copy()
fanuc_copy.sort_values(by="StDateTime", ascending=True, inplace=True, ignore_index=True)
fanuc_copy.tail(15)


# In[547]:


def delete_columns(df, col=[]):  # функция для удаления столбцов
    for i in col:
        if i not in df.columns:
            return None
    return df.drop(col, axis=1)


delete = ["IsContinuous", "ContinuousLogno", "TranSactionTime", "TranSactionMS"]
fanuc_copy = delete_columns(fanuc_copy, delete)
fanuc_copy.tail()


# In[548]:


from datetime import datetime, timedelta

fanuc_copy["Date"] = fanuc_copy["StDateTime"].apply(
    lambda x: x - timedelta(days=1) if 8 > pd.to_datetime(x).hour >= 0 else x
)
fanuc_copy["Date"] = pd.to_datetime(fanuc_copy["Date"], yearfirst=True).dt.date
fanuc_copy["Date"]


# In[549]:


work = fanuc_copy["CycleRecord"] == True
test = fanuc_copy[work].loc[:, ["MachineName", "ProgNo"]].copy()


class Machine:
    def __init__(self, name):
        self.name = name
        self.programm = ""

    def replace_prog(self, row):
        if row["MachineName"] == self.name:
            if row["ProgNo"] != "O9001" and row["ProgNo"] != "O0":
                self.programm = row["ProgNo"]
                return row
            else:
                if row["ProgNo"] != "O0":
                    row["ProgNo"] = self.programm
                    return row
                return row
        else:
            return row


n = Machine("VCENTR-102")
m = Machine("VTM9")
t = Machine("VCENTR-70")

# test_102 = test_102.apply(n.replace_prog, axis=1)
# test_VTM9 = test_VTM9.apply(m.replace_prog, axis=1)
# test_70 = test_70.apply(t.replace_prog, axis=1)

test = test.apply(n.replace_prog, axis=1)
test = test.apply(m.replace_prog, axis=1)
test = test.apply(t.replace_prog, axis=1)
fanuc_copy.loc[fanuc_copy["CycleRecord"] == True, "ProgNo"] = test


# In[550]:


fanuc_copy.shape  # РАЗМЕРНОСТЬ ТАБЛИЦЫ


# In[551]:


fanuc_copy.columns  # вывести информацию про все столбцы


# In[552]:


fanuc_copy.info()


# In[553]:


# сначала приведём столбцы к типу датавермя: pd.to_datetime
fanuc_copy["StDateTime"] = pd.to_datetime(fanuc_copy["StDateTime"])
fanuc_copy["EndDateTime"] = pd.to_datetime(fanuc_copy["EndDateTime"])
fanuc_copy["EndDateTime"].tail()


# In[554]:


# Затем создадим столбец с временем цикла в формате датавермя
fanuc_copy["Time_Cycle"] = fanuc_copy["EndDateTime"] - fanuc_copy["StDateTime"]


# In[555]:


# можно преобразовать время в секунды
fanuc_copy["Cycle_sec"] = fanuc_copy["Time_Cycle"].dt.total_seconds()
fanuc_copy["Cycle_sec"].tail(10)


# In[556]:


# преобразуем ячеку памяти для float до максимально низкой, для экономии места
fanuc_copy["StatusType"] = pd.to_numeric(fanuc_copy["StatusType"], downcast="float")
fanuc_copy["PartCount"] = pd.to_numeric(fanuc_copy["PartCount"], downcast="float")
fanuc_copy["ControlPartCount"] = pd.to_numeric(
    fanuc_copy["ControlPartCount"], downcast="float"
)
fanuc_copy["Cycle_sec"] = pd.to_numeric(fanuc_copy["Cycle_sec"], downcast="float")
fanuc_copy.info()


# In[557]:


def convert_to_second(sec):  # преобразовать секунды в формат времени
    # sec = sec % (24 * 3600)
    hour = sec // 3600
    sec %= 3600
    min = sec // 60
    sec %= 60
    return "%02d:%02d:%02d" % (hour, min, sec)
