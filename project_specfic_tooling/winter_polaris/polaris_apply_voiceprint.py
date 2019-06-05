import fileinput
import os
import pickle

FILE_LIST =[
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

#Example: $user_voice("01tubaki_0025");

def apply_voiceprint(ifile,ofile,vprint):
  """Reads line in ifile, applies voiceprint and writes to ofile"""
  for line in ifile:
    if "VoiceCommand" in line:
     writeline = line
    elif "$user_voice" in line:
      voicefile = line.split('"')[1]
      orig_comment_state = vprint[voicefile]
      raw_voiceline = '$user_voice("'+ voicefile + '");\n'
      if orig_comment_state == "":
        writeline= raw_voiceline
      elif orig_comment_state == "//":
        writeline = "////"+ raw_voiceline #denote originally commented w/ quadcomment
      elif orig_comment_state == "////":
        writeline = "//////" + raw_voiceline #pathological state, shouldn't see quad
      else:
        print("Error on", line)
        writeline = line
    else:
      writeline = line
    ofile.write(writeline)



if __name__ == '__main__':
  SOURCE_DIR="translated/"
  OUT_BASE_DIR="voiceprinted/"
  ORIG_DIR="originalvoice/"
  WITH_DIR="withvoice/"
  cmds = [OUT_BASE_DIR,
    OUT_BASE_DIR+ORIG_DIR,
    OUT_BASE_DIR+WITH_DIR]
#just brute force make the output directories
  for cmd in cmds:
    try:
      os.mkdir(cmd) 
    except:
      pass

  #First do this for orig voices
  p_no_voice = pickle.load(open("original_voices.pickle",'rb'))
  for fn in FILE_LIST: 
    ifile = open( SOURCE_DIR+fn, 'r', encoding='cp932')
    ofile = open( OUT_BASE_DIR+ORIG_DIR+fn,'w',encoding='cp932',newline='\r\n')
    voiceprint = p_no_voice
    apply_voiceprint(ifile,ofile,voiceprint)
  
  #First do this for orig voices
  p_with_voice = pickle.load(open("with_voices.pickle",'rb'))
  for fn in FILE_LIST: 
    ifile = open( SOURCE_DIR+fn, 'r', encoding='cp932')
    ofile = open( OUT_BASE_DIR+WITH_DIR+fn,'w',encoding='cp932',newline='\r\n')
    voiceprint = p_with_voice
    apply_voiceprint(ifile,ofile,voiceprint)
  print("Done! =D")
