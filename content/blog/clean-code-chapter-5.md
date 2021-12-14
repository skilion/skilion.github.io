---
title: "Clean Code, Chapter 5: Formatting"
date: 2021-12-10
---

This post is a summary of chapter 5 of the book "Clean Code", entitled "Formatting". Chapter 5 contains guidelines to use when formatting your code.

Code formatting is important. The organization, layout and arrangement of your code is a form of communication. And the quality of communication is what distinguishes a professional developer from a beginner. 

## The Newspaper Metaphor

Write your code like a well-written newspaper article. At the top you expect a headline and a summary that allow you to decide if it something that you want to read. As you continue downward all the details and facts of the story appear giving you the entire picture.

Code should be written the same way. At the top put the high level concepts and algorithms and the bottom put the lowest level functions and details.

If the newspaper were just one long story containing disorganized information and facts, then it would not be usable, and we would not read it.

## Vertical Formatting

As a rule of the thumb the shorter the file the better. The number of lines in a source file should rarely be more than 500 and if longer you should consider splitting the functionality. The sweet spot should be between 100-200 lines.

A typical source files has different concepts: package declaration, imports, class definition, properties, methods. We want to separate these concepts with blank lines to help the eye distinguish between the text blocks that make them up. Empty lines give visual cues to the eyes of the developer so that he can read the first line and decide whether to skip to the next block or keep reading.

Code that is tightly related should appear close together and vertically dense (without blank lines) to help the reader identify code that has similar functionality.
- Local variables should be declared as close as possible to their usage.
- Class properties should be declared at the top (or at the bottom depending on the convention) of the class but never in the middle. Properties are variables that should be used by most of the methods in the class.
- Functions that call each other (dependent functions) should be vertically close.
- Some functions may represents related concepts by having common naming or doing variations of the same basic task (conceptual affinity). They may not call each other but they fit nicely together. Examples: read and write, get and set, open and close.
- Function call dependencies should point to the bottom of the file. It means that the most called functions like utility and shared functions should be toward the end of the file.

## Horizontal Formatting

Similarly to file length, as a rule of the thumb the shorter the lines in the file the better.

You may have heard of the [Hollerith limit](https://en.wikipedia.org/wiki/Punched_card#The_Hollerith_card) of 80 characters per line, which is a bit arbitrary, and it does not really make sense anymore since we have wide monitors that can easily show up to 100-120 characters. However if the line starts to be longer than 200, it is a bit ridiculous and you must split it.

Use horizontal white space to associate things that are strongly related and disassociate things that are more weakly related.
- Add space around operators to highlight precedence's (ex. `var x = -a + b*c*d - 4*a;`)
- Don't add space between function names and parameters but add space between the comma separated parameters (ex. `Console.WriteLine("Welcome ", username, "!");`)

### Don't Use Horizontal Alignment

The alignment in code emphasize the wrong things. It is not useful to read code by column. If you have long lists that need to be aligned the problem is the length of the list and not the lack of alignment.

Example:

```c#
public class CompanyOverview {
    public string   Symbol                  { get; set; }
    public string   Description             { get; set; }
    public string   Country                 { get; set; }
    public float    Price                   { get; set; }
    public string   Currency                { get; set; }
    public long     MarketCapitalization    { get; set; }
    public long     OutstandingShares       { get; set; }
    public float    PeRatio                 { get; set; }
}

// Becomes:

public class CompanyOverview {
    public string Symbol { get; set; }
    public string Description { get; set; }
    public string Country { get; set; }
    public float Price { get; set; }
    public string Currency { get; set; }
    public long MarketCapitalization { get; set; }
    public long OutstandingShares { get; set; }
    public float PeRatio { get; set; }
}
```

### Indentation

A source file is a hierarchy. There is information that belong to the file as a whole, to the individual classes, to the methods within the classes, and the code blocks within the methods.

Indentation adds a visual cue to perceive this hierarchy, it allows the developer to rapidly see the structure of the file. Without it code would be an unreadable mess.

Don't break indentation for short statements. Maintain a consistent hierarchy even for one-liners.

```c#
public class Pizza {
    private readonly string name;
    private readonly List<string> ingredients = new List<string>();

    Pizza(string name) { this.name = name }

    public void AddIngredient(string ingredient) { ingredients.Add(ingredient); }
}

// Becomes:

public class Pizza
{
    private readonly string name;
    private readonly List<string> ingredients = new List<string>();

    Pizza(string name)
    {
        this.name = name
    }

    public void AddIngredient(string ingredient)
    {
        ingredients.Add(ingredient);
    }
}
```

## Team Rules

Most of the time in your career you will be working with other people on an existing codebase. When working in a team, learn and follow the conventions that have been set by team mates. Everybody should agree on one convention and stick to it because consistency is more important than following best practices (which can sometime be arbitrary). As a programmer I expect the formatting I see in one file to be be the same in others. Having multiple styles adds unnecessary complexity.
