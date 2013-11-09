#!/usr/bin/env python
#coding:utf-8

import constant_new as const
import functions_new as func
import types
import os
import sys

function = types.FunctionType
functionb = types.BuiltinFunctionType

def W_isatom(exp):
    _ , typ = evalconst(exp)
    return True if typ != const.LIST else False

def W_islist(exp):
    return not W_isatom(exp)

def W_isnil(exp):
    value ,typ = evalconst(exp)
    return True if typ == const.BOOLEAN and value == const.FALSE else False 

def W_isstring(exp):
    _ , typ = evalconst(exp)
    return True if typ == str else False 

def W_issymbol(exp):
    _ , typ = evalconst(exp)
    return True if typ == const.SYMBOL else False

def W_isbool(exp):
    _ , typ = evalconst(exp)
    return True if typ == const.BOOLEAN else False

def W_isfunction(exp):
    return isinstance(exp , function) or isinstance(exp , functionb)

#string1がstring2だけでなるか
def consis(str1 , str2):
    if str1 == "":
        return False
    elif len(str1) == 1:
        return True if str1[0] == str2 else False
    else:
        return False if str1[0] != str2 else consis(scdr(str1) , str2)

#文字列の先頭を返す
def scar(exp):return "" if exp == "" else exp[0]

#文字列の先頭以外を返す
def scdr(exp):return "" if exp == "" else exp[1:]

#文字列の最後を返す
def slast(exp):return exp[len(exp)-1]

#expの最初と最後がcarとlastである
def andeq(exp , car , last):return (scar(exp) == car) and (slast(exp) == last)

#辞書をくっつける.同一のキーがある場合は1番目が優先
def joindict(dic1 , dic2):
    for key in dic2:
        if not key in dic1:dic1[key] = dic2[key]
    return dic1

#nilであるか
def isnil(exp):
    #真偽値の定義からnilならnil
    if   exp == const.FALSE:
        return True
    #空のリストもnilとする
    elif exp == const.FALSE_:
        return True
    #空白が無駄に含まれていた場合. (          )
    elif andeq(exp , const.R_BACKET , const.L_BACKET) and exp[1] == " ":
        return isnil(const.R_BACKET + scdr(scdr(exp)))
    else:
        return False

#Lisp処理系の中で文字列となるか
def isstring(exp):
    #文字列ならば必ず最初と最後がダブルクォート
    #2文字以下なら無条件でアウト
    return False if (len(exp) < 2) or (not andeq(exp , const.D_QUOTE , const.D_QUOTE)) else True

#アトムであるか
def isatom(exp):
    #文字列なら無条件でアトム
    if isstring(exp):
        return True
    #'Aは(quote A)の略称なので
    elif scar(exp) == const.QUOTE :
        return False
    #括弧が含まれてなければアトム.シンボルとか
    elif (exp.find(const.R_BACKET) == -1) and (exp.find(const.L_BACKET) == -1):
        return True
    else:
        return False

#リストか否か
def islist(exp):return not isatom(exp)

#symbolかどうか
def issymbol(exp):
    return True if evalconst(exp)[1] == const.SYMBOL else False

def isquoted(exp):return True if exp[0] == const.QUOTE else False


#真偽値か否か
def isbool(exp):return (exp == const.TRUE) or (isnil(exp))


#リストをevalconstしたリストを返す
def mapevalconst(lst):return [evalconst(each)[0] for each in lst]

#リストを全てevalする
def mapeval(lst , scope):return [eval(each , scope) for each in lst]

#アトムとか真偽値とかの定数を評価する
def evalconst(exp):
    if W_isfunction(exp):return exp , const.FUNCTION
    exp = str(exp)
    if isbool(exp):
        if isnil(exp):
            return const.FALSE , const.BOOLEAN
        else:
            return const.TRUE , const.BOOLEAN
    if islist(exp):return exp , const.LIST
    if isstring(exp):return str(exp) , str
    #数かシンボルか
    try:
        float(exp)
        #実数か整数
        try:
            val = int(exp)
            if isinstance(val , int):
                return int(exp) , int
            else:
                #明示的にLがついてない場合の長整数をみつける
                return long(exp) , long
        except:
            return float(exp) , float
    except:
        #ここにきたなら長整数かシンボル
        try:
            long(exp)
            return long(exp) , long
            #長整数ただし、明示的にLのついてるものとする
        except:
            #ここにきたならシンボル
            return exp , const.SYMBOL

#文字列のリストをパーサにかける
def part(exp):
    ins = SexpressionParser(exp)
    argv = ins.argv[0:len(ins.argv)-1]
    return ins.car , argv

#関数名部と引数部にわけない
def tokenize(exp):
    car , cdr = part(exp)
    cdr.insert(0,car)
    return cdr



#引数を評価して普通に実行
def exec_nf(fname , argv , scope):
    if func.FUNCTIONS[fname][const.SCOPE]:
        tmp = [eval(each , scope) for each in argv]
        tmp.append(scope)
        return apply(func.FUNCTIONS[fname][const.FUNC_INS] , tmp)
    else:
        return apply(func.FUNCTIONS[fname][const.FUNC_INS] , [eval(each , scope) for each in argv])


#引数を評価しないで関数の実行. 文字列のリスト"(+ 1 2 3)"みたいのが渡る
def exec_sf(fname , argv , scope):
    argv.append(scope)
    return apply(func.FUNCTIONS[fname][const.FUNC_INS] , argv)

