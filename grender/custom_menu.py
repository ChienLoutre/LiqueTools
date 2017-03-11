from guerilla import command, Node
import grender.save as save
from grender.scene_init import liquerillaInit
li = liquerillaInit()

reload(save)

class SaveVersion(command):
	@staticmethod
	def action(luaObj, window, x, y, suffix):

		import grender.save as save
		reload(save)
		save.version()

class SaveMaster(command):
	@staticmethod
	def action(luaObj, window, x, y, suffix):

		import grender.save as save
		reload(save)
		save.master()

class LiqueRender(command):
	@staticmethod
	def action(luaObj, window, x, y, suffix):

		import grender.renderer as rd
		reload(rd)

		
class LiqueOpener(command):
	@staticmethod
	def action(luaObj, window, x, y, suffix):

		import grender.window as wi
		reload(wi)

class ReloadRefs(command):
	@staticmethod
	def action(luaObj, window, x, y, suffix):

		import grender.reload_refs as rr
		reload(rr)
		rr.getMissingRefs()
		
class getDocVersion(command):
	@staticmethod
	def action(luaObj, window, x, y, suffix):
		
		li.get_fileversion()

class getLiqueRenderPass(command):
	@staticmethod
	def action(luaObj, window, x, y, suffix):
		
		li.set_layer()


cmd = SaveVersion('Save Version')
cmd.install('Liquefacteur')

cmd = SaveMaster('Save Master')
cmd.install('Liquefacteur')

cmd = LiqueRender('LiqueRender')
cmd.install('Liquefacteur')

cmd = LiqueOpener('LiqueOpener')
cmd.install('Liquefacteur')

cmd = ReloadRefs('Reload Missing Refs')
cmd.install('Liquefacteur')

cmd = getDocVersion('Print Version')
cmd.install('Liquefacteur')

cmd = getLiqueRenderPass('Load LiqueRenderPass')
cmd.install('Liquefacteur')
