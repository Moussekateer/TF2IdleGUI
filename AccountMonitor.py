import Config, socket, re, time, subprocess, os, getpass
from PyQt4 import QtCore, QtGui
from sourcelib import SourceQuery
import steamodd as steam
import jaraco.windows.filesystem as fs

import Sandboxie

account_log_file = r'status_output.txt'

class AccountManager():
	def __init__(self, window):
		self.settings = Config.settings
		self.window = window
		self.createdSandboxes = []
		self.sandboxieINIIsModified = False
		self.AccountHealthMonitorThread = AccountHealthMonitorThread(self)
		self.SandboxieManager = Sandboxie.SandboxieManager()

	def startAccounts(self, action, accounts):
		easy_sandbox_mode = self.settings.get_option('Settings', 'easy_sandbox_mode')
		self.commands = []
		self.AccountHealthMonitorThread.start()

		# Error dialogs if no accounts selected
		if len(accounts) == 0:
			if action == 'idle':
				QtGui.QMessageBox.information(self.window, 'No accounts selected', 'Please select at least one account to idle')
			elif action == 'idle_unsandboxed':
				QtGui.QMessageBox.information(self.window, 'No account selected', 'Please select an account to idle')
			elif action == 'start_steam':
				QtGui.QMessageBox.information(self.window, 'No accounts selected', 'Please select at least one account to start Steam with')
			elif action == 'start_TF2':
				QtGui.QMessageBox.information(self.window, 'No accounts selected', 'Please select at least one account to start TF2 with')

		# Error dialog if > 1 accounts selected and trying to run them all unsandboxed
		elif action == 'idle_unsandboxed' and len(accounts) > 1:
			QtGui.QMessageBox.information(self.window, 'Too many accounts selected', 'Please select one account to idle')
		# Error dialog if easy sandbox mode is on and program isn't run with elevated privileges
		elif easy_sandbox_mode == 'yes' and action != 'idle_unsandboxed' and not self.window.runAsAdmin():
			QtGui.QMessageBox.information(self.window, 'Easy sandbox mode requires admin', 'TF2Idle requires admin privileges to create/modify sandboxes. Please run the program as admin.')
		else:
			steamlocation = self.settings.get_option('Settings', 'steam_location')
			secondary_steamapps_location = self.settings.get_option('Settings', 'secondary_steamapps_location')
			sandboxielocation = self.settings.get_option('Settings', 'sandboxie_location')

			for account in accounts:
				username = self.settings.get_option('Account-' + account, 'steam_username')
				password = self.settings.get_option('Account-' + account, 'steam_password')
				sandboxname = self.settings.get_option('Account-' + account, 'sandbox_name')
				startmonitoring = False
				if self.settings.get_option('Account-' + account, 'sandbox_install') == '' and easy_sandbox_mode == 'yes':
					sandbox_install = steamlocation
				else:
					sandbox_install = self.settings.get_option('Account-' + account, 'sandbox_install')
				# Check if account has launch parameters that override main parameters
				if self.settings.has_option('Account-' + account, 'launch_options') and self.settings.get_option('Account-' + account, 'launch_options') != '':
					steamlaunchcommand = self.settings.get_option('Account-' + account, 'launch_options')
				else:
					steamlaunchcommand = self.settings.get_option('Settings', 'launch_options')

				if not self.sandboxieINIIsModified and easy_sandbox_mode == 'yes':
					Sandboxie.backupSandboxieINI()
					self.sandboxieINIIsModified = True

				if action == 'idle_unsandboxed':
					steamlaunchcommand += ' +con_logfile %s' % account_log_file
					command = r'"%s/Steam.exe" -login %s %s -applaunch 440 %s' % (steamlocation, username, password, steamlaunchcommand)
					startmonitoring = True

				else:
					if action == 'idle':
						steamlaunchcommand += ' +con_logfile %s' account_log_file
						command = r'"%s/Steam.exe" -login %s %s -applaunch 440 %s' % (sandbox_install, username, password, steamlaunchcommand)
						startmonitoring = True
					elif action == 'start_steam':
						command = r'"%s/Steam.exe" -login %s %s' % (sandbox_install, username, password)
					elif action == 'start_TF2':
						command = r'"%s/Steam.exe" -login %s %s -applaunch 440' % (sandbox_install, username, password)

					if easy_sandbox_mode == 'yes' and self.settings.get_option('Account-' + account, 'sandbox_install') == '':
						self.SandboxieManager.addSandbox('TF2Idle' + username)
						self.createdSandboxes.append(username)
						command = r'"%s/Start.exe" /box:%s %s' % (sandboxielocation, 'TF2Idle' + username, command)
					else:
						command = r'"%s/Start.exe" /box:%s %s' % (sandboxielocation, sandboxname, command)

				self.commands.append([command, username, startmonitoring, action])
			self.commandthread = CommandThread(self.commands, self.AccountHealthMonitorThread)
			self.commandthread.start()

	def returnCreatedSandboxes(self):
		return self.createdSandboxes

	def removeCreatedSandbox(self, account):
		self.createdSandboxes.remove(account)

	def restoreSandboxieINI(self):
		if self.sandboxieINIIsModified:
			Sandboxie.restoreSandboxieINI()

	"""
	def returnServerPort(self, launcharguments):
		portnumberRE = re.compile(r'\+hostport\s(\d+)')
		res = portnumberRE.search(launcharguments)
		if res:
			portnumber = int(res.group(1))
			self.usedPorts.append(portnumber)
			return True, portnumber
		else:
			portnumber = 27015
			while True:
				if portnumber in self.usedPorts:
					portnumber += 1
					continue
				else:
					# Check if port is in use by another client started outside of TF2Idle
					if self.returnServerPlayers(portnumber) is None:
						self.usedPorts.append(portnumber)
						return False, portnumber
					else:
						self.usedPorts.append(portnumber)
						portnumber += 1
						continue

	def returnServerPlayers(self, port):
		address = socket.gethostbyname(socket.gethostname())
		try:
			players = []
			server = SourceQuery.SourceQuery(address, port, 3.0)
			for player in server.player():
				players.append(player['name'])
			return players
		except:
			# Server ded
			return None
	"""

	def reconnectPlayer(self, username, action):
		# Kill
		sandboxie_location = self.settings.get_option('Settings', 'sandboxie_location')
		if self.settings.get_option('Settings', 'easy_sandbox_mode') == 'yes' and self.settings.get_option('Account-' + username, 'sandbox_install') == '':
			sandbox = 'TF2Idle' + username
		else:
			sandbox = self.settings.get_option('Account-' + username, 'sandbox_name')
		command = r'"%s/Start.exe" /box:%s /terminate' % (sandboxie_location, sandbox)
		subprocess.call(command)
		# restart
		self.startAccounts(action, username)

