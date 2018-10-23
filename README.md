# script_counter
Counting asian characters in files

Usage:
====

cat original0* | python2.7 jp_wordcounter.py -c comment_chars -e shift_jis

Sometimes need to use iconv to work around weird issues with bad encoding characters...
cat orig/*.txt|iconv -f shift_jis -t utf-8 |python2.7 ~/code/script_counter/jp_wordcounter.py -c ~/code/script_counter/comment_chars -e utf-8

