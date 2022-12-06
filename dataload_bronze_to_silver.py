# Databricks notebook source
from pyspark.sql.functions import *
from delta.tables import *

# COMMAND ----------

spark.conf.set(
"fs.azure.account.key.hack20220612.dfs.core.windows.net",
"6yPpQUFbaVR8wCeCd+tOq/IpHuk8UhAUIexQNTpNg3aQWO7Yhl9/80KcKyi58NQBiSp2/7anSmLF+AStzFHKEw=="
)

# COMMAND ----------

# DBTITLE 1,Read the CSV file1
df_Emp_Dec = spark.read.format('csv').option("header","true").load("abfss://bronze@hack20220612.dfs.core.windows.net/employee_data_202212.csv")
df_Emp_Dec=df_Emp_Dec.drop(col("_c0"))

# COMMAND ----------

# DBTITLE 1,Read the CSV file2
df_Emp_Nov = spark.read.format('csv').option("header","true").load("abfss://bronze@hack20220612.dfs.core.windows.net/employee_data_202211.csv")
df_Emp_Nov=df_Emp_Nov.drop(col("_c0"))

# COMMAND ----------

# DBTITLE 1,Display the CSV file1
df_Emp_Dec.display()

# COMMAND ----------

# DBTITLE 1,Display the CSV file2
df_Emp_Nov.display()

# COMMAND ----------

# DBTITLE 1,Decimal to Integer Transformation
df_Emp_Dec = df_Emp_Nov.withColumn('salary',(col('salary')).astype('int'))

# COMMAND ----------

# DBTITLE 1,Union the File1 and File2
df_Emp = df_Emp_Dec.unionByName(df_Emp_Dec)

# COMMAND ----------

df_Emp.count()

# COMMAND ----------

# DBTITLE 1,Writing the data to Silver layer
df_Emp.write.format("parquet").mode("overwrite").save("abfss://silver@hack20220612.dfs.core.windows.net/employee_data")