class CommandThread(QtCore.QThread):
	def __init__(self, commands, healthmanager, parent=None):
		QtCore.QThread.__init__(self, parent)
		self.settings = Config.settings
		self.healthmanager = healthmanager
		self.commands = commands
		self.delay = int(self.settings.get_option('Settings', 'launch_delay_time'))

	def run(self):
		self.runCommands()

	def checkStatus(self, account):
		error_messages = ['Steam Connection Lost',
						  'Bad challenge',
						  'Failed to load Steam Service',
						  'STEAM validation rejected'
						  ]

		sandboxpath = os.path.splitdrive(self.settings.get_option('Settings', 'sandboxie_location'))[0]
		currentuser = getpass.getuser()
		sandboxname = self.settings.get_option('Account-' + account, 'sandbox_name')
		sandboxinstall = self.settings.get_option('Account-' + account, 'sandbox_install')
		steam_username = self.settings.get_option('Account-' + account, 'steam_username')
		logfilepath = os.path.join(sandboxpath, os.sep,
								   'Sandbox',
								   currentuser,
								   sandboxname,
								   'drive',
								   fs.get_final_path(sandboxinstall)[4:].replace(':',''),
								   'steamapps',
								   steam_username,
								   'team fortress 2/tf',
								   account_log_file
								   )

	def runCommands(self):
		steam.set_api_key(self.settings.get_option('Settings', 'API_key'))
		for com in self.commands:
			command = com[0]
			username = com[1]
			monitor = com[2]
			action = com[3]
			subprocess.call(command)
			self.checkStatus(username)
			if monitor:
				steampersona = steam.user.profile(self.settings.get_option('Account-' + username, 'steam_vanityid')).get_persona()
				self.healthmanager.addAccount(username, steampersona, action)
			if self.commands.index(com)+1 != len(self.commands):
				time.sleep(self.delay)

class AccountHealthMonitorThread(QtCore.QThread):
	def __init__(self, manager, parent=None):
		QtCore.QThread.__init__(self, parent)
		self.settings = Config.settings
		self.manager = manager
		self.accounts = []
		self.alive = True

	def addAccount(self, account, steampersona, action):
		entry = {'account': account, 'steampersona': steampersona, 'action': action}
		self.accounts.append(entry)

	def removeAccount(self, account):
		self.accounts.remove(account)

	def kill(self):
		self.alive = False

	def checkStatus(self, account):
		sandboxpath = os.path.splitdrive(self.settings.get_option('Settings', 'sandboxie_location'))[0]
		currentuser = getpass.getuser()
		sandboxname = self.settings.get_option('Account-' + account, 'sandbox_name')
		sandboxinstall = self.settings.get_option('Account-' + account, 'sandbox_install')
		steam_username = self.settings.get_option('Account-' + account, 'steam_username')
		logfilepath = sandboxpath + os.sep + 'Sandbox' + os.sep + currentuser + os.sep + sandboxname + os.sep + 'drive' + os.sep + fs.get_final_path(sandboxinstall)[4:] + os.sep + 'steamapps' + os.sep + steam_username + os.sep + 'team fortress 2/tf/status.txt'
		print logfilepath

	def run(self):
		while self.alive:
			for account in self.accounts:
				pass
				#do stuff
				#if errors
					#alert manager to reconnect
					#self.accounts.remove(account)
				#else
					#pass
			time.sleep(15*60)

class SmartIdleThread(QtCore.QThread):
	def __init__(self, maxaccounts, parent=None):
		QtCore.QThread.__init__(self, parent)
		self.settings = Config.settings
		self.activeaccounts = []
		self.queuedaccounts = []
		self.maxaccounts = maxaccounts