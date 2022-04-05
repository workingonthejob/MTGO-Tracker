import tkinter as tk
from tkinter import ttk
import os
import modo
from constants.ui.general import TITLE_NAME
from constants.ui.buttons import *
import logging
from logging.config import fileConfig

fileConfig('logging_config.ini')
logger = logging.getLogger()

class ui:

    def __init__(self):
        self.status_label = None
        self.ask_to_save = False
        self.window = None
        self.MAIN_WINDOW_SIZE = ("small", 1000, 490)
        self.INPUT_OPTIONS = {}

        self.window = tk.Tk()
        self.window.title(TITLE_NAME)
        self.window.iconbitmap(self.window,"icon.ico")

        self.load_window_size_setting()
        self.window.geometry(str(self.MAIN_WINDOW_SIZE[1]) + "x" + str(self.MAIN_WINDOW_SIZE[2]))
        self.window.resizable(False, False)

        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)

        bottom_frame = tk.LabelFrame(self.window)
        left_frame = tk.Frame(self.window)
        text_frame = tk.LabelFrame(self.window, text="Dataframe")
        bottom_frame.grid(row=1, column=1, sticky="ew")
        left_frame.grid(row=0, column=0, sticky="ns")
        text_frame.grid(row=0, column=1, sticky="nsew")

        text_frame.grid_columnconfigure(0, weight=1)
        text_frame.grid_columnconfigure(1, weight=0)
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_rowconfigure(1, weight=0)
        bottom_frame.grid_columnconfigure(0, weight=1)

        match_button = tk.Button(left_frame, text=MATCH_DATA_BUTTON_LABEL, state=tk.DISABLED,\
            command=lambda : self.set_display("Matches", update_status=True, start_index=0, reset=True))
        game_button = tk.Button(left_frame, text=GAME_DATA_BUTTON_LABEL, state=tk.DISABLED,\
            command=lambda : self.set_display("Games", update_status=True, start_index=0, reset=True))
        play_button = tk.Button(left_frame, text=PLAY_DATA_BUTTON_LABEL, state=tk.DISABLED,\
            command=lambda : self.set_display("Plays", update_status=True, start_index=0, reset=True))
        draft_button = tk.Button(left_frame, text="Drafts", state=tk.DISABLED,\
            command=lambda : self.set_display("Drafts", update_status=True, start_index=0, reset=True))
        pick_button = tk.Button(left_frame, text="Draft Picks", state=tk.DISABLED,\
            command=lambda : self.set_display("Picks", update_status=True, start_index=0, reset=True))
        stats_button = tk.Button(left_frame, text=STATISTICS_BUTTON_LABEL, state=tk.DISABLED,\
            command=lambda : get_stats())
        filter_button = tk.Button(left_frame, text=FILTER_BUTTON_LABEL, state=tk.DISABLED,\
            command=lambda : set_filter())
        clear_button = tk.Button(left_frame, text=CLEAR_FILTER_BUTTON_LABEL, state=tk.DISABLED,\
            command=lambda : clear_filter(update_status=True, reload_display=True))
        revise_button = tk.Button(left_frame, text="Revise Record(s)",\
            state=tk.DISABLED, command=lambda : revise_method_select())
        remove_button = tk.Button(left_frame, text="Remove Record(s)",\
            state=tk.DISABLED, command=lambda : remove_select())
        next_button = tk.Button(left_frame, text="Next",\
            command=lambda : self.next_page())
        back_button = tk.Button(left_frame, text="Back", state=tk.DISABLED,\
            command=lambda : back())

        self.status_label = tk.Label(bottom_frame, text="")
        self.status_label.grid(row=0, column=0)

        menu_bar = tk.Menu(self.window)

        file_menu = tk.Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="File", menu=file_menu)

        file_menu.add_command(label="Import MTGO GameLogs", command=lambda : import_window())
        file_menu.add_separator()
        file_menu.add_command(label="Load Saved Data", command=lambda : load_saved_window())
        file_menu.add_command(label="Save Data", command=lambda : save_window(exit=False), state=tk.DISABLED)
        file_menu.add_separator()
        file_menu.add_command(label="Set Main Window Size", command=lambda : set_default_window_size())
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=lambda : self.exit_select())

        export_menu = tk.Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="Export", menu=export_menu)

        export_csv = tk.Menu(export_menu, tearoff=False)
        export_csv.add_command(label="Match History", command=lambda : export2(matches=True, _csv=True))
        export_csv.add_command(label="Game History", command=lambda : export2(games=True, _csv=True))
        export_csv.add_command(label="Play History", command=lambda : export2(plays=True, _csv=True))
        export_csv.add_command(label="Draft History", command=lambda : export2(drafts=True, _csv=True))
        export_csv.add_command(label="Draft Pick History", command=lambda : export2(picks=True, _csv=True))
        export_csv.add_command(label="All Data (5 Files)",\
            command=lambda : export2(matches=True, games=True, plays=True, drafts=True, picks=True, _csv=True))
        export_csv.add_separator()
        export_csv.add_command(label="Match History (Inverse Join)", command=lambda : export2(matches=True, _csv=True, inverted=True))
        export_csv.add_command(label="Game History (Inverse Join)", command=lambda : export2(games=True, _csv=True, inverted=True))
        export_csv.add_command(label="All Data (Inverse Join, 5 Files)",\
            command=lambda : export2(matches=True, games=True, plays=True, drafts=True, picks=True, _csv=True, inverted=True))
        export_csv.add_separator()
        export_csv.add_command(label="Currently Displayed Data (with Filters)", command=lambda : export2(current=True, _csv=True, filtered=True))

        export_excel = tk.Menu(export_menu, tearoff=False)
        export_excel.add_command(label="Match History", command=lambda : export2(matches=True, _excel=True))
        export_excel.add_command(label="Game History", command=lambda : export2(games=True, _excel=True))
        export_excel.add_command(label="Play History", command=lambda : export2(plays=True, _excel=True))
        export_excel.add_command(label="Draft History", command=lambda : export2(drafts=True, _excel=True))
        export_excel.add_command(label="Draft Pick History", command=lambda : export2(picks=True, _excel=True))
        export_excel.add_command(label="All Data (5 Files)",\
            command=lambda : export2(matches=True, games=True, plays=True, drafts=True, picks=True, _excel=True))
        export_excel.add_separator()
        export_excel.add_command(label="Match History (Inverse Join)", command=lambda : export2(matches=True, _excel=True, inverted=True))
        export_excel.add_command(label="Game History (Inverse Join)", command=lambda : export2(games=True, _excel=True, inverted=True))
        export_excel.add_command(label="All Data (Inverse Join, 5 Files)",\
            command=lambda : export2(matches=True, games=True, plays=True, drafts=True, picks=True, _excel=True, inverted=True))
        export_excel.add_separator()
        export_excel.add_command(label="Currently Displayed Table (with Filters)", command=lambda : export2(current=True, _excel=True, filtered=True))

        export_menu.add_cascade(label="Export to CSV", menu=export_csv)
        export_menu.add_cascade(label="Export to Excel", menu=export_excel)
        export_menu.add_separator()
        export_menu.add_command(label="Set Default Export Folder", command=lambda : set_default_export())

        data_menu = tk.Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="Data", menu=data_menu)

        data_menu.add_command(label="Input Missing Match Data", command=lambda : input_missing_data(), state=tk.DISABLED)
        data_menu.add_command(label="Input Missing Game_Winner Data", command=lambda : get_winners(), state=tk.DISABLED)
        data_menu.add_command(label="Apply Best Guess for Deck Names", command=lambda : rerun_decks_window(), state=tk.DISABLED)
        data_menu.add_separator()
        data_menu.add_command(label="Apply Associated Draft_IDs to Limited Matches", command=lambda : get_associated_draftid_pre(), state=tk.DISABLED)
        data_menu.add_separator()
        data_menu.add_command(label="Set Default Hero", command=lambda : set_default_hero(), state=tk.DISABLED)
        data_menu.add_command(label="Set Default Import Folders", command=lambda : set_default_import())
        data_menu.add_separator()
        data_menu.add_command(label="Clear Loaded Data", command=lambda : clear_window(), state=tk.DISABLED)
        data_menu.add_command(label="Delete Saved Session", command=lambda : delete_session())

        self.window.config(menu=menu_bar)

        match_button.grid(row=BUTTON_ORDER[MATCH_DATA_BUTTON_LABEL], column=0, sticky="ew", padx=5, pady=(15, 5))
        game_button.grid(row=BUTTON_ORDER[GAME_DATA_BUTTON_LABEL], column=0, sticky="ew", padx=5, pady=(0, 5))
        play_button.grid(row=BUTTON_ORDER[PLAY_DATA_BUTTON_LABEL], column=0, sticky="ew", padx=5, pady=(0, 5))
        draft_button.grid(row=BUTTON_ORDER["Drafts"], column=0, sticky="ew", padx=5, pady=(0, 5))
        pick_button.grid(row=BUTTON_ORDER["Draft Picks"], column=0, sticky="ew", padx=5, pady=(0, 5))
        stats_button.grid(row=BUTTON_ORDER[STATISTICS_BUTTON_LABEL], column=0, sticky="ew", padx=5, pady=(20, 5))
        filter_button.grid(row=BUTTON_ORDER[FILTER_BUTTON_LABEL], column=0, sticky="ew", padx=5, pady=(20, 5))
        clear_button.grid(row=BUTTON_ORDER[CLEAR_FILTER_BUTTON_LABEL], column=0, sticky="ew", padx=5, pady=(0, 5))
        revise_button.grid(row=BUTTON_ORDER["Revise Record(s)"], column=0, sticky="ew", padx=5, pady=(20, 5))
        remove_button.grid(row=BUTTON_ORDER["Remove Record(s)"], column=0, sticky="ew", padx=5, pady=(0, 5))
        next_button.grid(row=BUTTON_ORDER["Next"], column=0, sticky="ew", padx=5, pady=(20, 5))
        back_button.grid(row=BUTTON_ORDER["Back"], column=0, sticky="ew", padx=5, pady=(0, 5))

        tree1 = ttk.Treeview(text_frame, show="tree")
        tree1.grid(row=0, column=0, sticky="nsew")
        tree1.bind("<Double-1>", self.tree_double)
        tree1.bind("<ButtonRelease-1>", self.activate_revise)

        # tree_scrolly = tk.Scrollbar(text_frame, command=tree1.yview)
        # tree1.configure(yscrollcommand=tree_scrolly.set)
        # tree_scrolly.grid(row=0, column=1, sticky="ns")

        tree_scrollx = tk.Scrollbar(text_frame, orient="horizontal", command=tree1.xview)
        tree1.configure(xscrollcommand=tree_scrollx.set)
        tree_scrollx.grid(row=1, column=0, sticky="ew")

        s = ttk.Style()
        s.theme_use("default")
        s.configure("Treeview",
                    background='white',
                    fieldbackground='white')
        s.map("Treeview",
              background=[("selected","#4a6984")],
              foreground=[("selected","#ffffff")])

        self.startup()
        self.window.protocol("WM_DELETE_WINDOW", lambda : self.exit_select())

        # Event loop: listens for events (keypress, etc.)
        # Blocks code after from running until window is closed.
        self.window.mainloop()

    def load_window_size_setting(self):
        global ln_per_page

        cwd = os.getcwd()
        logger.debug(cwd)
        if os.path.isdir("save") == True:
            os.chdir(cwd + "\\" + "save")
            if os.path.isfile("MAIN_WINDOW_SIZE"):
                self.MAIN_WINDOW_SIZE = pickle.load(open("MAIN_WINDOW_SIZE","rb"))
                if self.MAIN_WINDOW_SIZE[0] == "small":
                    ln_per_page = 20
                elif self.MAIN_WINDOW_SIZE[0] == "large":
                    ln_per_page = 35
            os.chdir(cwd)

    def tree_double(self, event):
        if tree1.focus() == "":
            return None
        if (display == "Plays") or (display == "Picks"):
            return None
        if tree1.identify_region(event.x, event.y) == "separator":
            return None
        if tree1.identify_region(event.x, event.y) == "heading":
            return None

    def activate_revise(self, event):
        if tree1.identify_region(event.x, event.y) == "heading":
            return
        if data_loaded == False:
            return
        if (display == "Matches"):
            revise_button["state"] = tk.NORMAL
            remove_button["state"] = tk.NORMAL
        elif (display == "Drafts"):
            # revise_button["state"] = tk.NORMAL
            remove_button["state"] = tk.NORMAL

    def startup(self):
        global FILEPATH_ROOT
        global FILEPATH_EXPORT
        global FILEPATH_LOGS
        global FILEPATH_LOGS_COPY
        global FILEPATH_DRAFTS
        global FILEPATH_DRAFTS_COPY
        global HERO
        global ALL_DATA
        global ALL_DATA_INVERTED
        global ALL_DECKS
        global TIMEOUT
        global DRAFTS_TABLE
        global PICKS_TABLE
        global PARSED_FILE_DICT
        global PARSED_DRAFT_DICT
        global data_loaded
        global ask_to_save

        if os.path.isfile("INPUT_OPTIONS.txt"):
            in_header = False
            in_instr = True
            x = ""
            y = []
            with io.open("INPUT_OPTIONS.txt","r", encoding="ansi") as file:
                initial = file.read().split("\n")
                for i in initial:
                    if i == "-----------------------------":
                        if in_instr:
                            in_instr = False
                        in_header = not in_header
                        if in_header == False:
                            x = last.split(":")[0].split("# ")[1]
                        elif x != "":
                            self.INPUT_OPTIONS[x] = y
                            y = []                        
                    elif (in_header == False) and (i != "") and (in_instr == False):
                        y.append(i)
                    last = i
        else:
            self.INPUT_OPTIONS["Constructed Match Types"] = modo.match_types(con=True)
            self.INPUT_OPTIONS["Booster Draft Match Types"] = modo.match_types(booster=True)
            self.INPUT_OPTIONS["Sealed Match Types"] = modo.match_types(sealed=True)
            self.INPUT_OPTIONS["Archetypes"] = modo.archetypes()
            self.INPUT_OPTIONS["Constructed Formats"] = modo.formats(con=True)
            self.INPUT_OPTIONS["Limited Formats"] = modo.formats(lim=True)
            self.INPUT_OPTIONS["Cube Formats"] = modo.formats(cube=True)
            self.INPUT_OPTIONS["Booster Draft Formats"] = modo.formats(booster=True)
            self.INPUT_OPTIONS["Sealed Formats"] = modo.formats(sealed=True)
        
        FILEPATH_ROOT = os.getcwd()
        if os.path.isdir("save") == False:
            os.mkdir(FILEPATH_ROOT + "\\" + "save")
        if os.path.isdir("export") == False:
            os.mkdir(FILEPATH_ROOT + "\\" + "export") 
        if os.path.isdir("gamelogs") == False:
            os.mkdir(FILEPATH_ROOT + "\\" + "gamelogs")
        if os.path.isdir("draftlogs") == False:
            os.mkdir(FILEPATH_ROOT + "\\" + "draftlogs")
        FILEPATH_EXPORT = FILEPATH_ROOT + "\\" + "export"
        FILEPATH_LOGS_COPY = FILEPATH_ROOT + "\\" + "gamelogs"
        FILEPATH_DRAFTS_COPY = FILEPATH_ROOT + "\\" + "draftlogs"
        os.chdir(FILEPATH_ROOT + "\\" + "save")

        if os.path.isfile("SETTINGS"):
            SETTINGS = pickle.load(open("SETTINGS","rb"))
            #FILEPATH_ROOT   =     SETTINGS[0]
            FILEPATH_EXPORT =      SETTINGS[1]
            FILEPATH_LOGS =        SETTINGS[2]
            #FILEPATH_LOGS_COPY =  SETTINGS[3]
            FILEPATH_DRAFTS =      SETTINGS[4]
            #FILEPATH_DRAFTS_COPY = SETTINGS[5]
            HERO =                 SETTINGS[6]

        if os.path.isfile("ALL_DECKS"):
            ALL_DECKS = pickle.load(open("ALL_DECKS","rb"))

        if (os.path.isfile("ALL_DATA") == False) & (os.path.isfile("DRAFTS_TABLE") == False):
            self.update_status_bar(status="No session data to load. Import your MTGO GameLog files to get started.")
            os.chdir(FILEPATH_ROOT)
            return
        ALL_DATA = pickle.load(open("ALL_DATA","rb"))
        TIMEOUT = pickle.load(open("TIMEOUT","rb"))
        DRAFTS_TABLE = pickle.load(open("DRAFTS_TABLE","rb"))
        PICKS_TABLE = pickle.load(open("PICKS_TABLE","rb"))
        PARSED_FILE_DICT = pickle.load(open("PARSED_FILE_DICT","rb"))
        PARSED_DRAFT_DICT = pickle.load(open("PARSED_DRAFT_DICT","rb"))

        ALL_DATA_INVERTED = modo.invert_join(ALL_DATA)

        filter_button["state"] = tk.NORMAL
        clear_button["state"] = tk.NORMAL
        if HERO != "":
            stats_button["state"] = tk.NORMAL
        data_loaded = True

        self.set_display("Matches", update_status=True, start_index=0, reset=True)
        data_menu.entryconfig("Set Default Hero", state=tk.NORMAL)
        data_menu.entryconfig("Clear Loaded Data", state=tk.NORMAL)
        file_menu.entryconfig("Save Data", state=tk.NORMAL)
        data_menu.entryconfig("Input Missing Match Data", state=tk.NORMAL)
        data_menu.entryconfig("Input Missing Game_Winner Data", state=tk.NORMAL)
        data_menu.entryconfig("Apply Best Guess for Deck Names", state=tk.NORMAL)
        data_menu.entryconfig("Apply Associated Draft_IDs to Limited Matches", state=tk.NORMAL)
        ask_to_save = False
        os.chdir(FILEPATH_ROOT)


    def update_status_bar(self, status):
        self.status_label.config(text=status)
        logger.debug(status)

    def exit_select(self):
        if self.ask_to_save:
            save_window(exit=True)
        else:
            self.close()

    def close(self):
        # Close window and exit program.
        self.window.destroy()

    def next_page(self):
        global display_index
        display_index += ln_per_page
        if (display == "Drafts") or (display == "Picks"):
            print_data(curr_data, headers=modo.header(display), update_status=True, start_index=display_index, apply_filter=False)
        else:
            print_data(curr_data, headers=modo.header(display), update_status=True, start_index=display_index, apply_filter=False)
        revise_button["state"] = tk.DISABLED
        remove_button["state"] = tk.DISABLED

