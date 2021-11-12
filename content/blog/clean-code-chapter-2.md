---
title: "Clean Code, Chapter 2: Meaningful Names"
date: 2021-11-12T19:21:02Z
draft: false
---

This post is a summary of chapter 2 of the book "Clean Code". Entitled "Meaningful Names", Chapter 2 introduces a series of principles to be used when naming variables, functions, arguments, classes, and packages.

At the time of writing, "Clean Code" is the number 3 best seller on Amazon in the category "Software Design, Testing & Engineering". In the book, the author, [Robert "Uncle Bob" Martin](https://en.wikipedia.org/wiki/Robert_C._Martin) promotes a coding style that is simple to read and understand.

Before I started coding professionally, I understated the value of choosing good names for variables and functions. Today I believe that a codebase with well named variables, functions, classes, etc. can be almost free of comments because the names themselves are enough to give context to the reader about what's going on.

Before diving in the rules, please note that the naming convention does not matter. A name could be `camelCaseName`, `snake_case_name` or even `kebab-case-name`. The only thing that matters is which convention you use.

## 1. Use Intention-revealing Names

The name of a declaration should make the reader understand exactly what it contains. As a rule of the thumb, if a declaration requires a comment, then the name does not reveal its intent.

Avoid one letter names. Disregard the fact that they are widely used in examples and snippets, in that context they are mainly used to save space. When you are writing code professionally you are writing code that will be read and re-read by many people after you. Space is not a concern, brain cycles are.

Examples:

```c#
int d; // elapsed time in days

// Becomes:

int elapsedTimeInDays;
```

```c#
int len = myString.Length;
for(int i = 0; i < len; i++) { /* ... */ }

// Becomes:

int myStringLength = myString.Length;
for(int charNum = 0; charNum < myStringLength; charNum++) { /* ... */ }
```

```c#
private List<int> getContractIds(){
    var list = new List<int>();
    /* ... */
    return list;
}

// Becomes:

private List<int> getContractIds(){
    var contractIds = new List<int>();
    /* ... */
    return contractIds;
}
```

## 2. Make Meaningful Distinctions

When you have similar named declarations it becomes confusing.

A common case is number-series naming. They provide no clue of the author intention. For example a numbered series of parameters: `contract1`, `contract2`, `contract3`.

Another case is variables padded with noise words: `contractInfo`, `contractData`, `contractObject`. They should be distinguished in such a way that the reader knows what are the differences they offer.

```c#
public function copyMessage(Message msg1, Message msg2);

// Becomes:

public function copyMessage(Message destination, Message source);
```

## 3. Use Pronounceable Names

Names that you write will eventually be used in spoken language. This matters because programming is a social activity, people talk about and discuss code. If the names cannot be pronounced they will create additional burden when connecting sound to meaning.

```c#
var ddMmYyyy = DateTime.Now.ToString("dd/MM/yyyy");
var ddddMmmmYyyy = DateTime.Now.ToString("dddd, dd MMMM yyyy");

// Becomes:

var shortDateTime = DateTime.Now.ToString("dd/MM/yyyy");
var longDateTime = DateTime.Now.ToString("dddd, dd MMMM yyyy");
```

## 4. Use Searchable Names

Single-letter names and numeric constants are difficult to be searched. You may want to locate them for refactoring or simply reference but they end up being part of other definitions.

Numeric constants are bad in general and its a well known [counterproductive behavior](https://en.wikipedia.org/wiki/Magic_number_%28programming%29#Unnamed_numerical_constants). Hopefully you have been told about this one in your early days of learning programming.

```c#
int d = 5;
int m = 0;
for (int i = 0; i < 365, i++)
{
    if ((i + d) % 7 == 0)
    {
        m++;
    }
}

// Becomes:

const int DaysInYear = 365;
const int DaysInWeek = 7;
const int Monday = 0;

int startWeekDay = 5
int mondaysCountInYear = 0;
for (int day = 0; day < DaysInYear, day++)
{
    if ((day  + startWeekDay) % DaysInWeek == Monday)
    {
        mondaysCountInYear++;
    }
}
```

## 5. Avoid Encodings

Prefixing the type to variable names, the ([Hungarian Notation](https://en.wikipedia.org/wiki/Hungarian_notation)), is a reminiscence from a time when computer where several times less powerful and compilers far less developer friendly. Nowadays our IDEs can tell the type of our variables and the compiler can enforce static checking of types. Having the type encoded in the variable name makes harder to change the name and type of a variable plus it makes it harder to read!

Other obscure practices like prefixing `m_` to class properties or prefixing `_` for private members is unnecessary. Your classes should be small enough that you don't need them. Moreover, your editing environment can highlight class members to make them distinct from other declarations.

## 6. Class Names Are Nouns, Methods Names Are Verbs

Classes and objects should have a noun or noun phrase names like: `Contract`, `ContractParser`, `FutureContract`. Again avoid 'noise' words like `Object`, `Data`, or `Info`, that do not add anything useful to the name.

Methods should have a verb or a verb phrase like `calculateValue`, `save`, `rollForward`. Access, mutators, and predicates should be named for their value and prefixed with `get`, `set`, `is`.

```c#
class Contract {
    public void sign();
    public void send();

    public int getMoneyAmount();
    public bool isValid();
}
```

## 7. Pick One Word per Concept

Before writing new code to a repository it is essential to look at what is already there to imitate the naming style and the concept used.

Many concepts have synonyms ex. "Controller" have synonyms like "Manager" or "Driver". Another example: "Adapter", "Decorator", and "Wrapper". "Aggregate", "Collection", and "Container". "Fetch", "Retrieve", and "Get".

You should word between synonyms and stick to it across your codebase.

## 8. Use Solution and Problem Domain Names

Choose technical names for those thing which is appropriate. By technical terms I mean topics from Computer Science like algorithms, design patterns, mathematical terms, well-known acronyms.

When there are no technical names for what you are doing, use names from the problem domain. You should at least be aware of the lexicon used by the client of your software, or else in you can always ask a domain expert.

## 9. Add Meaningful Context

It's rare that declarations are meaningful by themselves. Most are closely linked to others. It makes sense to enclose them together in well-named struct, class, or namespace.

```c#
int addressNumber;
string addressRoad;
string city;
string postCode;

// Becomes:

struct Address {
    public int number;
    public string road;
    public string city;
    public string postCode;
}
```