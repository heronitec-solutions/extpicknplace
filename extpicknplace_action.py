import os
import json
import subprocess
import csv
from io import StringIO
from datetime import datetime

import wx
import wx.lib.agw.persist.persistencemanager as PM
import pcbnew

from pathlib import Path


if __name__ == '__main__':
    import extpicknplace_gui
else:
    from . import extpicknplace_gui

class ExtPicknPlace(pcbnew.ActionPlugin):
    def defaults(self):
        self.version = ""
        self.metadata_file = os.path.join(os.path.dirname(__file__), 'metadata.json')
        with open(self.metadata_file, 'r') as f:
            data = json.load(f)
            self.version = data['versions'][0]['version']

        self.name = data['name']
        self.category = "Exporting extended pick and plcae data"
        self.description = data['description']
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'extpicknplace_24x24.png')

    def Run(self):
        self.frame = wx.FindWindowByName("PcbFrame")
        dlg = ExtPicknPlaceDialog(self.frame, self.version)
        dlg.SetIcon( wx.Icon(self.icon_file_name) )
        dlg.SetTitle( self.name + " v"+self.version )
        dlg.Show()


class ExtPicknPlaceDialog ( extpicknplace_gui.ExtPicknPlaceGUI ):
    def __init__(self, parent, version):
        extpicknplace_gui.ExtPicknPlaceGUI.__init__(self, parent)

        self.KICAD_VERSION = int(pcbnew.Version().split(".")[0])  
        self.version = version
        
        board = pcbnew.GetBoard()
        pcb_path = board.GetFileName()
        self.project_dir = os.path.dirname(pcb_path)
        self.settings_file = Path(self.project_dir, "extpicknplace_settings.json")
        
        # set start values
        self.m_selFormat.SetSelection(0)   
        self.m_selUnits.SetSelection(1)
        
        self.m_checkOrigin.SetValue(True)
        self.m_checkEdgeLayer.Enable(False)
        
        self.m_pickOutDir.SetPath(self.project_dir)
        
        self.field_names = self.__getFieldNames__()
        self.field_names.remove("Reference")
        self.field_names.remove("Sim.Pins")
        
        self.m_selAddFields.InsertItems(sorted(self.field_names), 0)
            
        self.m_selValueField.Append(sorted(self.field_names))
        value_int = self.m_selValueField.FindString("Value")
        self.m_selValueField.SetSelection(value_int)
        
        # check if settings file exists
        if self.settings_file.is_file():
            self.__loadSettings__()
        
            
    def m_btGenOutputOnLeftUp(self, event):
        
        if self.m_selFormat.GetSelection() == 2:
            # gerber output
            self.__exportGerber__()
        else:
            # plain text and csv output
            if self.m_selValueField.GetStringSelection() == "Value":
                checked_indices = self.m_selAddFields.GetCheckedItems()
                if len(checked_indices) == 0:
                    self.__exportPlainCSV__()
                else:
                    self.__exportModified__()
            else:
                self.__exportModified__()
                
                
        self.m_tcLog.AppendText("Done.\n")   
        
        self.__saveSettings__()
        
        event.Skip()
        
        
    def __exportGerber__(self):
        board = pcbnew.GetBoard()
        
        project_name = os.path.splitext(os.path.basename(board.GetFileName()))[0]
        
        pcb_filename = board.GetFileName()
            
        file_name_top = project_name + "-pnp_top.gbr"    
        cmd = [
            "kicad-cli", "pcb", "export", "pos",
            "--format", "gerber",
            "--side", "front",
            "--output", os.path.abspath(Path(self.m_pickOutDir.GetPath(), file_name_top)),
            os.path.abspath(pcb_filename),
        ]
        if self.m_checkDNP.GetValue():
            cmd.append("--exclude-dnp")
            
        if self.m_checkEdgeLayer.GetValue():
            cmd.append("--gerber-board-edge")
            
        if self.m_checkOrigin.GetValue():
            cmd.append("--use-drill-origin")
            
        subprocess.run(cmd, check=True)
        
        exporterTop = pcbnew.PLACE_FILE_EXPORTER(
            board,
            True,    # is mm?
            False,
            False,
            self.m_checkDNP.GetValue(),
            True,
            False,
            True,   # is csv?            
            self.m_checkOrigin.GetValue(),
            False
        )
        exporterTop.GenPositionData()
        
        self.m_tcLog.AppendText("Front (top side) placement file: '" + os.path.abspath(Path(self.m_pickOutDir.GetPath(), file_name_top)) + "'.\n")
        self.m_tcLog.AppendText("Component count: " + str(exporterTop.GetFootprintCount()) + ".\n")
        
        file_name_bottom = project_name + "-pnp_bottom.gbr"    
        cmd = [
            "kicad-cli", "pcb", "export", "pos",
            "--format", "gerber",
            "--side", "back",
            "--output", os.path.abspath(Path(self.m_pickOutDir.GetPath(), file_name_bottom)),
            os.path.abspath(pcb_filename),
        ]
        if self.m_checkDNP.GetValue():
            cmd.append("--exclude-dnp")
            
        if self.m_checkEdgeLayer.GetValue():
            cmd.append("--gerber-board-edge")
            
        if self.m_checkOrigin.GetValue():
            cmd.append("--use-drill-origin")
            
        subprocess.run(cmd, check=True)
        
        exporterBottom = pcbnew.PLACE_FILE_EXPORTER(
            board,
            True,    # is mm?
            False,
            False,
            self.m_checkDNP.GetValue(),
            False,
            True,
            True,   # is csv?            
            self.m_checkOrigin.GetValue(),
            False
        )
        exporterBottom.GenPositionData()
        
        self.m_tcLog.AppendText("Back (bottom side) placement file: '" + os.path.abspath(Path(self.m_pickOutDir.GetPath(), file_name_bottom)) + "'.\n")
        self.m_tcLog.AppendText("Component count: " + str(exporterBottom.GetFootprintCount()) + ".\n")
        self.m_tcLog.AppendText("Full component count: " + str(exporterTop.GetFootprintCount() + exporterBottom.GetFootprintCount()) + ".\n")
        
        
    def __exportPlainCSV__(self):
        board = pcbnew.GetBoard()
        
        project_name = os.path.splitext(os.path.basename(board.GetFileName()))[0]
        
        if self.m_checkSingleFile.GetValue():
            exporter = pcbnew.PLACE_FILE_EXPORTER(
                board,
                self.m_selUnits.GetSelection() == 1,    # is mm?
                self.m_checkOnlySMD.GetValue(),
                self.m_checkNoTH.GetValue(),
                self.m_checkDNP.GetValue(),
                True,
                True,
                self.m_selFormat.GetSelection() == 1,   # is csv?            
                self.m_checkOrigin.GetValue(),
                self.m_checkNegXCord.GetValue()
            )     
            
            pos_data = exporter.GenPositionData()
            file_name = project_name + "-all"
            if self.m_selFormat.GetSelection() == 0:
                file_name = file_name + ".pos"
            elif self.m_selFormat.GetSelection() == 1:
                file_name = file_name + "-pos.csv"               
                
            Path(self.m_pickOutDir.GetPath(), file_name).write_text(pos_data, encoding="utf-8")      
            
            self.m_tcLog.AppendText("Placement file: '" + os.path.abspath(Path(self.m_pickOutDir.GetPath(), file_name)) + "'.\n")
            self.m_tcLog.AppendText("Component count: " + str(exporter.GetFootprintCount()) + ".\n")
        else:
            exporterTop = pcbnew.PLACE_FILE_EXPORTER(
                board,
                self.m_selUnits.GetSelection() == 1,    # is mm?
                self.m_checkOnlySMD.GetValue(),
                self.m_checkNoTH.GetValue(),
                self.m_checkDNP.GetValue(),
                True,
                False,
                self.m_selFormat.GetSelection() == 1,   # is csv?            
                self.m_checkOrigin.GetValue(),
                self.m_checkNegXCord.GetValue()
            )
            
            pos_data_top = exporterTop.GenPositionData()
            file_name_top = project_name + "-" + exporterTop.GetFrontSideName()
            if self.m_selFormat.GetSelection() == 0:
                file_name_top = file_name_top + ".pos"
            elif self.m_selFormat.GetSelection() == 1:
                file_name_top = file_name_top + "-pos.csv"
            else:
                file_name_top = project_name + "-pnp_" + exporterTop.GetFrontSideName() + ".gbr"               
                
            Path(self.m_pickOutDir.GetPath(), file_name_top).write_text(pos_data_top, encoding="utf-8")
            
            self.m_tcLog.AppendText("Front (top side) placement file: '" + os.path.abspath(Path(self.m_pickOutDir.GetPath(), file_name_top)) + "'.\n")
            self.m_tcLog.AppendText("Component count: " + str(exporterTop.GetFootprintCount()) + ".\n")
            
            exporterBottom = pcbnew.PLACE_FILE_EXPORTER(
                board,
                self.m_selUnits.GetSelection() == 1,    # is mm?
                self.m_checkOnlySMD.GetValue(),
                self.m_checkNoTH.GetValue(),
                self.m_checkDNP.GetValue(),
                False,
                True,
                self.m_selFormat.GetSelection() == 1,   # is csv?            
                self.m_checkOrigin.GetValue(),
                self.m_checkNegXCord.GetValue()
            )
            
            pos_data_bottom = exporterBottom.GenPositionData()
            file_name_bottom = project_name + "-" + exporterBottom.GetBackSideName()
            if self.m_selFormat.GetSelection() == 0:
                file_name_bottom = file_name_bottom + ".pos"
            elif self.m_selFormat.GetSelection() == 1:
                file_name_bottom = file_name_bottom + "-pos.csv"
            else:
                file_name_bottom = project_name + "-pnp_" + exporterBottom.GetBackSideName() + ".gbr"               
                
            Path(self.m_pickOutDir.GetPath(), file_name_bottom).write_text(pos_data_bottom, encoding="utf-8")
            
            self.m_tcLog.AppendText("Back (bottom side) placement file: '" + os.path.abspath(Path(self.m_pickOutDir.GetPath(), file_name_bottom)) + "'.\n")
            self.m_tcLog.AppendText("Component count: " + str(exporterBottom.GetFootprintCount()) + ".\n")
            fcnt = exporterTop.GetFootprintCount() + exporterBottom.GetFootprintCount()
            self.m_tcLog.AppendText("Full component count: " + str(fcnt) + ".\n")
        
    
    def __exportModified__(self):
        comp_data = self.__getComponentData__()
        
        board = pcbnew.GetBoard()
        
        project_name = os.path.splitext(os.path.basename(board.GetFileName()))[0]
        
        if self.m_checkSingleFile.GetValue():
            exporter = pcbnew.PLACE_FILE_EXPORTER(
                board,
                self.m_selUnits.GetSelection() == 1,    # is mm?
                self.m_checkOnlySMD.GetValue(),
                self.m_checkNoTH.GetValue(),
                self.m_checkDNP.GetValue(),
                True,
                True,
                True,   # allways csv
                self.m_checkOrigin.GetValue(),
                self.m_checkNegXCord.GetValue()
            )     
            
            pos_data = exporter.GenPositionData()
            pos_data = self.__parseCsv__(pos_data)
            pos_data = self.__modifyDictData__(pos_data, comp_data)
            file_name = project_name + "-all"
            if self.m_selFormat.GetSelection() == 0:
                file_name = file_name + ".pos"
                self.__writePlainTextFile__(pos_data, Path(self.m_pickOutDir.GetPath(), file_name), "All", self.m_selUnits.GetSelection() == 1) 
            elif self.m_selFormat.GetSelection() == 1:
                file_name = file_name + "-pos.csv"          
                fieldnames = pos_data[0].keys()   
                with open(os.path.abspath(Path(self.m_pickOutDir.GetPath(), file_name)), "w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
                    writer.writeheader()
                    writer.writerows(pos_data)                                 
            
            self.m_tcLog.AppendText("Placement file: '" + os.path.abspath(Path(self.m_pickOutDir.GetPath(), file_name)) + "'.\n")
            self.m_tcLog.AppendText("Component count: " + str(exporter.GetFootprintCount()) + ".\n")
        else:
            exporterTop = pcbnew.PLACE_FILE_EXPORTER(
                board,
                self.m_selUnits.GetSelection() == 1,    # is mm?
                self.m_checkOnlySMD.GetValue(),
                self.m_checkNoTH.GetValue(),
                self.m_checkDNP.GetValue(),
                True,
                False,
                self.m_selFormat.GetSelection() == 1,   # is csv?            
                self.m_checkOrigin.GetValue(),
                self.m_checkNegXCord.GetValue()
            )
            
            pos_data_top = exporterTop.GenPositionData()
            pos_data_top = self.__parseCsv__(pos_data_top)
            pos_data_top = self.__modifyDictData__(pos_data_top, comp_data)
            file_name_top = project_name + "-" + exporterTop.GetFrontSideName()
            if self.m_selFormat.GetSelection() == 0:
                file_name_top = file_name_top + ".pos"
                self.__writePlainTextFile__(pos_data_top, Path(self.m_pickOutDir.GetPath(), file_name_top), "top", self.m_selUnits.GetSelection() == 1) 
            elif self.m_selFormat.GetSelection() == 1:
                file_name_top = file_name_top + "-pos.csv"                           
                fieldnames = pos_data_top[0].keys()   
                with open(os.path.abspath(Path(self.m_pickOutDir.GetPath(), file_name_top)), "w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
                    writer.writeheader()
                    writer.writerows(pos_data_top)              
            
            self.m_tcLog.AppendText("Front (top side) placement file: '" + os.path.abspath(Path(self.m_pickOutDir.GetPath(), file_name_top)) + "'.\n")
            self.m_tcLog.AppendText("Component count: " + str(exporterTop.GetFootprintCount()) + ".\n")
            
            exporterBottom = pcbnew.PLACE_FILE_EXPORTER(
                board,
                self.m_selUnits.GetSelection() == 1,    # is mm?
                self.m_checkOnlySMD.GetValue(),
                self.m_checkNoTH.GetValue(),
                self.m_checkDNP.GetValue(),
                False,
                True,
                self.m_selFormat.GetSelection() == 1,   # is csv?            
                self.m_checkOrigin.GetValue(),
                self.m_checkNegXCord.GetValue()
            )
            
            pos_data_bottom = exporterBottom.GenPositionData()
            pos_data_bottom = self.__parseCsv__(pos_data_bottom)
            pos_data_bottom = self.__modifyDictData__(pos_data_bottom, comp_data)
            file_name_bottom = project_name + "-" + exporterBottom.GetBackSideName()
            if self.m_selFormat.GetSelection() == 0:
                file_name_bottom = file_name_bottom + ".pos"
                self.__writePlainTextFile__(pos_data_bottom, Path(self.m_pickOutDir.GetPath(), file_name_bottom), "bottom", self.m_selUnits.GetSelection() == 1)
            elif self.m_selFormat.GetSelection() == 1:
                file_name_bottom = file_name_bottom + "-pos.csv"     
                fieldnames = pos_data_bottom[0].keys()
                with open(os.path.abspath(Path(self.m_pickOutDir.GetPath(), file_name_bottom)), "w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
                    writer.writeheader()
                    writer.writerows(pos_data_bottom)           
                
            
            self.m_tcLog.AppendText("Back (bottom side) placement file: '" + os.path.abspath(Path(self.m_pickOutDir.GetPath(), file_name_bottom)) + "'.\n")
            self.m_tcLog.AppendText("Component count: " + str(exporterBottom.GetFootprintCount()) + ".\n")
            fcnt = exporterTop.GetFootprintCount() + exporterBottom.GetFootprintCount()
            self.m_tcLog.AppendText("Full component count: " + str(fcnt) + ".\n")
        
        
    def __parseCsv__(self, csv_string):
        reader = csv.DictReader(StringIO(csv_string))
        
        rows = []
        for row in reader:
            row["PosX"] = float(row["PosX"])
            row["PosY"] = float(row["PosY"])
            row["Rot"] = float(row["Rot"])
            rows.append(row)
        
        return rows       
    
    
    def __modifyDictData__(self, dict_data, comp_data):
        checked_indices = self.m_selAddFields.GetCheckedItems()
        checked_items = [
            self.m_selAddFields.GetString(i)
            for i in checked_indices
        ]
        
        for row in dict_data:
            ref = row.get("Ref")
            
            #raise Exception(comp_data) 

            # replace Value field
            sel_value_field = self.m_selValueField.GetStringSelection()
            if sel_value_field != "Value":
                if ref in comp_data:
                    row["Val"] = comp_data[ref][sel_value_field]        
            
            # add additional fields            
            if len(checked_items) > 0:
                for item in checked_items:
                    if item is None:
                        continue
                    row[item] = comp_data[ref][item]
         
        return dict_data
    
    
    def __writePlainTextFile__(self, dict_data, file_path, side, isMM):
        
        with open(os.path.abspath(file_path), "w", encoding="utf-8") as f:
            # write header
            f.write("### Extended footprint positions - created on " + datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z") + " ###\n")
            f.write("### Printed by KiCad version " + pcbnew.Version() +" and ExtPicknPlace plugin version " + self.version + "\n")
            f.write("## Unit = ")
            if isMM:
                f.write("mm")
            else:
                f.write("inches")
            f.write(", Angle = deg.\n")
            f.write("## Side : " + side + "\n")
            
            column_names = dict_data[0].keys()       
            
            # Define which columns are numeric and how they should be formatted
            NUMERIC_FORMAT = {
                "PosX": "{:.4f}",
                "PosY": "{:.4f}",
                "Rot":  "{:.4f}",
            }                
            numeric_cols = set(NUMERIC_FORMAT)
            
            def display_value(col: str, raw: str) -> str:
                if raw is None:
                    return ""
                s = str(raw)
                if col in NUMERIC_FORMAT:
                    return NUMERIC_FORMAT[col].format(float(s)) if s.strip() else ""
                return s             

            # Compute max width for each column (consider header + all rows)
            column_width = {c: len(c) for c in column_names}        
            for row in dict_data:
                for c in column_names:
                    column_width[c] = max(column_width[c], len(display_value(c, row.get(c, ""))))
                    
            
            for c in column_names:
                column_width[c] += 2     
                
            column_width_header = column_width.copy()
            column_width["Ref"] += 2   # correction for Ref column
              
            # Print header
            f.write("# " + "  ".join(
                f"{c:>{column_width_header[c]}}" if c in numeric_cols else f"{c:<{column_width_header[c]}}"
                for c in column_names
            ) + "\n")      
            
            # Print rows
            for row in dict_data:
                f.write("  ".join(
                    f"{display_value(c, row.get(c, '')):>{column_width[c]}}" if c in numeric_cols
                    else f"{display_value(c, row.get(c, '')):<{column_width[c]}}"
                    for c in column_names
                ) + "\n")    
                                    
            
            # write end
            f.write("## End\n")
            
        
    def m_btCloseOnLeftUp(self, event):
        self.Close()   
        
        
    def m_selFormatOnChoice(self, event):
        self.__enableCheckBoxes__()
        
        
    def __enableCheckBoxes__(self):
        if self.m_selFormat.GetSelection() == 2:
            # Gerber C3 selected
            self.m_checkOnlySMD.Enable(False)
            self.m_checkNoTH.Enable(False)
            self.m_checkEdgeLayer.Enable(True)
            self.m_checkNegXCord.Enable(False)
            self.m_checkSingleFile.Enable(False)
            
            self.m_selValueField.Enable(False)
            self.m_selAddFields.Enable(False)
        else:
            # Plain text or CSV selected
            self.m_checkOnlySMD.Enable(True)
            self.m_checkNoTH.Enable(True)
            self.m_checkEdgeLayer.Enable(False)
            self.m_checkNegXCord.Enable(True)
            self.m_checkSingleFile.Enable(True)
            
            self.m_selValueField.Enable(True)
            self.m_selAddFields.Enable(True)
                    
        
    def __getFieldNames__(self):
        field_names = set()
        
        board = pcbnew.GetBoard()
        footprints = board.GetFootprints()

        for fp in footprints:
            field_names.update(fp.GetFieldsText().keys())

        return field_names
    
    
    def __getComponentData__(self):
        board = pcbnew.GetBoard()
        footprints = board.GetFootprints()

        field_names = self.__getFieldNames__()
            
        data = {}

        for fp in footprints:
            ref = fp.GetReference()  # e.g. "C3"

            # Get this footprint's fields (dict: name -> value)
            fields = fp.GetFieldsText()

            # Initialize row with empty strings
            row = {field: "" for field in field_names}

            # Fill in existing fields
            for field_name, value in fields.items():
                row[field_name] = value

            data[ref] = row
        
        return data
        
    
    def __loadSettings__(self):
        with open(self.settings_file, 'r') as f:
            data = json.load(f)
            # load settings...
            self.m_pickOutDir.SetPath(data['output_dir'])
            self.m_selFormat.SetSelection(data['format'])  
            self.__enableCheckBoxes__() 
            self.m_selUnits.SetSelection(data['units'])
            value_int = self.m_selValueField.FindString(data['value_field'])
            self.m_selValueField.SetSelection(value_int)
            
            self.m_checkOnlySMD.SetValue(data['only_smd']),
            self.m_checkNoTH.SetValue(data['no_th']),
            self.m_checkDNP.SetValue(data['no_dnp']),
            self.m_checkEdgeLayer.SetValue(data['edge_layer']),                
            self.m_checkOrigin.SetValue(data['origin'])
            self.m_checkNegXCord.SetValue(data['neg_xcord'])
            self.m_checkSingleFile.SetValue(data['single_file'])
            
            checked_items = data.get("checked_items", [])
            for i in range(self.m_selAddFields.GetCount()):
                label = self.m_selAddFields.GetString(i)
                if label in checked_items:
                    self.m_selAddFields.Check(i, True)
        
    
    def __saveSettings__(self):
        with open(self.settings_file, 'w') as f:            
            data = {
                'output_dir': self.m_pickOutDir.GetPath(),
                'format': self.m_selFormat.GetSelection(),
                'units': self.m_selUnits.GetSelection(),
                'value_field': self.m_selValueField.GetStringSelection(),
                
                'only_smd': self.m_checkOnlySMD.GetValue(),
                'no_th': self.m_checkNoTH.GetValue(),
                'no_dnp': self.m_checkDNP.GetValue(),
                'edge_layer': self.m_checkEdgeLayer.GetValue(),
                'origin': self.m_checkOrigin.GetValue(),
                'neg_xcord': self.m_checkNegXCord.GetValue(),
                'single_file': self.m_checkSingleFile.GetValue()
            }
            
            checked_indices = self.m_selAddFields.GetCheckedItems()
            checked_items = [
                self.m_selAddFields.GetString(i)
                for i in checked_indices
            ]
            data['checked_items'] = checked_items
            
            json.dump(data, f, indent=4)
        

    
if __name__ == '__main__':
    print("Starting Pick and Place plugin...")
    app = wx.App(False)
    plg = ExtPicknPlace()
    plg.defaults()
    plg.Run()
    app.MainLoop()