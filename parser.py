import nltk
from nltk.tokenize import RegexpTokenizer
import re
import sys
from Tree import TreeNode


inputProgram = input("Enter your program\n")

tk = RegexpTokenizer("#include|\d*[\.]\d+|[\w]+\.h|[\w]+|<=|>=|>|!=|!|<|==|[^ ]")




#print(inputProgram)

input_tokens = tk.tokenize(inputProgram)

#print(input_tokens)





keywordsRegex = "^int$|^double$|^float$|^while$|^#include$|^main$|^puts$"
headerfileRegex = "^[a-zA-Z]+\.[h]"
numbersRegex = "^\d*[\.]?\d+$"
arithmeticOperatorRegex = "[\+ \- \/ \*]" 
relationalOperatorRegex = "<|<=|>=|>|!=|==|!"
assignmentOperatorRegex = "^=$"
specialSymbolsRegex = "\#|\(|\)|\{|\}|\""
identifierRegex = "^[a-zA-Z_][a-zA-Z0-9]*$"



numbers = []
relationalOperators = []
arithmeticOperators = []
headerFiles = []
identifiers = []



print("\n")

for tokens in input_tokens:
    if(re.findall(keywordsRegex,tokens)):
        print(tokens,"\t<keyword>")

    elif(re.findall(headerfileRegex,tokens)):
        print(tokens,"\t<header-file>")
        headerFiles.append(tokens)

    elif(re.findall(numbersRegex,tokens)):
        print(tokens,"\t<positiveNumber-value>")
        numbers.append(tokens)

    elif(re.findall(relationalOperatorRegex,tokens)):
        print(tokens,"\t<relational-operator>")
        relationalOperators.append(tokens)

    elif(re.findall(arithmeticOperatorRegex,tokens)):
        print(tokens,"\t<arithmetic-operator>")
        arithmeticOperators.append(tokens)

    elif(re.findall(assignmentOperatorRegex,tokens)):
        print(tokens,"\t<assignment-operator>")

    elif(re.findall(identifierRegex,tokens)):
        print(tokens,"\t<identifier>")
        identifiers.append(tokens)

    elif(re.findall(specialSymbolsRegex,tokens)):
        print(tokens,"\t<special-symbol>")
    else:
        print(tokens,"\tToken not recognized")


# print(numbers)
# print(identifiers)
# print(headerFiles)
# print(relationalOperators)
# print(arithmeticOperators)

#SCANNER ENDS HERE
#PARSER BEGINS HERE

count = 0


ProgramTree = TreeNode("<program>")

#function to parse the entire program 
def ParseProgram():
    global input_tokens
    global count

    
    node1 = parseIncludes()
    node2 = parseMain()

    ProgramTree.addChild(node1)
    ProgramTree.addChild(node2)

    print("\n\n",repr(ProgramTree))

#mainNode = TreeNode("<main>")

def parseMain():
    global count
    global input_tokens
    
    mainNode = TreeNode("<main>")

    if(input_tokens[count]=="main"):
        node1 = TreeNode(input_tokens[count])
        mainNode.addChild(node1)



        count = count + 1

        node2 = parseOpeningBracket()
        mainNode.addChild(node2)
        

        node3 = parseClosingBracket()
        mainNode.addChild(node3)

        

        node4 = parseOpeningBrace()
        mainNode.addChild(node4)

      

        node5 = parseStatements()
        mainNode.addChild(node5)
        

        node6 = parseClosingBrace()
        mainNode.addChild(node6)

        if(count==len(input_tokens)):
            return mainNode
        elif(input_tokens[count]):
            print("Additional tokens detected at",input_tokens[count])
            sys.exit()

        return mainNode
       

        

    else:
        print("Expected main but got ",input_tokens[count])
        sys.exit()


statementsTree = TreeNode("<statements>")

