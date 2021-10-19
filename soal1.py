from string import  ascii_uppercase
from itertools import permutations


s="BANANA"

class Player():
    def __init__(self,S,vowel=True) :
        self.s=S
        self.vowel=vowel
    def letterTest(self):
        consonants=[]
        vowels=[]
        for letter in self.s:
            if letter in "AIUEO":
                vowels.append(letter)
            else:
                consonants.append(letter)
        return consonants,vowels
    def createWord(self):
        arr=list(permutations(self.s))
        newArr=[]
        words=[]
        if self.vowel==False:
            for i in arr:
                newArr.append("".join(i))
            for length in range(len(self.s)):
                for i in newArr:
                    for j in self.letterTest()[0]:
                        if i.startswith(j) and i[:length+1] not in words:
                            words.append(i[:length+1])
        else:
            for i in arr:
                newArr.append("".join(i))
            for length in range(len(self.s)):
                for i in newArr:
                    for j in self.letterTest()[1]:
                        if i.startswith(j) and i[:length+1] not in words:
                            words.append(i[:length+1])
        return(words)


#yang dimaksud kata apa?? konsonan dan vowel selang-seling?? atau semua kemungkinan susunan huruf??
#ada beberapa kata yang memiliki kemungkinan huruf konsonan muncul berurutan        

stuart=Player(s,vowel=False)
kevin=Player(s)
wordKevin=kevin.createWord()
wordStuart=stuart.createWord()

print("score Kevin :",len(wordKevin))
print("score Stuart :",len(wordStuart))

if len(wordKevin)>len(wordStuart):
    print("pemenangnya Kevin")
elif len(wordKevin)<len(wordStuart):
    print("pemenangnya Stuart")
else:
    print("Draw")