from Utils import load_ascii_faces
from Sequences import boot_sequence, load_AI, home

face_frames = load_ascii_faces("images/ascii")

boot_sequence()
load_AI(face_frames)
home(face_frames, "idle")