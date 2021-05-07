from abc import ABC, abstractmethod

class PluginBase(ABC):
	@property
	@abstractmethod
	def id(self):
		pass

def MCMMPlugin(plugin_class):
	plugin_class._is_mcmm_plugin = True
	return plugin_class

def DownloadHandler(func):
	func._is_mcmm_handler = True
	func._mcmm_event = HandlerType.download
	return func

class HandlerType:
	download = "download"
	info = "info"
