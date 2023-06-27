from tkinter import messagebox

from ttkwidgets.autocomplete.autocompletecombobox import AutocompleteCombobox

class ComboBoxWidget(AutocompleteCombobox):
    def __init__(self, master=None, values_selection=[], **kwargs):
        super().__init__(master, **kwargs)
        self.__set_validation_widget()
        self.__values = None
        self.set_values_selection(values_selection)

    def set_values_selection(self, selection = None):
        if type(selection) not in [list, dict]:
            self.__values = []
            raise ValueError("the selection is not list or dictionary")

        self.__values = selection.copy()
        self.configure(completevalues=selection)

    def get_selection(self):
        selected = self.get()
        return \
            self.__values[selected] if type(self.__values) is dict \
            else selected

    def __checkbox_validate(self, p_entry_value):
        return p_entry_value == '' or \
            (p_entry_value in self['completevalues'] and p_entry_value in self.__values)

    def __on_invalid(self, p_entry_value):
        messagebox.showerror('error tester name', f'{p_entry_value} is not on the list')
        self.set('')

    def __make_valid(self):
        self.configure(validatecommand=(self.register(self.__checkbox_validate), "%P"))

    def __make_invalid(self):
        self.configure(
            invalidcommand=(self.register(self.__on_invalid), "%P", '%S'))  # tring to make it short as function

    def __set_validation_widget(self):
        self.configure(validate="focusout")
        self.__make_valid()
        self.__make_invalid()
        
    def print(self):
        print(self.__values)


