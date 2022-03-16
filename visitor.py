if __name__ is not None and "." in __name__:
    from .logo3dParser import logo3dParser
    from .logo3dVisitor import logo3dVisitor
    from turtle3d import Turtle3D
else:
    from logo3dParser import logo3dParser
    from logo3dVisitor import logo3dVisitor
    from turtle3d import Turtle3D


class visitor(logo3dVisitor):
    def __init__(self, name, arguments):
        '''
        Constructora del visitor

        Atributs:
            stack: pila de memòries per guardar el context de cada procediment.
            startingProc: procediment incial a executar.
            procs: llista amb tots els procediments del programa.
            turtle: tortuga que permet dibuixar les escenes.
        '''
        self.__stack = []
        self.__startingProc = name
        self.__stack.append(arguments)
        self.__procs = None
        self.__turtle = Turtle3D()

    def visitProgram(self, ctx):
        '''
        Arrel del AST, en aquesta funcio comprovem que no hi han procediments repetits
        o redefincions de procediments propis de la classe Turtle3D; si no hi han problemes
        es comença amb l'execució del programa.
        '''
        self.__procs = list(ctx.getChildren())
        funcNames = []
        i = 0
        n = len(self.__procs) - 1
        index = -1
        while i < n:
            name = list(self.__procs[i].getChildren())[1].getText()
            if name in funcNames:
                raise SystemExit(
                    "Multiple declarations of procedure: '" + name + "'")
            elif self.__isTurtleProcedure(name):
                raise SystemExit(
                    "Redeclaration of Turtle3D procedure: '" + name + "'")
            else:
                funcNames.append(name)
                if name == self.__startingProc:
                    index = i
            i += 1
        funcNames = None
        '''
        Aquí comprovem si hem trobat el index del métode pricipal del programa, o bé
        si aquest és directament una crida a un métode de la tortuga; si no és cap abortem.
        '''
        if (index != -1):
            self.visit(self.__procs[index])
        elif self.__isTurtleProcedure(self.__startingProc):
            self.__executeTurtleProcedure(self.__startingProc)
        else:
            raise SystemExit("Undeclared procedure: '" +
                             self.__startingProc + "'")

    def visitProcedure(self, ctx):
        '''
        Funcio que visita el Node d'un procediment, comprovem que el nombre d'arguments
        coincideix amb la seva declaració altrament abortem; si tot funciona be preparem la
        memoria contextual i avaluem el bloc del procediment.
        '''
        children = list(ctx.getChildren())
        parameters = []
        arguments = self.__stack.pop()
        if len(children) > 7:
            parameters = self.visit(children[3])
        if len(parameters) != len(arguments):
            raise SystemExit(
                "Number of arguments does not match definition of procedure '" + children[1].getText() + "'")
        else:
            memory = dict()
            '''
            Aquí fem la copia dels arguments que estan al top de la pila en una llista
            a un mapa on tenim el parell Identificador-Valor.
            '''
            for i in range(len(parameters)):
                memory[parameters[i]] = arguments[i]
            self.__stack.append(memory)
            parameters = arguments = None
            if len(memory) == 0:
                self.visit(children[5])
            else:
                self.visit(children[6])
            self.__stack.pop()

    def visitParameters(self, ctx):
        '''
        Funció que s'encarrega d'obtenir el idetificador de cada parametre i comprovar
        que no esta repetit.
        '''
        children = list(ctx.getChildren())
        parameters = []
        while True:
            if children[0].getText() in parameters:
                raise SystemExit("Multiple declarations of parameter '" +
                                 children[0].getText() + "' in procedure")
            else:
                parameters.append(children[0].getText())
            if len(children) > 1:
                children = list(children[2].getChildren())
            else:
                break
        return parameters

    def visitBlock(self, ctx):
        '''
        Funció que visita totes les instrucions de un bloc i les executa.
        '''
        for i in list(ctx.getChildren()):
            self.visit(i)

    def visitStatement(self, ctx):
        '''
        Funció que visita una instruccio i la executa segons quin tipus és.
        '''
        children = list(ctx.getChildren())
        try:
            '''
            Aquest try unicamet serveix per veure si estem en una regla o no ja que
            un statement pot ser simplment una declaració de variables i aquesta a la
            gramatica es solament un ID; si la variable ja estava declarada abortem.
            '''
            children[0].getSymbol().type
            memory = self.__stack.pop()
            if children[0].getText() is memory:
                raise SystemExit(
                    "Multiple declaration of variable '" + children[0].getText() + "' in procedure")
            else:
                memory[children[0].getText()] = 0
                self.__stack.append(memory)
        except SystemExit as ex:
            raise ex
        except Exception as ex:
            '''
            Si no era una excepció de SystemExit indica que el tipus del statement es regla
            per tant el avaluem.
            '''
            self.visit(children[0])

    def visitVarAssig(self, ctx):
        '''
        Assignació de valor a una variable.
        '''
        children = list(ctx.getChildren())
        memory = self.__stack.pop()
        self.__stack.append(memory)
        memory[children[0].getText()] = self.visit(children[2])

    def visitIo(self, ctx):
        '''
        Procediment de entrada/sortida, si es entrada llegim un real, si es sortida
        avaluem la expressió i la escrivim per pantalla.
        '''
        children = list(ctx.getChildren())
        if children[0].getSymbol().type == logo3dParser.RD:
            memory = self.__stack.pop()
            memory[children[1].getText()] = float(input())
            self.__stack.append(memory)
        else:
            print(self.visit(children[1]))

    def visitTerm(self, ctx):
        '''
        Funció que analitza un terme i retorna el seu valor, si era una variable
        consultem la memòria, si no existeix abortem, altrament retornem el seu valor;
        si era un numero el interpretem com a float i el retornem.
        '''
        children = list(ctx.getChildren())
        if children[0].getSymbol().type == logo3dParser.ID:
            memory = self.__stack.pop()
            value = memory.get(children[0].getText())
            if value is None:
                raise SystemExit("Undeclared variable '" +
                                 children[0].getText() + "'")
            else:
                self.__stack.append(memory)
                return value
        else:
            if len(children) == 1:
                return float(children[0].getText())
            else:
                return -float(children[1].getText())

    def visitCall(self, ctx):
        '''
        Aquesta funcio s'encarrega de executar les crides a procedimes del nostre progrmaa logo3d,
        primer obtenim els arguments, els deixem en una llista a la pila i seguidament comprovem
        si la crida és a un procediment de la tortuga o del programa.
        '''
        children = list(ctx.getChildren())
        if len(children) > 3:
            val = self.visit(children[2])
            self.__stack.append(val)
        if self.__isTurtleProcedure(children[0].getText()):
            self.__executeTurtleProcedure(children[0].getText())
        else:
            self.__findProcedure(self.__procs, children[0].getText())

    def visitArguments(self, ctx):
        '''
        Funcio que agrupa els arguments en una llista i els retorna.
        '''
        children = list(ctx.getChildren())
        arguments = []
        while True:
            arguments.append(self.visit(children[0]))
            if len(children) > 1:
                children = list(children[2].getChildren())
            else:
                break
        return arguments

    def visitConditional(self, ctx):
        '''
        Funcio que avalua un condicional, una vega avaluat actualitzem la memòria.
        '''
        children = list(ctx.getChildren())
        oldMemory = self.__stack.pop()
        self.__stack.append(self.__memoryCopy(oldMemory))
        if self.visit(children[1]) == 1:
            self.visit(children[3])
        elif len(children) > 5:
            self.visit(children[5])
        self.__updateStack(oldMemory, self.__stack.pop())

    def visitWhileLoop(self, ctx):
        '''
        Funcio que avalua un bucle, al final de cadaa iteració actualitzem les variables
        de la memòria que estaven presents ans del bucle.
        '''
        children = list(ctx.getChildren())
        oldMemory = self.__stack.pop()
        self.__stack.append(self.__memoryCopy(oldMemory))
        while self.visit(children[1]) == 1:
            self.visit(children[3])
            self.__updateStack(oldMemory, self.__stack.pop())
            oldMemory = self.__stack.pop()
            self.__stack.append(self.__memoryCopy(oldMemory))
        newMemory = self.__stack.pop()
        self.__updateStack(oldMemory, self.__stack.pop())

    def visitForLoop(self, ctx):
        '''
        Similar a la funció anterior, aquesta avalua un bucle for, inicialitza la variable
        de control i al final de cada iteració actualitza les variables que pertoquin. Cal
        mencionar que el for acepta que la variable de control sigui un real ja que als exmples
        tenim "FOR i FROM 1 TO costats DO", costats pot ser valor real ja que en logo tots els nombres
        son real així que he permés que es puguin fer coses del estil: "FOR i FROM 1.5 TO 7.7 DO",
        igualment el increment al final de la iteració, si no se ha alterat la i, serà 1.
        '''
        children = list(ctx.getChildren())
        oldMemory = self.__stack.pop()
        newMemory = self.__memoryCopy(oldMemory)
        self.__stack.append(newMemory)
        i = children[1].getText()
        newMemory[i] = int(self.visit(children[3]))
        n = int(self.visit(children[5]))
        while newMemory[i] <= n:
            self.visit(children[7])
            newMemory[i] = newMemory[i] + 1
            index = newMemory[i]
            self.__updateStack(oldMemory, self.__stack.pop())
            oldMemory = self.__stack.pop()
            newMemory = self.__memoryCopy(oldMemory)
            newMemory[i] = index
            self.__stack.append(newMemory)
        newMemory = self.__stack.pop()
        self.__updateStack(oldMemory, newMemory)

    def visitExpression(self, ctx):
        '''
        Avaluació d'una expressió aritmètica, si es una divisio per 0 abortem.
        '''
        children = list(ctx.getChildren())
        if len(children) == 1:
            return self.visit(children[0])
        elif children[0].getText() == '(':
            return self.visit(children[1])
        else:
            left = self.visit(children[0])
            op = children[1].getText()
            right = self.visit(children[2])
            if op == '*':
                return left * right
            elif op == '/':
                if right == 0:
                    raise SystemExit("Division by 0")
                else:
                    return left / right
            elif op == '+':
                return left + right
            else:
                return left - right

    def visitRelational(self, ctx):
        '''
        Avaluació d'una expressió booleana.
        '''
        children = list(ctx.getChildren())
        if len(children) == 1:
            value = self.visit(children[0])
            return 1 - int(value >= -1 * 10 ** -6 and value <= 10 ** -6)
        else:
            left = self.visit(children[0])
            op = children[1].getText()
            right = self.visit(children[2])
            if op == '<':
                return int(left < right)
            elif op == '>':
                return int(left > right)
            elif op == '<=':
                return int(left <= right)
            elif op == '>=':
                return int(left >= right)
            elif op == '==':
                return int(left == right)
            else:
                return int(left != right)

    def __findProcedure(self, procs, name):
        '''
        Funció que busca dins de la llista de procediments declarats el que volem executar,
        si no el trobem abortem la execució ja que no estaria declarat.
        '''
        found = False
        i = 0
        n = len(procs) - 1
        while i < n:
            if list(procs[i].getChildren())[1].getText() == name:
                self.visit(procs[i])
                found = True
                break
            i += 1
        if not found:
            raise SystemExit("Undeclared procedure: '" + name + "'")

    def __isTurtleProcedure(self, name):
        '''
        Funció la qual comprova si el procediment que volem executar és un métode de la classe tortuga.
        '''
        return name == "up" or name == "down" or name == "show" or name == "hide" or name == "left" or name == "right" or name == "home" or name == "color" or name == "forward" or name == "backward"

    def __executeTurtleProcedure(self, name):
        '''
        Funció que executa un procediment de la classe tortuga amb els sues paràmetres adients,
        aquests els obtenim de la pila.
        '''
        args = self.__stack.pop()

        if name == "up":
            self.__turtle.up(args[0])
        elif name == "down":
            self.__turtle.down(args[0])
        elif name == "left":
            self.__turtle.left(args[0])
        elif name == "right":
            self.__turtle.right(args[0])
        elif name == "show":
            self.__turtle.show()
        elif name == "hide":
            self.__turtle.hide()
        elif name == "home":
            self.__turtle.home()
        elif name == "color":
            self.__turtle.color(args[0], args[1], args[2])
        elif name == "forward":
            self.__turtle.forward(args[0])
        else:
            self.__turtle.backward(args[0])

    def __updateStack(self, old, new):
        '''
        Aquesta funcó s'encarreda de substituir totes els valors de les claus de la
        memoria old que estiguin presents en new, i restaura la memoria old a la pila;
        aquesta funció és crida després de haver evaluat condicionals, a finals de cada
        iteració de bulce, quan en sortim d'un o retornem d'una funció.
        '''
        for i in old:
            value = new.get(i)
            if value is not None:
                old[i] = value
        self.__stack.append(old)

    def __memoryCopy(self, mem):
        '''
        Funció que retorna una deep copy de la memòria parametre per a ser usada
        mes endavant en la la avaluació dels bucles, condiconals i funcions.
        '''
        newMem = dict()
        for i in mem:
            newMem[i] = mem[i]
        return newMem
