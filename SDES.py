#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 20:57:43 2019
..
@author: martin
"""

import fileinput

def GetSubKeys(key):
    Permuted_Key = permut ([2,4,1,6,3,9,0,8,7,5], key)
    
    #split in half
    key_half_1 = Permuted_Key[:5]
    key_half_2 = Permuted_Key[5:]
    
    #generate subkey 1
    #one shift to the left
    key_half_1 = permut([1,2,3,4,0], key_half_1)
    key_half_2 = permut([1,2,3,4,0], key_half_2)
    key = (key_half_1 + key_half_2)
    subkey_1 = permut([5,2,6,3,7,4,9,8], key)
    
    #Generate subkey 2
    key_half_1 = permut([2,3,4,0,1], key_half_1)
    key_half_2 = permut([2,3,4,0,1], key_half_2)
    key2 = (key_half_1 + key_half_2)
    subkey_2 = permut([5,2,6,3,7,4,9,8], key2)
    
    return subkey_1, subkey_2


#permut 
def permut(new_positions, original_bits):
    new_bits = []
    for i in new_positions:
        new_bits.append(original_bits[i])
    return ''.join(map(str, new_bits))
  
    
def Int_str(str1, str2):
    return int(str1, base=2) ^ int(str2, base=2)

  
def feistel(permutedText, subkey, s_box0, s_box1):
    left = permutedText[:4]
    right = permutedText[4:]
    exp_right = permut([3,0,1,2,1,2,3,0],right)

    xor_right = Int_str(exp_right, subkey)
    xor_right = format(xor_right, '08b')

    row = int(permut([0,3], xor_right[:4]), base=2)
    col = int(permut([1,2], xor_right[:4]), base=2)
    s0 = s_box0[row][col]

    row = int(permut ([0,3], xor_right[4:]), base=2)
    col = int(permut ([1,2], xor_right[4:]), base=2)
    s1 = s_box1[row][col]

    s0s1 = format(s0, '02b')+format(s1, '02b') 
    s0s1 = permut([1,3,2,0], s0s1)
    xor_left = Int_str(left, s0s1)
    xor_left = format(xor_left, '04b')
    return xor_left, right
   
    


def main():

    file_input = fileinput.input()
    mode = file_input[0]
    mode = mode.replace('\n','')

    key = file_input[1]
    key = key.replace('\n','')
    
    Text = file_input[2]
    Text = Text.replace('\n','')
    
    
    
    s_box0 = [[1,0,3,2],[3,2,1,0],[0,2,1,3],[3,1,3,2]]
    s_box1 = [[0,1,2,3],[2,0,1,3],[3,0,1,0],[2,1,0,3]]
    
    if (mode == 'E'):
        SubKey1, SubKey2 = GetSubKeys(key)
    else:
        SubKey2, SubKey1 = GetSubKeys(key)
    
    permutedText = permut([1,5,2,0,3,7,4,6], Text)
    left, right = feistel(permutedText, SubKey1, s_box0, s_box1)
    right_left = right+left
    left, right = feistel(right_left, SubKey2, s_box0, s_box1)
    left_right = left+right
    inverse = permut([3,0,2,4,6,1,7,5],left_right)
    print(inverse)
        

if __name__ == "__main__":
	main()
