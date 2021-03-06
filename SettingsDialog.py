import Config, os
from PyQt4 import QtCore, QtGui

from Common import returnResourcePath
from Common import curry

backpackViewerDict = {'0': 'Backpack.tf', '1': 'OPTF2', '2': 'Steam', '3': 'TF2B', '4': 'TF2Items'}

class QTextEditWithPlaceholderText(QtGui.QTextEdit):
	textEdited = QtCore.pyqtSignal('QString') 
	def __init__(self, placeholderText, parent=None):
		QtGui.QTextEdit.__init__(self, parent)
		self.placeholderText = placeholderText
		self.placedText = False

	def focusOutEvent(self, e): 
		super(QTextEditWithPlaceholderText, self).focusOutEvent(e)
		if self.toPlainText() == '':
			self.setStyleSheet('color: rgb(149, 149, 149);')
			self.setText(self.placeholderText)
			self.placedText = True
		else:
			self.placedText = False
		self.textEdited.emit(self.toPlainText())

	def focusInEvent(self, e):
		super(QTextEditWithPlaceholderText, self).focusInEvent(e)
		self.setStyleSheet('')
		if self.placedText:
			self.setText('')
		self.textEdited.emit(self.toPlainText())

	def setPlaceholderText(self):
		self.setStyleSheet('color: rgb(149, 149, 149);')
		self.setText(self.placeholderText)
		self.placedText = True

	def containsPlacedText(self):
		return self.placedText

