import ox
import operator as op

#r'[0-9]' = \d
#r'[-+*/] -> o '-' deve vir primeiro pois ele eh um caracter especial.
lexer = ox.make_lexer([
    ('NUMBER', r'\d+(\.\d*)?(e\d*)?'), 
    ('OP_S', r'[-+]'),
    ('OP_M', r'[*/]'),
    ('OP_N', r'[\^]'),
    ('L_PAR', r'\('),
    ('R_PAR', r'\)'),
    ('BOING', r'boing')
    ])

tokens_list = ['NUMBER', 'OP_S', 'OP_M', 'OP_N', 'L_PAR', 'R_PAR', 'BOING']

#Simbolo terminal(NUMBER) significa que nao tem mais como ser processada mais.
#Um token de NUMBER vai ser jogada na func e vai retornar um atom
#NUMBER eh uma string, deve ser convertida para numero. A funcao (float) ira fazer isso.

#Compilador faz uma serie de passos apos a analise sintatica -> analise semantica(verificacao de erros e etc) geracao de codigo para uma segunda linguagem, otimizacao... E interpretador apenas interpreta oq foi obtido a partir da AST.

#AST -> Abstract sintatic tree
infix = lambda x, op, y: (op, x, y) #Funcao apenas para reordenar para ser infix -> Ex: + 1 2
par = lambda left, expr, right: (expr)
atom = lambda x: ('atom', float(x))
bloing = lambda a,b,x,y,c: ('atom', (sum(range(int(
parser = ox.make_parser([
    ('boing : BOING L_PAR expr expr R_PAR', bloing),
    ('expr : expr OP_S term', infix),
    ('expr : term', lambda x: x), #Nao faz nada demais, apenas retorna o atomo.
    ('term : term OP_M term', infix),
    ('term : pot', lambda x: x),
    ('pot : pot OP_N expr', infix),
    ('pot : par', lambda x: x),
    ('par : L_PAR expr R_PAR', par),
    ('par : atom', lambda x: x),
    ('atom : NUMBER', atom),
], tokens_list)

OP_TO_FUNC = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
    '^': lambda x,y: x ** y,
}

def :
    head, *tail = ast
    if head == 'atom':
        return tail[0]
    elif head in ['+', '-', '*', '/', '^']:
        func = OP_TO_FUNC[head]
        #map retorna um objeto map, ele eh do tipo lazy map no sentido em que ele apenas executa quando eh necessario, ou seja, quando transforma esse objeto map retornado em uma lista.
        #map recebe uma funcao e uma ou mais lista de argumentos, e utilizado abaixo ele retorna uma lista sendo que cada elemento dessa lista eh uma aplicacao da funcao eval a um elemento da lista tail.
        #eval usado abaixo eh uma funcao built-in do python que recebe uma string e retorna o calculo que essa string representa.
        x, y = map(eval, tail) 
        return func(x, y)
    else:
        raise ValueError('operador invalido: %s'%(head))


expr = input('expr: ')
tokens = lexer(expr)
tree = parser(tokens)
print('tokens: ', tokens)
print('arvore sintatica(AST): ', tree)