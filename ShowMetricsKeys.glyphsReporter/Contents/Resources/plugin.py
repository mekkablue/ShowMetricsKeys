# encoding: utf-8

import objc
import sys, os, re, math, traceback
from GlyphsApp import *
from GlyphsApp.plugins import *

class ShowMetricsKeys (ReporterPlugin):

	def settings(self):
		self.menuName = "Metrics Keys"
	
	def foreground( self, Layer ):
		"""
		Whatever you draw here will be displayed IN FRONT OF the paths.
		Setting a color:
			NSColor.colorWithCalibratedRed_green_blue_alpha_( 1.0, 1.0, 1.0, 1.0 ).set() # sets RGBA values between 0.0 and 1.0
			NSColor.redColor().set() # predefined colors: blackColor, blueColor, brownColor, clearColor, cyanColor, darkGrayColor, grayColor, greenColor, lightGrayColor, magentaColor, orangeColor, purpleColor, redColor, whiteColor, yellowColor
		Drawing a path:
			myPath = NSBezierPath.alloc().init()  # initialize a path object myPath
			myPath.appendBezierPath_( subpath )   # add subpath to myPath
			myPath.fill()   # fill myPath with the current NSColor
			myPath.stroke() # stroke myPath with the current NSColor
		To get an NSBezierPath from a GSPath, use the bezierPath() method:
			myPath.bezierPath().fill()
		You can apply that to a full layer at once:
			if len( myLayer.paths > 0 ):
				myLayer.bezierPath()       # all closed paths
				myLayer.openBezierPath()   # all open paths
		See:
		https://developer.apple.com/library/mac/documentation/Cocoa/Reference/ApplicationKit/Classes/NSBezierPath_Class/Reference/Reference.html
		https://developer.apple.com/library/mac/documentation/cocoa/reference/applicationkit/classes/NSColor_Class/Reference/Reference.html
		"""
		try:
			thisGlyph = Layer.parent
			Font = thisGlyph.parent

			xHeight = Font.selectedFontMaster.xHeight
			angle = Font.selectedFontMaster.italicAngle
			yPos = -100
			# rotation point is half of x-height
			offset = math.tan(math.radians(angle)) * xHeight/2
			shift = math.tan(math.radians(angle)) * yPos - offset

			glyphLeftMetricsKey = thisGlyph.leftMetricsKey
			glyphRightMetricsKey = thisGlyph.rightMetricsKey
			
			layerLeftMetricsKey = Layer.leftMetricsKey()
			layerRightMetricsKey = Layer.rightMetricsKey()
			layerWidth = Layer.width + 10.0

			leftMetricsKeyString = "Glyph: '%s'\nLayer: '%s'" % ( glyphLeftMetricsKey, layerLeftMetricsKey)
			rightMetricsKeyString = "Glyph: '%s'\nLayer: '%s'" % ( glyphRightMetricsKey, layerRightMetricsKey)
			
			leftMetricsKeyString = leftMetricsKeyString.replace("'None'", "-")
			rightMetricsKeyString = rightMetricsKeyString.replace("'None'", "-")
			
			# Text Alignments:
			# top left: 6
			# top center: 7
			# top right: 8
			# center left: 3
			# center center: 4
			# center right: 5
			# bottom left: 0
			# bottom center: 1
			# bottom right: 2

			self.drawTextAtPoint( leftMetricsKeyString, NSPoint( -10.0 + shift, yPos), fontSize=9.0, textAlignment=2, fontColor=NSColor.orangeColor() )
			self.drawTextAtPoint( rightMetricsKeyString, NSPoint( layerWidth + shift, yPos), fontSize=9.0, textAlignment=0, fontColor=NSColor.orangeColor() )
		except Exception as e:
			self.logToConsole( "drawForegroundForLayer_: %s" % str(e) )
