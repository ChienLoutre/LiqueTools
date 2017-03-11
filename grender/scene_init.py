# Liquerilla Scene Init
from variables import *
from guerilla import Document, Modifier, pynode


class liquerillaInit():
	
	def __init__(self):

		self.renderpass = guerillabank
		self.charvalue = None
		self.doc = Document()

	def clear_variables(self):
		'''
		Flushes the cache of the RenderPass and go back to the variable of you project.


		'''
		self.renderpass = guerillabank

	def scene_location(self):

		file_name = self.doc.getfilename()
		self.charvalue = str(file_name).split('/')

		if not project_name in self.charvalue:
			raise ValueError('You are not working in the project !')

	def clear_rPasses(self):

		for renderpass in self.doc.children (type="RenderPass", recursive=True):
			with Modifier() as mod:
				mod.deletenode(renderpass)

	def set_layer(self):

		self.clear_variables()
		self.scene_location()
		self.clear_rPasses()	

		print(self.charvalue)
		if 'seq' in self.charvalue:
			self.renderpass += '/renderPass_sequence.glayer'
		else:
			self.renderpass += '/renderPass_asset.glayer'

		self.doc.loadfile(self.renderpass)

	def get_fileversion(self):

		self.scene_location()
		print('You are working on ' + self.charvalue[-2])


	def get_Rpass(self):

		rList = []

		for renderpass in self.doc.children (type="RenderPass", recursive=True):
			rList.append(renderpass)

		if not len(rList) == 1:
			raise ValueError('You Must have only one RenderPass in your scene.')

		rPass = rList[0]

		return rPass

	def set_gamma(self, g=1):
		'''
		Sets the Project Gamma to a float value you enter.
		Linear = 1
		sRGB = 2.2
		
		set_gamma(1)

		'''
		self.doc.Preferences.ProjectGamma.set(g)