def set_display(self, d, update_status, start_index, reset):
    global display
    global prev_display
    global display_index

    if data_loaded == False:
        return

    if display != d:
        prev_display = display
        display = d
    
    if reset:
        display_index = 0

    text_frame.config(text=display)
    
    if len(ALL_DATA[0]) > 0:
        match_button["state"] = tk.NORMAL
        game_button["state"] = tk.NORMAL
        play_button["state"] = tk.NORMAL
    else:
        match_button["state"] = tk.DISABLED
        game_button["state"] = tk.DISABLED
        play_button["state"] = tk.DISABLED
    if len(DRAFTS_TABLE) > 0:
        draft_button["state"] = tk.NORMAL
        pick_button["state"] = tk.NORMAL
    else:
        draft_button["state"] = tk.DISABLED
        pick_button["state"] = tk.DISABLED

    if d == "Matches":
        if resize:
            if MAIN_WINDOW_SIZE[0] == "large":
                window.geometry("1740x" + str(MAIN_WINDOW_SIZE[2]))
        print_data(ALL_DATA[0], modo.header(display), update_status, start_index, apply_filter=True)
    elif d == "Games":
        if resize:
            if MAIN_WINDOW_SIZE[0] == "large":
                window.geometry("1315x" + str(MAIN_WINDOW_SIZE[2]))
        print_data(ALL_DATA[1], modo.header(display), update_status, start_index, apply_filter=True)
    elif d == "Plays":
        if resize:
            if MAIN_WINDOW_SIZE[0] == "large":
                window.geometry("1665x" + str(MAIN_WINDOW_SIZE[2]))
        print_data(ALL_DATA[2], modo.header(display), update_status, start_index, apply_filter=True)
    elif d == "Drafts":
        print_data(DRAFTS_TABLE, modo.header(display), update_status, start_index, apply_filter=True)
    elif d == "Picks":
        print_data(PICKS_TABLE, modo.header(display), update_status, start_index, apply_filter=True)
    revise_button["state"] = tk.DISABLED
    remove_button["state"] = tk.DISABLED

if __name__ == "__main__":
    ui()