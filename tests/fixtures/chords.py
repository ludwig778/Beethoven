from beethoven.models import Chord, Note

c4_maj = Chord(root=Note(name="C", octave=4), name="maj")
c_maj7 = Chord(root=Note(name="C"), name="maj7")
d_min7 = Chord(root=Note(name="D"), name="min7")
e_min7 = Chord(root=Note(name="E"), name="min7")
f_maj7 = Chord(root=Note(name="F"), name="maj7")
g_7 = Chord(root=Note(name="G"), name="7")
a_min7 = Chord(root=Note(name="A"), name="min7")
b_min7b5 = Chord(root=Note(name="B"), name="min7b5")

c_major_7th_chords = [c_maj7, d_min7, e_min7, f_maj7, g_7, a_min7, b_min7b5]
