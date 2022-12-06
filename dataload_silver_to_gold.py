# Databricks notebook source
from pyspark.sql.functions import *
from delta.tables import *
import random
from random import randint

# COMMAND ----------

spark.conf.set(
"fs.azure.account.key.hack20220612.dfs.core.windows.net",
"6yPpQUFbaVR8wCeCd+tOq/IpHuk8UhAUIexQNTpNg3aQWO7Yhl9/80KcKyi58NQBiSp2/7anSmLF+AStzFHKEw=="
)

# COMMAND ----------

# DBTITLE 1,Read the Silver Layer
df_Silver = spark.read.format("parquet").load("abfss://silver@hack20220612.dfs.core.windows.net/employee_data")

# COMMAND ----------

# DBTITLE 1,Derive PerSalaryEMI
df_Silver = df_Silver.withColumn('PerSalaryEMI',rand(9)*5)

# COMMAND ----------

df_Silver = df_Silver.withColumn('PerSalaryEMI',(col('PerSalaryEMI')).astype('int'))

# COMMAND ----------

# DBTITLE 1,Derive SalaryEMI
df_Silver = df_Silver.withColumn('SalaryEMI',((col('PerSalaryEMI')/100)*col('Salary')))

# COMMAND ----------

df_Silver = df_Silver.withColumn('Tenure',ceil(col('purchase_value')/col('SalaryEMI')))

# COMMAND ----------

# DBTITLE 1,Writing the data to Gold layer
df_Silver.write.format("parquet").mode("overwrite").save("abfss://gold@hack20220612.dfs.core.windows.net/gold_employee_data")
