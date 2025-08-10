from Utils import load_ascii_faces
from Sequences import boot_sequence, load_AI, home
import os

face_frames = load_ascii_faces("images/ascii")

os.environ['INTEL'] = '0'

#boot_sequence()
#load_AI(face_frames)
home(face_frames, "idle")