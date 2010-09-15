import logging
import re

_log = logging.getLogger("speakjet")

class Commands:
    # MSA commands
    # http://www.magnevation.com/pdfs/speakjetusermanual.pdf

    def __init__(self):
        self._phoneme_to_code = {}
        self._code_to_phoneme = {}

        self._add_phoneme("P0", 0)
        self._add_phoneme("P1", 1)
        self._add_phoneme("P2", 2)
        self._add_phoneme("P3", 3)
        self._add_phoneme("P4", 4)
        self._add_phoneme("P5", 5)
        self._add_phoneme("P6", 6)

        self._add_phoneme("FAST", 7)
        self._add_phoneme("SLOW", 8)
        self._add_phoneme("STRESS", 14)
        self._add_phoneme("RELAX", 15)
        self._add_phoneme("SOFT", 18)

        self._add_phoneme("IY", 128)
        self._add_phoneme("IH", 129)

        self._add_phoneme("EY", 130)
        self._add_phoneme("EH", 131)
        self._add_phoneme("AY", 132)
        self._add_phoneme("AX", 133)
        self._add_phoneme("UX", 134)

        self._add_phoneme("OH", 135)
        self._add_phoneme("AW", 136)
        self._add_phoneme("OW", 137)
        self._add_phoneme("UH", 138)
        self._add_phoneme("UW", 139)

        self._add_phoneme("MM", 140)
        self._add_phoneme("NE", 141)
        self._add_phoneme("NO", 142)
        self._add_phoneme("NGE", 143)
        self._add_phoneme("NGO", 144)

        self._add_phoneme("LE", 145)
        self._add_phoneme("LO", 146)
        self._add_phoneme("WW", 147)
        self._add_phoneme("RR", 148)
        self._add_phoneme("IYRR", 149)

        self._add_phoneme("EYRR", 150)
        self._add_phoneme("AXRR", 151)
        self._add_phoneme("AWRR", 152)
        self._add_phoneme("OWRR", 153)
        self._add_phoneme("EYIY", 154)

        self._add_phoneme("OHIY", 155)
        self._add_phoneme("OWIY", 156)
        self._add_phoneme("OHIH", 157)
        self._add_phoneme("IYEH", 158)
        self._add_phoneme("EHLE", 159)

        self._add_phoneme("IYUW", 160)
        self._add_phoneme("AXUW", 161)
        self._add_phoneme("IHWW", 162)
        self._add_phoneme("AYWW", 163)
        self._add_phoneme("OWWW", 164)
        
        self._add_phoneme("JH", 165)
        self._add_phoneme("VV", 166)
        self._add_phoneme("ZZ", 167)
        self._add_phoneme("ZH", 168)
        self._add_phoneme("DH", 169)

        self._add_phoneme("BE", 170)
        self._add_phoneme("BO", 171)
        self._add_phoneme("EB", 172)
        self._add_phoneme("OB", 173)
        self._add_phoneme("DE", 174)

        self._add_phoneme("DO", 175)
        self._add_phoneme("ED", 176)
        self._add_phoneme("OD", 177)
        self._add_phoneme("GE", 178)
        self._add_phoneme("GO", 179)

        self._add_phoneme("EG", 180)
        self._add_phoneme("OG", 181)
        self._add_phoneme("CH", 182)
        self._add_phoneme("HE", 183)
        self._add_phoneme("HO", 184)

        self._add_phoneme("WH", 185)
        self._add_phoneme("FF", 186)
        self._add_phoneme("SE", 187)
        self._add_phoneme("SO", 188)
        self._add_phoneme("SH", 189)

        self._add_phoneme("TH", 190)
        self._add_phoneme("TT", 191)
        self._add_phoneme("TU", 192)
        self._add_phoneme("TS", 193)
        self._add_phoneme("KE", 194)

        self._add_phoneme("KO", 195)
        self._add_phoneme("EK", 196)
        self._add_phoneme("OK", 197)
        self._add_phoneme("PE", 198)
        self._add_phoneme("PO", 199)

    def _add_phoneme(self, phoneme, code):
        if phoneme in self._phoneme_to_code:
            raise Error("phoneme already mapped: %s" % phoneme)
        if code in self._phoneme_to_code:
            raise Error("code already mapped: %s" % code)

        self._phoneme_to_code[phoneme] = code
        self._code_to_phoneme[code] = phoneme

    def get_code(self, phoneme):
        if phoneme[0] == '\\':
            phoneme = phoneme[1:]

        return self._phoneme_to_code.get(phoneme)

class Dictionary:
    def __init__(self):
        self._commands = Commands()
        self._words = {}

    def load_file(self, filename):
        fd = open(filename)

        for line in fd.xreadlines():
            line = line.strip()

            m = re.match("([a-z]+)\s*=\s*(.*)", line, re.I)
            if m is not None:
                word = m.group(1).strip()
                codes = m.group(2).strip()

                self._load_word(word, codes)

        fd.close()

    def _load_word(self, word, codes):
        codes = re.split("\s+", codes)

        # skip dictionary words that start with "fx" for now
        if word.startswith("fx"):
            return

        # normalize word and codes
        word = word.lower()
        codes = [ code.upper() for code in codes ]

        for code in codes:
            code = code.upper()

            if code[0] != "\\":
                # skip any words that don't have properly escaped codes
                _log.debug("Skipping word in dictionary: %s", code)
                return

            if self._commands.get_code(code[1:]) is None:
                print "%s: missing code: %s" % (word, code[1:])

        self._words[word] = codes

    def lookup(self, word):
        try:
            codes = map(self._commands.get_code, self._words[word])
        except KeyError:
            # word will fall through to TTS256
            if word == '':
                codes = [ self._commands.get_code("P5") ] # 60 ms
            elif word == '.':
                codes = [ self._commands.get_code("P2") ] # 200 ms
            elif word == ',':
                codes = [ self._commands.get_code("P5") ] # 60 ms
            elif word == ':':
                codes = [ self._commands.get_code("P3") ] # 700 ms
            else:
                codes = word

        return codes

class Tokenizer:
    def __init__(self):
        pass

    def _normalize_punctuation(self, token):
        if len(token) > 0 and token[0] in ".?!":
            return "."
        else:
            # remove apostrophes around tokens
            return token.strip("'")

    def tokenize(self, phrase):
        phrase = phrase.strip().lower()

        tokens = re.findall("([a-z']+|[0-9]+| +|\.+|,+|:+|\?+)", phrase)

        # for now, replace all sentence ending punctuation with a period token
        tokens = map(self._normalize_punctuation, tokens)

        return [ t.strip() for t in tokens ]
