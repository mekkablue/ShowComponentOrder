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
from AppKit import NSColor, NSRoundLineJoinStyle, NSClassFromString, NSBezierPath, NSAffineTransform, NSMidY

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
		self.colorComponents( layer, colorfactor=0.6, selectionCounts=False )

	@objc.python_method
	def conditionsAreMetForDrawing(self):
		"""
		Don't activate if text or pan (hand) tool are active.
		"""
		currentController = self.controller.view().window().windowController()
		if currentController:
			tool = currentController.toolDrawDelegate()
			textToolIsActive = tool.isKindOfClass_( NSClassFromString("GlyphsToolText") )
			handToolIsActive = tool.isKindOfClass_( NSClassFromString("GlyphsToolHand") )
			if not textToolIsActive and not handToolIsActive: 
				return True
		return False
	
	@objc.python_method
	def fitLayerInFrame(self, layer, frame):
		ascender, descender = layer.ascender, layer.descender
		master = layer.master
		previewAscender = master.customParameters["Preview Ascender"]
		if not previewAscender is None:
			ascender = abs(previewAscender)
		previewDescender = master.customParameters["Preview Descender"]
		if not previewDescender is None:
			descender = -abs(previewDescender)
		
		scaleFactor = frame.size.height / ((ascender - descender) * 1.3)
		scale = NSAffineTransform.transform()
		scale.translateXBy_yBy_(
			frame.origin.x + (frame.size.width - (layer.width * scaleFactor)) / 2.0,
			NSMidY(frame) - (ascender * scaleFactor * 0.5) - (descender * scaleFactor * 0.125),
		)
		scale.scaleBy_(scaleFactor)
		return scale
	
	def drawFontViewForegroundForLayer_inFrame_(self, layer, frame):
		if not layer.components:
			return
		scale = self.fitLayerInFrame(layer, frame)
		components = layer.components
		factor = 1.0 / len(components)
		for i, thisShape in enumerate(components):
			difference = factor * i
			shapeColor = NSColor.colorWithCalibratedRed_green_blue_alpha_( 
				(difference ** 2.0), # red
				(1.0 - difference),  # green
				difference,          # blue
				0.8, # alpha
				)
			shapeColor.set()
			shapeArea = thisShape.bezierPath
			shapeArea.transformUsingAffineTransform_(scale)
			shapeArea.fill()
		
	@objc.python_method
	def colorComponents(self, Layer, colorfactor=1.0, selectionCounts=True):
		if Layer.components:
			currentlyEditing = self.conditionsAreMetForDrawing()
			factor = 1.0 / len(Layer.components)
			
			if Glyphs.versionNumber >= 3:
				# GLYPHS 3
				layerObjects = Layer.shapes
			else:
				# GLYPHS 2
				layerObjects = Layer.components
			
			pathBezier = NSBezierPath.bezierPath()
			for i, thisShape in enumerate( layerObjects ):
				if type(thisShape) is GSComponent:
					difference = factor * float( i )
					componentArea = thisShape.bezierPath
				
					# colored fill
					componentColor = NSColor.colorWithCalibratedRed_green_blue_alpha_( 
						colorfactor * (difference ** 2.0), # red
						colorfactor * (1.0 - difference),  # green
						colorfactor * difference,          # blue
						0.67, # alpha
						)
					
					shapeSelected = selectionCounts and thisShape in Layer.selection
					shapeUnaligned = not (thisShape.automaticAlignment and thisShape.isAligned() == 2)
					
					if shapeSelected:
						componentColor.highlightWithLevel_(0.33).set()
					else:
						componentColor.set()
					componentArea.fill()
					
					# draw contour if selected or unaligned:
					if shapeSelected or shapeUnaligned:
						if shapeSelected and currentlyEditing:
							#componentColor.colorWithAlphaComponent_(1.0).set()
							componentArea.setLineWidth_(3.0/self.getScale()**0.9)
						else:
							componentColor.colorWithAlphaComponent_(0.8).set()
							componentArea.setLineWidth_(2.0/self.getScale()**0.9)
						if shapeUnaligned:
							componentArea.setLineDash_count_phase_((4/self.getScale()**0.9,3/self.getScale()**0.9),2,0.0)
						componentArea.setLineJoinStyle_(NSRoundLineJoinStyle)
						componentArea.stroke()
				else:
					# GLYPHS 3
					pathBezier.appendBezierPath_(thisShape.bezierPath)

			# GLYPHS 2:
			if Glyphs.versionNumber < 3.0:
				for thisPath in Layer.paths:
					pathBezier.appendBezierPath_(thisPath.bezierPath)
					
			NSColor.textColor().colorWithAlphaComponent_(0.25).set()
			pathBezier.fill()
	
	def needsExtraMainOutlineDrawingForInactiveLayer_(self, layer):
		if layer.components:
			return False
		else:
			return True
	
	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
