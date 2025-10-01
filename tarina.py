import textwrap

story = '''Olet intensiivisessä lentokisassa Möttöstä vastaan. 

Tavoitteesi on voittaa mahdollisimman lyhyessä ajassa. Kisa ei ole kuitenkaan yksinkertainen, 

Islannin, Espanjan ja Portugalin verisen sodan syystä niiden maiden lentokentät eivät ole käytettävissä. 

Oletko sinä valmis haastamaan Möttösen?'''

wrapper = textwrap.TextWrapper(width=80, break_long_words=False, replace_whitespace=False)

word_list = wrapper.wrap(text=story)

def story():
    return word_list