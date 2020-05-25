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
			'fr': 'ordre des composants',
			'es': 'orden de componentes',
			'nl': 'volgorde van componenten',
		})
	
	@objc.python_method
	def foreground(self, layer):
		self.colorComponents( layer )
		
	@objc.python_method
	def inactiveLayerBackground(self, layer):
		self.colorComponents( layer, colorfactor=0.65 )

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
					componentColor = NSColor.colorWithCalibratedRed_green_blue_alpha_( 
						colorfactor * (difference ** 2.0), # red
						colorfactor * (1.0 - difference),  # green
						colorfactor * difference,          # blue
						0.7, # alpha
						)
					
					if thisComponent in Layer.selection:
						componentColor.highlightWithLevel_(0.7).set()
					else:
						componentColor.set()
					componentArea.fill()
					
					if not thisComponent.automaticAlignment:
						componentColor.colorWithAlphaComponent_(0.8).set()
						componentArea.setLineWidth_(2.0/self.getScale())
						componentArea.setLineDash_count_phase_((4/self.getScale()**0.9,3/self.getScale()**0.9),2,0.0)
						componentArea.stroke()
			
			NSColor.textColor.colorWithAlphaComponent_(0.4).set()
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
