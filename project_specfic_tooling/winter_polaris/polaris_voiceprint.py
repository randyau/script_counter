#Functions to checkt he state of every voice line in a
#file and to match it against the accepted standard
import fileinput
import  pickle

file_list =[
'A01.txt',
'A02.txt',
'A03.txt',
'A04.txt',
'A05.txt',
'A06.txt',
'A07.txt',
'A08.txt',
'a09.txt',
'a10.txt',
'B01.txt',
'B02.txt',
'B03.txt',
'B04.txt',
'B05.txt',
'B06.txt',
'B07.txt',
'B08.txt',
'epilogue.txt',
]

#EXample: $user_voice("01tubaki_0025");
def extract_voiceprint(file_directory, output_fn):
    #expected to read original script files
    vprint = {}
    for f in file_list:
      with open(file_directory+f, encoding='cp932') as ifile:
        for line in ifile:
          if "VoiceCommand" in line: continue #skip the initial voice def
          if "$user_voice" in line:
          #we only care about voice lines
              voicefile = line.split('"')[1]
              if line[0] == "$":
                  comment_state = ""
              elif line[:4] == '////':
                  comment_state = "////"
              elif line[:2] == '//':
                  comment_state = "//"
              else:
                  comment_state = "PARSE_ERR"
                  print ("Error:", line)
              vprint[voicefile] = comment_state
    out = open(output_fn,'wb')
    pickle.dump(vprint, out)

if __name__=="__main__":
  extract_voiceprint("orig/", "original_voices.pickle")
  extract_voiceprint("orig_w_voice/", "with_voices.pickle")
