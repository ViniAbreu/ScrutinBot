from datetime import datetime
import sqlite3

class Database:
    def __init__(self,group_id,group_title,userid):
        self.conn = sqlite3.connect('Scrutin.db')
        self.cursor = self.conn.cursor()
        self.group_id = group_id
        self.group_title = group_title
        self.userid = userid
    
    def add_groups(self):
        try:
            self.cursor.execute("""INSERT INTO Groups VALUES (?,?,?);""",(self.group_title,self.group_id,self.userid))
            self.conn.commit()
        except Exception as e:
            print(e)

    def remove_groups(self):
        try:
            self.cursor.execute("""DELETE FROM Groups where group_id={}""".format(self.group_id))
            self.conn.commit()
        except Exception as e:
            print(e)

    # def create_table(self): 
        # self.cursor.execute("""create table Scanners (type_scan varchar(5), data_exec timestamp, user varchar(255) DEFAULT 'anonymous',id int,site text);""")
        # self.cursor.execute("""create table Crawler (crawler_name varchar(5), data_exec timestamp, user varchar(255) DEFAULT 'anonymous', id int, dork text);""")
        # self.cursor.execute("""create table Users (data timestamp, user varchar(255), id int, primary key(id));""")
        # self.cursor.execute("""create table Groups (name_group varchar(255),group_id int,who_add int,primary key(group_id));""")
        # self.cursor.execute("""create table Generators (gen varchar(5), data_exec timestamp, user varchar(255) DEFAULT 'anonymous', id int, generated text);""")
        # self.cursor.execute("""create table Cryptography (algorithm varchar(10), data_exec timestamp, user varchar(255) DEFAULT 'anonymous', id int, strings text);""")
        # self.conn.commit()                    
        # self.cursor.close()
        # pass

    def get_admin(self):
        adms = []
        self.cursor.execute("""SELECT * FROM Admin;""")
        for admin in self.cursor.fetchall():
            adms.append(admin[2])
        return adms

    def return_users(self):
        _users = []
        sql_querys = {'users':'SELECT id from Users;','groups':'SELECT group_id from Groups;'}
        for x in self.cursor.execute(sql_querys['users']).fetchall():
            _users.append(''.join(str(x[0])))
        for x in self.cursor.execute(sql_querys['groups']).fetchall():
            _users.append(''.join(str(x[0])))
        return _users

    def update(self):
        try:
            with open("groups.txt","r",encoding='utf-8') as file:
                for line in file.readlines():
                    z = line.strip()
                    print(z)
                    
                    x = z.split(',')[0]
                    s = z.split(',')[1]
                    ss = z.split(',')[2]
                    
                    try:
                        self.cursor.execute("""insert into Groups values (?,?,?);""",(x,s,ss))
                        self.conn.commit()
                    except Exception as e:
                        print(e)
        except Exception as e:
            print(e)

    def get_statistic(self):
        now = datetime.now().strftime('%Y-%m-%d')
        month = datetime.now().strftime('%Y-%m')

        sql_querys = {
            'scanners': "SELECT count(type_scan) from Scanners;",
            'sqli': "SELECT count(type_scan) from Scanners where type_scan='SQL';",
            'xss': "SELECT count(type_scan) from Scanners where type_scan='XSS';",
            'lfi': "SELECT count(type_scan) from Scanners where type_scan='LFI';",
            'targets': "SELECT count(DISTINCT site) from Scanners;",
            'users': "SELECT count(id) from Users;",
            'dorks': "SELECT count(gen) from Generators;",
            'crawler': "SELECT count(crawler_name) from Crawler;",
            'U_today': "SELECT count(data) from Users WHERE DATA LIKE \"%"+str(now)+"%\";",
            'U_month': "SELECT count(data) from Users WHERE DATA LIKE \"%"+str(month)+"%\";",
            'all_Groups': "SELECT count(group_id) from Groups;",
        }
        statistic ={
            "all_scan":''.join(str(x[0]) for x in self.cursor.execute(sql_querys['scanners']).fetchall()),
            "sqli":''.join(str(x[0]) for x in self.cursor.execute(sql_querys['sqli']).fetchall()),
            "xss":''.join(str(x[0]) for x in self.cursor.execute(sql_querys['xss']).fetchall()),
            "lfi":''.join(str(x[0]) for x in self.cursor.execute(sql_querys['lfi']).fetchall()),
            "targets":''.join(str(x[0]) for x in self.cursor.execute(sql_querys['targets']).fetchall()),
            "users":''.join(str(x[0]) for x in self.cursor.execute(sql_querys['users']).fetchall()),
            "dorks":''.join(str(int(x[0])*42) for x in self.cursor.execute(sql_querys['dorks']).fetchall()),
            "crawler":''.join(str(int(x[0])*10) for x in self.cursor.execute(sql_querys['crawler']).fetchall()),
            "U_today":''.join(str(x[0]) for x in self.cursor.execute(sql_querys['U_today']).fetchall()),
            "U_month":''.join(str(x[0]) for x in self.cursor.execute(sql_querys['U_month']).fetchall()),
            "all_Groups":''.join(str(x[0]) for x in self.cursor.execute(sql_querys['all_Groups']).fetchall()),
        }

        return statistic

class LogManager:

    def __init__(self,text,idd,nick,gid,gtt):
        self.text = text.get('text')
        self.textS = self.text.split(' ')
        self.id = idd
        self.nick = nick
        self.idG = gid
        self.ttG = gtt
        self.cmd = self.text.split(' ')[0].replace('/','')
        self.now = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.conn = sqlite3.connect('Scrutin.db')
        self.cursor = self.conn.cursor()

    def scanners(self):
        site = self.text.split(' ')[1]
        try:
            self.cursor.execute("""INSERT INTO Scanners VALUES (?,?,?,?,?);""",(self.cmd.upper(),self.now,self.nick,self.id,site))
            self.conn.commit()
            self.cursor.close()
        except Exception as e:
            print(e)

    def crawler(self):
        search = self.text.replace("/bing ", "")
        try:
            self.cursor.execute("""INSERT INTO Crawler VALUES (?,?,?,?,?);""",(self.cmd.upper(),self.now,self.nick,self.id,search))
            self.conn.commit()
        except Exception as e:
            print(e)
    
    def generators(self):
        generated = self.text.replace(self.cmd,'')
        try:
            self.cursor.execute("""INSERT INTO Generators VALUES (?,?,?,?,?);""", (self.cmd.upper(),self.now,self.nick,self.id,generated.replace('/ ','')))
            self.conn.commit()
        except Exception as e:
            print(e)
    
    def encrypt(self):
        algorithm = self.textS[1]+'_encode'
        string = self.text.replace('/encrypt {} '.format(self.textS[1]),'')
        try:
            self.cursor.execute("""INSERT INTO Cryptography VALUES (?,?,?,?,?);""",(algorithm,self.now,self.nick,self.id,string))
            self.conn.commit()
        except Exception as e:
            print(e)

    def decrypt(self):
        algorithm = self.textS[1]+'_decode'
        string = self.text.replace('/decrypt {} '.format(self.textS[1]),'')
        try:
            self.cursor.execute("""INSERT INTO Cryptography VALUES (?,?,?,?,?);""",(algorithm,self.now,self.nick,self.id,string))
            self.conn.commit()
        except Exception as e:
            print(e)

    def users(self):
        try:
            self.cursor.execute("""INSERT INTO Users VALUES (?,?,?);""", (self.now,self.nick,self.id))
            self.conn.commit()
        except Exception as e:
            print(e)

    

#Database().update()