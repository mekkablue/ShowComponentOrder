# encoding: utf-8
from __future__ import division, print_function, unicode_literals

###########################################################################################################
#
#
#	Reporter Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Reporter
#
#
###########################################################################################################

from GlyphsApp import *
from GlyphsApp.plugins import *
from AppKit import NSRoundLineJoinStyle

class ShowComponentOrder(ReporterPlugin):

	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': 'Component Order',
			'de': 'Reihenfolge der Komponenten',
			'fr': 'ordre des components',
			'es': 'orden de componentes'
			'nl': 'volgorde van componenten',
		})
	
	@objc.python_method
	def foreground(self, layer):
		self.colorComponents( layer )
		
	@objc.python_method
	def inactiveLayerBackground(self, layer):
		self.colorComponents( layer, colorfactor=0.8 )

	@objc.python_method
	def colorComponents(self, Layer, colorfactor=1.0):
		if Layer.components:
			factor = 1.0 / len(Layer.components)
			
			try:
				# GLYPHS 3
				layerObjects = Layer.shapes
			except:
				# GLYPHS 2
				layerObjects = Layer.components
			
			for i, thisComponent in enumerate( layerObjects ):
				if type(thisComponent) is GSComponent:
					difference = factor * float( i )
					componentArea = thisComponent.bezierPath
				
					# colored fill
					NSColor.colorWithCalibratedRed_green_blue_alpha_( 
						colorfactor * (difference ** 2.0), # red
						colorfactor * (1.0 - difference),  # green
						colorfactor * difference,          # blue
						0.6                                # alpha
						).set()
					componentArea.fill()
			
			NSColor.colorWithRed_green_blue_alpha_(0, 0, 0, 0.5).set()
			for thisPath in Layer.paths:
				thisPath.bezierPath.fill()
	
	
	def needsExtraMainOutlineDrawingForInactiveLayer_(self, layer):
		if layer.components:
			return False
		else:
			return True
	
	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
