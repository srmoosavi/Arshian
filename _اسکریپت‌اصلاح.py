import json,unicodedata,os,shutil

MIRROR={'(':')',')':'(','[':']',']':'[','{':'}','}':'{','«':'»','»':'«','<':'>','>':'<'}
def is_ltr(ch):
    o=ord(ch)
    return (('a'<=ch<='z') or ('A'<=ch<='Z') or ('0'<=ch<='9')
            or 0x06F0<=o<=0x06F9 or 0x0660<=o<=0x0669)
NUM_SEP=set("./-:،٫,%")

def smart_reverse(line):
    rev=line[::-1]; out=[]; i=0; n=len(rev)
    while i<n:
        if is_ltr(rev[i]):
            j=i
            while j<n and (is_ltr(rev[j]) or (rev[j] in NUM_SEP and j+1<n and is_ltr(rev[j+1]))):
                j+=1
            out.append(rev[i:j][::-1]); i=j
        else:
            ch=rev[i]
            out.append(MIRROR.get(ch,ch)); i+=1
    return ''.join(out)

def fix_line(line):
    if not line.strip(): return line
    return unicodedata.normalize('NFKC', smart_reverse(line))
def fix_text(t): return '\n'.join(fix_line(l) for l in t.split('\n'))

split=json.load(open('/tmp/split.json'))
OUT="/tmp/corrected/Arshian-corrected"
if os.path.exists("/tmp/corrected"): shutil.rmtree("/tmp/corrected")
os.makedirs(OUT)
for rel in split['fixable']:
    text=open(rel,encoding='utf-8').read().replace('\ufeff','')
    dst=os.path.join(OUT,rel); os.makedirs(os.path.dirname(dst),exist_ok=True)
    open(dst,'w',encoding='utf-8').write(fix_text(text))

# manifest of table files needing re-conversion
with open(os.path.join(OUT,'_فایل‌های‌نیازمند‌تبدیل‌مجدد.txt'),'w',encoding='utf-8') as f:
    f.write("این فایل‌ها معکوس بودند ولی جدولِ تکه‌تکه‌شده‌اند و با معکوس‌کردن قابل بازیابی نیستند.\n")
    f.write("باید از فایل PDF/منبع اصلی با ابزار بهتر دوباره تبدیل شوند:\n\n")
    for p in split['tables']: f.write("• "+p+"\n")

# save the script too
shutil.copy('/tmp/corrector_final.py', os.path.join(OUT,'_اسکریپت‌اصلاح.py'))

# zip it
shutil.make_archive('/tmp/Arshian-corrected','zip','/tmp/corrected')
print("fixable:",len(split['fixable']),"| tables flagged:",len(split['tables']))
print("zip size:", os.path.getsize('/tmp/Arshian-corrected.zip'))
# verify a bracket fix
t=open("/tmp/corrected/Arshian-corrected/Letters/مکاتبات وارده/نامه از سابیر ابلاغ صورتجلسه ایستگاه های عمان سامانی و شاهد 1404.07.28/04.25.1610 (1).md",encoding='utf-8').read()
for l in t.split('\n'):
    if 'شاهد' in l: print("bracket check:",l.strip()[:90]); break
