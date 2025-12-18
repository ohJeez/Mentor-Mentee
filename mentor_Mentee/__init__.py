import pymysql
pymysql.version_info = (2, 2, 1, "final", 0)  # fake version to satisfy Django
pymysql.install_as_MySQLdb()