def parseStatements():
    global count
    global input_tokens
    
    

    if(count == len(input_tokens)):
        print("Expected valid statement")
        sys.exit()
    elif(input_tokens[count]=="int" or input_tokens[count]=="float" or input_tokens[count]=="double" or input_tokens[count] in identifiers):
        try:
            node1 = parseAssignment()
            statementsTree.addChild(node1)
            return statementsTree
        except:
            print("Syntax error when assigning near ",input_tokens[count])
            sys.exit()
            
        finally:
            parseStatements()

    elif(input_tokens[count]=="while"):
        try:
            node2 = parseWhile()
            statementsTree.addChild(node2)
            return statementsTree
        except:
            print("Syntax error in while loop near",input_tokens[count])
            sys.exit()

        finally:
            parseStatements()

    elif(input_tokens[count]=="puts"):
        try:
            node3 = parsePuts()
            statementsTree.addChild(node3)
            return statementsTree
        
        except:
            print("Syntax error in puts statement near",input_tokens[count])
            sys.exit()
        finally:
            parseStatements()

    elif(input_tokens[count]=="}"):
        return TreeNode(" ")
    else:
        print("Syntax error.Expected a valid statement near ",input_tokens[count])
        sys.exit()



# putsTree = TreeNode("<puts>")

def parsePuts():
    global count
    global input_tokens

    
    putsTree = TreeNode("<puts>")


    if(count == len(input_tokens)):
        return putsTree
        
    elif(input_tokens[count]=="puts"):

        node1 = TreeNode(input_tokens[count])
        putsTree.addChild(node1)

        count = count + 1

        node2 = parseOpeningBracket()
        putsTree.addChild(node2)
       

        if(input_tokens[count] in identifiers or input_tokens[count] in numbers):
            
            node3 = TreeNode(input_tokens[count])
            putsTree.addChild(node3)

            count = count+1


            node4 = parseClosingBracket()
            putsTree.addChild(node4)

            return putsTree
            
            
            
        else:
            print("Expected number or identifier in  \'puts\' but got ",input_tokens[count])
            sys.exit()




# whileTree = TreeNode("<while>")

def parseWhile():
    global count

    global input_tokens


    whileTree = TreeNode("<while>")

    
    

    if(count == len(input_tokens)):
        return whileTree

    elif(input_tokens[count]=="while"):

        node1 = TreeNode(input_tokens[count])
        whileTree.addChild(node1)
        
        
        count = count + 1

        node2 = parseOpeningBracket()
        whileTree.addChild(node2)

        node3 = parseRelational()
        whileTree.addChild(node3)


        node4 = parseClosingBracket()
        whileTree.addChild(node4)
       
       

        node5 = parseOpeningBrace()
        whileTree.addChild(node5)

        

        node6 = parseWhileStatements()
        whileTree.addChild(node6)
        # print(repr(node6))

        

        node7 = parseClosingBrace() 
        whileTree.addChild(node7)


        return whileTree 


# whileStatement = TreeNode("<while-statements>")

def parseWhileStatements():
    global count
    global input_tokens

    whileStatement = TreeNode("<while-statements>")
    

    if(count == len(input_tokens)):
        return TreeNode(" ")
    while(input_tokens[count]=="int" or input_tokens[count]=="float" or input_tokens[count]=="double" or input_tokens[count]=="while" or input_tokens[count]=="puts" or input_tokens[count] in identifiers):

        if(input_tokens[count]=="int" or input_tokens[count]=="float" or input_tokens[count]=="double" or input_tokens[count] in identifiers):
            try:
                node1 = parseAssignment()
            # whileStatement.addChild(node1)
            

            # print(repr(TreeNode("while-statements").addChild(node1)))
            # return (TreeNode("<while-statements").addChild(node1))
            except:
                print("Syntax error when assigning near ",input_tokens[count])
                sys.exit()

            finally:
                whileStatement.addChild(node1)
                # parseWhileStatements()

        elif(input_tokens[count]=="while"):
            node2 = TreeNode(" ")
            try:
                node2 = parseWhile()
            # whileStatement.addChild(node2)
               
            # print(repr(TreeNode("while-statements").addChild(node2)))
            # return (TreeNode("<while-statements>").addChild(node2))
            except:
                print("Syntax error in while loop near",input_tokens[count])
                sys.exit()
            finally:
                whileStatement.addChild(node2)
                # parseWhileStatements()

        elif(input_tokens[count]=="puts"):
            node3 = TreeNode(" ")
            try:
                node3 = parsePuts()
            # whileStatement.addChild(node3)
          
            # print(repr((TreeNode("while-statements").addChild(node3))))
            # return (TreeNode("while-statements").addChild(node3))
                # whileStatement.addChild(node3)
        
            except:
                print("Syntax error in puts statement near",input_tokens[count])
                sys.exit()

            finally:
                whileStatement.addChild(node3)
                # parseWhileStatements()

        elif(input_tokens[count]=="}"):
            return TreeNode(" ")
        else:
            print("Syntax error.Expected a valid statement near ",input_tokens[count])
            sys.exit()

    return whileStatement

        
        


