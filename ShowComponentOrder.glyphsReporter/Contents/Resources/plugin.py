# encoding: utf-8

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

	def settings(self):
		self.menuName = Glyphs.localize({
			'en': u'Component Order',
			'de': u'Reihenfolge der Komponenten',
			'fr': u'ordre des components',
			'nl': u'volgorde van componenten',
		})
		
	def foreground(self, layer):
		self.colorComponents( layer )
		
	def inactiveLayers(self, layer):
		self.colorComponents( layer, colorfactor=0.8 )

	def colorComponents(self, Layer, colorfactor=1.0):
		if Layer.components:
			factor = 1.0 / len(Layer.components)
			
			for i, thisComponent in enumerate( Layer.components ):
				difference = factor * float( i )
				componentArea = Layer.components[i].bezierPath
				
				# colored fill
				NSColor.colorWithCalibratedRed_green_blue_alpha_( 
					colorfactor * (difference ** 2.0), # red
					colorfactor * (1.0 - difference),  # green
					colorfactor * difference,          # blue
					1.0                                # alpha
					).set()
				componentArea.fill()
				
				# stroke
				NSColor.blackColor().set()
				componentArea.setLineJoinStyle_( NSRoundLineJoinStyle )
				componentArea.setLineWidth_( 8.0 )
				componentArea.stroke()
			
			NSColor.colorWithRed_green_blue_alpha_(0, 0, 0, 0.5).set()
			for thisPath in Layer.paths:
				thisPath.bezierPath.fill()
	
	def needsExtraMainOutlineDrawingForInactiveLayer_(self, layer):
		if layer.components:
			return False
		else:
			return True
	
