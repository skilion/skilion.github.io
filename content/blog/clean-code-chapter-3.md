---
title: "Clean Code, Chapter 3: Functions"
date: 2021-11-18T09:50:39Z
---

This post is a summary of chapter 2 of the book "Clean Code". Entitled "Functions", Chapter 3 introduces a series of principles to be used when writing functions. Functions deserve a full chapter about them because they are the first level of abstraction in any program.

## 1. Single-responsability Principle (SRP)

This recommendation is key, your function should do one thing and that thing should clearly stated in its name. At a glance, anybody can understand what it does withot looking at the code.

What does this principle means in practice? It means that your function should only perfrom a handful of operations that are one level of abstraction below its name. If the function tries to do more than that, then you should be able to extract more functions by refactoring it.

There are two signals that tells if a function is doing more than one thing:
 - The number of lines of code is more than 20 or 30.
 - The are more than 2 or 3 `if`, `for`, and `while` statements (nested or not).

```c#
void synchronizeRemoteItems()
{
	Server remoteServerInstance = getServerInstance();
	List<Item> items = getAvailableItems();
	foreach (Item item in items) {
		Identifier id = item.getId();
		if (remoteServerInstance.hasItem(id)) {
			RemoteItem remoteItem = remoteServerInstance.getItem(id);
			if (remoteItem.getHash() != item.getHash()) {
				remoteServerInstance.upload(item);
			}
		} else {
			remoteServerInstance.upload(item);
		}
	}
}

// Becomes:

void synchronizeRemoteItems()
{
	Server remoteServerInstance = getServerInstance();
	List<Item> items = getAvailableItems();
	foreach (Item item in items) {
		ensureItemIsSynced(item, remoteServerInstance);
	}
}

private void ensureItemIsSynced(Item item, Server remoteServerInstance)
{
	Identifier id = item.getId();
	if (remoteServerInstance.hasItem(id)) {
		RemoteItem remoteItem = remoteServerInstance.getItem(id);
		if (remoteItem.getHash() != item.getHash()) {
			remoteServerInstance.upload(item);
		}
	} else {
		remoteServerInstance.upload(item);
	}
}
```

Another relevant example is error handling. "Try/catch" blocks confuse the structure of the code and mix error processing with the busineess logic. So it is better to extract the bodies of the try and catch blocks out into functions of their own.

```c#
void synchronizeRemoteItems()
{
	try {
		Server remoteServerInstance = getServerInstance();
		List<Item> items = getAvailableItems();
		foreach (Item item in items) {
			ensureItemIsSynced(item, remoteServerInstance);
		}
	} catch (ConnectionException e) {
		logException(e)
		throw new SyncFailedException();
	}
}

// Becomes:

void synchronize()
{
	try {
		synchronizeRemoteItems();
	} catch (ConnectionException e) {
		logException(e)
		throw new SyncFailedException();
	}
}

private void synchronizeRemoteItems()
{
	Server remoteServerInstance = getServerInstance();
	List<Item> items = getAvailableItems();
	foreach (Item item in items) {
		ensureItemIsSynced(item, remoteServerInstance);
	}
}
```

## 2. Use the least number of arguments

The more arguments the more difficult is to understand what the function does. You should never use more than 3 arguments. If you find yourself in the situation it is likely that some of those arguments should be wrapped in a `struct` or `class` because they are part of a concept that deserves a name of its own.

Also, never use boolean flags. They imply that the function does two things, one when the flag is true and one when it's false. What you really need is two distinct functions.

```c#
void drawRectangle(int x, int y, int width, int height);

// Becomes:

class Rectangle {
	public int x;
	public int y;
	public int width;
	public int height;
}

void drawRectangle(Rectangle rect);
```

```c#
void makePizza(bool vegan);

// Becomes:

void makePizza();
void makeVeganPizza();
```

## 3. Have No Side Effects

Side effects are unexpected changes to the state of the program. It may be in the form of **global variables** or unexpected variables of the class of the same method.

Side effects create temporal coupling. Temporal coupling is an implicit relationship requiring the client to invoke one function after another. Basically it means that a function can only be called at certain times and incurring in the risk of unexpected side effects at others.

If you must have side effects they should be clearly made explicit in the function name, ex. `Initialize()`.

## 4. Avoid Output Arguments

Function that use output arguments are confusing and should be avoided in general. It's not immediate to understand that an argument is an output and you certainly have to look the definition.

Output arguments were widely used before object oriented (OO) programming, however in an OO language the need for output arguments disappears because when you are a calling a method, the object owning it is the intended ouput argument (`this`).

```c#
void addCheese(Pizza pizza, Cheese cheese);

// Becomes:

pizza.add(cheese);
```

## 5. Command/Query Separation

A function should either do something or answer a query, but not both. Doing both leads to confusion and it likely indicates that the function is doing two things.

```c#
class Hashmap {
	public bool setIfKeyExists(string key, string value);
}

// Becomes:

class Hashmap {
	public bool exists(string key);
	public void set(string key, string value);
}
```

Returning error codes count as breaking this rule. It leads to creating deeply nested `if` statements because you need to handle the errors immediately. Using exceptions instead enables to keep the business logic and the error processing code separated resulting in simplified code.

## 6. Don't Repeat Yourself (DRY)

"Avoid code duplication" is something you have been told to death if you had a formal education in computer science, and for a good reason. If there is an algorithm that gets duplicated N times, the source code will require N-times to be modificated should the algorithm ever change.

Also the readability of your code base is improved if reduntant code is replaced with a single function.
