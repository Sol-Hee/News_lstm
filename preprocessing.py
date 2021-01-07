import tensorflow as tf
import numpy as np
import re
import os

with open("D:/news_joongang1.txt", "r", encoding='utf-8') as file:
    data = file.read()

# preprocessing
text = data
len(text) # 720441

# 1. 문자 제거
def delete_str(text, string):
    dontNeed = sorted(set(re.findall(string,text)))
    for i in dontNeed:
       text = text.replace(i, ' ')
    return text

# 1-1. <>괄호 제거
re.findall('\xa0',text)
text=delete_str(text,'\xa0')
re.findall('\uec38',text)
text=delete_str(text,'\uec38')
text=delete_str(text,'\uec37')

# 1-2. 이메일 제거 (~ 기자 제거)
re.findall('\w+\@\w+\.+\w+\.\w+',text)
text = delete_str(text,'\w+\@\w+\.+\w+\.\w+')
re.findall('\w+\.\w+\@\s',text)
re.findall('[\w,\s]+기자+',text)
text = delete_str(text,'[\w,\s]+기자+')
re.findall('[\w,\s]+교수+',text)
text = delete_str(text,'[\w,\s]+교수+')
text = delete_str(text,'\w+\.\w+\@\s')

# 1-3. 특수문자 제거
re.findall('[-~@\*#▶·「■」=]+',text)
text = delete_str(text,'[-~@\*#▶·「■」=]+')

# 1-4. () 괄호 제거
re.findall('\(+[\w,\s,-,\.]+\)',text)
text = delete_str(text,'\(+[\w,\s,-,\.]+\)')

# 1-5. [] 괄호 제거
re.findall('\[+[\w,\s,\,\.]+\]',text)
text = delete_str(text,'\[+[\w,\s,\,\.]+\]')

# 1-6. ' ', " "
re.findall('[\'\"]',text)
text = delete_str(text, '[\'\"]')
re.findall('[\”\“]',text)
text = delete_str(text, '[\”\“]')

# 1-7. 논설위원
re.findall('[\w,\s]+논설위원+',text)
text=delete_str(text,'[\w,\s]+논설위원+')

# 1-9.\n 제거
re.findall('\\n',text)
text = delete_str(text,'\\n')

# 1-10. (홈페이지) 괄호 제거
re.findall('\([A-Za-z]+\.[A-Za-z]+\.[A-Za-z]+\/?[A-Za-z]+\/?[A-Za-z]{0,}\/?\w{0,}\)',text)
text = delete_str(text,'\([A-Za-z]+\.[A-Za-z]+\.[A-Za-z]+\/?[A-Za-z]+\/?[A-Za-z]{0,}\/?\w{0,}\)')


# 1-11. 기타 제거
# lee~ 제거
re.findall('lee\w?\.\w?\s?',text)
text = delete_str(text,'lee\w?\.\w?\s?')
# ‘ 제거
re.findall('[‘:’]+', text)
text = delete_str(text,'[‘:’]')
# <> 제거
re.findall('\<\w+\>',text)
text = delete_str(text, '\<\w+\>')
# 제거 못한 () 제거
re.findall('\(\s?\w+\s?\w{0,}\s?\)',text)
text = delete_str(text, '\(\s?\w+\s?\w{0,}\s?\)')
# 괄호 안까지 날리지 않고 살아있는 것들은 의미가 있어보여 괄호만 없애기로
re.findall('[\(\)]',text)
text = delete_str(text, '[\(\)]')
# ※제거
re.findall('※[\s\w]+',text)
text = delete_str(text, '※[\s\w]+')

len(text) # 682764

# 사람이름 제거 (기자이름 제거. 정치인사 , 연예인, ceo 등은 제거하지 않음)
re.findall('\s+[김임박정심]+[현서익순수안희윤여원갑]+[가-힇]+',text)
# 김현서 임익순 김수안 정희윤 심여진 박원갑 김현정 김윤태 정익중 박현주 김윤호 박현영 박원곤
stopword=['김현서', '임익순', '김수안', '정희윤','심여진','박원갑','김현정','김윤태','정익중','박현주','김윤호','박현영','박원곤']

for i in stopword:
    text1 = text.replace(i, '')
    text = text1

set(re.findall('[A-Za-z]{3,}',text))
re.findall('choi',text)
text=delete_str(text,'choi')

re.findall('뉴스1',text)
text=delete_str(text,'뉴스1')

with open("D:/joongang_01_07_1110.txt","w",encoding="utf-8") as file:
    file.write(text)

re.findall('그래픽\s?\w{3,3}',text)
text = delete_str(text,'그래픽\s?\w{3,3}')

re.findall('[→』『]',text)
text = delete_str(text,'[→』『]')
re.findall('[정유진강광우황선윤]{3,3}',text)
stopword=['정유진','강광우','황선윤','이해준','정진우','김성룡']
for i in stopword:
    text1 = text.replace(i, '')
    text = text1

re.findall('\[\w+\s{0,}\w+\s?[ 0-9\w&\…]{0,}\]',text)
text = delete_str(text,'\[\w+\s{0,}\w+\s?[ 0-9\w&\…]{0,}\]')
re.findall('\[',text)
text = delete_str(text,'\[')
re.findall('\]',text)
text = delete_str(text,'\]')

