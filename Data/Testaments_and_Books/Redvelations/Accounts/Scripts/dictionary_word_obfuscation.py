# -------------------------------------------------------------------------------
# Copyright: (c) BLS OPS LLC.
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# -------------------------------------------------------------------------------

#!/usr/bin/env python3

import re
import sys
import string

if len(sys.argv) < 2:
    print('usage: python dictionary_word_obfuscation.py <vba_text_file>')
    exit(1)

decode_fn = 'CalculateInterest'

words = ['able','about','absolutely','access','according','actually','adams','adding','addressing','adds','advertise','advertising','affiliate','affiliates','affluent','afloat','africa','after','agreeing','allow','already','also','always','amazon','amount','analyze','answer','anyone','anything','anywhere','appear','approaching','area','around','article','articles','asia','assess','assist','attention','audience','audiences','authentic','author','authority','automated','away','back','backs','bank','barber','barren','base','basic','because','become','been','before','behind','best','better','bigger','biggest','blog','blogger','blogging','blueprint','boil','boils','book','books','boost','both','brand','breaking','brian','broadcasts','budget','build','building','built','burdensome','burn','business','businesses','busy','buyer','buyers','buys','called','camera','catch','certainly','certification','chain','challenges','cheat','checklist','churning','clear','clearly','click','clickbank','clicks','coalition','collaborate','collect','comes','commission','communicate','communicator','companies','company','concepts','connections','consumer','consumers','contact','content','continuing','contribute','contributor','contributors','conundrum','conversion','conversions','converting','convey','conveying','cookies','copy','copyright','could','countless','course','covers','create','creating','credit','custom','customer','customers','data','david','days','dealing','deals','deathly','define','delivered','demands','demographic','description','desert','different','digital','direct','directly','discounts','discouraged','discover','does','doing','domains','dominating','done','down','drastically','drive','driving','drop','each','easier','easily','east','easy','ebook','economy','edition','editions','effective','effectively','effectiveness','eileen','either','else','email','emotions','engaging','engine','engineer','engines','ensure','entrepreneur','entrepreneurial','entrepreneurs','equity','espa','especially','estate','europe','even','every','everyone','everything','example','excel','exclusive','experiences','expert','experts','explosive','expressed','eyes','facebook','faced','facing','fact','fail','farm','feature','feeling','figure','find','first','focus','followers','found','founder','franchise','fray','free','frightened','frightening','from','fuel','fundamentals','funnel','gauge','generally','geographic','georgia','gets','getting','getty','give','giving','going','good','google','great','green','grit','ground','grow','growing','growth','guide','guru','hair','half','hand','hands','happening','hardest','have','head','heaping','heard','hearing','help','here','hire','hold','holding','homage','housing','however','huge','humans','hundred','idea','ideas','identify','identifying','ignore','image','images','immediate','immediately','immutable','impact','importantly','impossible','improve','inbox','includes','increase','increased','increasingly','incredibly','india','industry','influencer','influencers','information','inside','insider','insightful','instagram','install','instant','instantly','insurance','interest','interests','intimidating','into','introduce','invested','join','journey','jumpstart','junction','just','jvzoo','keywords','kindle','know','lack','land','large','larger','largest','later','latest','laws','lead','leading','leads','learn','lees','level','leverage','leveraging','licensing','like','likely','likened','limit','link','linkedin','list','liveplan','loads','location','long','looking','losing','lots','love','made','magazine','magic','magnet','mail','make','makes','making','manager','many','march','market','marketing','massive','master','matter','mechanics','media','medium','message','messages','methods','micro','middle','might','millions','minded','minefield','mistakes','model','moment','momentum','money','more','most','much','mundane','must','naming','navigating','need','neglect','network','never','newsletter','next','niche','obvious','offer','often','once','online','onto','operations','opinions','opportunity','optimization','optimize','order','other','others','outset','outsource','outsourcing','over','overlook','pacific','page','pain','part','partner','partners','pass','passionate','passively','paying','pbns','peddling','people','persistence','pixel','pixels','place','plan','planning','platform','platforms','play','playing','please','plus','podcasts','point','points','policies','policy','post','posting','posts','potential','power','powered','powerful','present','presented','press','pricing','privacy','problem','product','products','profile','profit','profitable','program','properly','provide','publish','publishing','pull','question','questions','queue','quicker','quora','rage','reach','reaching','read','ready','real','really','reaping','reddit','related','relationship','relationships','relevant','report','reprints','reserved','resource','responds','responses','result','results','return','revealing','revolution','rewards','right','rights','risk','rocket','ross','rules','running','runs','sales','says','scale','schemes','science','scoop','search','second','secret','secrets','seeing','segment','segmenting','sell','semi','send','sense','september','sequence','sequences','seriously','services','setbacks','seven','shady','share','sheet','shirt','shocking','shoestring','shop','short','shortcuts','should','shown','sign','simply','sincerely','site','situation','situations','sizable','sizzling','skills','skyrocket','slice','small','snapchat','social','software','solely','solution','solve','some','someone','something','sound','south','spam','specific','spend','split','spotlight','spreading','squeeze','staff','start','starts','states','status','staying','step','stop','store','stories','straight','strategies','strategy','stuck','subscribe','subscriber','subscribers','success','successful','such','supply','supposed','sure','sustaining','sweat','systems','take','takes','taking','talk','target','targeting','teach','tell','tens','term','terms','test','tests','than','that','their','them','then','there','these','they','thin','things','think','this','thoughts','thousand','thousands','through','throwing','time','times','tips','tirelessly','today','topics','track','traffic','transparent','tremendous','trick','tricky','trigger','truck','true','truly','truth','trying','tutorial','tutorials','twice','twitter','type','ultimate','ultimately','understand','unique','united','unless','until','used','useful','users','using','valuable','value','values','very','viable','video','videos','viral','virtually','visibility','visit','visited','visitors','visually','voice','vying','walk','wanderlustworker','want','wants','wasters','water','ways','webinars','websites','week','well','what','whatever','when','whenever','where','whether','which','while','wield','will','willing','with','without','women','word','work','working','works','world','worried','would','years','your','yourself','youtube']

vba_file = sys.argv[1]

# GET THE VBA FILE
string_regex = re.compile(r'"[^"]+"', re.I)
strings = set()
with open(vba_file) as f:
    vba_text = [line.strip() for line in f.readlines()]
    for line in vba_text:
        for match in string_regex.findall(line):
            strings.add(match[1:-1])
    print(strings)

char_dict = dict()

for i, char in enumerate(list(set(''.join(strings)))):
    #if char in str_to_obfuscate:
    char_dict[char] = words[i]


### WRITE DECODE FUNCTION ###

print(f'''Function {decode_fn}(phrase)
Set dict = CreateObject("Scripting.Dictionary")''')
for char,word in char_dict.items():
    print(f'dict.Add "{word}", "{char}"')

print(f'''Dim words As Variant
Dim s As String
s = ""
words = Split(phrase, " ")
For i = 0 To UBound(words)
    s = s & dict.Item(words(i))
Next i
{decode_fn} = s
End Function
''')

### REPLACE ALL STRINGS ###

for line in vba_text:
    for s in strings:
        phrase = ' '.join([char_dict[c] for c in s])
        line = line.replace(f'"{s}"', f'{decode_fn}("{phrase}")')
    print(line)