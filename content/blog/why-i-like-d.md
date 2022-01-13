---
title: "Why I Like D"
date: 2022-01-09
lastmod: 2022-01-13
---

My engineer friends are surprised when I mention I know and I even wrote code in the [D programming language](https://en.wikipedia.org/wiki/D_(programming_language)) (aka Dlang).

D is not exactly a mainstream language. According to the [Tiobe Index](https://www.tiobe.com/tiobe-index/), which measures programming languages popularity, D doesn't make the first 20th languages, as of today. Its peak was in 2009 when it reached the [12th position](https://www.tiobe.com/tiobe-index/d/).

I discovered D in 2016. I can't remember if it was from [Hacker News](https://hn.algolia.com/?q=dlang) or some random Google search. At the time I was looking for a new language to replace C/C++ because I had enough of the amount of obscure behaviors, crazy complicated template system, and long compilation times. When writing C++ I have limit myself to use a subset of the features of the language to avoid "shooting myself in the foot". I wanted to switch to a more productive language where I could focus on writing code.

My requirements for a new language were: compiled, strongly typed, easy to learn and use (think Python), and binary compatible with existing C libraries such as [OpenGL](https://en.wikipedia.org/wiki/OpenGL) and the various operating system libraries.

My candidates at the time were [D](https://dlang.org/), [Go](https://go.dev/), and [Rust](https://www.rust-lang.org/). They are all compiled languages, however Go did not have generic types at the time so I excluded it immediately. Being already familiar in C, D won over Rust easily, because the syntax of Rust is quite far from C compared to D. My only pet peeve against D was that it came with a built-in garbage collector and I was against it for performance reasons, but the GC can be disabled programmatically so I concluded that it was worth taking D for a test drive.

Around the same time I registered for [Microsoft Onedrive](https://www.microsoft.com/en-gb/microsoft-365/onedrive/online-cloud-storage) to make use of a promotion and, being a Linux user, found the landscape lacking of a good client to sync my files. The best option was a client written in Python which I didn't quite like so I decided to write [my own client](https://github.com/skilion/onedrive) and to use D to become familiar with the new language.

In hindsight, that was a great choice. The need to write a good program for myself made me focus in learning D. I picked up [one of the best books](https://erdani.com/tdpl/) about it, written by Andrei Alexandrescu, and dived in. The book was great and it made me completely fall in love with the language.

Here are the reasons.

## Better C

**D** main "reason d'etre" is removing the limitations that C and C++ have accumulated over the years, while keeping compatibility with their binary interface and similar syntax.

If you already know C/C++ that's a great thing. Remove the pre-processor, the template system, the architecture dependent differences (ex. the size of an `int`), the cruft of legacy features that accumulated over the years (ex. different flavors of the standard library). Then start adding modern features like foreach, modules, [delegates](https://tour.dlang.org/tour/en/basics/delegates), dynamic and associative arrays (aka dictionaries or maps). The resulting syntax is so similar to C/C++ that you can will pick it up in a day. Just try out the interactive [Dlang Tour](https://tour.dlang.org/) if you don't believe me. 

A nice perk of the similar syntax when you are converting your code: you can assume that any expression that you wrote in C/C++ will lead the same result in D or it won't compile (ex. because you may need an explicit cast).

D strives to keep binary compatibility with C and C++ programs. That is excellent if you want to start porting your codebase or simply have to interface with legacy libraries. Furthermore you can directly link static libraries compiled in C within your D executable---and vice versa---as long as you translate the header files for the library.

## Consistency

D has been designed from the ground up by a small number of very experienced people, namely [Walter Bright](https://en.wikipedia.org/wiki/Walter_Bright) and [Andrei Alexandrescu](https://en.wikipedia.org/wiki/Andrei_Alexandrescu). Their unified vision is reflected both in the syntax and the standard library of the language.

The standard library is rich of features. It provides both basic things like containers, date handling, math functions and more advanced things such as concurrency, regexes, and cryptography. You even get interfaces to common libraries like [SQLite](https://sqlite.org/) and [Curl](https://curl.se/).

The standard library is built from the ground up making extensive use of [generic types](https://en.wikipedia.org/wiki/Generic_programming) and [ranges](https://tour.dlang.org/tour/en/basics/ranges) (equivalent of C++ or Python *iterators*). A great example is [std.algorithm](https://dlang.org/phobos/std_algorithm.html). All common operations like iteration, sorting, search, and comparison work on any existing or custom type that you will create (assuming you implement the expected interface for a range).

Another thing I like are the syntax choices that make the language simple and predictable. For example you cannot have multiple inheritance of classes (only of interfaces) so you cannot fall into the [diamond problem](https://en.wikipedia.org/wiki/Multiple_inheritance#The_diamond_problem) like in C++ or Java. Furthermore all that in C++ is achieved with the pre-processor and template metaprogramming can be achieved with the same syntax that you use for writing runtime code. More on this later.

## Built-in dynamic and associative arrays

I like to define D as a wonderful marriage between C and Python. You have the advantages of compiled code with the powerful features of Python.

In my experience, when coding, I will use dynamic and associative arrays (aka maps or dictionaries) 80% of the time. Having them built in the language is a incredible productivity boost as you don't have to import some library or build your own. Furthermore you have dedicated syntax that make using them much less verbose than it would as if they were and external library.

Some examples:

```d
// Create a dynamic array of 10 ints, initialized to 0
auto array = new int[10];

// Take a slice of the second half
auto half = array[4..$].dup;

// Increment all elements by one (array-wise expression)
half[] += 1;

// Concatenate the two arrays
auto concat = array ~ half;
```

```d
// Create an associative array
int[string] dict = [ "Hello": 10, "World": 23 ];

// Execute the code if "Hello" exists
if (int* value = "Hello" in dict) {
	// do something with value
}

// Element wise comparison
assert(dict == dict);
```

## Generics Types

Generic types are a breeze in D. They are intuitive and the compiler does a lot of smart inference behind the scene to optimize the resulting code.

An example to give an idea:

```d
// Generic types are pre-pended to the actual arguments
auto add(T)(T lhs, T rhs) {
    return lhs + rhs;
}

int a = 5; int b = 10;
// T is deduced to int
auto result1 = add(a, b); 

// Explicitly force T to be float
auto result2 = add!float(a, b);

float c = 5.0;
// T is deduced to float
auto result3 = add(a, c);
```

What is even better is that a safe subset of D code can be evaluated by the compiler **at compile time** thus allowing the possibility of checking complex conditions.

For example here is function that can only be used when the types satisfy the given condition:

```d
T[] find(T, E)(T[] haystack, E needle)
// Check that T and E can be compared for inequality
if (is(typeof(haystack[0] != needle) == bool)) 
{
	// Actual code of find()
}
```

This example shows how to accept a variable number of arguments with different types:

```d
// This function accepts variadic template parameters
void write(T...)(T args) {
	// This foreach loop is unrolled at compile time!
	foreach (arg; args) {
		// to() is a convenience function from the std library to convert types
		auto stringArg = to!string(arg);
		stdout.rawWrite(stringArg);
	}
}

write("There are ", 3, " cows");
```

## Compile Time Code Generation (Metaprogramming)

I have hinted that D allows you to execute code at compile time, so why not execute code at compile time that generates other code? Let me explain that: you can generate strings, that contain D code, at compile-time, and have the compiler include them in your executable. Enter the magic world of the keyword `mixin`.

If you need to generate a large structure of pre-computed values, you can do it!.

If you need to generate boilerplate code and you want to avoid typing it, you can do it!

```d
// Returns "int[name] = [0, 1, ..., count - 1]";
string createArray(string name, int count) {
	string result = "int[" ~ to!string(count) ~ "] ";
	result ~= name ~ " = [ ";
	foreach (n; 0 .. count) {
		result ~= to!string(n);
		result ~= ", ";
	}
	result ~= "];";
	return result;
}

// here the magic happens
mixin(createArray("myArray", 5));

assert(myArray[0] == 0);
assert(myArray[4] == 4);
```

Creating raw strings may be overkill in some situations. So there is also a way to create injectable scopes of code with `mixin template`:

```d
mixin template Foo()
{
    void func() { writeln("Foo.func()"); }
}

class Bar
{
    mixin Foo;
}

void test()
{
    Bar b = new Bar();
    b.func(); // calls Foo.func()
}
```

If you need to generate super duper optimized code for custom use-case, you can do it! A great example of this are [compile time regexes](https://dlang.org/phobos/std_regex.html#ctRegex) which can generate optimized native machine code to match any regex.

## Garbage Collector

Some people may not consider the GC a feature, I certainly did not at the beginning. I came from a hard-core game developer mindset where you need to know the exact timing for every operation in your critical path. I lived by quotes like: "the programmer knows better how to manage memory" and "you cannot have unexpected pauses for GC collection".

However it turns out that unless you are writing a computer game, a high frequency trading system, a web server, or anything that really cares about sub-second latency, chances are that a garbage collector is your best friend. It will remove the burden of having to think about memory management at all and at the same time guarantee that you won't have any memory leaks in your code.

In case you are writing a performance critical piece of software, remember you can turn off the garbage collector! People on forums like to bash that in such case you cannot use many functions from standard library. So what? If performances are essential for your system you are likely already writing you own utility library with highly optimized algorithms and data structures for your use case, so you won't really miss the standard library much.

## Hacker Features

If you had ever worked in the most "esoteric" aspect of coding such as: writing shellcodes, assembly language, executable packing, obfuscation, process hacking, etc. Here are a couple of gems that you'll love:

Hexadecimal strings:

```d
// Same as "\xAB\xCD\x01\x23\x45"
auto s = x"ABCD012345"; 
```

Including binary blobs
```d
// Inline the content of "resource.bin"
auto x = import("resource.bin");
```

## Mature developer tools

Compared to Go or Rust that have the backing of big companies, D took many years to get a solid ecosystem of productivity tools. I blame this as the main reason for D not being more widely adopted today.

However nowadays there are:
- 3 compilers: the official reference compiler DMD, [GCC](https://wiki.dlang.org/GDC), and [LLVM](https://wiki.dlang.org/LDC) which cover any architecture which you may want to develop for.
- Autocompletion and debugging for all [major IDEs](https://wiki.dlang.org/Editors): Visual Studio, VS Code, Vim, Emacs, Sublime Text.

## Package Manager

In line with modern programming languages such as Python, Node Js and C#, D has it's own official package manger, called [DUB](https://code.dlang.org/).

To be honest here, the package ecosystem is not nearly as developed as Python or Node Js. But this is to be expected given the lower adoption that D has. Nevertheless you have the most common use cases covered such as web development, protocols such as gRPC or REST, parsers, interfaces with commonly used libraries like SDL, OpenGL, Linux and Windows system libraries.

## Conclusion

Hopefully this post has gave you a bit of curiosity to learn about D yourself. If that's the case I suggest you to spend 30 minutes on this [interactive tutorial](https://tour.dlang.org/) which will teach you the 80% of the language feature and practice them from your browser.

"Ok, that's nice...", you may say, "...but what about real work, can I get paid to learn and write in D?". Well sort of. There are a very few places in the world that hire people to write in D, but they are niches which you will love and they will love you back if you have the hacker mentality which has pushed you to learn this elegant programming language. You can find them on Google ;)

---

[Comments](https://news.ycombinator.com/item?id=29863557)
