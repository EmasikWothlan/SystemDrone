from pheromones.journal import Journal
from pheromones.pheromone import Pheromone
from drone.drone import Drone
from modules import boorulikes

import os


class OneLineCmdBuilder:
    legendary = """Welcome using System Drone - One Line Journal Console.
    no more step by step input, you can input your instruction in ONE line.

    usage: KEYWORDS_SPLITTED_BY_SPACE [OPTIONS] [launch]

    options:
        -p, --save-path EXISTING_DIRECTORY:     an existing directory.
        -t, --save-pattern SAVING_PATTERN:      a pattern that you want to split coming pics into different folders.
        -c, --config-file FILENAME:             filename of a config.
        -l, --load-file FILENAME:               a file that has list of command. can also write config in it.
        -f, --filters FILTER_EXPRESSION:        a set of expressions separated by "&" or "|"
                                                 Note: --filters MUST be indicated at the last of your instruction.
        -m, --module-set:                       the module you want to use
                                                 Note: if no module indicated, danbooru will be used as default.
        help [pattern|config|filter|modules]:   show this message or details about pattern, config, filter, or modules.

        options:                                show current options' value.

        launch:                                 input by itself or at the end of your instruction will start scraping.

    example:
        tanaka_takayuki -t /-Artist-%A/%c
            """
    pattern_message = """
    save patterns:
        %A is artist
        %c is character
        %C is Copyright
        %M is MD5  # is there anybody want this to be a folder's name?
        %K is the main key words
        %K1 is the first main key words
        %K2 is the second key words
        / is a directory

        example:
            /- Artist - %A/%c/
            means to save the pics under save path's directory named "- Artist - ARTIST_NAME",
            and in that folder, makedir named by the characters.
            """
    config_message = """
            coming soon...
            """
    filter_message = """
            coming soon...
            """

    module_message = """
    currently available modules are:
        %s
            """ % "\n\t".join(boorulikes.__all__)

    def __init__(self,
                 *keywords,
                 filters=None,
                 pool_mode=False,
                 pool_name=None,
                 save_path=None,
                 save_pattern=None,
                 interval=None,

                 module_set=None,
                 ):
        self.keywords = keywords or list()
        self.filters = filters

        self.pool_mode = pool_mode
        self.pool_name = pool_name
        self.save_path = save_path
        self.save_pattern = save_pattern

        self.load_file = None
        self.config_file = None

        self.interval = interval

        self.module_set = module_set or boorulikes.danbooru

        self.confirm = False

    def build(self):
        if self.save_path is None:
            self.save_path = os.path.join(".", "default_save_path")
        j = Journal(*self.keywords,
                    filters=self.filters,
                    pool_mode=self.pool_mode,
                    pool_name=self.pool_name,
                    save_path=self.save_path,
                    save_pattern=self.save_pattern,
                    interval=self.interval)
        p = Pheromone(journal=j, console_mode=False, module_set=self.module_set)
        return Drone(p)

    def console(self):
        self._first_run_only()

        while True:
            if self.confirm:
                if self.keywords and self.module_set:
                    print("Journal confirmed, launching Drone...")

                    self.launch_drone(self.build())

                    self.keywords = list()

                else:
                    if not self.keywords:
                        print("you need to indicate at least one keyword.")
                self.confirm = False
            else:
                cmd = input("System Drone - Console$ ")
                if cmd == '':
                    pass
                elif cmd.lower() == "clear":
                    self.keywords = list()
                    self.filters = None

                    self.pool_mode = None
                    self.pool_name = None
                    self.save_path = None
                    self.save_pattern = None

                    self.load_file = None
                    self.config_file = None

                    self.module_set = boorulikes.danbooru

                    self.confirm = False
                elif cmd.startswith("help"):
                    if cmd.find("pattern") != -1:
                        print(self.pattern_message)
                    elif cmd.find("config") != -1:
                        print(self.config_message)
                    elif cmd.find('filter') != -1:
                        print(self.filter_message)
                    elif cmd.find("modules") != -1:
                        print(self.module_message)
                    else:
                        print(self.legendary)
                elif cmd.lower() in ("option", "options"):
                    self.show_options()
                elif cmd.lower() in ("launch", "run", "exploit"):
                    self.confirm = True
                else:
                    self.separate_cmd(cmd)

    def separate_cmd(self, cmd):
        cmds = cmd.split(' ')
        while cmds.count(""):
            cmds.remove("")
        # self.keywords = []
        # self.save_path = None
        # self.save_pattern = None
        # self.config_file = None  # not in use
        # self.load_file = None  # not in use
        # self.filters = []
        # self.module_set = boorulikes.danbooru
        # self.confirm = False
        while cmds:
            if cmds[-1] == "launch":
                self.confirm = True
                cmds.pop(-1)
            c = cmds.pop(0)
            if c in ("-p", "--save-path"):
                p_cmd = []
                while cmds:
                    if cmds[0] not in ("-p", "--save-path",
                                       "-t", "--save-pattern",
                                       "-c", "--config-file",
                                       "-l", "--load-file",
                                       "-f", "-filters"):
                        p_cmd.append(cmds.pop(0))
                    else:
                        break
                self.save_path = " ".join(p_cmd) or "."
            elif c in ("-t", "--save-pattern"):
                t_cmd = []
                while cmds:
                    if cmds[0] not in ("-p", "--save-path",
                                       "-t", "--save-pattern",
                                       "-c", "--config-file",
                                       "-l", "--load-file",
                                       "-f", "-filters"):
                        t_cmd.append(cmds.pop(0))
                    else:
                        break
                self.save_pattern = " ".join(t_cmd) or "/- Artist - %A/"
            elif c in ("-c", "--config-file"):
                c_cmd = []
                while cmds:
                    if cmds[0] not in ("-p", "--save-path",
                                       "-t", "--save-pattern",
                                       "-c", "--config-file",
                                       "-l", "--load-file",
                                       "-f", "-filters"):
                        c_cmd.append(cmds.pop(0))
                    else:
                        break
                self.config_file = " ".join(c_cmd)
                # TODO: override save_pattern and save_path.
            elif c in ("-l", "--load-file"):
                l_cmd = []
                while cmds:
                    if cmds[0] not in ("-p", "--save-path",
                                       "-t", "--save-pattern",
                                       "-c", "--config-file",
                                       "-l", "--load-file",
                                       "-f", "-filters"):
                        l_cmd.append(cmds.pop(0))
                    else:
                        break
                self.load_file = " ".join(l_cmd)
                # TODO: override save_pattern, save_path, and keywords.
            elif c in ("-f", "-filters"):
                f_cmd = []
                while cmds:
                    if cmds[0] not in ("-p", "--save-path",
                                       "-t", "--save-pattern",
                                       "-c", "--config-file",
                                       "-l", "--load-file",
                                       "-f", "-filters"):
                        f_cmd.append(cmds.pop(0))
                    else:
                        break
                self.filters = " ".join(f_cmd)
            elif c in ("-m", "--module-set"):
                some_module = cmds.pop(0)
                if some_module in boorulikes.__all__:
                    self.module_set = some_module
            else:
                self.keywords.append(c)
                self.keywords = list(set(self.keywords))

    def launch_drone(self, drone, silent_mode=False, max_retry=3):
        if not silent_mode:
            rsp = ""
            drone, report, exception = drone.launch()
            while rsp.lower() not in ("abort", "a", "finish", "f"):
                if exception:
                    print("your drone has run into some trouble: ", exception)
                    rsp = input("what to do? [(C)ONTINUE|(a)bort|(r)eport]") or "continue"
                else:
                    print("your drone has done the task.")
                    rsp = input("what to do? [(R)EPORT|(f)inish]") or "report"
                if rsp.lower() in ("continue", "c"):
                    drone, report, exception = drone.launch()
                elif rsp.lower() in ("report", "r"):
                    print(report)
        else:
            drone, report, exception = drone.launch()
            retry_time = 0
            if not drone.finished() and retry_time < max_retry:
                retry_time += 1
                drone, report, exception = drone.launch()


    def show_options(self):
        print("Options:")
        print("\tkeywords: %s" % self.keywords)
        print("\tsave path: %s" % self.save_path)
        print("\tsave pattern: %s" % self.save_pattern)
        print("\tconfig file: %s" % self.config_file)
        print("\tload file: %s" % self.load_file)
        print("\n\tmodule set: %s" % self.module_set)

    def _first_run_only(self):
        if os.path.exists("config.cfg"):
            pass
        else:
            print(self.legendary)
            print("\nYou can always input \"help\" to get above message.\n")
            print("It seems this is the first time you run System Drone. Please make sure you have all dependencies ready.")
            if (input("Do you wish to have a quick check for dependencies?[YES|no]").lower() or "yes") in ("y", "yes"):
                no_problem = True
                try:
                    import lxml
                except:
                    print("dependency lackage: lxml")
                    no_problem = False
                try:
                    import bs4
                except:
                    print("dependency lackage: bs4")
                    no_problem = True
                try:
                    import requests
                except:
                    print("dependency lackage: requests")
                    no_problem = True
                if no_problem:
                    print("\nCongrats! You have all dependencies ready! Hope you enjoy System Drone.")
                else:
                    print("lackage found, you might try to run \"deploy.py\" to solve it.")
            else:
                print("Skip checking.")

            open('config.cfg', mode="a+")
