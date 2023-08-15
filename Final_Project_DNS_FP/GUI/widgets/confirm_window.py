class ConfirmDeatilsWindow:
    COLUMNS = ('title', 'selction', 'more')
    def __init__(self, tester, site, dns_servers, domain_names, session_name):
        self.tester = tester
        self.site = site
        self.dns_servers = dns_servers
        self.domain_names = domain_names
        self.session_name = session_name

        # for k in self.__dict__.keys():
        #     print(k)
        print(list(self.__dict__))

    def get_as_table_data(self):
        '''
        the function makes from the details the data in the format of the table that tkinter wants
        :return: tuple[2]: (columns, the whole data as list of tuples)
        '''
        col_len = len(self.COLUMNS)
        lines = []
        for arg in self.__dict__:
            val = self.__getattribute__(arg)        # get the value of the field
            title = arg.replace('_', ' ').title()     # replace the '_' with space for title presentation

            try:
                assert not isinstance(val, str)
                val = tuple(val)
            except:
                val = (val,)        # if not iterable type then make it as tuple with simple value
            # append a tuple of the title (singel), and the rest of the val.
            # after that make sure that there is no more than the columns amount
            curr_line = ((title,) + val)[:col_len]
            # fill the tuple to the size of the amount of the columns
            # *note* if the amount is non-positive nothing will be added
            curr_line += ('',)*(col_len - len(curr_line))
            # add the line to the list of lines
            lines += [curr_line]
        return tuple(self.COLUMNS), lines



a = (1,2,3,4,5)
a += ('',)*(3-len(a))
print(a[:3])
a = (1,2,3)
a = tuple(a)

print(a[1])
# a[1] = 3
# print(a[1])
