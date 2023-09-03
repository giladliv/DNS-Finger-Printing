from tkinter import *
from tkinter import ttk

from utils.utils import *

from collections.abc import Iterable

def adjust_row_values(val: tuple, sep: str = '\n'):
    ret_row = []
    for arg in val:
        if isinstance(arg, str):
            ret_row += [arg]
            continue
        try:
            ret_row += [sep.join(arg)]
        except:
            ret_row += [str(arg)]
    return tuple(ret_row)

def table_overlook_repair(columns, lines):
    '''
    fix and set the values according to the format
    :param columns: columns headers
    :param lines: list of tuples - rows
    :return:
    '''
    return adjust_row_values(columns), \
        [adjust_row_values(line) for line in lines]

def create_table_window(columns, lines):

    # columns, lines = table_overlook_repair(columns, lines)
    print(columns, lines, sep='\n'+"*"*50+'\n')

    ws = Tk()
    ws.title('PythonGuides')
    ws.geometry('1152x768')
    # ws['bg'] = '#AC99F2'

    frame = Frame(ws)
    frame.pack(fill=BOTH, expand=True)

    # scrollbar
    frame_scroll_y = Scrollbar(frame)
    frame_scroll_y.pack(side=RIGHT, fill=Y)

    frame_scroll_x = Scrollbar(frame, orient='horizontal')
    frame_scroll_x.pack(side=BOTTOM, fill=X)

    table = ttk.Treeview(frame, yscrollcommand=frame_scroll_y.set, xscrollcommand=frame_scroll_x.set)

    table.pack(fill=BOTH, expand=True)

    frame_scroll_y.config(command=table.yview)
    frame_scroll_x.config(command=table.xview)

    #set the table data
    set_data_to_tables(table=table, columns=columns, lines=lines)
    btn = ttk.Button(ws, text='CLICK')
    btn.pack(side=TOP)

    ws.mainloop()

# define our column

CLMN_NAME = 'column name'
CLMN_TXT = 'column text'
def set_data_to_tables(table, columns, lines):
    table['columns'] = columns
    keys_of_cols = {}


    # format our column
    table.column("#0", width=20, anchor=CENTER, stretch=NO)
    table.heading("#0", text="", anchor=CENTER)
    is_first = True
    for title_og in columns:

        col_var = replace_whitespace(title_og, replacement='_').lower()
        col_text = col_var.replace('_', ' ').title()

        try:
            table.column(col_var, anchor=CENTER, stretch=YES)    # sometimes name can trigger the try_catch
        except:
            col_var = replace_whitespace(title_og, replacement='_')
            table.column(col_var, anchor=CENTER, stretch=YES)
        finally:
            table.heading(col_var, text=col_text, anchor=CENTER)

    for line in lines:
        if not isinstance(line[2], Iterable) or isinstance(line[2], str):
            table.insert(parent='', index='end', values=line)
            continue
        row = table.insert(parent='', index='end', values=line[:2] + ('...',))
        for val in line[2]:
            table.insert(parent=row, index='end', values=('', '', val))

# def set_data_to_tables(table, columns, lines):
#     table['columns'] = columns[1:]
#     keys_of_cols = {}
#
#
#     # format our column
#     table.column("#0", minwidth=20, stretch=YES)
#     # table.heading("#0", text="", anchor=CENTER)
#     is_first = True
#     for title_og in columns:
#
#         col_var = replace_whitespace(title_og, replacement='_').lower()
#         col_text = col_var.replace('_', ' ').title()
#         if is_first:
#             table.heading("#0", text=col_text, anchor=CENTER)
#             is_first = not is_first
#             continue
#
#         try:
#             table.column(col_var, anchor=CENTER, stretch=YES)    # sometimes name can trigger the try_catch
#         except:
#             col_var = replace_whitespace(title_og, replacement='_')
#             table.column(col_var, anchor=CENTER, stretch=YES)
#         finally:
#             table.heading(col_var, text=col_text, anchor=CENTER)
#
#     for line in lines:
#         if not isinstance(line[2], Iterable) or isinstance(line[2], str):
#             table.insert(parent='', index='end', text=line[0], values=line[1:])
#             continue
#         row = table.insert(parent='', index='end', text=line[0], values=(line[1],'...'))
#         for val in line[2]:
#             table.insert(parent=row, index='end', values=('', val))

    # table.pack()

# cols = ('player_id', 'player_name', 'player_Rank', 'player_states', 'player_city')
# data = [
#     ('1', 'Ninja', '101', 'Oklahoma', 'Moore'),
#     ('2', 'Ranger', '102', 'Wisconsin', 'Green Bay'),
#     ('3', 'Deamon', '103', 'California', 'Placentia'),
#     ('4', 'Dragon', '104', 'New York', 'White Plains'),
#     ('5', 'CrissCross', '105', 'California', 'San Diego'),
#     ('6', 'ZaqueriBlack', '106', 'Wisconsin', 'TONY'),
#     ('7', 'RayRizzo', '107', 'Colorado', 'Denver'),
#     ('8', 'Byun', '108', 'Pennsylvania', 'ORVISTON'),
#     ('9', 'Trink', '109', 'Ohio', 'Cleveland'),
#     ('10', 'Twitch', '110', 'Georgia', 'Duluth'),
#     ('11', 'Animus', '111', 'Connecticut', 'Hartford')
# ]
cols = ('title', 'selction', 'more')
# data = [('Tester', 'Gilad', ''),
#         ('Site', 'home', ''),
#         ('Dns Servers', 'base', '8.8.8.8\n1.1.1.1'),
#         ('Domain Names', 'group 1', 'wikipedia.org\nchina.org.cn\nfdgdhghfhfghfjfdhdh.com\ncnbc.com\nlexico.com\ntr-ex.me\ntvtropes.org\ntandfonline.com\namazon.in\narchive.org\namitdvir.com\nnihonsport.com\naeon-ryukyu.jp\n4stringsjp.com'),
#         ('Session Name', '08/15/2023 22:11:54', '')
#         ]
data = [('Tester', 'Gilad', ''),
        ('Site', 'home', ''),
        ('Dns Servers', 'base', '8.8.8.8\n1.1.1.1'.split('\n')),
        ('Domain Names', 'group 1', 'wikipedia.org\nchina.org.cn\nfdgdhghfhfghfjfdhdh.com\ncnbc.com\nlexico.com\ntr-ex.me\ntvtropes.org\ntandfonline.com\namazon.in\narchive.org\namitdvir.com\nnihonsport.com\naeon-ryukyu.jp\n4stringsjp.com'.split('\n')),
        ('Session Name', '08/15/2023 22:11:54', '')
        ]

create_table_window(columns=cols, lines=data)