# relationalTree = TreeNode("<relational>")

def parseRelational():
    global count
    global input_tokens 

    relationalTree = TreeNode("<relational>")

    if(count == len(input_tokens)):
        return relationalTree

    elif((input_tokens[count] in identifiers) or (input_tokens[count] in numbers)):
        node1 = TreeNode(input_tokens[count])
        relationalTree.addChild(node1)

        count = count + 1

        if(input_tokens[count] in relationalOperators):
            node2 = TreeNode(input_tokens[count])
            relationalTree.addChild(node2)

            count = count + 1

            if((input_tokens[count] in identifiers) or (input_tokens[count] in numbers)):
                node3 = TreeNode(input_tokens[count])
                relationalTree.addChild(node3)

                count = count + 1
                return relationalTree
            
            else:
                print("Expected number or identifier but got ",input_tokens[count])
                sys.exit()

                
        else:
            print("Expected a relational operator but got ",input_tokens[count])
            sys.exit()

    else:
        print("Expected number or identifier before relational but got ",input_tokens[count])
        sys.exit()





# assignmentTree = TreeNode("<asssignment>")
def parseFactor():
    global count
    global input_tokens

    

    if((input_tokens[count] in numbers) or (input_tokens[count] in identifiers)):
        try:
            node1 = TreeNode(input_tokens[count])
            return node1
            # return tokens[count]
        finally:
            count = count+1
    elif(input_tokens[count]=="("):

        bracketTree = TreeNode("()")

        if(input_tokens[count+1]=="-"):
            count = count + 1

            unaryTree = TreeNode(input_tokens[count])
            count = count + 1
            node4 = TreeNode(input_tokens[count])
            node3 = TreeNode("0")
            unaryTree.addChild(node3)
            unaryTree.addChild(node4)

            count = count+1
            # print(unaryTree)
            bracketTree.addChild(unaryTree)

            if(input_tokens[count]==")"):
                count= count+1
                print(bracketTree)
                return bracketTree
            else:
                print("Expected \')\' but got",tokens[count])
                sys.exit()

            


        else:
            count = count+1

            node2 = parseSubtraction()
            bracketTree.addChild(node2)
        # num1 = parseSubtraction()


            if(input_tokens[count]==")"):
                count= count+1
                return bracketTree
            else:
                print("Expected \')\' but got",tokens[count])
                sys.exit()

    else:
        print("Expected number but got ",tokens[count])
        sys.exit()

def parseDivision():
    global count
    global input_tokens

    # num1 = parseFactor()

    node1 = parseFactor()
    divTree = TreeNode("/")

    divTree.addChild(node1)
    
    if(count==len(input_tokens)):
      
        # return num1
        return divTree
    if(input_tokens[count]=="/"):
        count = count+1
        node2 = parseFactor()
        divTree.addChild(node2)

        
        if(count==len(input_tokens)):
            return divTree
    while(input_tokens[count]=="/"):
        tree2 = TreeNode(input_tokens[count])

        count = count+1

        node3 = parseFactor()
        tree2.addChild(node3)
        divTree.addChild(tree2)
        
        # num2 = parseFactor()
        # num1 = float(num1)/float(num2)

        if(count==len(input_tokens)):
           
            # return num1
            return divTree

    # return num1 
    return divTree

