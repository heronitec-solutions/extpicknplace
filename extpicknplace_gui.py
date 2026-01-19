# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

import gettext
_ = gettext.gettext

###########################################################################
## Class ExtPicknPlaceGUI
###########################################################################

class ExtPicknPlaceGUI ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Generate Extended Placement Files"), pos = wx.DefaultPosition, size = wx.Size( 699,602 ), style = wx.DEFAULT_FRAME_STYLE|wx.STAY_ON_TOP|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        bSizer7 = wx.BoxSizer( wx.VERTICAL )

        bSizer8 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, _(u"Output directory:"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )

        bSizer8.Add( self.m_staticText1, 0, wx.ALL, 5 )

        self.m_pickOutDir = wx.DirPickerCtrl( self, wx.ID_ANY, wx.EmptyString, _(u"Select a folder"), wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
        bSizer8.Add( self.m_pickOutDir, 1, wx.EXPAND|wx.ALL, 5 )


        bSizer7.Add( bSizer8, 0, wx.EXPAND, 5 )

        bSizer71 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer61 = wx.BoxSizer( wx.VERTICAL )

        fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizer1.SetFlexibleDirection( wx.BOTH )
        fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, _(u"Format:"), wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
        self.m_staticText2.Wrap( -1 )

        fgSizer1.Add( self.m_staticText2, 0, wx.ALL, 5 )

        m_selFormatChoices = [ _(u"Plain text"), _(u"CSV"), _(u"Gerber X3") ]
        self.m_selFormat = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 250,-1 ), m_selFormatChoices, 0 )
        self.m_selFormat.SetSelection( 0 )
        fgSizer1.Add( self.m_selFormat, 0, wx.ALL, 5 )

        self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, _(u"Units:"), wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
        self.m_staticText3.Wrap( -1 )

        fgSizer1.Add( self.m_staticText3, 0, wx.ALL, 5 )

        m_selUnitsChoices = [ _(u"Inches"), _(u"Millimeters") ]
        self.m_selUnits = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 250,-1 ), m_selUnitsChoices, 0 )
        self.m_selUnits.SetSelection( 0 )
        fgSizer1.Add( self.m_selUnits, 0, wx.ALL, 5 )

        self.m_staticText51 = wx.StaticText( self, wx.ID_ANY, _(u"Use as Value:"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText51.Wrap( -1 )

        fgSizer1.Add( self.m_staticText51, 0, wx.ALL, 5 )

        m_selValueFieldChoices = []
        self.m_selValueField = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 250,-1 ), m_selValueFieldChoices, 0 )
        self.m_selValueField.SetSelection( 0 )
        fgSizer1.Add( self.m_selValueField, 0, wx.ALL, 5 )


        bSizer61.Add( fgSizer1, 0, wx.EXPAND, 5 )

        self.m_checkOnlySMD = wx.CheckBox( self, wx.ID_ANY, _(u"Include only SMD footprints"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer61.Add( self.m_checkOnlySMD, 0, wx.ALL, 5 )

        self.m_checkNoTH = wx.CheckBox( self, wx.ID_ANY, _(u"Exclude all footprints with through hole pads"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer61.Add( self.m_checkNoTH, 0, wx.ALL, 5 )

        self.m_checkDNP = wx.CheckBox( self, wx.ID_ANY, _(u"Exclude all footprints with the Do Not Popuplate flag set"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer61.Add( self.m_checkDNP, 0, wx.ALL, 5 )

        self.m_checkEdgeLayer = wx.CheckBox( self, wx.ID_ANY, _(u"Include board edge layer"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer61.Add( self.m_checkEdgeLayer, 0, wx.ALL, 5 )

        self.m_checkOrigin = wx.CheckBox( self, wx.ID_ANY, _(u"Use drill/place file origin"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer61.Add( self.m_checkOrigin, 0, wx.ALL, 5 )

        self.m_checkNegXCord = wx.CheckBox( self, wx.ID_ANY, _(u"Use negative X coordinates for footprints on bottom layer"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer61.Add( self.m_checkNegXCord, 0, wx.ALL, 5 )

        self.m_checkSingleFile = wx.CheckBox( self, wx.ID_ANY, _(u"Generate single file with both front and back positions"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer61.Add( self.m_checkSingleFile, 0, wx.ALL, 5 )


        bSizer61.Add( ( 0, 20), 0, wx.EXPAND, 5 )


        bSizer71.Add( bSizer61, 1, wx.EXPAND, 5 )


        bSizer71.Add( ( 50, 0), 0, wx.EXPAND, 5 )

        bSizer81 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, _(u"Additional Fields:"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText6.Wrap( -1 )

        bSizer81.Add( self.m_staticText6, 0, wx.TOP|wx.BOTTOM|wx.RIGHT, 5 )

        m_selAddFieldsChoices = []
        self.m_selAddFields = wx.CheckListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_selAddFieldsChoices, 0 )
        bSizer81.Add( self.m_selAddFields, 1, wx.ALL|wx.EXPAND, 0 )


        bSizer81.Add( ( 0, 20), 0, wx.EXPAND, 0 )


        bSizer71.Add( bSizer81, 1, wx.EXPAND, 0 )


        bSizer7.Add( bSizer71, 1, wx.EXPAND, 5 )

        sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _(u"Output Messages") ), wx.VERTICAL )

        self.m_tcLog = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_READONLY )
        sbSizer1.Add( self.m_tcLog, 1, wx.ALL|wx.EXPAND, 5 )


        bSizer7.Add( sbSizer1, 1, wx.EXPAND, 5 )

        bSizer5 = wx.BoxSizer( wx.HORIZONTAL )


        bSizer5.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_btGenOutput = wx.Button( self, wx.ID_ANY, _(u"Generate Position File"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer5.Add( self.m_btGenOutput, 0, wx.ALL, 5 )

        self.m_btClose = wx.Button( self, wx.ID_ANY, _(u"Close"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer5.Add( self.m_btClose, 0, wx.ALL, 5 )


        bSizer7.Add( bSizer5, 0, wx.EXPAND, 5 )


        bSizer1.Add( bSizer7, 1, wx.EXPAND|wx.ALL, 5 )


        self.SetSizer( bSizer1 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.m_selFormat.Bind( wx.EVT_CHOICE, self.m_selFormatOnChoice )
        self.m_btGenOutput.Bind( wx.EVT_LEFT_UP, self.m_btGenOutputOnLeftUp )
        self.m_btClose.Bind( wx.EVT_LEFT_UP, self.m_btCloseOnLeftUp )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def m_selFormatOnChoice( self, event ):
        event.Skip()

    def m_btGenOutputOnLeftUp( self, event ):
        event.Skip()

    def m_btCloseOnLeftUp( self, event ):
        event.Skip()