#関数を実行
def exec_f(fname , argv , scope):
    fname = eval(fname , scope)
    if (not fname in func.FUNCTIONS) and (not isinstance(fname , function)) : 
        raise Error(const.ERROR["FUNC_UNDEF"] %(fname))
    if isinstance(fname , function):
        #ラムダでfnameには関数の自体が入ってるはず
        return apply(fname , [eval(eacharg , scope) for eacharg in argv])
    if func.FUNCTIONS[fname][0]:
        return exec_nf(fname , argv , scope)
    else:
        return exec_sf(fname , argv , scope)



#eval("(+ x y z)" , {"x": 1 , "y": 2 , "z": 3})
#eval("(fact x)" , {"x": 5})
def eval(exp , scope = const.GLOBAL_VALUE):
    value , typ = evalconst(exp)
    #アトムは評価してもそのまま
    if typ != const.SYMBOL and typ != const.LIST:return value
    
    # これ以降スコープを考慮した評価を行う必要がある
    # 特にシンボルについて

    #nilで無いリスト
    if typ == const.LIST:
        #クォートの除去
        if isquoted(exp):return scdr(exp)
        (fname , arg) = part(exp)
        return evalconst(exec_f(fname , arg , scope))[0] 
    elif typ == const.SYMBOL:
        if not exp in scope:
            #スコープ内で定義されてないシンボル名だけど実は関数名だった場合
            if exp in func.FUNCTIONS:
                return exp
            else:
                raise Error(const.ERROR["NO_VAL"] %exp)
        else:
            return evalconst(scope[exp])[0]
    else:
        pass




#真偽値の変換
def booltolisp(boolean): return const.TRUE if boolean else const.FALSE

#真偽値の変換
def booltopy(boolean) : return False if boolean == const.FALSE else True

#ファイルからn個のS式を読む
def filereader(filepath):
    #n個のS式を返す
    code = \
    [each for each in  [eachline.strip(const.EOL_PATTERN) for eachline in open(os.path.expanduser(filepath)).readlines() ] if each != "" and each[0] != const.COMMENT] 
    result= []
    fix = ""
    fixflag = 0
    for each in code:
        if isatom(each) and fixflag == 0:
            result.append(each)
        #整形の必要のないS式
        elif (each.count(const.R_BACKET) == each.count(const.L_BACKET)) and fixflag == 0:
            result.append(each)
        #整形が必要なS式
        else:
            fix += each + " "
            if fix.count(const.R_BACKET) == fix.count(const.L_BACKET):
                fixflag = 0
                result.append(fix.strip(const.EOL_PATTERN))
                fix = ""
            else:
                fixflag = 1    
    return result


#debug用
def Debug(exp):SexpressionParser(exp).debug()

#例外の送出クラス
class Error(Exception):
    def __init__(self , message):
        self.message = message
    def __str__(self):
        return repr(self.message)


#S式パースするクラス
class SexpressionParser:

    def __init__(self , expr_string):
        self.expr   = expr_string
        self.isnil  = isnil(self.expr)
        self.isatom = isatom(self.expr)
        self.length = len(self.expr)
        self.qtflg  = False
        self.car    = self.getcar()
        self.argv   = self.getargv()

    def debug(self):
        print "EXPR: %s"     %(self.expr)
        print "EXPR LEN: %s" %(self.length)
        print "ISATOM: %s"   %(self.isatom)
        print "ISNIL: %s"    %(self.isnil)
        print "CAR: \"%s\""  %(self.car)
        print "CDR: %s"      %(self.argv)
        print 

    def getcar(self):
        if self.isatom:return ""
        if self.isnil: return const.FALSE

        result = "" 
        backf  = 0
        dblqt  = False
        cnt    = 1
        escp   = 0
        first  = True 
      
        #糖衣構文クォートの特殊用
        if self.expr[0] == const.QUOTE:
            self.qtflg = True
            self.argv  = [scdr(self.expr) , const.FALSE] 
            return const.QUOTE
        
        while self.length - 1> cnt :
            char = self.expr[cnt:cnt+1]

            #先頭の空白を除去するため
            if first and char == " ":
                cnt += 1
                continue
            else:
                first = False

            if ((char==const.R_BACKET)and(backf == 0))and(not dblqt)and(result != "")and(not consis(result , const.QUOTE)):break


            if char == const.R_BACKET:backf += 1
            if char == const.L_BACKET:backf -= 1

            if char == const.D_QUOTE and (escp == 0) : dblqt = not dblqt
            escp = 1 if char == "\\" else 0
            if ((char == " ") and (backf == 0)) and (not dblqt):break
            result += char 
            if ((char == const.L_BACKET) and (backf == 0)) and (not dblqt) and (result != ""):break
            cnt += 1
        return result
 
    def getargv(self):
        result = []        
        if self.qtflg:return self.argv 
        if self.isatom or isnil(self.expr):return result
        nxt = const.R_BACKET + self.expr[self.expr.find(self.car)+len(self.car):]
        ins = SexpressionParser(nxt)
        result.append(ins.car)
        result.extend(ins.argv)
        return result

def test(codelst):
    for each in map(eval , codelst):print each

def main():
    if len(sys.argv) > 1:
        map(eval , filereader(sys.argv[1]))
    else:
         while True:
            try:
                print eval(raw_input(">>> "))
            except Exception,i:
                print i.message

if __name__ == "__main__" : main()