class SettingsDialog(QtGui.QDialog):
	def __init__(self, parent=None):
		QtGui.QDialog.__init__(self, parent)
		self.settings = Config.settings
		
		# Create dialog
		self.setWindowModality(QtCore.Qt.NonModal)
		self.setWindowTitle('TF2Idle Settings')
		self.setWindowIcon(QtGui.QIcon(returnResourcePath('images/settings.png')))

		self.vBoxLayout = QtGui.QGridLayout(self)

		# Add tab widget and tabs
		self.tabWidget = QtGui.QTabWidget(self)
		self.vBoxLayout.addWidget(self.tabWidget)

		self.generalTab = QtGui.QWidget()
		self.tf2idleTab = QtGui.QWidget()
		self.droplogTab = QtGui.QWidget()
		
		self.tabWidget.addTab(self.generalTab, 'TF2')
		self.tabWidget.addTab(self.tf2idleTab, 'TF2Idle')
		self.tabWidget.addTab(self.droplogTab, 'Drop Log')
		
		# Add layouts for tabs
		self.generalVBoxLayout = QtGui.QVBoxLayout(self.generalTab)
		self.tf2idleVBoxLayout = QtGui.QGridLayout(self.tf2idleTab)
		self.droplogVBoxLayout = QtGui.QGridLayout(self.droplogTab)
		
		# Set fonts/styles
		self.greyoutstyle = 'background-color: rgb(225, 225, 225);'

		titleStyle = "QGroupBox {font-weight: bold;}"

		italicfont = QtGui.QFont()
		italicfont.setItalic(True)

		# TF2 settings tab
		
		# Locations section
		self.locationsGroupBox = QtGui.QGroupBox(self.generalTab)
		self.locationsGroupBox.setStyleSheet(titleStyle)
		self.locationsGroupBox.setTitle('Locations')
		
		self.generalVBoxLayout.addWidget(self.locationsGroupBox)
		
		self.locationsGroupBoxLayout = QtGui.QGridLayout(self.locationsGroupBox)
		
		self.steamLocationLabel = QtGui.QLabel(self.locationsGroupBox)
		self.steamLocationLabel.setToolTip('The path to your Steam installation. This folder should contain Steam.exe')
		self.steamLocationLabel.setText('Steam installation location:')
		self.locationsGroupBoxLayout.addWidget(self.steamLocationLabel, 0, 0, 1, 1)
		
		self.steamLocationLineEdit = QtGui.QLineEdit()
		self.steamLocationLineEdit.setToolTip('The path to your Steam installation. This folder should contain Steam.exe')
		self.steamLocationLineEdit.setPlaceholderText('Steam folder path')
		self.locationsGroupBoxLayout.addWidget(self.steamLocationLineEdit, 0, 1, 1, 1)

		self.steamLocationButton = QtGui.QPushButton()
		self.steamLocationButton.setText('..')
		self.steamLocationButton.setMaximumSize(QtCore.QSize(30, 20))
		self.locationsGroupBoxLayout.addWidget(self.steamLocationButton, 0, 2, 1, 1)
		
		self.secondarySteamappsLocationLabel = QtGui.QLabel(self.locationsGroupBox)
		self.secondarySteamappsLocationLabel.setToolTip('The path to your backup copy of the steamapps folder. This folder should contain the common Folder. Optional, only if you wish to use sandboxes')
		self.secondarySteamappsLocationLabel.setText('Secondary Team Fortress 2 folder location:')
		self.locationsGroupBoxLayout.addWidget(self.secondarySteamappsLocationLabel, 1, 0, 1, 1)
		
		self.secondarySteamappsLocationLineEdit = QtGui.QLineEdit()
		self.secondarySteamappsLocationLineEdit.setToolTip('The path to your backup copy of the steamapps folder. This folder should contain the common Folder. Optional, only if you wish to use sandboxes')
		self.secondarySteamappsLocationLineEdit.setPlaceholderText('Team Fortress 2 folder path')
		self.locationsGroupBoxLayout.addWidget(self.secondarySteamappsLocationLineEdit, 1, 1, 1, 1)
		
		self.secondarySteamappsLocationButton = QtGui.QPushButton()
		self.secondarySteamappsLocationButton.setText('..')
		self.secondarySteamappsLocationButton.setMaximumSize(QtCore.QSize(30, 20))
		self.locationsGroupBoxLayout.addWidget(self.secondarySteamappsLocationButton, 1, 2, 1, 1)
		
		self.sandboxieLocationLabel = QtGui.QLabel(self.locationsGroupBox)
		self.sandboxieLocationLabel.setToolTip('The path to your Sandboxie installation. This folder should contain sandboxie.exe. Optional, only if you wish to use sandboxes')
		self.sandboxieLocationLabel.setText('Sandboxie installation location:')
		self.locationsGroupBoxLayout.addWidget(self.sandboxieLocationLabel, 2, 0, 1, 1)
		
		self.sandboxieLocationLineEdit = QtGui.QLineEdit()
		self.sandboxieLocationLineEdit.setToolTip('The path to your Sandboxie installation. This folder should contain sandboxie.exe. Optional, only if you wish to use sandboxes')
		self.sandboxieLocationLineEdit.setPlaceholderText('Sandboxie folder path')
		self.locationsGroupBoxLayout.addWidget(self.sandboxieLocationLineEdit, 2, 1, 1, 1)
		
		self.sandboxieLocationButton = QtGui.QPushButton()
		self.sandboxieLocationButton.setText('..')
		self.sandboxieLocationButton.setMaximumSize(QtCore.QSize(30, 20))
		self.locationsGroupBoxLayout.addWidget(self.sandboxieLocationButton, 2, 2, 1, 1)
		
		# Steam API section
		self.steamAPIGroupBox = QtGui.QGroupBox(self.generalTab)
		self.steamAPIGroupBox.setStyleSheet(titleStyle)
		self.steamAPIGroupBox.setTitle('Steam API Settings')
		
		self.generalVBoxLayout.addWidget(self.steamAPIGroupBox)

		self.SteamAPIGroupBoxLayout = QtGui.QGridLayout(self.steamAPIGroupBox)
		
		self.steamAPIKeyLabel = QtGui.QLabel(self.steamAPIGroupBox)
		self.steamAPIKeyLabel.setToolTip('Your Steam WebAPI key. Optional, only if you wish to use the drop log feature')
		self.steamAPIKeyLabel.setText('Steam API key:')
		self.SteamAPIGroupBoxLayout.addWidget(self.steamAPIKeyLabel, 0, 0, 1, 1)
		
		self.steamAPIKeyLineEdit = QtGui.QLineEdit()
		self.steamAPIKeyLineEdit.setToolTip('Your Steam WebAPI key. Optional, only if you wish to use the drop log feature')
		self.steamAPIKeyLineEdit.setPlaceholderText('Steam WebAPI key')
		self.SteamAPIGroupBoxLayout.addWidget(self.steamAPIKeyLineEdit, 0, 1, 1, 1)
		
		# Backpack viewer section
		self.backpackGroupBox = QtGui.QGroupBox(self.generalTab)
		self.backpackGroupBox.setStyleSheet(titleStyle)
		self.backpackGroupBox.setTitle('Backpack Viewer Settings')

		self.generalVBoxLayout.addWidget(self.backpackGroupBox)

		self.backpackGroupBoxLayout = QtGui.QGridLayout(self.backpackGroupBox)
		
		self.backpackViewerLabel = QtGui.QLabel(self.backpackGroupBox)
		self.backpackViewerLabel.setToolTip('Your choice of backpack viewer')
		self.backpackViewerLabel.setText('Backpack viewer:')
		self.backpackGroupBoxLayout.addWidget(self.backpackViewerLabel, 0, 0, 1, 1)
		
		self.backpackViewerComboBox = QtGui.QComboBox()
		self.backpackViewerComboBox.insertItem(1, 'Backpack.tf')
		self.backpackViewerComboBox.insertItem(2, 'OPTF2')
		self.backpackViewerComboBox.insertItem(3, 'Steam')
		self.backpackViewerComboBox.insertItem(4, 'TF2B')
		self.backpackViewerComboBox.insertItem(5, 'TF2Items')
		self.backpackGroupBoxLayout.addWidget(self.backpackViewerComboBox, 0, 1, 1, 1)
		
		# TF2 settings section
		self.TF2SettingsGroupBox = QtGui.QGroupBox(self.generalTab)
		self.TF2SettingsGroupBox.setStyleSheet(titleStyle)
		self.TF2SettingsGroupBox.setTitle('TF2 Settings')

		self.generalVBoxLayout.addWidget(self.TF2SettingsGroupBox)

		self.TF2SettingsGroupBoxLayout = QtGui.QGridLayout(self.TF2SettingsGroupBox)
		
		self.idleLaunchLabel = QtGui.QLabel(self.TF2SettingsGroupBox)
		self.idleLaunchLabel.setToolTip('Your TF2 launch options for idling')
		self.idleLaunchLabel.setText('Idle launch settings:')
		self.TF2SettingsGroupBoxLayout.addWidget(self.idleLaunchLabel, 0, 0, 1, 1)
		
		self.idleLaunchTextEdit = QTextEditWithPlaceholderText('TF2 launch options for idling')
		self.idleLaunchTextEdit.setTabChangesFocus(True)
		self.idleLaunchTextEdit.setToolTip('Your TF2 launch options for idling')
		self.TF2SettingsGroupBoxLayout.addWidget(self.idleLaunchTextEdit, 0, 1, 1, 2)
		
		self.idleLaunchTextButton = QtGui.QPushButton()
		self.idleLaunchTextButton.setText('Restore default launch settings')
		self.TF2SettingsGroupBoxLayout.addWidget(self.idleLaunchTextButton, 1, 1, 1, 2)
		
		self.delayTimerLabel = QtGui.QLabel(self.TF2SettingsGroupBox)
		self.delayTimerLabel.setToolTip('Choose the delay between launching accounts')
		self.delayTimerLabel.setText('Account launch delay (secs):')
		self.TF2SettingsGroupBoxLayout.addWidget(self.delayTimerLabel, 2, 0, 1, 1)

		self.delayTimerSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
		self.delayTimerSlider.setToolTip('Choose the delay between launching accounts')
		self.delayTimerSlider.setTickInterval(10)
		self.delayTimerSlider.setMinimum(0)
		self.delayTimerSlider.setMaximum(600)
		self.delayTimerSlider.valueChanged[int].connect(curry(self.changeValue, spinbox='launch_delay_time'))
		self.TF2SettingsGroupBoxLayout.addWidget(self.delayTimerSlider, 2, 1, 1, 1)
		
		self.delayTimerSpinBox = QtGui.QSpinBox()
		self.delayTimerSpinBox.setToolTip('Choose the delay between launching accounts')
		self.delayTimerSpinBox.setSingleStep(10)
		self.delayTimerSpinBox.setMinimum(0)
		self.delayTimerSpinBox.setMaximum(600)
		self.delayTimerSpinBox.valueChanged[int].connect(curry(self.changeSlider, slider='launch_delay_time'))
		self.TF2SettingsGroupBoxLayout.addWidget(self.delayTimerSpinBox, 2, 2, 1, 1)
		
		# TF2Idle settings tab

		# Encryption section
		self.encryptionGroupBox = QtGui.QGroupBox(self.tf2idleTab)
		self.encryptionGroupBox.setStyleSheet(titleStyle)
		self.encryptionGroupBox.setTitle('Encryption')

		self.tf2idleVBoxLayout.addWidget(self.encryptionGroupBox)

		self.encryptionGroupBoxLayout = QtGui.QGridLayout(self.encryptionGroupBox)
		
		self.encryptionModeLabel = QtGui.QLabel(self.encryptionGroupBox)
		self.encryptionModeLabel.setToolTip('Choose whether to encrypt your config file')
		self.encryptionModeLabel.setText('Config file encryption:')
		self.encryptionGroupBoxLayout.addWidget(self.encryptionModeLabel, 0, 0, 1, 1)

		self.encryptionModeVLayout = QtGui.QVBoxLayout()
		self.encryptionModeVLayout.setMargin(0)
		self.encryptionGroupBoxLayout.addLayout(self.encryptionModeVLayout, 0, 1, 1, 1)
		
		self.encryptionOffRadioButton = QtGui.QRadioButton()
		self.encryptionOffRadioButton.setText('Encryption off')
		self.encryptionModeVLayout.addWidget(self.encryptionOffRadioButton)
		
		self.encryptionOnRadioButton = QtGui.QRadioButton()
		self.encryptionOnRadioButton.setText('Encryption on')
		self.encryptionModeVLayout.addWidget(self.encryptionOnRadioButton)

		self.encryptionModeDescriptionLabel = QtGui.QLabel(self.encryptionGroupBox)
		self.encryptionModeDescriptionLabel.setToolTip('Encryption mode description')
		self.encryptionModeDescriptionLabel.setFont(italicfont)
		self.encryptionModeDescriptionLabel.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
		self.encryptionGroupBoxLayout.addWidget(self.encryptionModeDescriptionLabel, 1, 1, 1, 1)

		self.encryptionKeyLabel = QtGui.QLabel(self.encryptionGroupBox)
		self.encryptionKeyLabel.setToolTip('Your encryption key')
		self.encryptionKeyLabel.setText('Encryption key:')
		self.encryptionGroupBoxLayout.addWidget(self.encryptionKeyLabel, 2, 0, 1, 1)

		self.encryptionKeyLineEdit = QtGui.QLineEdit(self.encryptionGroupBox)
		self.encryptionKeyLineEdit.setToolTip('Your encryption key')
		self.encryptionKeyLineEdit.setMaxLength(32)
		self.encryptionKeyLineEdit.setEchoMode(QtGui.QLineEdit.PasswordEchoOnEdit)
		self.encryptionGroupBoxLayout.addWidget(self.encryptionKeyLineEdit, 2, 1, 1, 1)

		# Sandboxie mode section
		self.sandboxesGroupBox = QtGui.QGroupBox(self.tf2idleTab)
		self.sandboxesGroupBox.setStyleSheet(titleStyle)
		self.sandboxesGroupBox.setTitle('Sandboxes')

		self.tf2idleVBoxLayout.addWidget(self.sandboxesGroupBox)

		self.sandboxesGroupBoxLayout = QtGui.QGridLayout(self.sandboxesGroupBox)

		self.sandboxModeLabel = QtGui.QLabel(self.sandboxesGroupBox)
		self.sandboxModeLabel.setToolTip('Choose a Sandboxie mode')
		self.sandboxModeLabel.setText('Sandboxie mode:')
		self.sandboxesGroupBoxLayout.addWidget(self.sandboxModeLabel, 0, 0, 1, 1)

		self.sandboxModeVLayout = QtGui.QVBoxLayout()
		self.sandboxModeVLayout.setMargin(0)
		self.sandboxesGroupBoxLayout.addLayout(self.sandboxModeVLayout, 0, 1, 1, 1)

		self.easySandboxModeRadioButton = QtGui.QRadioButton()
		self.easySandboxModeRadioButton.setText('Easy sandbox mode (experimental)')
		self.sandboxModeVLayout.addWidget(self.easySandboxModeRadioButton)
		
		self.advancedSandboxModeRadioButton = QtGui.QRadioButton()
		self.advancedSandboxModeRadioButton.setText('Advanced sandbox mode')
		self.sandboxModeVLayout.addWidget(self.advancedSandboxModeRadioButton)
		
		self.sandboxModeDescriptionLabel = QtGui.QLabel(self.sandboxesGroupBox)
		self.sandboxModeDescriptionLabel.setToolTip('Sandbox mode description')
		self.sandboxModeDescriptionLabel.setFont(italicfont)
		self.sandboxModeDescriptionLabel.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
		self.sandboxesGroupBoxLayout.addWidget(self.sandboxModeDescriptionLabel, 1, 1, 1, 1)

		# Low priority mode section
		self.priorityModeGroupBox = QtGui.QGroupBox(self.tf2idleTab)
		self.priorityModeGroupBox.setStyleSheet(titleStyle)
		self.priorityModeGroupBox.setTitle('Priority mode')

		self.tf2idleVBoxLayout.addWidget(self.priorityModeGroupBox)

		self.priorityModeGroupBoxLayout = QtGui.QGridLayout(self.priorityModeGroupBox)

		self.priorityModeLabel = QtGui.QLabel(self.priorityModeGroupBox)
		self.priorityModeLabel.setToolTip('Choose a priority mode')
		self.priorityModeLabel.setText('Mode:')
		self.priorityModeGroupBoxLayout.addWidget(self.priorityModeLabel, 0, 0, 1, 1)

		self.priorityModeVLayout = QtGui.QVBoxLayout()
		self.priorityModeVLayout.setMargin(0)
		self.priorityModeGroupBoxLayout.addLayout(self.priorityModeVLayout, 0, 1, 1, 1)

		self.lowPriorityModeRadioButton = QtGui.QRadioButton()
		self.lowPriorityModeRadioButton.setText('Low priority mode')
		self.priorityModeVLayout.addWidget(self.lowPriorityModeRadioButton)

		self.normalPriorityModeRadioButton = QtGui.QRadioButton()
		self.normalPriorityModeRadioButton.setText('Normal priority mode')
		self.priorityModeVLayout.addWidget(self.normalPriorityModeRadioButton)

		self.priorityModeDescriptionLabel = QtGui.QLabel(self.priorityModeGroupBox)
		self.priorityModeDescriptionLabel.setToolTip('Priority mode description')
		self.priorityModeDescriptionLabel.setFont(italicfont)
		self.priorityModeDescriptionLabel.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
		self.priorityModeGroupBoxLayout.addWidget(self.priorityModeDescriptionLabel, 1, 1, 1, 1)
		
		# UI settings section
		self.userInterfaceSettingsGroupBox = QtGui.QGroupBox(self.tf2idleTab)
		self.userInterfaceSettingsGroupBox.setStyleSheet(titleStyle)
		self.userInterfaceSettingsGroupBox.setTitle('User Interface')

		self.tf2idleVBoxLayout.addWidget(self.userInterfaceSettingsGroupBox)

		self.userInterfaceSettingsGroupBoxLayout = QtGui.QGridLayout(self.userInterfaceSettingsGroupBox)

		self.closeBehaviourLabel = QtGui.QLabel()
		self.closeBehaviourLabel.setToolTip('Close the program to the tray')
		self.closeBehaviourLabel.setText('Close program to tray:')
		self.userInterfaceSettingsGroupBoxLayout.addWidget(self.closeBehaviourLabel, 0, 0, 1, 1)

		self.closeBehaviourCheckbox = QtGui.QCheckBox()
		self.userInterfaceSettingsGroupBoxLayout.addWidget(self.closeBehaviourCheckbox, 0, 1, 1, 1)
		
		self.noOfColumnsLabel = QtGui.QLabel()
		self.noOfColumnsLabel.setToolTip('The number of account boxes to display per row')
		self.noOfColumnsLabel.setText('No of account boxes per row:')
		self.userInterfaceSettingsGroupBoxLayout.addWidget(self.noOfColumnsLabel, 1, 0, 1, 1)
		
		self.noOfColumnsSlider = QtGui.QSlider(QtCore.Qt.Horizontal, )
		self.noOfColumnsSlider.setToolTip('The number of account boxes to display per row')
		self.noOfColumnsSlider.setTickInterval(1)
		self.noOfColumnsSlider.setMinimum(1)
		self.noOfColumnsSlider.setMaximum(20)
		self.noOfColumnsSlider.valueChanged[int].connect(curry(self.changeValue, spinbox='no_of_columns'))
		self.userInterfaceSettingsGroupBoxLayout.addWidget(self.noOfColumnsSlider, 1, 1, 1, 1)
		
		self.noOfColumnsSpinBox = QtGui.QSpinBox()
		self.noOfColumnsSpinBox.setToolTip('The number of account boxes to display per row')
		self.noOfColumnsSpinBox.setMinimum(1)
		self.noOfColumnsSpinBox.setMaximum(20)
		self.noOfColumnsSpinBox.valueChanged[int].connect(curry(self.changeSlider, slider='no_of_columns'))
		self.userInterfaceSettingsGroupBoxLayout.addWidget(self.noOfColumnsSpinBox, 1, 2, 1, 1)
		
		self.accountFontSizeLabel = QtGui.QLabel()
		self.accountFontSizeLabel.setToolTip('The size of the font used in the account boxes')
		self.accountFontSizeLabel.setText('Account box font size:')
		self.userInterfaceSettingsGroupBoxLayout.addWidget(self.accountFontSizeLabel, 2, 0, 1, 1)
		
		self.accountFontSizeSlider = QtGui.QSlider(QtCore.Qt.Horizontal, )
		self.accountFontSizeSlider.setToolTip('The size of the icon used in the account boxes')
		self.accountFontSizeSlider.setTickInterval(1)
		self.accountFontSizeSlider.setMinimum(1)
		self.accountFontSizeSlider.setMaximum(50)
		self.accountFontSizeSlider.valueChanged[int].connect(curry(self.changeValue, spinbox='account_font_size'))
		self.userInterfaceSettingsGroupBoxLayout.addWidget(self.accountFontSizeSlider, 2, 1, 1, 1)
		
		self.accountFontSizeSpinBox = QtGui.QSpinBox()
		self.accountFontSizeSpinBox.setToolTip('The size of the font used in the account boxes')
		self.accountFontSizeSpinBox.setMinimum(1)
		self.accountFontSizeSpinBox.setMaximum(50)
		self.accountFontSizeSpinBox.valueChanged[int].connect(curry(self.changeSlider, slider='account_font_size'))
		self.userInterfaceSettingsGroupBoxLayout.addWidget(self.accountFontSizeSpinBox, 2, 2, 1, 1)
		
		self.accountIconSizeLabel = QtGui.QLabel()
		self.accountIconSizeLabel.setToolTip('The size of the icon used in the account boxes')
		self.accountIconSizeLabel.setText('Account box icon size:')
		self.userInterfaceSettingsGroupBoxLayout.addWidget(self.accountIconSizeLabel, 3, 0, 1, 1)
		
		self.accountIconSizeSlider = QtGui.QSlider(QtCore.Qt.Horizontal, )
		self.accountIconSizeSlider.setToolTip('The size of the icon used in the account boxes')
		self.accountIconSizeSlider.setTickInterval(1)
		self.accountIconSizeSlider.valueChanged[int].connect(curry(self.changeValue, spinbox='account_icon_size'))
		self.userInterfaceSettingsGroupBoxLayout.addWidget(self.accountIconSizeSlider, 3, 1, 1, 1)
		
		self.accountIconSizeSpinBox = QtGui.QSpinBox()
		self.accountIconSizeSpinBox.setToolTip('The size of the icon used in the account boxes')
		self.accountIconSizeSpinBox.setMinimum(0)
		self.accountIconSizeSpinBox.setMaximum(99)
		self.accountIconSizeSpinBox.valueChanged[int].connect(curry(self.changeSlider, slider='account_icon_size'))
		self.userInterfaceSettingsGroupBoxLayout.addWidget(self.accountIconSizeSpinBox, 3, 2, 1, 1)
		
		self.accountIconLabel = QtGui.QLabel()
		self.accountIconLabel.setToolTip('Choose an image to use as the account box icons')
		self.accountIconLabel.setText('Account box icon:')
		self.userInterfaceSettingsGroupBoxLayout.addWidget(self.accountIconLabel, 4, 0, 1, 1)
		
		self.accountIconLineEdit = QtGui.QLineEdit()
		self.accountIconLineEdit.setFrame(True)
		self.accountIconLineEdit.setToolTip('Choose an image to use as the account box icons')
		self.userInterfaceSettingsGroupBoxLayout.addWidget(self.accountIconLineEdit, 4, 1, 1, 1)

		self.accountIconButton = QtGui.QPushButton()
		self.accountIconButton.setText('..')
		self.accountIconButton.setMaximumSize(QtCore.QSize(30, 20))
		self.userInterfaceSettingsGroupBoxLayout.addWidget(self.accountIconButton, 4, 2, 1, 1)
		
		self.accountIconRestoreButton = QtGui.QPushButton()
		self.accountIconRestoreButton.setText('Restore default icon')
		self.userInterfaceSettingsGroupBoxLayout.addWidget(self.accountIconRestoreButton, 5, 1, 1, 1)
		
		self.accountBoxPreviewLabel = QtGui.QLabel()
		self.accountBoxPreviewLabel.setToolTip('Account box preview')
		self.accountBoxPreviewLabel.setText('Account box preview:')
		self.userInterfaceSettingsGroupBoxLayout.addWidget(self.accountBoxPreviewLabel, 6, 0, 1, 1)

		ui_account_box_font_size = self.settings.get_option('Settings', 'ui_account_box_font_size')
		ui_account_box_icon_size = int(self.settings.get_option('Settings', 'ui_account_box_icon_size'))
		ui_account_box_icon = self.settings.get_option('Settings', 'ui_account_box_icon')

		self.commandLinkButton = QtGui.QCommandLinkButton()
		icon = QtGui.QIcon()
		if ui_account_box_icon != '':
			icon.addPixmap(QtGui.QPixmap(ui_account_box_icon))
		else:
			icon.addPixmap(QtGui.QPixmap(returnResourcePath('images/unselected_button.png')), QtGui.QIcon.Selected, QtGui.QIcon.Off)
			icon.addPixmap(QtGui.QPixmap(returnResourcePath('images/selected_button.png')), QtGui.QIcon.Selected, QtGui.QIcon.On)
		self.commandLinkButton.setIcon(icon)
		self.commandLinkButton.setIconSize(QtCore.QSize(ui_account_box_icon_size, ui_account_box_icon_size))
		self.commandLinkButton.setCheckable(True)
		self.commandLinkButton.setStyleSheet('font: %spt "TF2 Build";' % ui_account_box_font_size)
		self.commandLinkButton.setText('Idling account')
		self.userInterfaceSettingsGroupBoxLayout.addWidget(self.commandLinkButton, 6, 1, 1, 1)
		
		# Drop log settings tab

		# Poll time and file formatting section
		self.dropLogGroupBox = QtGui.QGroupBox(self.droplogTab)
		self.dropLogGroupBox.setStyleSheet(titleStyle)
		self.dropLogGroupBox.setTitle('Drop Log')

		self.droplogVBoxLayout.addWidget(self.dropLogGroupBox)

		self.dropLogGroupBoxLayout = QtGui.QGridLayout(self.dropLogGroupBox)
		
		self.pollTimeLabel = QtGui.QLabel(self.dropLogGroupBox)
		self.pollTimeLabel.setToolTip('Choose the amount of time between backpack polls')
		self.pollTimeLabel.setText('Backpack polling interval (mins):')
		self.dropLogGroupBoxLayout.addWidget(self.pollTimeLabel, 0, 0, 1, 1)

		self.pollTimeSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
		self.pollTimeSlider.setToolTip('Choose the amount of time between backpack polls')
		self.pollTimeSlider.setTickInterval(1)
		self.pollTimeSlider.setMinimum(1)
		self.pollTimeSlider.setMaximum(30)
		self.pollTimeSlider.valueChanged[int].connect(curry(self.changeValue, spinbox='log_poll_time'))
		self.dropLogGroupBoxLayout.addWidget(self.pollTimeSlider, 0, 1, 1, 1)
		
		self.pollTimeSpinBox = QtGui.QSpinBox()
		self.pollTimeSpinBox.setToolTip('Choose the amount of time between backpack polls')
		self.pollTimeSpinBox.setMinimum(1)
		self.pollTimeSpinBox.setMaximum(30)
		self.pollTimeSpinBox.valueChanged[int].connect(curry(self.changeSlider, slider='log_poll_time'))
		self.dropLogGroupBoxLayout.addWidget(self.pollTimeSpinBox, 0, 2, 1, 1)

		self.fileFormattingLegendLabel = QtGui.QLabel()
		self.fileFormattingLegendLabel.setFont(italicfont)
		self.fileFormattingLegendLabel.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
		self.fileFormattingLegendLabel.setText('Keywords:\n\n{time}, {date}, {item}\n\n{itemtype}, {id}, {account}\n\n{accountnickname}, {nline}')
		self.dropLogGroupBoxLayout.addWidget(self.fileFormattingLegendLabel, 1, 1, 1, 2)

		self.fileFormattingLabel = QtGui.QLabel(self.dropLogGroupBox)
		self.fileFormattingLabel.setToolTip('The formatting of the log when you save to a text file')
		self.fileFormattingLabel.setText('Log file formatting:')
		self.dropLogGroupBoxLayout.addWidget(self.fileFormattingLabel, 2, 0, 1, 1)

		self.fileFormattingLineEdit = QtGui.QLineEdit()
		self.fileFormattingLineEdit.setToolTip('The formatting of the log when you save to a text file')
		self.fileFormattingLineEdit.setPlaceholderText('Log format string')
		self.dropLogGroupBoxLayout.addWidget(self.fileFormattingLineEdit, 2, 1, 1, 2)

		self.fileFormattingTextButton = QtGui.QPushButton()
		self.fileFormattingTextButton.setText('Restore default file formatting')
		self.dropLogGroupBoxLayout.addWidget(self.fileFormattingTextButton, 3, 1, 1, 2)

		self.webViewLabel = QtGui.QLabel(self.dropLogGroupBox)
		self.webViewLabel.setToolTip('Turn the web viewer on or off')
		self.webViewLabel.setText('Web viewer:')
		self.dropLogGroupBoxLayout.addWidget(self.webViewLabel, 4, 0, 1, 1)

		self.webViewVLayout = QtGui.QVBoxLayout()
		self.webViewVLayout.setMargin(0)
		self.dropLogGroupBoxLayout.addLayout(self.webViewVLayout, 4, 1, 1, 1)

		self.webViewOnRadioButton = QtGui.QRadioButton()
		self.webViewOnRadioButton.setText('On')
		self.webViewVLayout.addWidget(self.webViewOnRadioButton)
		
		self.webViewOffRadioButton = QtGui.QRadioButton()
		self.webViewOffRadioButton.setText('Off')
		self.webViewVLayout.addWidget(self.webViewOffRadioButton)

		self.webViewDescriptionLabel = QtGui.QLabel(self.dropLogGroupBox)
		self.webViewDescriptionLabel.setToolTip('Web view description')
		self.webViewDescriptionLabel.setFont(italicfont)
		self.webViewDescriptionLabel.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
		self.dropLogGroupBoxLayout.addWidget(self.webViewDescriptionLabel, 5, 1, 1, 1)

		self.webViewPortLabel = QtGui.QLabel(self.dropLogGroupBox)
		self.webViewPortLabel.setToolTip('Choose the port to use for the web viewer')
		self.webViewPortLabel.setText('Web viewer port:')
		self.dropLogGroupBoxLayout.addWidget(self.webViewPortLabel, 6, 0, 1, 1)
		
		self.webViewPortSpinBox = QtGui.QSpinBox()
		self.webViewPortSpinBox.setToolTip('Choose the port to use for the web viewer')
		self.webViewPortSpinBox.setMinimum(1024)
		self.webViewPortSpinBox.setMaximum(49151)
		self.dropLogGroupBoxLayout.addWidget(self.webViewPortSpinBox, 6, 1, 1, 1)

		self.trayNotificationsLabel = QtGui.QLabel(self.dropLogGroupBox)
		self.trayNotificationsLabel.setToolTip('Turn system tray notifications on or off')
		self.trayNotificationsLabel.setText('System tray notifications:')
		self.dropLogGroupBoxLayout.addWidget(self.trayNotificationsLabel, 7, 0, 1, 1)

		self.trayNotificationsHLayout = QtGui.QHBoxLayout()
		self.trayNotificationsHLayout.setMargin(0)
		self.dropLogGroupBoxLayout.addLayout(self.trayNotificationsHLayout, 7, 1, 1, 1)

		self.trayNotificationsHatsCheckbox = QtGui.QCheckBox()
		self.trayNotificationsHatsCheckbox.setText('Hats')
		self.trayNotificationsHLayout.addWidget(self.trayNotificationsHatsCheckbox)

		self.trayNotificationsWeaponsCheckbox = QtGui.QCheckBox()
		self.trayNotificationsWeaponsCheckbox.setText('Weapons')
		self.trayNotificationsHLayout.addWidget(self.trayNotificationsWeaponsCheckbox)

		self.trayNotificationsToolsCheckbox = QtGui.QCheckBox()
		self.trayNotificationsToolsCheckbox.setText('Tools')
		self.trayNotificationsHLayout.addWidget(self.trayNotificationsToolsCheckbox)

		self.trayNotificationsCratesCheckbox = QtGui.QCheckBox()
		self.trayNotificationsCratesCheckbox.setText('Crates')
		self.trayNotificationsHLayout.addWidget(self.trayNotificationsCratesCheckbox)

		self.dropViewValueLabel = QtGui.QLabel()
		self.dropViewValueLabel.setToolTip('Show item values on the drop log view')
		self.dropViewValueLabel.setText('Show item values:')
		self.dropLogGroupBoxLayout.addWidget(self.dropViewValueLabel, 8, 0, 1, 1)

		self.dropViewValueCheckbox = QtGui.QCheckBox()
		self.dropViewValueCheckbox.setFont(italicfont)
		self.dropViewValueCheckbox.setText('Uses the backpack.tf API to display dropped item values')
		self.dropLogGroupBoxLayout.addWidget(self.dropViewValueCheckbox, 8, 1, 1, 1)

		self.autoLogLabel = QtGui.QLabel()
		self.autoLogLabel.setToolTip('Automatically add accounts to the drop log when idled')
		self.autoLogLabel.setText('Auto log accounts:')
		self.dropLogGroupBoxLayout.addWidget(self.autoLogLabel, 9, 0, 1, 1)

		self.autoLogCheckbox = QtGui.QCheckBox()
		self.autoLogCheckbox.setFont(italicfont)
		self.autoLogCheckbox.setText('Automatically add accounts to the drop log when idled')
		self.dropLogGroupBoxLayout.addWidget(self.autoLogCheckbox, 9, 1, 1, 1)

		# Drop log UI section
		self.dropLogUIGroupBox = QtGui.QGroupBox(self.droplogTab)
		self.dropLogUIGroupBox.setStyleSheet(titleStyle)
		self.dropLogUIGroupBox.setTitle('User Interface')

		self.droplogVBoxLayout.addWidget(self.dropLogUIGroupBox)

		self.dropLogUIGroupBoxLayout = QtGui.QGridLayout(self.dropLogUIGroupBox)
		
		self.dropLogBackgroundColourLabel = QtGui.QLabel(self.dropLogUIGroupBox)
		self.dropLogBackgroundColourLabel.setToolTip('The background colour used in the log viewer')
		self.dropLogBackgroundColourLabel.setText('Drop log background colour:')
		self.dropLogUIGroupBoxLayout.addWidget(self.dropLogBackgroundColourLabel, 0, 0, 1, 1)

		self.dropLogBackgroundColourFrame = QtGui.QLineEdit()
		self.dropLogBackgroundColourFrame.setReadOnly(True)
		self.dropLogUIGroupBoxLayout.addWidget(self.dropLogBackgroundColourFrame, 0, 1, 1, 1)

		self.dropLogBackgroundColourButton = QtGui.QPushButton()
		self.dropLogBackgroundColourButton.setText('..')
		self.dropLogBackgroundColourButton.setMaximumSize(QtCore.QSize(30, 20))
		self.dropLogUIGroupBoxLayout.addWidget(self.dropLogBackgroundColourButton, 0, 2, 1, 1)
		
		self.dropLogFontColourLabel = QtGui.QLabel(self.dropLogUIGroupBox)
		self.dropLogFontColourLabel.setToolTip('The font colour used in the log viewer')
		self.dropLogFontColourLabel.setText('Drop log font colour:')
		self.dropLogUIGroupBoxLayout.addWidget(self.dropLogFontColourLabel, 1, 0, 1, 1)

		self.dropLogFontColourFrame = QtGui.QLineEdit()
		self.dropLogFontColourFrame.setReadOnly(True)
		self.dropLogUIGroupBoxLayout.addWidget(self.dropLogFontColourFrame, 1, 1, 1, 1)

		self.dropLogFontColourButton = QtGui.QPushButton()
		self.dropLogFontColourButton.setText('..')
		self.dropLogFontColourButton.setMaximumSize(QtCore.QSize(30, 20))
		self.dropLogUIGroupBoxLayout.addWidget(self.dropLogFontColourButton, 1, 2, 1, 1)
		
		self.dropLogFontLabel = QtGui.QLabel(self.dropLogUIGroupBox)
		self.dropLogFontLabel.setToolTip('The font used in the log viewer')
		self.dropLogFontLabel.setText('Drop log font:')
		self.dropLogUIGroupBoxLayout.addWidget(self.dropLogFontLabel, 2, 0, 1, 1)
		
		self.dropLogFontPreviewLabel = QtGui.QLabel()
		self.dropLogFontPreviewLabel.setText('You have found: Razorback!')
		self.dropLogUIGroupBoxLayout.addWidget(self.dropLogFontPreviewLabel, 2, 1, 1, 1)
		
		self.dropLogFontButton = QtGui.QPushButton()
		self.dropLogFontButton.setText('..')
		self.dropLogFontButton.setMaximumSize(QtCore.QSize(30, 20))
		self.dropLogUIGroupBoxLayout.addWidget(self.dropLogFontButton, 2, 2, 1, 1)

		# Add buttons
		self.buttonBox = QtGui.QDialogButtonBox(self)
		self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
		self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
		self.buttonBox.setCenterButtons(False)
		self.vBoxLayout.addWidget(self.buttonBox)

		# Set mininmum label lengths on all groupboxes to align right hand side widgets
		self.setMinLabelLength(self.generalTab)
		self.setMinLabelLength(self.tf2idleTab)
		self.setMinLabelLength(self.droplogTab)
		
		# Signal connections
		QtCore.QObject.connect(self.steamLocationButton, QtCore.SIGNAL('clicked()'), curry(self.getDirectory, action='steam_location'))
		QtCore.QObject.connect(self.secondarySteamappsLocationButton, QtCore.SIGNAL('clicked()'), curry(self.getDirectory, action='secondary_steamapps_location'))
		QtCore.QObject.connect(self.sandboxieLocationButton, QtCore.SIGNAL('clicked()'), curry(self.getDirectory, action='sandboxie_location'))
		QtCore.QObject.connect(self.idleLaunchTextButton, QtCore.SIGNAL('clicked()'), curry(self.restoreDefault, action='idle_launch'))
		QtCore.QObject.connect(self.encryptionOnRadioButton, QtCore.SIGNAL('clicked()'), self.updateEncryptionModeDescription)
		QtCore.QObject.connect(self.encryptionOffRadioButton, QtCore.SIGNAL('clicked()'), self.updateEncryptionModeDescription)
		QtCore.QObject.connect(self.easySandboxModeRadioButton, QtCore.SIGNAL('clicked()'), self.updateSandboxModeDescription)
		QtCore.QObject.connect(self.advancedSandboxModeRadioButton, QtCore.SIGNAL('clicked()'), self.updateSandboxModeDescription)
		QtCore.QObject.connect(self.lowPriorityModeRadioButton, QtCore.SIGNAL('clicked()'), self.updatePriorityModeDescription)
		QtCore.QObject.connect(self.normalPriorityModeRadioButton, QtCore.SIGNAL('clicked()'), self.updatePriorityModeDescription)
		QtCore.QObject.connect(self.webViewOnRadioButton, QtCore.SIGNAL('clicked()'), self.updateWebViewDescription)
		QtCore.QObject.connect(self.webViewOffRadioButton, QtCore.SIGNAL('clicked()'), self.updateWebViewDescription)
		QtCore.QObject.connect(self.accountIconButton, QtCore.SIGNAL('clicked()'), self.getIconFile)
		QtCore.QObject.connect(self.accountIconRestoreButton, QtCore.SIGNAL('clicked()'), curry(self.restoreDefault, action='account_icon'))
		QtCore.QObject.connect(self.fileFormattingTextButton, QtCore.SIGNAL('clicked()'), curry(self.restoreDefault, action='file_formatting'))
		QtCore.QObject.connect(self.dropLogBackgroundColourButton, QtCore.SIGNAL('clicked()'), curry(self.getColour, component='background'))
		QtCore.QObject.connect(self.dropLogFontColourButton, QtCore.SIGNAL('clicked()'), curry(self.getColour, component='font'))
		QtCore.QObject.connect(self.dropLogFontButton, QtCore.SIGNAL('clicked()'), self.getFont)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL('accepted()'), self.accept)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL('rejected()'), self.reject)

		self.populateDetails()

	def setMinLabelLength(self, tabwidget):
		groupboxes = tabwidget.findChildren(QtGui.QGroupBox)
		labels = []
		for groupbox in groupboxes:
			labels.extend(groupbox.findChildren(QtGui.QLabel))
		largestwidth = labels[0].sizeHint().width()
		for label in labels[1:]:
			if label.sizeHint().width() > largestwidth:
				largestwidth = label.sizeHint().width()
		for label in labels:
			label.setMinimumSize(QtCore.QSize(largestwidth, 0))

	def updatePreview(self, action, value):
		if action == 'account_font_size':
			self.commandLinkButton.setStyleSheet('font: %spt "TF2 Build";' % value)
		elif action == 'account_icon_size':
			self.commandLinkButton.setIconSize(QtCore.QSize(int(value), int(value)))
		elif action == 'account_icon':
			icon = QtGui.QIcon()
			if value != '':
				icon.addPixmap(QtGui.QPixmap(value))
			else:
				icon.addPixmap(QtGui.QPixmap(returnResourcePath('images/unselected_button.png')), QtGui.QIcon.Selected, QtGui.QIcon.Off)
				icon.addPixmap(QtGui.QPixmap(returnResourcePath('images/selected_button.png')), QtGui.QIcon.Selected, QtGui.QIcon.On)
			self.commandLinkButton.setIcon(icon)

	def updateEncryptionModeDescription(self):
		if self.encryptionOnRadioButton.isChecked():
			self.encryptionModeDescriptionLabel.setText('TF2Idle will encrypt your config file. This requires you to enter your key to decrypt\nthe config file every time you start up TF2Idle')
			self.encryptionKeyLineEdit.setText(self.settings.get_encryption_key())
			self.encryptionKeyLineEdit.setReadOnly(False)
			self.encryptionKeyLineEdit.setStyleSheet('')
		else:
			self.encryptionModeDescriptionLabel.setText('TF2Idle will not encrypt your config file\n')
			self.encryptionKeyLineEdit.setReadOnly(True)
			self.encryptionKeyLineEdit.setStyleSheet(self.greyoutstyle)

	def updateSandboxModeDescription(self):
		if self.easySandboxModeRadioButton.isChecked():
			self.sandboxModeDescriptionLabel.setText('TF2Idle will create and delete sandboxes\non the fly as needed')
		else:
			self.sandboxModeDescriptionLabel.setText('You will need to create sandboxes for the\naccounts yourself')

	def updatePriorityModeDescription(self):
		if self.lowPriorityModeRadioButton.isChecked():
			self.priorityModeDescriptionLabel.setText('Steam will be started in low priority mode')
		else:
			self.priorityModeDescriptionLabel.setText('Steam will be started in normal priority mode')
	
	def updateWebViewDescription(self):
		if self.webViewOnRadioButton.isChecked():
			self.webViewDescriptionLabel.setText('The item drop log will be viewable online at <ipaddress>:<port>\n(may require you to set up port forwarding for external networks)')
		else:
			self.webViewDescriptionLabel.setText('No web view for the item drop log\n')

	def changeValue(self, value, spinbox):
		if spinbox == 'no_of_columns':
			self.noOfColumnsSpinBox.setValue(int(value))
		elif spinbox == 'account_font_size':
			self.accountFontSizeSpinBox.setValue(int(value))
			self.updatePreview('account_font_size', value)
		elif spinbox == 'account_icon_size':
			self.accountIconSizeSpinBox.setValue(int(value))
			self.updatePreview('account_icon_size', value)
		elif spinbox == 'log_poll_time':
			self.pollTimeSpinBox.setValue(int(value))
		elif spinbox == 'launch_delay_time':
			self.delayTimerSpinBox.setValue(int(value))

	def changeSlider(self, value, slider):
		if slider == 'no_of_columns':
			self.noOfColumnsSlider.setValue(int(value))
		if slider == 'account_font_size':
			self.accountFontSizeSlider.setValue(int(value))
		elif slider == 'account_icon_size':
			self.accountIconSizeSlider.setValue(int(value))
		elif slider == 'log_poll_time':
			self.pollTimeSlider.setValue(int(value))
		elif slider == 'launch_delay_time':
			self.delayTimerSlider.setValue(int(value))
	
	def getDirectory(self, action):
		if action == 'steam_location':
			filepath = str(QtGui.QFileDialog.getExistingDirectory(self.generalTab, 'Select Steam Directory'))
			if filepath:
				self.steamLocationLineEdit.setText(filepath)
		elif action == 'secondary_steamapps_location':
			filepath = str(QtGui.QFileDialog.getExistingDirectory(self.generalTab, 'Select Secondary Steamapps Directory'))
			if filepath:
				self.secondarySteamappsLocationLineEdit.setText(filepath)
		elif action == 'sandboxie_location':
			filepath = str(QtGui.QFileDialog.getExistingDirectory(self.generalTab, 'Select Sandboxie Directory'))
			if filepath:
				self.sandboxieLocationLineEdit.setText(filepath)
	
	def getIconFile(self):
		filepath = str(QtGui.QFileDialog.getOpenFileName(self.tf2idleTab, 'Select Account Icon', filter='Images (*.png *.jpeg *.jpg *.gif *.bmp)'))
		if filepath:
			self.accountIconLineEdit.setText(filepath)
			self.updatePreview('account_icon', filepath)

	def getColour(self, component):
		colour = QtGui.QColorDialog.getColor()
		if colour.isValid():
			if component == 'background':
				self.dropLogBackgroundColourFrame.setStyleSheet('background-color: %s;' % colour.name())
				self.dropLogBackgroundColour = str(colour.name())[1:]
			elif component == 'font':
				self.dropLogFontColourFrame.setStyleSheet('background-color: %s;' % colour.name())
				self.dropLogFontColour = str(colour.name())[1:]
	
	def getFont(self):
		font, valid = QtGui.QFontDialog().getFont(self.dropLogFont)
		if valid:
			self.dropLogFont = font
			self.dropLogFontPreviewLabel.setFont(font)
			self.dropLogFontSize = font.pointSize()
			self.dropLogFontFamily = font.family()
			self.dropLogFontItalic = font.style()
			self.dropLogFontBold = font.weight()

	def restoreDefault(self, action):
		if action == 'idle_launch':
			self.idleLaunchTextEdit.setText('+exec idle.cfg -textmode -nosound -low -novid -nopreload -nojoy -sw +sv_lan 1 -width 640 -height 480 +map itemtest')
		elif action == 'account_icon':
			self.accountIconLineEdit.setText('')
			self.updatePreview('account_icon', '')
		elif action == 'file_formatting':
			self.fileFormattingLineEdit.setText('{date}, {time}, {itemtype}, {item}, {id}, {account}{nline}')
	
	def accept(self):
		steam_location = str(self.steamLocationLineEdit.text())
		secondary_steamapps_location = str(self.secondarySteamappsLocationLineEdit.text())
		sandboxie_location = str(self.sandboxieLocationLineEdit.text())
		API_key = str(self.steamAPIKeyLineEdit.text()).strip()
		backpack_viewer = backpackViewerDict[str(self.backpackViewerComboBox.currentIndex())]
		launch_options = str(self.idleLaunchTextEdit.toPlainText())
		launch_delay_time = str(self.delayTimerSpinBox.text())
		log_file_formatting = str(self.fileFormattingLineEdit.text())
		close_to_tray = str(self.closeBehaviourCheckbox.isChecked())
		ui_no_of_columns = str(self.noOfColumnsSpinBox.text())
		ui_account_box_font_size = str(self.accountFontSizeSpinBox.text())
		ui_account_box_icon_size = str(self.accountIconSizeSpinBox.text())
		ui_account_box_icon = str(self.accountIconLineEdit.text())
		log_poll_time = str(self.pollTimeSpinBox.text())
		web_view_port = str(self.webViewPortSpinBox.text())

		if self.encryptionOnRadioButton.isChecked():
			encryption_key = str(self.encryptionKeyLineEdit.text())

		if self.easySandboxModeRadioButton.isChecked():
			easy_sandbox_mode = 'yes'
		elif self.advancedSandboxModeRadioButton.isChecked():
			easy_sandbox_mode = 'no'

		if self.lowPriorityModeRadioButton.isChecked():
			low_priority_mode = 'yes'
		elif self.normalPriorityModeRadioButton.isChecked():
			low_priority_mode = 'no'

		if self.webViewOnRadioButton.isChecked():
			web_view = 'On'
		elif self.webViewOffRadioButton.isChecked():
			web_view = 'Off'

		if self.dropViewValueCheckbox.isChecked():
			log_show_item_value = 'True'
		else:
			log_show_item_value = 'False'

		if self.autoLogCheckbox.isChecked():
			auto_add_to_log = 'True'
		else:
			auto_add_to_log = 'False'

		sys_tray_notification_toggles = ''
		if self.trayNotificationsHatsCheckbox.isChecked():
			sys_tray_notification_toggles += 'hats,'
		if self.trayNotificationsWeaponsCheckbox.isChecked():
			sys_tray_notification_toggles += 'weapons,'
		if self.trayNotificationsToolsCheckbox.isChecked():
			sys_tray_notification_toggles += 'tools,'
		if self.trayNotificationsCratesCheckbox.isChecked():
			sys_tray_notification_toggles += 'crates'
		if sys_tray_notification_toggles != '':
			if sys_tray_notification_toggles[len(sys_tray_notification_toggles)-1] == ',':
				sys_tray_notification_toggles = sys_tray_notification_toggles[:len(sys_tray_notification_toggles)-1]

		self.settings.set_option('Settings', 'sys_tray_notifications', sys_tray_notification_toggles)

		allowedFileTypes = ['.png', '.jpeg', '.jpg', '.gif', '.bmp']

		if steam_location == '':
			QtGui.QMessageBox.warning(self, 'Error', 'Please enter a Steam install location')
		elif launch_options == '':
			QtGui.QMessageBox.warning(self, 'Error', 'Please enter some launch options')
		elif ui_account_box_icon != '' and (not os.path.isfile(ui_account_box_icon) or os.path.splitext(ui_account_box_icon)[1] not in allowedFileTypes):
			QtGui.QMessageBox.warning(self, 'Error', 'Account icon is not a valid image file')
		elif self.encryptionOnRadioButton.isChecked() and encryption_key == '':
			QtGui.QMessageBox.warning(self, 'Error', 'Please enter an encryption key')
		else:
			self.settings.set_option('Settings', 'steam_location', steam_location)
			self.settings.set_option('Settings', 'secondary_steamapps_location', secondary_steamapps_location)
			self.settings.set_option('Settings', 'sandboxie_location', sandboxie_location)
			self.settings.set_option('Settings', 'API_key', API_key)
			self.settings.set_option('Settings', 'backpack_viewer', backpack_viewer)
			if not self.idleLaunchTextEdit.containsPlacedText():
				self.settings.set_option('Settings', 'launch_options', launch_options)
			else:
				self.settings.set_option('Settings', 'launch_options', '')
			self.settings.set_option('Settings', 'launch_delay_time', launch_delay_time)
			self.settings.set_option('Settings', 'log_file_formatting', log_file_formatting)
			self.settings.set_option('Settings', 'close_to_tray', close_to_tray)
			self.settings.set_option('Settings', 'ui_no_of_columns', ui_no_of_columns)
			self.settings.set_option('Settings', 'ui_account_box_font_size', ui_account_box_font_size)
			self.settings.set_option('Settings', 'ui_account_box_icon_size', ui_account_box_icon_size)
			self.settings.set_option('Settings', 'ui_account_box_icon', ui_account_box_icon)
			self.settings.set_option('Settings', 'easy_sandbox_mode', easy_sandbox_mode)
			self.settings.set_option('Settings', 'low_priority_mode', low_priority_mode)
			self.settings.set_option('Settings', 'log_web_view', web_view)
			self.settings.set_option('Settings', 'log_web_view_port', web_view_port)
			self.settings.set_option('Settings', 'log_show_item_value', log_show_item_value)
			self.settings.set_option('Settings', 'auto_add_to_log', auto_add_to_log)
			self.settings.set_option('Settings', 'log_poll_time', log_poll_time)
			self.settings.set_option('Settings', 'ui_log_background_colour', self.dropLogBackgroundColour)
			self.settings.set_option('Settings', 'ui_log_font_colour', self.dropLogFontColour)
			self.settings.set_option('Settings', 'ui_log_font_size', str(self.dropLogFontSize))
			self.settings.set_option('Settings', 'ui_log_font_family', str(self.dropLogFontFamily))
			self.settings.set_option('Settings', 'ui_log_font_style', str(self.dropLogFontItalic))
			self.settings.set_option('Settings', 'ui_log_font_weight', str(self.dropLogFontBold))
			if self.encryptionOnRadioButton.isChecked():
				self.settings.set_encryption(True)
				self.settings.set_encryption_key(encryption_key)
			else:
				self.settings.set_encryption(False)

			# Start webserver for drop logger
			self.emit(QtCore.SIGNAL('web_view_status'), web_view)
			# Toggle system tray notifications for drop logger
			self.emit(QtCore.SIGNAL('toggle_sys_tray_notification'), sys_tray_notification_toggles)
			# Toggle item values in drop logger
			self.emit(QtCore.SIGNAL('toggle_item_values_display'), log_show_item_value)

			self.settings.flush_configuration()
			self.close()
		
	def populateDetails(self):
		self.steamLocationLineEdit.setText(self.settings.get_option('Settings', 'steam_location'))
		self.secondarySteamappsLocationLineEdit.setText(self.settings.get_option('Settings', 'secondary_steamapps_location'))
		self.sandboxieLocationLineEdit.setText(self.settings.get_option('Settings', 'sandboxie_location'))
		self.steamAPIKeyLineEdit.setText(self.settings.get_option('Settings', 'API_key'))
		viewer = [key for key, value in backpackViewerDict.iteritems() if value == self.settings.get_option('Settings', 'backpack_viewer')][0]
		self.backpackViewerComboBox.setCurrentIndex(int(viewer))
		if self.settings.get_option('Settings', 'launch_options') != '':
			self.idleLaunchTextEdit.setText(self.settings.get_option('Settings', 'launch_options'))
		else:
			self.idleLaunchTextEdit.setPlaceholderText()
		self.delayTimerSpinBox.setValue(int(self.settings.get_option('Settings', 'launch_delay_time')))
		self.fileFormattingLineEdit.setText(self.settings.get_option('Settings', 'log_file_formatting'))
		self.noOfColumnsSpinBox.setValue(int(self.settings.get_option('Settings', 'ui_no_of_columns')))
		self.accountFontSizeSpinBox.setValue(int(self.settings.get_option('Settings', 'ui_account_box_font_size')))
		self.accountIconSizeSlider.setValue(int(self.settings.get_option('Settings', 'ui_account_box_icon_size')))
		self.accountIconLineEdit.setText(self.settings.get_option('Settings', 'ui_account_box_icon'))

		if self.settings.get_option('Settings', 'close_to_tray') == 'True':
			self.closeBehaviourCheckbox.setChecked(True)

		if self.settings.get_encryption():
			self.encryptionKeyLineEdit.setText(self.settings.get_encryption_key())
			self.encryptionOnRadioButton.setChecked(True)
		else:
			self.encryptionOffRadioButton.setChecked(True)
			self.encryptionKeyLineEdit.setReadOnly(True)
			self.encryptionKeyLineEdit.setStyleSheet(self.greyoutstyle)

		if self.settings.get_option('Settings', 'easy_sandbox_mode') == 'yes':
			self.easySandboxModeRadioButton.setChecked(True)
		else:
			self.advancedSandboxModeRadioButton.setChecked(True)

		if self.settings.get_option('Settings', 'low_priority_mode') == 'yes':
			self.lowPriorityModeRadioButton.setChecked(True)
		else:
			self.normalPriorityModeRadioButton.setChecked(True)

		sys_tray_notification_toggles = self.settings.get_option('Settings', 'sys_tray_notifications').split(',')

		if 'hats' in sys_tray_notification_toggles:
			self.trayNotificationsHatsCheckbox.setChecked(True)
		if 'weapons' in sys_tray_notification_toggles:
			self.trayNotificationsWeaponsCheckbox.setChecked(True)
		if 'tools' in sys_tray_notification_toggles:
			self.trayNotificationsToolsCheckbox.setChecked(True)
		if 'crates' in sys_tray_notification_toggles:
			self.trayNotificationsCratesCheckbox.setChecked(True)

		if self.settings.get_option('Settings', 'log_web_view') == 'On':
			self.webViewOnRadioButton.setChecked(True)
		else:
			self.webViewOffRadioButton.setChecked(True)

		if self.settings.get_option('Settings', 'log_show_item_value') == 'True':
			self.dropViewValueCheckbox.setChecked(True)
		else:
			self.dropViewValueCheckbox.setChecked(False)

		if self.settings.get_option('Settings', 'auto_add_to_log') == 'True':
			self.autoLogCheckbox.setChecked(True)
		else:
			self.autoLogCheckbox.setChecked(False)

		self.webViewPortSpinBox.setValue(int(self.settings.get_option('Settings', 'log_web_view_port')))
		self.pollTimeSpinBox.setValue(int(self.settings.get_option('Settings', 'log_poll_time')))
		self.pollTimeSlider.setValue(int(self.settings.get_option('Settings', 'log_poll_time')))
		self.dropLogBackgroundColour = self.settings.get_option('Settings', 'ui_log_background_colour')
		self.dropLogBackgroundColourFrame.setStyleSheet('background-color: #%s;' % self.dropLogBackgroundColour)

		self.dropLogFontColour = self.settings.get_option('Settings', 'ui_log_font_colour')
		self.dropLogFontColourFrame.setStyleSheet('background-color: #%s;' % self.dropLogFontColour)

		self.dropLogFontSize = self.settings.get_option('Settings', 'ui_log_font_size')
		self.dropLogFontFamily = self.settings.get_option('Settings', 'ui_log_font_family')
		self.dropLogFontItalic = self.settings.get_option('Settings', 'ui_log_font_style')
		self.dropLogFontBold = self.settings.get_option('Settings', 'ui_log_font_weight')
		self.dropLogFont = QtGui.QFont(self.dropLogFontFamily, int(self.dropLogFontSize), int(self.dropLogFontBold), self.dropLogFontItalic == '1')
		self.dropLogFontPreviewLabel.setFont(self.dropLogFont)

		self.updateEncryptionModeDescription()
		self.updateSandboxModeDescription()
		self.updatePriorityModeDescription()
		self.updateWebViewDescription()