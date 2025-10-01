import textwrap
GOLD = "\033[38;5;220m"
ITALIC = "\033[3m"
RESET = "\033[0m"

story = f'''{GOLD}{ITALIC}Olet intensiivisessä lentokisassa Möttöstä vastaan. 

Tavoitteesi on päästä maaliin ennen Möttöstä. Kisa ei ole kuitenkaan yksinkertainen, 

Islannin, Espanjan ja Portugalin verisen sodan syystä niiden maiden lentokentät eivät ole käytettävissä.

Lataa lentokone tai heitä noppaa saadaksesi yllätyksiä lentokentillä.{RESET}'''

wrapper = textwrap.TextWrapper(width=60, break_long_words=False, replace_whitespace=False)

word_list = wrapper.wrap(text=story)

def story():
    return word_list