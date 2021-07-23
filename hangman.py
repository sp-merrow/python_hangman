from random import randint
from os import system, name

hangWords = []
manStates = [[], [], [], [], [], [], []]

def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')



with open('words.txt', 'r') as words:
    for line in words:
        line = line.replace('\n', '')
        if line.isalpha():
            hangWords.append(line)
    words.close()


with open('hangman_ascii.txt', 'r') as man:
    stateCount = -1
    for line in man:
        line = line.replace('\n', '')
        if line == '  +---+':
            stateCount += 1
        manStates[stateCount].append(line)
    man.close()


class Game:
    def __init__(self, word):
        if not word:
            self.word = hangWords[randint(0, len(hangWords) - 1)]
        else:
            self.word = word
        self.currentMan = 0
        self.guessedLtr = []
    

    def __str__(self):
        clear()
        returnStr = ''
        if self.guessedLtr:
            for c, ltr in enumerate(self.guessedLtr):
                if c < len(self.guessedLtr) and c > 0 and ltr not in self.word:
                    if returnStr:
                        returnStr += ', '
                if ltr not in self.word:
                    if not returnStr:
                        returnStr += 'Does not include: '
                    returnStr += ltr

        returnStr += '\n\n'
        for i in manStates[self.currentMan]:
            returnStr += i + '\n'
        
        if self.guessedLtr:
            for ltr in self.guessedLtr:
                if ltr == self.guessedLtr[0]:
                    charIndex = self.findChar(ltr)
                else:
                    for ele in self.findChar(ltr):
                        charIndex.append(ele)
            subReturn = '_' * len(self.word)
            if charIndex:
                for ind in charIndex:
                    subReturn = subReturn[:ind] + self.word[ind] + subReturn[ind+1:]
            subReturn = ' '.join(subReturn)
            
            returnStr += '\n\n' + subReturn
        else:
            returnStr += '\n' + '_ ' * len(self.word)

        return returnStr


    def findChar(self, chr):
        return [l for l, lttr in enumerate(self.word) if lttr == chr]

    def getGameState(self):
        chkLetters = []
        for ltr in self.word:
            if ltr in self.guessedLtr:
                chkLetters.append(ltr)
        
        if self.currentMan == 6:
            return 'lost'
        elif len(chkLetters) == len(self.word):
            return 'won'
        else:
            return 'ongoing'

    def guess(self):
        while True:
            enteredGuess = str(input('\nEnter letter: '))
            if len(enteredGuess) == 1 and enteredGuess.isalpha() and enteredGuess not in self.guessedLtr:
                break
            else:
                print('Invalid input. Try again please.')
        
        self.guessedLtr.append(enteredGuess.lower())

        if enteredGuess.lower() not in self.word:
            self.currentMan += 1


def inputValidator(inputType, valids):
    while True:
        data = str(input('{}'.format(inputType)))
        if data not in valids:
            print('Invalid input. Please enter again.\n')
        else:
            return data


def main():
    while True:
        clear()
        print('*** Hangman ***\n')
        print('1. Enter a word\n2. Pick random word\n\n')
        gameOption = inputValidator('Enter an option: ', ('1', '2'))

        if gameOption == '1':
            while True:
                selectedWord = input('Enter a word: ')
                if not selectedWord.isalpha():
                    print('\nInvalid input.')
                else:
                    break
            
            currentGame = Game(selectedWord.lower())
        else:
            currentGame = Game(None)
        
        while currentGame.getGameState() == 'ongoing':
            print(currentGame)
            currentGame.guess()
        
        print(currentGame)
        if currentGame.getGameState() == 'won':
            print('\n*** You win! ***')
        else:
            print('\n*** GAME OVER ***\n\nThe word was {}'.format(currentGame.word))

        cont = inputValidator('\nPlay again (y/n)? ', ('y', 'n'))

        if cont == 'n':
            break
            
main()

input('\n\nPress Enter to exit')
