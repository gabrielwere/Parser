# Parser
The program demonstrates the lexical analysis and syntax analysis phase of compiler construction.<br>
The mini-grammar is represented by the BNF grammar shown below.
Brackets () are used in the notation instead of angle brackets <> 

<h3>BNF grammar<h3>

 (program) :: = (include)(main)<br>

(include) ::= #include(header-file)<br>

(header-file) ::= stdio.h | stdlib.h<br>

(main) ::= main () { (block) }<br>

(block) ::= (statement-list)<br>
(statement-list) :: = (statement) | (statement) (statement-list)<br>

(statement) ::= (expression)<br>

(expression) ::= (assign-expression) | (arithmetic-expression) | (while-loop)<br>

(arithmetic-expression) ::= (identifier)(arithmetic-operator)(identifier) |
(const)(arithmetic-operator)(const) |(identifier)(arithmetic-operator)(const) |
(const)(arithmetic-operator)(identifier) |
(arithmetic-expression)<br>

(assign-expression) ::= (identifier) = (const) | (identifier) = (arithmetic-expression)<br>

(while-loop) ::= while ( (relational-expression) ) { (statement-list) }<br>

(const) ::= INTEGER | FLOAT | DOUBLE /*set of all real numbers*/<br>

(relational-expression) ::= (identifier)(relational-operator)(identifier) |
(const)(relational-operator)(const) |(identifier)(relational-operator)(const)
(const)(relational-operator)(identifier)<br>

(identifier) ::= (type) id<br>

(type) ::= int | float | double<br>

(arithmetic-operator) ::= + | - | * | / | %<br>

(relational-operator) ::= < | <= | == | > | >= | != | !<br>

<h3>Sample program<h3>
 
 #include stdio.h<br>
 main(){<br>
 int x=0<br>
 
 while(x<=10){<br>
 puts(x)<br>
 x=x+1<br>
 }<br>
 }<br>
 

 
