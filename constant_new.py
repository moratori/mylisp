#!/usr/bin/env python
#coding:utf-8

#グローバル変数
GLOBAL_VALUE = {}


#コメントは何ではじまるか
COMMENT = "#"

#文字列用
D_QUOTE = "\""

#評価を避ける記号
QUOTE     = "\'"

#括弧の定義
R_BACKET  = "("
L_BACKET  = ")"

#無限大の定義
inf = float("inf")

#ファイルからS式を呼んだ時の形の整形用
EOL_PATTERN = " \t\n"

#真偽値の定義
TRUE = "true"
FALSE = "nil"
FALSE_ = "()"


#型の名前
LIST = "list"
BOOLEAN = "boolean"
FUNCTION = "function"
INT = "int"
LONG = "long"
FLOAT = "float"
STRING = "string"
SYMBOL = "symbol"




#エラー文
ERROR = {\
    "FUNC_UNDEF": "Error: undefined function name %s" , 
    "FUNC_ARGST": "Error: %s function takes %s arguments" ,
    "NO_VAL"    : "Error: variable %s has no value" ,
    "VAL_UNDEF" : "Error: variable %s can not be used",
    "NOT_SYMBL" : "Error: %s is not a symbol",
}

SP_FUNC = 0
FUNC_INS = 1
SCOPE = 2



