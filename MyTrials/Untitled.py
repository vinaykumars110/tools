# _*_ coding: utf-8 _*_

import ui
import re
import random
import speech

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Routines used in this code
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# what happens when 'Next' button is tapped 
def next_button_tapped(sender):
	global word_from_database
	word_from_database = get_random_word()
	text = word_from_database
	v['word'].text= text
	speech.say(text)
	v['pic'].image=ui.Image.named('')
	v['label'].text = ''
	
# what happens when 'Image' button is tapped
def image_button_tapped(sender):
	v['pic'].image=ui.Image.named(word_dict[word_from_database]['media'][0])
	text = word_dict[word_from_database]['slide1'][0]
	v['label'].text = text
	speech.say(text)
	

# what happens when 'Reveal' button is tapped
def reveal_button_tapped(sender):
	v['label'].text = word_dict[word_from_database]['slide2'][0]
	

	
def get_random_word():
	temp_word = random.sample(word_dict.keys(),1)[0]
	return temp_word

############################################
# Generate word database from the ppt file	
############################################

# Word Dictionary - word : word slides info
word_dict = {}

# Dictionary to hold slides info of each word
slide_dict = {'media':[],'slide1':[],'slide2':[]}

# file handle
f=open("collect_ppt_words.txt","r",encoding='utf-8') 
# check the encoding of the file
#print(f.encoding)
#print(f.read())

# Initial values for the variables
word_start = 0
word_finish = 0
word_begin = 0
media_begin = 0
slide1_text_begin = 0
slide2_text_begin = 0
key = ''

# Main iteration loop over each line
											
for linei in f:
  line = linei.rstrip()
  #print(line)
  if re.match('word_start',line):
    word_finish = 0
  if re.match('word_finish',line):
    word_start = 0
    word_finish = 1
  if re.match('word_end',line):
    word_begin = 0
  if re.match('media_end',line):
    media_begin = 0
  if re.match('slide1_text_end',line):
    slide1_text_begin = 0
  if re.match('slide2_text_end',line):
    slide2_text_begin = 0

  if word_start is 1:
    if word_begin is 1:
      key = line
  
  if word_finish is 1: 
     word_dict[key] = slide_dict
     slide_dict={'media':[],'slide1':[],'slide2':[]}
     #print(word_dict[key])

  if media_begin is 1:
    slide_dict['media'].append(line)

  if slide1_text_begin is 1:
    slide_dict['slide1'].append(line)

  if slide2_text_begin is 1:
    slide_dict['slide2'].append(line)

  if re.match('word_start',line):
    word_start = 1
    word_finish = 0
  if re.match('word_begin',line):
    word_begin = 1
  if re.match('media_begin',line):
    media_begin = 1
  if re.match('slide1_text_begin',line):
    slide1_text_begin = 1
  if re.match('slide2_text_begin',line):
    slide2_text_begin = 1																
# Complete Database is present in word_dict
#print(word_dict['wizened (adj)'])
																			
################################################# 
# Database generation complete
#################################################

															




v = ui.load_view('swipe')
v.background_color='black'
#pic=v['pic']
#pic.image=ui.Image.named('../media/image1.jpeg')

v.present('sheet')