# 일러스트 삭제
re.findall('일러스트[\s\w]{0,5}',text)
text = delete_str(text,'일러스트\s?김회룡')
re.findall('\w{4,}\s+일러스트',text)
text = delete_str(text,'\w{4,}\s+일러스트')
re.findall('[a-zA-Z]{3,3}\s+연합\w+',text)
text = delete_str(text,'[a-zA-Z]{3,3}\s+연합\w+')
re.findall('\w+\s?중앙일보',text)
re.findall('온라인\s?중앙일보',text)
text = delete_str(text,'온라인\s?중앙일보')

# 글, 사진, 동행취재 삭제
re.findall('[\s\w]+,\s+\w+\s{0,},\s?동행취재', text)
text = delete_str(text,'[\s\w]+,\s+\w+\s{0,},\s?동행취재')

set(re.findall('\s+[a-z]{3,}',text))
# https, cha , chae yoon chun heo park kim, jeong youn suh, suk, hyun, kang, jun, bae baek hong jang kwen
# sohn kwon moon shin  han jung
re.findall('https\s\/\/\w+\.\w+\/\w+',text)
text = delete_str(text,'https\s\/\/\w+\.\w+\/\w+')
stopword = ['cha', 'cha','chae','yoon','chun','heo','park','kim','jeong','youn','suh','suk','hyun','kang','jun','bae','baek','hong','jang','kwen',
            'sohn','kwon','moon','shin','han','jung','jin','대구 김정석','제주 최충일','na.','채혜선  .  ',
            '김경미 김지아  ','오종택','대전 김방현',' yoo. ','sung.','울산 백경서  k.','해남 손민호',' 채혜선 전익진 최모란  e.  ',
            '  장 미셸 오토니엘, Stairs to Paradisel, 2020, Clear blue, dark blue and grey mirrored glass, wood, 86 x 174 x 32cm.      ',
            '장 미셸 오토니엘, Precious Stonewall,2020,Green and emerald green mirrored glass, wood ,33 x 32 x 22 cm.         장 미셸 오토니엘, Stairs to Paradisel, 2020, Clear blue, dark blue and grey mirrored glass, wood, 86 x 174 x 32cm.        ',
            'Precious Stonewall 2020 Amber and emerald green mirrored glass, wood, 33 x 32 x 22 cm '
            ]
for i in stopword:
    text1 = text.replace(i, '')
    text = text1

re.findall('jin',text)
re.findall('[\w\s]+연합뉴스        ',text)
text = delete_str(text, '[\w\s]+연합뉴스        ')
re.findall('[△◆]',text)
text = delete_str(text, '[△◆]')

with open("D:/joongang_01_07_1156.txt","w",encoding="utf-8") as file:
    file.write(text)

re.findall('[㈜]',text)
text = delete_str(text, '[㈜]')

text = delete_str(text, '[△◆]')

re.findall('2020\.\d+\.\d+\s+\/[\d\s]+\/[\s〈\w\dⓒ\.]+〉',text)
text = delete_str(text, '2020\.\d+\.\d+\s+\/[\d\s]+\/[\s〈\w\dⓒ\.]+〉')
re.findall('[가-힇]+\,\s+[가-힇]{3,3}\s+[가-힇]{2,2}\s{4,}[가-힇\s\,]+[a-zA-Z\s0-9\,]{6,}',text)
re.findall(' Precious Stonewall\s',text)



#############
with open("D:/joongang_01_07_1216.txt", "w", encoding="utf-8") as file:
    file.write(text)

stopword = ['신진호 , 이에스더',' oh.',' e. ','힙으뜸 유튜브 캡처.  ','   무안 진창일  .   ',
            '그래픽  . ','창원   김원  .  ','ko. ','Claire Dorn 촬영. ',' 2021.1.6/ ',
            '  오현석 김효성  oh.','           세종 손해용ㆍ김기환  .             전호겸의 구독경제로 보는 세상     ',
            '           세종 손해용  .             ','    그래미 트로피.    ',
            '  글 김은혜 꿈트리 에디터          ', '사진 기아차 ']
for i in stopword:
    text1 = text.replace(i, '')
    text = text1

with open("D:/joongang_01_07_2002.txt", "w", encoding="utf-8") as file:
    file.write(text)

import re


re.findall('\d{0,}\s?㎏\w+',text)
text=delete_str(text, '\d{0,}\s?㎏\w+')
re.findall('㎝\s+\w+',text)
text=delete_str(text,'㎝\s+\w+')
re.findall('[A-Za-z]{1,}',text)
text=delete_str(text,'[A-Za-z]{1,}')
re.findall(',',text)
text=delete_str(text,',')
re.findall('[\d\.\s]+%',text)
text=delete_str(text,'[\d\.\s]+%')

re.findall('[A-Za-z]{0,}\s?[A-Za-z]{1,}\s+[A-Za-z]{1,}',text)
text=delete_str(text,'[A-Za-z]{0,}\s?[A-Za-z]{1,}\s+[A-Za-z]{1,}')

re.findall('[〈〉○●▲▽△■ㅁ]',text)
text=delete_str(text,'[〈〉○●▲▽△■ㅁ]')

re.findall('\s?[a-zA-Z]{1,}\s?',text)
text=delete_str(text,'\s?[a-zA-Z]{1,}\s?')

re.findall('\d+\\/\d+',text)
re.findall('[0-9]+\/[0-9]+',text)
stopword=re.findall('[0-9]\/+[0-9]',text)
for i in stopword:
    text1 = text.replace(i, '')
    text = text1

re.findall('\s{2,}는\s+',text)
text=delete_str(text,'\s{2,}는\s+')

with open("D:/joongang_01_07_1837.txt", "w", encoding="utf-8") as file:
    file.write(text)