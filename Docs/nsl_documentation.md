# Nugget Software Language (NSL) - Documentation

Welcome to Nugget Software Language (NSL)!
NSL is a simple scripting language for quizzes, games, and small applications.

---

## Table of Contents
- [Introduction](#introduction)
- [Commands](#commands)
- [Loops and Conditions](#loops-and-conditions)
- [Functions](#functions)
- [Examples](#examples)
- [About the Author](#about-the-author)

---

## Introduction
NSL allows you to:
- Use simple commands: `ECHO`, `VAR`, `READ`
- Implement loops and conditions: `FOR`, `WHILE`, `IF/ELSE`
- Create functions: `PROC` and `CALL`
- Run interactive examples and quizzes

---

## Commands

### ECHO
Prints text or variables to the screen.

ECHO Hello World!
ECHO Your score is v%Score

### VAR
Creates a variable or changes its value.

VAR Score 0
VAR Score v%Score+1

### READ
Reads input from the user.

READ "What is the capital of Croatia?" Answer

### RANDOM
Generates a random number between two values and stores it in a variable.

RANDOM Number 1 DO 10

### SLEEP
Pauses execution for a specified number of seconds.

SLEEP 2.5

### CLEAR
Clears the terminal screen.

CLEAR


### BREAK
Stops program execution.

```
BREAK
```

---

## Loops and Conditions

### IF / ELSE / ENDIF

```
IF v%Score >= 3 THEN
    ECHO Congratulations!
ELSE
    ECHO Try again
ENDIF
```

### FOR / NEXT

```
FOR i = 1 TO 5
    ECHO Number v%i
NEXT
```

### WHILE / ENDWHILE

```
VAR i 1
WHILE v%i <= 5
    ECHO Number v%i
    VAR i v%i+1
ENDWHILE
```

---

## Functions

### PROC / END
Defines a function with parameters.

```
PROC Sum a b
    VAR total v%a+v%b
    ECHO The result is v%total
END
```

### CALL
Calls a function with arguments.

```
CALL Sum 5 7
```
Warning! You cannot use integers as parameters of functions for now!

---

## Examples

### Quiz
```
ECHO Welcome to the NSL quiz!
VAR Score 0

READ "What is the capital of Croatia?" Answer1
IF v%Answer1 == "Zagreb" THEN
    VAR Score v%Score+1
    ECHO Correct!
ELSE
    ECHO Wrong! The correct answer is Zagreb.
ENDIF
```

### Loops
```
FOR i = 1 TO 5
    ECHO Number v%i
NEXT
```

---

## About the Author
NSL was created by Petar Reljić 🐱‍💻
Purpose of the language: fast learning and fun programming of small scripts.