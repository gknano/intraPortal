from ldap3 import Server, Connection, SIMPLE, SYNC, ASYNC, SUBTREE, ALL
from collections import Counter
import pymongo
import json
import operator

#Подключение к контроллеру домена
#***********************************************************************************************************************
AD_SERVER = ''
AD_USER = ''
AD_PASSWORD = ''
AD_SEARCH_TREE = 'OU=, dc=, dc=, dc='

server = Server(AD_SERVER)
connAD = Connection(server, user=AD_USER, password=AD_PASSWORD)
connAD.bind()
connAD.search(AD_SEARCH_TREE,'(&(objectCategory=Person)(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(givenName=*)(sn=*))',
    SUBTREE,
    attributes = ['cn','proxyAddresses','department','sAMAccountName', 'displayName', 'telephoneNumber', 'ipPhone', 'streetAddress',
    'title','manager','objectGUID','company','lastLogon', 'mobile', 'mail']
     )
#***********************************************************************************************************************

#Для nosql решения
sortLogin = []
allUsersAd = {}
for login in connAD.entries:
    sortLogin.append(str(login.sAMAccountName))
sortLogin.sort()
for loginAd in sortLogin:
    for attrib in connAD.entries:
        if (str(attrib.sAMAccountName) == loginAd):
            allUsersAd[str(attrib.sAMAccountName)] = { '_id': str(attrib.sAMAccountName),
                                                        'idInfo': {
                                                            'displayName': str(attrib.displayName),
                                                            'telephoneNumber': str(attrib.telephoneNumber),
                                                            'mobile': str(attrib.mobile),
                                                            'email': str(attrib.mail)
                                                        }
            }
#*****************************************************************************************

#Выгрузка в формате noSql
#**********************************************************************************************
connDB = pymongo.MongoClient("mongodb:///")  # соединяемся с бд на localhost
db = connDB[""]  # выбираем базу
for i in allUsersAd:
    db.nosqlAd.insert_one(allUsersAd[i])
#***********************************************************************************************



# #Для sql решения
# def exportAdSql():
#     for login in sortLogin:
#         for attrib in connAD.entries:
#             if (str(attrib.sAMAccountName) == str(login)):
#                 allUsersAd[login] = {
#                     'displayName': str(attrib.displayName),
#                     'telephoneNumber': str(attrib.telephoneNumber),
#                     'mobile': str(attrib.mobile)
#              }
#     return allUsersAd
# #*****************************************************************************************

# Выгрузка в формате sql
#**********************************************************************************************
# connDB = pymongo.MongoClient("mongodb:///")  # соединяемся с бд
# db = connDB[""]  # выбираем базу
#
# for i in m:
#     db.sqlAd.insert_one(m[i])
#**********************************************************************************************


