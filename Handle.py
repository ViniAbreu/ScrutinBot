import datetime as dt
from base64 import b64decode,b64encode
from binascii import hexlify,unhexlify
from urllib.parse import quote_from_bytes,unquote_to_bytes
from subprocess import check_output
from zipfile import ZipFile

import PyMyAdmin
import Scanners
import Crawler
import Generators


def isAdmin(idd):
	db = PyMyAdmin.Database('','','')
	for idu in db.get_admin():
		if idu == idd:
			return True
	return False

class user_commands:
	def __init__(self,bot,msg):
		self.bot = bot
		self.msg = msg
		#self datas chat
		self.chat_id = str(msg['chat']['id'])
		self.chat_type = msg['chat']['type']
		try:
			self.chat_title = str(msg['chat']['title'])
		except:
			self.chat_title = ''
		#self datas messages
		self.msgt = msg.get('text')
		self.msg_id = msg['message_id']
		self.msg_s = msg['text'].split(' ')
		#self datas users
		self.uid = msg['from']['id']
		self.nick = msg['from']['username']
		self.group_id = str(-1001166468779)
		#instancias 
		self.scan = Scanners.Scans(msg)
		self.log = PyMyAdmin.LogManager(self.msg, self.uid, self.nick, self.chat_id, self.chat_title)
		self.crawler = Crawler.Crawlers(self.msg)
		self.generators = Generators.generators(self.msg)
		self.data = PyMyAdmin.Database('','','').get_statistic()

	def welcome(self):
		if self.chat_type == 'private':
			self.bot.sendMessage(self.chat_id,"*Hi, I'm Scrutin was developed in Python by @SrBiggs e @cyr4x !*\n\n*Type * `/help` *to see my list of commands* \n\n *Thanks for signing up :)*",parse_mode="Markdown",reply_to_message_id=self.msg_id)
			self.log.users()
		else:
			self.bot.sendMessage(self.chat_id,"Please start a private conversation!",reply_to_message_id=self.msg_id)

	def help_users(self):
		text_help = '''
			   *Scrutin - Commands *

*/sql* - `Start the SQL Injection scanner to look for crashes`\n
*/xss* - `Start the XSS scanner to check for glitches`\n
*/lfi* - `Start the LFI scanner to check for glitches`\n
*/bing* - `Crawlea links no bing from the provided dork`\n
*/dork* - `Automatically generate dorks from supplied keywords`\n
*/encrypt* - `Encrypt user-supplied strings`\n
*/decrypt* - `Describe string strings by user`\n

*If you still have difficulty executing type:* `/help /name_cmd` 
			   '''

		help_plus = {
			'/sql': "*The command* `/sql` *command requires the site to be scanned.*\n\n*Example:* `/sql http://testphp.vulnweb.com/listproducts.php?cat=1`\n\n*Note:* `Note that the link must contain parameter passing to inject the payloads.`",
			'/xss': "*The command* `/xss` *needs to be passed the site to be scanned.*\n\n*Example:* `/xss http://testphp.vulnweb.com/listproducts.php?cat=1`\n\n*Note:* `Note that the link must contain parameter passing to inject the payloads.`",
			'/lfi': "*The command* `/lfi` *needs to be passed the site to be scanned.*\n\n*Example:* `/lfi http://testphp.vulnweb.com/listproducts.php?cat=1`\n\n*Note:* `Note that the link must contain parameter passing to inject the payloads.`",
			'/bing': "*The command* `/bing` *command requires that a dork be passed to return crawled links in the search engine.*\n\n*Example:* `/bing index.php? file=`",
			'/dork': "*The command* `/dork` *needs to be passed keywords to generate dorks.*\n\n*Example:* `/ dork index file =`",
			'/encrypt': "*The command* `/encrypt` *command needs to be passed an encryption algorithm and the string to be encrypted.*\n\n*Example:* `/encrypt b64 ScrutinBot` \n\n*This command would return the string \"ScrutinBot\" encrypted in Base64.*",
			'/decrypt': "*The command* `/decrypt` *command requires that an encryption algorithm and the encrypted encryption be passed.*\n\n*Example:* `/decrypt b64 U2NydXRpbkJvdA==` \n\n *This command would return the cipher \"U2NydXRpbkJvdA==\" decrypted in Base64.*"
		}

		if not len(self.msg_s) > 1:
			self.bot.sendMessage(self.chat_id,text_help,parse_mode="Markdown",reply_to_message_id=self.msg_id)
		else:
			try:
				self.bot.sendMessage(self.chat_id,help_plus[self.msg_s[1]],parse_mode="Markdown",reply_to_message_id=self.msg_id)
			except:
				self.bot.sendMessage(self.chat_id,"*Scrutin - Help Users*\n*Syntax command* : `/help /name_cmd`\n*Example:* `/help /bing`",parse_mode="Markdown",reply_to_message_id=self.msg_id)
			
	def sqli(self):
		if len(self.msg_s) > 1:
			self.bot.sendMessage(self.chat_id,self.scan.sql_injection(),
								parse_mode="HTML",
								reply_to_message_id=self.msg_id,
								disable_web_page_preview=True)
			self.log.scanners()
		else:
			self.bot.sendMessage(self.chat_id,'*Scrutin - Scanners*\n*Syntax command* : `/sql [target_url]`\n*Example:* `/sql http://testphp.vulnweb.com/listproducts.php?cat=1`',parse_mode='Markdown',reply_to_message_id=self.msg_id)
		
	def xss(self):
		if len(self.msg_s) > 1:
			self.bot.sendMessage(self.chat_id,self.scan.XSS(),
								parse_mode='Markdown',
								reply_to_message_id=self.msg_id,
								disable_web_page_preview=True)
			self.log.scanners()
		else:
			self.bot.sendMessage(self.chat_id,'*Scrutin - Scanners*\n*Syntax command* : `/xss [target_url]`\n*Example:* `/xss http://testphp.vulnweb.com/listproducts.php?cat=1`',parse_mode='Markdown',reply_to_message_id=self.msg_id)

	def lfi(self):
		if len(self.msg_s) > 1:
			self.bot.sendMessage(self.chat_id,self.scan.LFI(),
								parse_mode='HTML',
								reply_to_message_id=self.msg_id,
								disable_web_page_preview=True)
			self.log.scanners()
		else:
			self.bot.sendMessage(self.chat_id,'*Scrutin - Scanners*\n\n*Syntax command* : `/lfi [target_url]`\n*Example:* `/lfi http://testphp.vulnweb.com/index?file=contact.php`',parse_mode='Markdown',reply_to_message_id=self.msg_id)

	def bing(self):
		if len(self.msg_s) == 2:
			self.bot.sendMessage(self.chat_id,self.crawler.bing(),
								parse_mode='HTML',
								reply_to_message_id=self.msg_id,
								disable_web_page_preview=True)
			self.log.crawler()
		else:
			self.bot.sendMessage(self.chat_id,'*Scrutin - Crawler*\n\n*Syntax command* : `/bing [dork]`\n*Example:* `/bing index.php?id=`',parse_mode='Markdown',reply_to_message_id=self.msg_id)
	
	def gen_dork(self):
		if len(self.msg_s) == 3:
			self.bot.sendMessage(self.chat_id,self.generators.dork_Generator(),
								parse_mode='Markdown',
								reply_to_message_id=self.msg_id)
			self.log.generators()
		else:
			self.bot.sendMessage(self.chat_id,'*Scrutin - Dork generator*\n\n*Syntax command* : `/dork [nameFile] [paramter]`\n*Example:* `/dork index id=`',parse_mode='Markdown',reply_to_message_id=self.msg_id)
	
	def _Encrypt(self):
		encode = {
			'b64': b64encode,
			'hex': hexlify,
			'url': quote_from_bytes
		}
		
		if len(self.msg_s) > 2:
			plain_text = self.msgt.replace('/encrypt {} '.format(self.msg_s[1]),'').encode()
			result = encode[self.msg_s[1]](plain_text)
			
			self.bot.sendMessage(self.chat_id,"*Scrutin - Cryptography*\n\n*[+] Plain-Text:* `{}`\n\n*[+] Algorithm:* `{}_encode`\n\n*[+] ChiperText:* `{}`".format(plain_text,self.msg_s[1],result),
											 parse_mode="Markdown",
											 reply_to_message_id=self.msg_id)
			self.log.encrypt()
		else:
			self.bot.sendMessage(self.chat_id,'*Scrutin - Cryptography*\n\n*Type Algorithms:* `url,b64,hex`\n*Syntax command*: `/encrypt [algorithm] [plain_text]` *Example:* `/encrypt b64 ScrutinBot`',parse_mode="Markdown",reply_to_message_id=self.msg_id)
	
	def _Decrypt(self):
		decode = {
			'b64': b64decode,
			'hex': unhexlify,
			'url': unquote_to_bytes
		}
	
		if len(self.msg_s) > 2:
			chiper_text = self.msgt.replace('/decrypt {} '.format(self.msg_s[1]),'').encode()
			result = decode[self.msg_s[1]](chiper_text)
			
			self.bot.sendMessage(self.chat_id,"*Scrutin - Cryptography*\n\n*[+] ChiperText:* `{}`\n\n*[+] Algorithm:* `{}_decode`\n\n*[+] Plain-Text:* `{}`".format(chiper_text,self.msg_s[1],result),
								parse_mode="Markdown",
								reply_to_message_id=self.msg_id)
			self.log.decrypt()
		else:
			self.bot.sendMessage(self.chat_id,'*Scrutin - Cryptography*\n\n*Type Algorithms:* `url,b64,hex`\n*Syntax command*: `/decrypt [algorithm] [plain_text]`\n*Example:* `/decrypt b64 U2NydXRpbkJvdA==`',parse_mode="Markdown",reply_to_message_id=self.msg_id)
	
	def manual_bkp(self):
		if isAdmin(self.uid):
			data = check_output('ls')
			files = [i for i in data.decode().split('\n') if not (i == '')]
			filename = 'Backup-Scrutin.zip'
			mode = 'a'
			if filename in files:
				mode = 'w'
			with ZipFile(filename, mode) as zip_arquive:
				for file in files:
					zip_arquive.write(file)
			self.bot.sendMessage(self.chat_id,"*[+] Backup Done Successfully*\n*[+] Sending the backup file*",parse_mode="Markdown",reply_to_message_id=self.msg_id)
			try:
				self.bot.sendDocument(self.chat_id,open('Backup-Scrutin.zip','rb'),reply_to_message_id=self.msg_id)
			except:
				self.bot.sendMessage(self.chat_id,"*[!] Backup file not found.*",parse_mode="Markdown",reply_to_message_id=self.msg_id)
		else:
			self.bot.sendMessage(self.chat_id,"*Only my creators can use this command*",parse_mode="Markdown",reply_to_message_id=self.msg_id)

	def sendFile(self):
		if isAdmin(self.uid):
			try:
				self.bot.sendDocument(self.chat_id,open(self.msg_s[1],'rb'),reply_to_message_id=self.msg_id)
			except:
				self.bot.sendMessage(self.chat_id,"*[!] File not found.*",parse_mode="Markdown",reply_to_message_id=self.msg_id)
		else:
			self.bot.sendMessage(self.chat_id,"*Only my creators can use this command*",parse_mode="Markdown",reply_to_message_id=self.msg_id)
	def changelog_for_users(self):
		if isAdmin(self.uid):
			if len(self.msg_s) > 2:
				_users = PyMyAdmin.Database('','','').return_users()
				for user in _users:
					try:
						self.bot.sendMessage(user,self.msg.get('text').replace('/ch ',''),parse_mode="Markdown")
					except Exception as erro:
						self.bot.sendMessage(self.chat_id,'ID: '+user+'\n\nERRO: '+str(erro),reply_to_message_id=self.msg_id)
			else:
				self.bot.sendMessage(self.chat_id,'*Notify me of updates to changelog*',parse_mode="Markdown",reply_to_message_id=self.msg_id)
		else:
			self.bot.sendMessage(self.chat_id,"*Only my creators can use this command*",parse_mode="Markdown",reply_to_message_id=self.msg_id)
	
	def statistcs(self):
		if isAdmin(self.uid):
			now = dt.datetime.now().strftime('[%d-%m-%Y]')
			def used_cmd(self):
				numbers_ = {'/sql':self.data.get('sqli'),'/xss':self.data.get('xss'),'/lfi':self.data.get('lfi')}
				maior = numbers_['/lfi']
				for key,value in numbers_.items():
					if value > maior:
						maior = key
					return maior


			text = '''#statistics `{0}` :

📉 *Sites already scanned* : `{1}`
📉 *Scans made* : `{2}`
      📉 *SQLi* : `{3}`
      📉 *XSS* : `{4}`
      📉 *LFI* : `{5}`
📉 *Dorks Geradas* : `{6}`
📉 *Most Used Command* : `{7}`
📉 *Links crawleados* : `{8}`\n
👤 *Registered users* : `{9}`
👤 *Registered Users Today* : `{10}`
👤 *Registered Users this Month* : `{11}`
👥 *Total Groups* : `{12}`'''.format(str(now),
												self.data.get('targets'),
										    	self.data.get('all_scan'),
												self.data.get('sqli'),
												self.data.get('xss'),
												self.data.get('lfi'),
												self.data.get('dorks'),
												used_cmd(self),
												self.data.get('crawler'),
												self.data.get('users'),
												self.data.get('U_today'),
												self.data.get('U_month'),
												self.data.get('all_Groups'))
			try:
				self.bot.sendMessage(self.chat_id,text,parse_mode="Markdown",reply_to_message_id=self.msg_id)
			except Exception as erro:
				self.bot.sendMessage(self.chat_id,str(erro))
		
		else:
			self.bot.sendMessage(self.chat_id,"*Only my creators can use this command*",parse_mode="Markdown",reply_to_message_id=self.msg_id)
