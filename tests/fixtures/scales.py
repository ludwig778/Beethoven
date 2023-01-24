from beethoven.models import Note, Scale

c_major = Scale(tonic=Note(name="C"), name="major")
d_lydian = Scale(tonic=Note(name="D"), name="lydian")
a_minor = Scale(tonic=Note(name="A"), name="minor")
a_minor_pentatonic = Scale(tonic=Note(name="A"), name="pentatonic")
