import wx
import os
import json
import pyperclip


# Function: Loads the Client list from JSON file
def load_client_items():
    with open("data.json", "r") as file:
        data = json.load(file)
        return data["SYDFILESVM02_clients"]


# Function: Loads the Business units from JSON file (Commonwealth Bank only)
def load_business_units():
    with open("data.json", "r") as file:
        data = json.load(file)
        return data["business units"]


# Function: Checks if the there are at least one Sub Folder selected
def check_sub_folders(sub_folders):
    if len(sub_folders) == 0:
        wx.MessageBox("Please select at least one Job Type", "Error", wx.OK | wx.ICON_ERROR)
        return False
    else:
        return True


def max_char_check(folder):
    if len(folder) >= 254:
        wx.MessageBox("Job number and/or description too long\n(254 Characters max)", "Error", wx.OK | wx.ICON_ERROR)
        return False
    else:
        return True


class AppFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(AppFrame, self).__init__(*args, **kw)

        # Adding components to App Frame
        self.result_label = None
        self.business_unit_dropdown = None
        self.copy_button = None
        self.result_text = None
        self.tv_checkbox = None
        self.studio_checkbox = None
        self.jobbags_checkbox = None
        self.digital_checkbox = None
        self.design_checkbox = None
        self.select_all_checkbox = None
        self.description_entry = None
        self.job_number_entry = None
        self.client_dropdown = None
        self.campaign_dropdown = None
        self.init_ui()

    # Initialise the GUI
    def init_ui(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Apply modern font and color
        modern_font_large = wx.Font(20, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        modern_font_small = wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        panel.SetBackgroundColour("#5A5A5A")  # Dark gray background

        # Header
        header_label = wx.StaticText(panel, label="Create Folder Structure")
        header_label.SetFont(modern_font_large)
        header_label.SetForegroundColour("#ffffff")  # Dark text color
        vbox.Add(header_label, flag=wx.LEFT | wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=15)

        business_unit_label = wx.StaticText(panel, label="Business Unit:")
        business_unit_label.SetFont(modern_font_small)
        vbox.Add(business_unit_label, flag=wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        units = load_business_units()
        self.business_unit_dropdown = wx.ComboBox(panel, choices=units, value=" ", style=wx.CB_READONLY)
        self.business_unit_dropdown.SetFont(modern_font_small)
        vbox.Add(self.business_unit_dropdown, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        self.business_unit_dropdown.Disable()

        # Client: Label and Dropdown
        client_label = wx.StaticText(panel, label="Client:")
        client_label.SetFont(modern_font_small)
        vbox.Add(client_label, flag=wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        clients = load_client_items()
        self.client_dropdown = wx.ComboBox(panel, choices=clients, style=wx.CB_READONLY)
        self.client_dropdown.SetFont(modern_font_small)
        vbox.Add(self.client_dropdown, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        self.client_dropdown.Bind(wx.EVT_COMBOBOX, self.business_unit_enable)

        # Business Unit: Label and Dropdown
        business_unit_label = wx.StaticText(panel, label="Business Unit:")
        business_unit_label.SetFont(modern_font_small)
        vbox.Add(business_unit_label, flag=wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        units = load_business_units()
        self.business_unit_dropdown = wx.ComboBox(panel, choices=units, value=" ", style=wx.CB_READONLY)
        self.business_unit_dropdown.SetFont(modern_font_small)
        vbox.Add(self.business_unit_dropdown, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        self.business_unit_dropdown.Disable()

        # Campaign: Label and Dropdown
        campaign_dropdown = wx.StaticText(panel, label="Campaign:")
        campaign_dropdown.SetFont(modern_font_small)
        vbox.Add(campaign_dropdown, flag=wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        self.campaign_dropdown = wx.ComboBox(panel, choices=["New Campaign"], style=wx.CB_READONLY)
        self.campaign_dropdown.SetFont(modern_font_small)
        vbox.Add(self.campaign_dropdown, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        self.campaign_dropdown.SetSelection(0)

        vbox.Add((10, 10))

        # Campaign: Update/Refresh Button
        update_button = wx.Button(panel, label="Update Campaigns")
        update_button.SetFont(modern_font_small)
        update_button.Bind(wx.EVT_BUTTON, self.update_campaign_list)
        vbox.Add(update_button, flag=wx.LEFT | wx.ALIGN_RIGHT, border=10)

        # Job Number: Label and Text Entry Field
        job_number_label = wx.StaticText(panel, label="Job Number:")
        job_number_label.SetFont(modern_font_small)
        vbox.Add(job_number_label, flag=wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        self.job_number_entry = wx.TextCtrl(panel)
        self.job_number_entry.SetFont(modern_font_small)
        vbox.Add(self.job_number_entry, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        # Description: Label and Text Entry Field
        description_label = wx.StaticText(panel, label="Description:")
        description_label.SetFont(modern_font_small)
        vbox.Add(description_label, flag=wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        self.description_entry = wx.TextCtrl(panel)
        self.description_entry.SetFont(modern_font_small)
        vbox.Add(self.description_entry, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        # Checkboxes: Label
        checkbox_header = wx.StaticText(panel, label="Required Sub-Folders:")
        checkbox_header.SetFont(modern_font_small)
        vbox.Add(checkbox_header, flag=wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # CheckBoxes: UI container
        checkboxes_hbox = wx.BoxSizer(wx.HORIZONTAL)

        # Checkboxes: Left spacer (column)
        check_vbox1 = wx.BoxSizer(wx.VERTICAL)
        self.select_all_checkbox = wx.CheckBox(panel, label='Select All')
        self.select_all_checkbox.SetFont(modern_font_small)
        check_vbox1.Add(self.select_all_checkbox, flag=wx.LEFT | wx.TOP, border=10)
        self.design_checkbox = wx.CheckBox(panel, label='Design')
        self.design_checkbox.SetFont(modern_font_small)
        check_vbox1.Add(self.design_checkbox, flag=wx.LEFT | wx.TOP, border=10)
        self.digital_checkbox = wx.CheckBox(panel, label='Digital')
        self.digital_checkbox.SetFont(modern_font_small)
        check_vbox1.Add(self.digital_checkbox, flag=wx.LEFT | wx.TOP, border=10)

        # Checkboxes: Right spacer (column)
        check_vbox2 = wx.BoxSizer(wx.VERTICAL)
        self.jobbags_checkbox = wx.CheckBox(panel, label='JobBags')
        self.jobbags_checkbox.SetFont(modern_font_small)
        check_vbox2.Add(self.jobbags_checkbox, flag=wx.LEFT | wx.TOP, border=10)
        self.studio_checkbox = wx.CheckBox(panel, label='Studio')
        self.studio_checkbox.SetFont(modern_font_small)
        check_vbox2.Add(self.studio_checkbox, flag=wx.LEFT | wx.TOP, border=10)
        self.tv_checkbox = wx.CheckBox(panel, label='TV')
        self.tv_checkbox.SetFont(modern_font_small)
        check_vbox2.Add(self.tv_checkbox, flag=wx.LEFT | wx.TOP, border=10)

        # Checkboxes: Add Left and Right spacers to container
        checkboxes_hbox.Add(check_vbox1, flag=wx.RIGHT, border=30)
        checkboxes_hbox.Add(check_vbox2)
        vbox.Add(checkboxes_hbox, flag=wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # Checkboxes: Bind checkbox to event handler
        self.design_checkbox.Bind(wx.EVT_CHECKBOX, self.on_checkbox_change)
        self.digital_checkbox.Bind(wx.EVT_CHECKBOX, self.on_checkbox_change)
        self.jobbags_checkbox.Bind(wx.EVT_CHECKBOX, self.on_checkbox_change)
        self.studio_checkbox.Bind(wx.EVT_CHECKBOX, self.on_checkbox_change)
        self.tv_checkbox.Bind(wx.EVT_CHECKBOX, self.on_checkbox_change)

        # Checkboxes: Bind "Select All" to separate handler
        self.select_all_checkbox.Bind(wx.EVT_CHECKBOX, self.on_select_all)
        self.select_all_checkbox.SetValue(True)
        self.on_select_all(None)

        checkboxes_hbox.Add((100, 100))

        # Submit Button: Label and bind to event handler
        submit_button = wx.Button(panel, label="Submit")
        submit_button.SetFont(modern_font_small)
        submit_button.Bind(wx.EVT_BUTTON, self.on_submit)
        vbox.Add(submit_button, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        # Result: Label and Readonly Text Field for File Path Output
        result_label = wx.StaticText(panel, label="Result:")
        result_label.SetFont(modern_font_small)
        vbox.Add(result_label, flag=wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        self.result_text = wx.TextCtrl(panel, style=wx.TE_READONLY | wx.TE_MULTILINE)
        vbox.Add(self.result_text, flag=wx.EXPAND | wx.ALL, border=10)

        # Action Buttons: UI Container
        buttons_hbox = wx.BoxSizer(wx.HORIZONTAL)

        # Action Buttons: "Copy" button - Label and bind to event handler (Disabled by default - enabled after Submit)
        self.copy_button = wx.Button(panel, label="Copy")
        self.copy_button.Bind(wx.EVT_BUTTON, self.copy_path)
        buttons_hbox.Add(self.copy_button, flag=wx.LEFT | wx.ALIGN_LEFT, border=10)
        self.copy_button.Disable()

        # Action Buttons: Stretchable space to push the buttons apart
        buttons_hbox.AddStretchSpacer()

        # Action Buttons: "Close" button - Label and bind to event handler
        quit_button = wx.Button(panel, label="Close")
        quit_button.SetFont(modern_font_small)
        quit_button.Bind(wx.EVT_BUTTON, self.quit_button)
        buttons_hbox.Add(quit_button, border=10)

        vbox.Add(buttons_hbox, flag=wx.EXPAND | wx.ALL, border=10)

        self.result_label = wx.StaticText(panel, label="")
        self.result_label.SetFont(modern_font_small)
        vbox.Add(self.result_label, flag=wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # End of UI - Sizer
        panel.SetSizer(vbox)

    def business_unit_enable(self, event):
        choice = self.client_dropdown.GetValue()
        if choice == "COMMONWEALTH BANK":
            self.business_unit_dropdown.Enable()
            return True
        else:
            self.business_unit_dropdown.Disable()
            return False

    def business_unit_empty(self, client):
        if client == "COMMONWEALTH BANK":
            business_unit = self.business_unit_dropdown.GetValue()
            if not business_unit:
                wx.MessageBox("Commonwealth Bank selected\nBusiness Unit cannot be blank", "Error", wx.OK | wx.ICON_ERROR)
                return False
            else:
                return True
        else:
            return True

# Function
    def selected_sub_folders(self):
        sub_folders = []
        if self.design_checkbox.GetValue():
            sub_folders.append("Design")
        if self.digital_checkbox.GetValue():
            sub_folders.append("Digital")
        if self.jobbags_checkbox.GetValue():
            sub_folders.append("JobBags")
        if self.studio_checkbox.GetValue():
            sub_folders.append("Studio")
        if self.tv_checkbox.GetValue():
            sub_folders.append("TV")
        return sub_folders

    # Function: Checks if the Text entry fields are populated
    def text_entry_empty(self):
        # Retrieve values
        job_number = self.job_number_entry.GetValue()
        description = self.description_entry.GetValue()

        # 'if' statement to check entry fields
        if len(job_number) == 0:
            # Error message popup using native dialog box
            wx.MessageBox("Job Number cannot be empty", "Error", wx.OK | wx.ICON_ERROR)
            return False
        if len(description) == 0:
            # Error message popup using native dialog box
            wx.MessageBox("Description cannot be empty", "Error", wx.OK | wx.ICON_ERROR)
            return False
        else:
            return True

    # Function: Check if illegal characters used in text entry
    def illegal_char(self):
        # Retrieve values
        job_number = self.job_number_entry.GetValue()
        description = self.description_entry.GetValue()

        # List of illegal characters that will not work as a folder name
        illegal_characters = ["/", "*", "<", ">", "#", "&", "{", "}", "\\", "?", "@", "+", "'", "|", "=", "$", "!"]

        # Iterates through list to make sure there are no illegal characters in the inputted text
        for char in illegal_characters:
            if char in job_number:
                # Error message popup using native dialog box
                wx.MessageBox(f"Illegal character found in Job Number: {char}", "Error", wx.OK | wx.ICON_ERROR)
                return False
            if char in description:
                # Error message popup using native dialog box
                wx.MessageBox(f"Illegal character found in Description: {char}", "Error", wx.OK | wx.ICON_ERROR)
                return False
        return True

    # Function: Updates the "Campaign" dropdown based on the current 'Client' Selection
    def update_campaign_list(self, event):
        client = self.client_dropdown.GetValue()  # Retrieve 'Client' Selection
        business_unit = self.business_unit_dropdown.GetValue()

        if client == "COMMONWEALTH BANK":
            directory_path = f'SYDFILESVM02/Clients/{client}/{business_unit}'
        else:
            directory_path = f'SYDFILESVM02/Clients/{client}'  # Define the file path with correct client

        directories = []
        # Try and except: Attempts to list all the current folders in the path
        try:
            # List all entries in the directory
            all_entries = os.listdir(directory_path)
        except FileNotFoundError:  # This error occurs when there are no folders in the file path
            directories.insert(0, "New Campaign")
            self.campaign_dropdown.SetItems(directories)
            return  # ends the function

        # Filter out entries to keep only directories
        directories = [folder for folder in all_entries if os.path.isdir(os.path.join(directory_path, folder))]
        directories.sort()

        # Update the 'Campaign' dropdown to reflect the folders in the directory
        directories.insert(0, "New Campaign")
        self.campaign_dropdown.SetItems(directories)

    # Function: Select and Deselect the 'Select All' Checkbox based on the state of the other checkboxes
    def on_checkbox_change(self, event):
        # If any checkbox is unchecked, uncheck 'Select All'
        if not (self.design_checkbox.GetValue() and
                self.digital_checkbox.GetValue() and
                self.jobbags_checkbox.GetValue() and
                self.studio_checkbox.GetValue() and
                self.tv_checkbox.GetValue()):
            self.select_all_checkbox.SetValue(False)
        else:
            # If all checkboxes are selected, check 'Select All'
            self.select_all_checkbox.SetValue(True)

    # Function: Select all functionality - when 'Select All' is selected, check all boxes
    def on_select_all(self, event):
        value = self.select_all_checkbox.GetValue()
        self.select_all_checkbox.SetValue(value)
        self.design_checkbox.SetValue(value)
        self.digital_checkbox.SetValue(value)
        self.jobbags_checkbox.SetValue(value)
        self.studio_checkbox.SetValue(value)
        self.tv_checkbox.SetValue(value)

    # Function: 'Submit Button' functionality
    def on_submit(self, event):
        sub_folders = self.selected_sub_folders()
        client_name = self.client_dropdown.GetValue()
        business_unit = self.business_unit_dropdown.GetValue()
        job_number = self.job_number_entry.GetValue()
        campaign = self.campaign_dropdown.GetValue()
        description = self.description_entry.GetValue()
        folder_name = job_number + " - " + description

        # Ensures the fields are not empty and there are no illegal characters
        if not self.text_entry_empty():
            return
        if not self.illegal_char():
            return
        if not check_sub_folders(sub_folders):
            return
        if not max_char_check(folder_name):
            return
        if not self.business_unit_empty(client_name):
            return

        if self.business_unit_dropdown.GetValue():
            client_name = os.path.join(client_name, business_unit)
        if campaign == "New Campaign" or "":
            folder_path = os.path.join(client_name, folder_name)
        else:
            folder_path = os.path.join(client_name, campaign, folder_name)

        live_path = os.path.join("SYDFILESVM02/Clients/", folder_path)
        archive_path = os.path.join("zArchive/", folder_path)

        if not os.path.exists(live_path) and not os.path.exists(archive_path):
            for sub_folder in sub_folders:
                os.makedirs(os.path.join(live_path, sub_folder))
                os.makedirs(os.path.join(archive_path, sub_folder))
            print(f'{folder_name} has been created')
            print(f'File path live: {live_path}')
            print(f'File path Archive: {archive_path}')
        else:
            wx.MessageBox(f"{folder_name} already exists.", "Error", wx.OK | wx.ICON_ERROR)

        # Enable the 'Copy' button
        self.copy_button.Enable()
        # Set the 'Result' text box to reflect Created file path
        self.result_text.SetValue(live_path)

        # Function: Quits the Application
    def quit_button(self, event):
        print("Closed by user")
        wx.Exit()

    # Function: Copies the 'Result' Text box to Clipboard
    def copy_path(self, event):
        result = self.result_text.GetValue()
        pyperclip.copy(result)
        self.result_label.SetLabel("File path copied to clipboard")


if __name__ == '__main__':
    app = wx.App(False)
    frame = AppFrame(None, title="CFS", size=(400, 700))
    frame.Show()
    app.MainLoop()
