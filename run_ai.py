import os
import sys
if 'win' in sys.platform:
    import ctypes
import importlib
from multiprocessing import Process, Value, set_start_method
import time
import socket
import io

from othello_admin import Strategy, shared_dir

ORIGINAL_SYS = sys.path[:]

class AIBase:
    def __init__(self, name, possible_names, *args, extra=None, **kw):
        self.name = name
        self.possible_names = possible_names
        self.extra = extra

    def get_move(self, board, player, timelimit):
        return -1

def get_strat(name):
    old_path = os.getcwd()

    path = os.path.join(old_path, 'students/', name)
    new_path = path
    os.chdir(path)

    sys.path = [os.getcwd(), shared_dir] + ORIGINAL_SYS
    new_sys = sys.path[:]
    
    strat = importlib.import_module('students.'+name+'.strategy').\
            Strategy().best_strategy

    os.chdir(old_path)
    sys.path = ORIGINAL_SYS

    return strat, new_path, new_sys
    
def multiplatform_kill(p):
    if 'win' in sys.platform:
        handle = ctypes.windll.kernel32.OpenProcess(1, False, p.pid)
        ctypes.windll.kernel32.TerminateProcess(handle, -1)
        ctypes.windll.kernel32.CloseHandle(handle)
    else:
        os.kill(p.pid, 9)

class LocalAI(AIBase):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.strat = None
        self.new_path = self.old_path = os.getcwd()
        self.new_sys = self.old_sys = ORIGINAL_SYS
        if self.name in self.possible_names:
            self.strat, self.new_path, self.new_sys = get_strat(self.name)

    def strat_wrapper(self, board, player, best_shared, running):
        os.chdir(self.new_path)
        sys.path = self.new_sys
        move = self.strat(board, player, best_shared, running)
        os.chdir(self.old_path)
        sys.path = self.old_sys
        return move

    def get_move(self, board, player, timelimit, kill_event):
        best_shared = Value("i", -1)
        running = Value("i", 1)
        
        # Double wrapping for EXTRA ASSURANCE
        os.chdir(self.new_path)
        sys.path = self.new_sys
        p = Process(target=self.strat_wrapper, args=(list(board), player, best_shared, running))
        p.start()
        os.chdir(self.old_path)
        sys.path = self.old_sys
        
        t1 = time.time()
        
        if kill_event:
            kill_event.wait(timelimit)
            p.join(0.01)
        else:
            p.join(timelimit)
        
        if p.is_alive():
            running.value = 0
            p.join(0.01)
            if p.is_alive(): 
                p.terminate()
        move = best_shared.value
        return move, 'unknown'
