import os, time, shutil, random, threading, sys, msvcrt
from colorama import init, Fore, Back, Style

from Utils import clear_console, type_line, speak, center_text, load_ascii_faces
from Sequences import boot_sequence, load_AI, home

face_frames = load_ascii_faces("images/ascii")

# ANSI escape codes
SAVE_CURSOR = '\033[s'
RESTORE_CURSOR = '\033[u'
CURSOR_UP = '\033[A'
CLEAR_LINE = '\033[K'


boot_sequence()
load_AI(face_frames)
home(face_frames, "idle")