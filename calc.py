###################################
####    Scientfic Calculator   ####
####    Written by Zijian Yao  ####
####    TextUI:  for testing   ####
###################################

from parser import lexer, acc
from convert import converter
while True:
    res = ''
    try:
        s = input('calc > ') 
    except EOFError:
        break
    try:
        lexer.input(s)
        print([(tok.type, tok.value) for tok in lexer])
    except:
        print('Lex Error')
        continue
    else:
        try:
            res = str(acc.parse(s))
            print(res)
        except SyntaxError:
            print('Invalid Syntax')
            continue        
        except:
            print('Value Error')
            continue
        else:
            try:
                print(converter.parse(res))
            except:
                pass