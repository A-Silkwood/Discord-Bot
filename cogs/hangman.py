from discord.ext import commands
import random
import os


class Hangman(commands.Cog):
    sessions = {}
    _help = 'Prefixes: hangman, hang, hm\nEnter ">hangman (letter)" to make a guess\nEnter ">hangman quit" to end the' \
            'game\nEnter ">hangman reset" to start a new game\n Enter ">hangman show" to show current game'

    def __init__(self, client):
        self.client = client
        path = os.getcwd() + r'\assets\hangman\wordbank.txt'
        file = open(path, 'r')
        self._word_bank = file.read().splitlines()
        print('Loaded word bank')

    @commands.command(aliases=['hm', 'hang'])
    async def hangman(self, ctx, *args):
        if not self.has_session(ctx.author.id):
            await self.create_session(ctx)
        else:
            if len(args) == 1:
                if len(args[0]) == 1 and args[0].isalpha():
                    session = self.sessions.get(ctx.author.id)
                    curr_guess = args[0].upper()
                    if not self.has_guessed(curr_guess, session):
                        '''checking guess'''
                        is_correct = self.is_correct_guess(curr_guess, session)
                        self.mark_guess(curr_guess, session)
                        await self.show_progress(ctx, session, curr_guess, is_correct)
                        '''check win or loss conditions'''
                        if is_correct:
                            if self.has_won(session):
                                await ctx.send(f'You successfully solved the word!\nUse ">hangman" to start a new game')
                                await self.end_session(ctx, False)
                        else:
                            if self.has_loss(session):
                                await ctx.send(f'You failed to the solve the word\nWord: {session.get("word")}\nUse'
                                               f' ">hangman" to start a new game')
                                await self.end_session(ctx, False)
                    else:
                        await ctx.send(f"'{curr_guess}' was already guessed")
                elif args[0] == 'quit':
                    await self.end_session(ctx)
                elif args[0] == 'reset':
                    await self.end_session(ctx)
                    await self.create_session(ctx)
                elif args[0] == 'show':
                    await self.show_progress(ctx, self.sessions.get(ctx.author.id))
                elif args[0] == 'help':
                    await ctx.send(self._help)
                else:
                    await ctx.send('Use ">hangman help" for all commands')

    async def create_session(self, ctx):
        word = random.choice(self._word_bank)
        found_letters = []
        for i in range(len(word)):
            found_letters.append(False)
        new_session = {'guesses': {},
                       'word': word.upper(),
                       'found letters': found_letters}
        self.sessions[ctx.author.id] = new_session
        await ctx.send(f'Created hangman game with {ctx.author.display_name}\nUse ">hangman help" for all commands')
        await self.show_progress(ctx, new_session)
        print(f'Created hangman session with {ctx.author}')

    async def end_session(self, ctx, create_message=True):
        self.sessions.pop(ctx.author.id)
        if create_message:
            await ctx.send(f'Ended hangman game with {ctx.author.display_name}')
        print(f'Ended hangman session with {ctx.author}')

    def mark_guess(self, guess, session):
        is_correct = self.is_correct_guess(guess, session)
        if is_correct:
            found_letters = session.get('found letters')
            for ix, letter in enumerate(session.get('word')):
                if guess == letter:
                    found_letters[ix] = True
        guesses = session.get('guesses')
        guesses[guess] = is_correct

    async def show_progress(self, ctx, session, guess=None, is_correct=None):
        if guess is not None:
            response = f"'{guess}' was {'correct' if is_correct else 'incorrect'}\n"
        else:
            response = ''
        msg = await ctx.send(response + self.create_progress_report(self.sessions.get(ctx.author.id)))
        '''add used letters'''
        emojis = {'A': '🇦',
                  'B': '🇧',
                  'C': '🇨',
                  'D': '🇩',
                  'E': '🇪',
                  'F': '🇫',
                  'G': '🇬',
                  'H': '🇭',
                  'I': '🇮',
                  'J': '🇯',
                  'K': '🇰',
                  'L': '🇱',
                  'M': '🇲',
                  'N': '🇳',
                  'O': '🇴',
                  'P': '🇵',
                  'Q': '🇶',
                  'R': '🇷',
                  'S': '🇸',
                  'T': '🇹',
                  'U': '🇺',
                  'V': '🇻',
                  'W': '🇼',
                  'X': '🇽',
                  'Y': '🇾',
                  'Z': '🇿'
                  }
        guesses = session.get('guesses')
        for guess in guesses:
            if not guesses.get(guess):
                await msg.add_reaction(emojis.get(guess))

    def create_progress_report(self, session):
        progress_report = self.create_gallow(self.get_mistakes(session)) + '\nWord:'
        word = session.get('word')
        found_letters = session.get('found letters')
        for ix, letter in enumerate(found_letters):
            if letter:
                progress_report = progress_report + ' ' + word[ix]
            else:
                progress_report = progress_report + ' ?'

        return progress_report

    @staticmethod
    def get_mistakes(session):
        mistakes = 0
        guesses = session.get('guesses')
        for guess in guesses:
            if not guesses.get(guess):
                mistakes = mistakes + 1
        return mistakes

    @staticmethod
    def create_gallow(mistakes):
        gallow = '===|\n|'
        if mistakes >= 1:
            gallow = gallow + '      O'
        gallow = gallow + '\n|'
        if mistakes == 2:
            gallow = gallow + '       |'
        elif mistakes == 3:
            gallow = gallow + '     /|'
        elif mistakes >= 4:
            gallow = gallow + '     /|\\'
        gallow = gallow + '\n|'
        if mistakes >= 5:
            gallow = gallow + '     /'
        if mistakes >= 6:
            gallow = gallow + ' \\'
        return gallow

    def has_session(self, user_id):
        session = self.sessions.get(user_id)
        if session is not None:
            return True
        else:
            return False

    @staticmethod
    def has_guessed(check, session):
        guesses = session.get('guesses')
        for guess in guesses:
            if check == guess:
                return True
        return False

    @staticmethod
    def is_correct_guess(check, session):
        for letter in session.get('word'):
            if check == letter:
                return True
        return False

    @staticmethod
    def has_won(session):
        found_letters = session.get('found letters')
        for letter in found_letters:
            if not letter:
                return False
        return True

    def has_loss(self, session):
        if self.get_mistakes(session) >= 6:
            return True
        else:
            return False


def setup(client):
    client.add_cog(Hangman(client))
