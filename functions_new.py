#!/usr/bin/env python
#coding:utf-8

import main as pr
import constant_new as const
import math
import sys


def functionisntace(func):
    if pr.W_isfunction(func):
        return func
    elif (func in const.GLOBAL_VALUE) and (pr.W_isfunction(const.GLOBAL_VALUE[func])):
        return functionisntace(const.GLOBAL_VALUE[func])
    elif func in FUNCTIONS:
        return functionisntace(FUNCTIONS[func][1])
    else:
        raise pr.Error(const.ERROR["FUNC_UNDEF"]%(func))


#(define fact (n) (if (= n 0) 1 (* n (fact (- n 1)))))
#funcname = "fact"
#["fact" , "(n)" , "(if ..)" , scope]
#(define fact (n))

#こいつが関数の実態
#(True,(lambda *arg:pr.eval(body,scope=pr.joindict({e:arg[i]for i,e in enumerate(pr.tokenize(argv))},scope))))
def makefunc(dmyarg ,body,scope):

    def FUNCTION(*arg):
        #ここで束縛されるargは実引数となる
        #dmyargは"(x , y , z)"みたいな仮引数
        if dmyarg == "nil": 
            lst = [pr.eval(each , scope) for each in body]
        else:
            s = pr.joindict({e:arg[i]for i,e in enumerate(pr.tokenize(dmyarg))},scope) 
            lst = [pr.eval(each , s) for each in body]
        return lst.pop()

    return FUNCTION

#(define fname (arg))
def define(*arg):
    if len(arg) < 3:raise pr.Error(const.ERROR["FUNC_ARGST"] %("define" , "more than 2"))

    scope = arg[len(arg)-1]

    fname = arg[0]
    argv  = arg[1]
    body  = arg[2:len(arg)-1]
    
    if not pr.issymbol(fname) :
        raise pr.Error(const.ERROR["NOT_SYMBL"]%(fname))
    
    #引数を全て評価するような関数しかユーザ定義ではできない
    #スコープも得れない
    FUNCTIONS[fname] = (True , makefunc(argv , body , scope) , False) 
    return fname

#(defconst SYMBOL VALUE)
def defconst(symbol , value , scope):
    if not pr.issymbol(symbol):raise pr.Error(const.ERROR["NOT_SYMBL"]%(symbol))


    if symbol in const.GLOBAL_VALUE:return const.GLOBAL_VALUE[symbol]

    val = pr.eval(value,scope) 
    const.GLOBAL_VALUE[symbol] = val
    return val

#printが関数じゃないからしょうがなく定義
def show(exp):
    print exp
    return exp


#リストを作る関数
def makelist(*seq):
    return pr.evalconst(const.R_BACKET + reduce((lambda x,y: str(x) + " " + str(y)) , seq , "").strip(" ") + const.L_BACKET)[0]


#(lambda(x)x)
#('(x)', 'x', {})
#(lambda(x)(print x)(print x))
#('(x)','(print x)' , '(print x)',{})
#(lambda(x))
def lmd(*arg):

    if len(arg) < 2 : raise pr.Error(const.ERROR["FUNC_ARGST"] %("lambda" , "more than 1" ))

    scope = arg[len(arg)-1]
    argv  = arg[0]
    body  = arg[1:len(arg)-1]

    return makefunc(argv , body , scope)
    

def last(lst):
    l = pr.tokenize(lst)
    #nilだったらnil
    return const.FALSE if l[0] == "" else l[len(l)-1]

def init(lst):
    l = pr.tokenize(lst)
    return apply(makelist , l) if l[0] == "" else apply(makelist , l[0:len(l)-1])

def map_(func , lst ):
    l = pr.tokenize(lst)
    #nilだったらnil
    if l == [""] : return const.FALSE
    #tokenizeでばらした要素そのままでは文字列のままである
    return apply(makelist , map(functionisntace(func) , pr.mapevalconst(l)))


def filter_(func , lst):
    l = pr.tokenize(lst)
    if l == [""] : return const.FALSE
    return apply(makelist , [elm for elm in pr.mapevalconst(l) if pr.booltopy(functionisntace(func)(elm))])


def fin():
    print "bye!"
    sys.exit()


def eval(*arg):
    return pr.eval(arg[0] , arg[1])


#{関数名: (引数を評価していいか , 関数の実態 , scopeが欲しいか)}
#評価しないFalseな関数にはscopeが与えられる
FUNCTIONS = {\
    "sin"     :(True , math.sin , False), 
    "cos"     :(True , math.cos , False),
    "tan"     :(True , math.tan , False),
    
    "+"       :(True , (lambda *arg: reduce((lambda x,y: x+y) , arg)) , False),
    "-"       :(True , (lambda *arg: reduce((lambda x,y: x-y) , arg)) , False),
    "*"       :(True , (lambda *arg: reduce((lambda x,y: x*y) , arg)) , False),
    "/"       :(True , (lambda *arg: reduce((lambda x,y: x/y) , arg)) , False),
    ">"       :(True , (lambda x,y: pr.booltolisp(x>y)) , False),
    ">="      :(True , (lambda x,y: pr.booltolisp(x>=y)), False),
    "<"       :(True , (lambda x,y: pr.booltolisp(x<y)) , False),
    "<="      :(True , (lambda x,y: pr.booltolisp(x<=y)) , False),
    "="       :(True , (lambda x,y: pr.booltolisp(x == y)) , False),
    "and"     :(True , (lambda x,y: pr.booltolisp(pr.booltopy(x) and pr.booltopy(y))) , False),
    "or"      :(True , (lambda x,y: pr.booltolisp(pr.booltopy(x) or pr.booltopy(y))) , False),
    "not"     :(True , (lambda x: pr.booltolisp(not pr.booltopy(x)) ) , False),
  
    "cons"    :(True , (lambda x,y: apply(makelist,[x] + pr.tokenize(y))) , False),
    "car"     :(True , (lambda x:pr.tokenize(x)[0]) , False),
    "cdr"     :(True , (lambda x:apply(makelist ,pr.tokenize(x)[1:])) , False),
    "list"    :(True , makelist , False),
    "last"    :(True , last , False),
    "length"  :(True , (lambda x: len(pr.tokenize(x))) , False),
    "init"    :(True , init , False),
    "map"     :(True , map_ , False),
    "filter"  :(True , filter_  , False),

    "list?"   :(True , (lambda x:pr.booltolisp(pr.W_islist(x))) , False),
    "atom?"   :(True , (lambda x:pr.booltolisp(pr.W_isatom(x))) , False),
    "symbol?" :(True , (lambda x:pr.booltolisp(pr.W_issymbol(x))) , False),
    "null?"   :(True , (lambda x:pr.booltolisp(pr.W_isnil(x))) , False),
    "equal?"  :(True , (lambda x,y: pr.booltolisp(x == y)) , False),
    
    "print"   :(True , (lambda x: show(x)) , False),
    "define"  :(False , define , False),
    "defconst":(False , defconst , False),
    "lambda"  :(False , lmd , False),
    "if"      :(False , (lambda c,x,y,s: pr.eval(x,s) if pr.booltopy(pr.eval(c,s)) else pr.eval(y,s)) , False),

    "eval"    :(True , eval ,True),

    "exit"    :(True , fin , False)
}



