#coding: UTF8
"""
Unit tests the wordcount module
"""
import wordcount
from wordcount import is_asian, nonj_len, filter_jchars
from wordcount import get_wordcount as gwc
from wordcount import get_wordcount_obj as gwo
import string

KANJI = ''.join([u"漢字",
            u"蓋棺事定",
            u"武運長久",
            u"竜頭鷁首",
            u"煙霞痼疾",
            u"流転輪廻",
            u"武陵桃源",
            u"六韜三略",
            u"翠帳紅閨",
            u"有智高才",
            u"残杯冷炙"])

def test_is_asian_kanji():
    for char in KANJI:
        assert is_asian(char), ord(char)

def test_is_asian_symbol():
    assert not is_asian(unichr(0x03A6)), unichr(0x03A6)

def test_is_asian_half_kata():
    for char in u"ｶﾀｶﾅ":
        assert is_asian(char), ord(char)

def test_is_asian_hiragana():

    for char in u"ひらがなあいうえおかきくけこ":
        assert is_asian(char), ord(char)

def dest_is_asian_katakana():

    for char in u"カタカナアメリカヨーロッパ":
        assert is_asian(char), ord(char)

def dest_is_asian_jpunct():

    for char in u"。「」『』【】、，．（）・／":
        assert is_asian(char), ord(char)

def test_is_asian_ascii():
    for char in u"AZ!.\n~()'&%$#'":
        assert not is_asian(char), char

def test_assumption_about_spaces():
    assert unichr(0x3000).isspace()


def test_nonj_Len():
    assert nonj_len(u"日本語AアジアンB") == 2
    assert nonj_len("hello") == 1
    assert nonj_len(u"日本") == 0

def test_filter_jchars_kanji():
    for char in KANJI:
        assert filter_jchars(char) == ' '

def test_filter_letters():
    for letter in string.letters:
        assert filter_jchars(letter) == letter, letter

def test_filter_digits():
    for digit in string.digits:
        assert filter_jchars(digit) == digit, digit

def test_filter_punct():
    for punct in string.punctuation:
        assert filter_jchars(punct) == punct, punct

def test_d2o():
    d = dict(a=1, b=2)
    obj = wordcount.dict2obj(d)
    assert obj.a == 1
    assert obj.b == 2

class TestGetWordcount(object):
    
    def test_one(self):
        wc = gwc("one")
        assert wc["characters"] == 3, wc
        assert wc["chars_no_spaces"] == 3, wc
        assert wc["asian_chars"] == 0, wc
        assert wc["words"] == 1, wc
        assert wc["non_asian_words"] == 1, wc

    def testJSentence(self):
        wc = gwc(u"本日晴天なり。")
        assert wc["characters"] == 7, wc
        assert wc["chars_no_spaces"] == 7, wc
        assert wc["asian_chars"] == 7, wc
        assert wc["words"] == 7, wc
        assert wc["non_asian_words"] == 0, wc

    def test_kanji(self):
        wc = gwc(KANJI)
        assert wc["characters"] == len(KANJI), wc
        assert wc["chars_no_spaces"] == len(KANJI), wc
        assert wc["asian_chars"] == len(KANJI), wc
        assert wc["words"] == len(KANJI), wc
        assert wc["non_asian_words"] == 0, wc

class TestGetWordcountObj(object):

    def testSimple(self):
        wc = gwo("foo")
        assert 1 == wc.words
        assert 3 == wc.characters
        assert 3 == wc.chars_no_spaces
        assert 0 == wc.asian_chars
        assert 1 == wc.non_asian_words

    def testSentence(self):
        wc = gwo("foo is a bar")
        assert 4 == wc.words
        assert 12 == wc.characters
        assert 9 == wc.chars_no_spaces
        assert 0 == wc.asian_chars
        assert wc.words == wc.non_asian_words

    def testJSentence(self):
        wc = gwo(u"本日晴天なり。")
        assert 7 == wc.words
        assert 7 == wc.characters
        assert 7 == wc.chars_no_spaces
        assert 7 == wc.asian_chars
        assert 0 == wc.non_asian_words

    def testempty(self):
        wc = gwo("")
        assert 0 == wc.words
        assert 0 == wc.characters
        assert 0 == wc.chars_no_spaces
        assert 0 == wc.asian_chars
        assert 0 == wc.non_asian_words

    def testOneWord(self):
        wc = gwo("foo")
        assert 1 == wc.words
        assert 3 == wc.characters
        assert 3 == wc.chars_no_spaces
        assert 0 == wc.asian_chars
        assert 1 == wc.non_asian_words

    def testSimpleSentence(self):
        wc = gwo("This is a simple sentence.")
        assert 5 == wc.words
        assert 26 == wc.characters
        assert 22 == wc.chars_no_spaces
        assert 0 == wc.asian_chars
        assert 5 == wc.non_asian_words

    def testSimpleSentenceWithJ(self):
        wc = gwo(u"This is a simple sentence. 日本語もある。")
        assert 12 == wc.words
        assert 34 == wc.characters
        assert 29 == wc.chars_no_spaces
        assert 7 == wc.asian_chars
        assert 5 == wc.non_asian_words

    def testPunctLine(self):
        wc = gwo(u"{|}C:\\dev\\c++\\WTL80_6137\\Samples\\WTLExplorer\\res\\WTLExplorer.ico{|}t{|}")
        assert 1 == wc.words
        assert 71 == wc.characters
        assert 71 == wc.chars_no_spaces
        assert 0 == wc.asian_chars
        assert 1 == wc.non_asian_words
            
    def testWordliness(self):
        """Make sure we get the same wordcount as MS Word for this."""
        
        text = u"""There was no time to waste (was there any?). The haste-making were-rats were upon the peaceful Ur*hamsters; and the destruction ? nay, the devoration ? was upon them, to the 2^4 and the 2-5th generations! (日本語も挿入しておく)"""
        wc = gwo(text)
        assert 47 == wc.words
        assert 217 == wc.characters
        assert 182 == wc.chars_no_spaces
        assert 10 == wc.asian_chars # 10 jibes with Word, but we are fudging Unicode
                                    # ndashes into single byte...
        assert 37 == wc.non_asian_words