def parseMultiplication():
    global count
    global input_tokens

    # num1 = parseFactor()

    node1 = parseDivision()
    multTree = TreeNode("*")

    multTree.addChild(node1)
    
    if(count==len(input_tokens)):
      
        # return num1
        return multTree
    if(input_tokens[count]=="*"):
        count = count+1
        node2 = parseDivision()
        multTree.addChild(node2)

        if(count==len(input_tokens)):
            return multTree
    while(input_tokens[count]=="*"):
        tree2 = TreeNode(input_tokens[count])

        count = count+1

        node3 = parseDivision()
        tree2.addChild(node3)
        multTree.addChild(tree2)
        
        # num2 = parseFactor()
        # num1 = float(num1)/float(num2)

        if(count==len(input_tokens)):
           
            # return num1
            return multTree

    # return num1 
    return multTree

def parseAddition():
    global count
    global input_tokens

    # num1 = parseFactor()

    node1 = parseMultiplication()
    addTree = TreeNode("+")

    addTree.addChild(node1)
    
    if(count==len(input_tokens)):
      
        # return num1
        return addTree
    if(input_tokens[count]=="+"):
        count = count+1
        node2 = parseMultiplication()
        addTree.addChild(node2)

        if(count==len(tokens)):
            return addTree
    while(input_tokens[count]=="+"):
        tree2 = TreeNode(input_tokens[count])

        count = count+1

        node3 = parseMultiplication()
        tree2.addChild(node3)
        addTree.addChild(tree2)
        
        # num2 = parseFactor()
        # num1 = float(num1)/float(num2)

        if(count==len(input_tokens)):
           
            # return num1
            return addTree

    # return num1 
    return addTree

def parseSubtraction():
    global count
    global input_tokens

    # num1 = parseFactor()

    node1 = parseAddition()
    subtractTree = TreeNode("-")

    subtractTree.addChild(node1)
    
    if(count==len(input_tokens)):
      
        # return num1
        return subtractTree
    if(input_tokens[count]=="-"):
        count = count+1
        node2 = parseAddition()
        subtractTree.addChild(node2)

        if(count==len(input_tokens)):
            return subtractTree

    while(input_tokens[count]=="-"):
        tree2 = TreeNode(input_tokens[count])

        count = count+1

        node3 = parseAddition()
        tree2.addChild(node3)
        subtractTree.addChild(tree2)
        
        # num2 = parseFactor()
        # num1 = float(num1)/float(num2)

        if(count==len(input_tokens)):
           
            # return num1
            return subtractTree

    # return num1 
    return subtractTree

def parseAssignment():
    global count
    global input_tokens

    assignmentTree = TreeNode("<assignment>")

    if(count == len(input_tokens)):
        return assignmentTree
    elif(input_tokens[count]=="int" or input_tokens[count]=="float" or input_tokens[count]=="double"):
        node1 = TreeNode(input_tokens[count])
        assignmentTree.addChild(node1)
 

        count = count + 1

        if(input_tokens[count] in identifiers):
            node2 = TreeNode(input_tokens[count])
            assignmentTree.addChild(node2)

            count = count + 1

            if(input_tokens[count]=="="):
                node3 = TreeNode(input_tokens[count])
                assignmentTree.addChild(node3)

                count = count + 1 

                node4 = parseSubtraction()
                assignmentTree.addChild(node4)
                return assignmentTree


                # if((input_tokens[count] in numbers or input_tokens[count] in identifiers)):
                #     if(input_tokens[count+1] in arithmeticOperators):
                #         node5 = parseSubtraction()
                #         assignmentTree.addChild(node5)
                #         return assignmentTree
                #     else:
                #         if((input_tokens[count] in numbers or input_tokens[count] in identifiers)):
                #             node4 = TreeNode(input_tokens[count])
                #             assignmentTree.addChild(node4)
                        
                #             count = count + 1
                #             return assignmentTree
                #         else:
                #             print("Expected positive integer,decimal or arithmetic expression  but got ",input_tokens[count])


                # # elif(parseArithmetic()==True):
                #     # return

                # else:
                #     print("Expected positive integer,decimal or arithmetic expression  but got ",input_tokens[count])

            else:
                print("Expected \'=\'  but got ",input_tokens[count])
                sys.exit()
 
        else:
            print("Expected identifier but got ",input_tokens[count])
            sys.exit()
    
    elif(input_tokens[count] in identifiers):
        node6 = TreeNode(input_tokens[count])
        assignmentTree.addChild(node6)

        count = count + 1
        if(input_tokens[count]=="="):
            node7 = TreeNode(input_tokens[count])
            assignmentTree.addChild(node7)

            count = count+1
            node8 = parseSubtraction()
            assignmentTree.addChild(node8)
            return assignmentTree
            # if((input_tokens[count] in numbers or input_tokens[count] in identifiers)):
            #         if(input_tokens[count+1] in arithmeticOperators):
            #             node8 = parseSubtraction()
            #             assignmentTree.addChild(node8)
            #             return assignmentTree
            #         else:
            #             if((input_tokens[count] in numbers or input_tokens[count] in identifiers)):
            #                 node9 = TreeNode(input_tokens[count])
            #                 assignmentTree.addChild(node9)
                        
            #                 count = count + 1
            #                 return assignmentTree
            #             else:
            #                 print("Expected positive integer,decimal or arithmetic expression  but got ",input_tokens[count])



        else:
            print("Expected \'=\'  but got ",input_tokens[count])
            sys.exit()

    else:
        print("Expected \'int\' or \'float\' or \'double\' or identifier but got ",input_tokens[count])
        sys.exit()


def parseClosingBrace():
    global count
    global input_tokens

    if(count == len(input_tokens)):
        print("Expected } but got \' \'",)
        sys.exit()
        return TreeNode(" ")

    elif(input_tokens[count]=="}"):
        closingBraceTree = TreeNode(input_tokens[count])
        count = count + 1
        return closingBraceTree

    else:
        print("Expected } but got ",input_tokens[count])
        sys.exit()


def parseOpeningBrace():
    global count
    global input_tokens

    if(count == len(input_tokens)):
        print("Expected { but got ",input_tokens[count])
        return TreeNode(" ")

    elif(input_tokens[count]=="{"):
        openingBraceTree = TreeNode(input_tokens[count])
        count = count + 1
        return openingBraceTree


    else:
        print("Expected { but got ",input_tokens[count])
        sys.exit()




def parseOpeningBracket():
    global count
    global input_tokens

    if(count == len(input_tokens)):
        print("Expected ( but got ",input_tokens[count])
        return TreeNode(" ")

    elif(input_tokens[count]=="("):
        openingBracketTree = TreeNode(input_tokens[count])

        count = count + 1
        return openingBracketTree

    else:
        print("Expected ( but got ",input_tokens[count])
        sys.exit()



def parseClosingBracket():
    global count
    global input_tokens

    if(count == len(input_tokens)):
        print("Expected ) but got ",input_tokens[count])
        return TreeNode(" ")

    elif(input_tokens[count]==")"):
        closingBracketTree = TreeNode(input_tokens[count])

        count = count + 1
        return closingBracketTree

    else:
        print("Expected ) but got ",input_tokens[count])
        sys.exit()


includeTree = TreeNode("<includes>")


def parseIncludes():
    global input_tokens
    global count

    

    if(count == len(input_tokens)):
        print("Missing symbols")
        sys.exit()

    elif(input_tokens[count]=="#include"):

        node1 = TreeNode(input_tokens[count])
        includeTree.addChild(node1)

        

        count = count + 1
        
        

        if(input_tokens[count] in headerFiles):

            try:
                node2 = TreeNode(input_tokens[count])
                includeTree.addChild(node2)
                count = count + 1

                return includeTree
            except:
                print("Syntax Error")
                sys.exit()

            finally:
                parseIncludes()
            

        else:
            print("\nExpected \'file\'.h but got ",input_tokens[count],"\n")
            sys.exit()
    
    elif(input_tokens[count]=="main"):
       return

    else:
        print("\nExpected #include but got ",input_tokens[count],"\n")
        sys.exit()


ParseProgram()




