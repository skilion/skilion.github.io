---
title: "Clean Code, Chapter 4: Comments"
date: 2021-11-27
---

This post is a summary of chapter 4 of the book "Clean Code", entitled "Comments". Chapter 4 contains a few examples of what to do and not to do when commenting code.

## Comments Do Not Make Up for Bad Code

Having to write comments is often a failure of writing *expressive* code. The code itself should be explaining what it is doing.

Don't use a comment when you can introduce a function.

```c#
// Check to see if the pizza is cooked
if ((pizza.flags & COOKING_FLAG) && (pizza.cookingTime > 15))
{
    // ...
}

// Becomes:

if (pizza.isCooked())
{
    // ...
}
```

Don't use a comment if a variable can be renamed to add more context.

```c#
// time when the user submitted the request
TimeStamp theTime;

// Becomes:

TimeStamp userRequestTime;
```

```c#
// length in kilometers
double routeLenght

// Becomes:

double routeLenghtInKilometers;
```

## Good Comments

There are situations when comments are necessary and useful. Here are some cases.

### Informative Comments and Clarifications

Informative comments give information when the code cannot be more expressive than it already is.

For example, when dealing with regular expressions it may be useful to add a description.

```c#
// match dates in the format dd.mm.yyyy only between years 1900-2099
var dateMatcher = new Regex(@"(3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.((?:19|20)\d{2})");
```

### Explanation of Intent

Sometimes a piece of code may may look odd. It could make the reader think: "Why was it written this way?".

When you are writing something unconventional do add a comment to help the future developers understand your intentions.

```c#
void updatePage(Content content) {
    body.set(content);
    view.invalidate();
    // Invalidate the view twice to avoid rendering errors
    view.invalidate();
}
```

```c#
switch (operationType) {
    case OperationType.READ:
    case OperationType.UPDATE:
        row.refresh();
        break;
    case OperationType.DELETE:
        row.markToDelete();
        break;
    case OperationType.CREATE:
        // do nothing
        break;
}
```

### Warning of Consequences

Sometimes it is useful to warn about consequences that are not immediately apparent to the readers.

```c#
// Trigger the operating system limit of running threads
// It will make the OS unresponsive for a few seconds
for (int i = 0; i < 1_000_000; i++) {
    thread.start()
}
```

### Amplification

A comment may be used to amplify the importance of some operation that may otherwise be seen as unimportant.

```c#
// Trigger the operating system limit of running threads
// It will make the OS unresponsive for a few seconds
for (int i = 0; i < 1_000_000; i++) {
    thread.start()
}
```

### Public APIs

When using a third-party library I always look for good documentation. It makes using them much more easier.

If you are building a public interface that will be released to the world or used by other teams in your company, do add comments on it. It is preferred to use a standard format for this type of comments (such as Javadoc for Java or `///` comments for C#) that allows you to generate documentation from your code.

### TODO Comments

"To do" comments indicate that future work is needed but the developer just does not have the time to do it right now.

Nowadays most IDEs have functionality to keep track of them so you can go back and get rid of them.

They are is useful for example to explain why a function has an incomplete implementation and what should be done in the future.

```c#
void sendText(string message)
{
	// TODO: actually send the email
	return;
}
```

```c#
void bakePizza(Pizza pizza)
{
	// TODO: should use the new FireOven class
	var oven = new ElectricOven();

	oven.setTemperatureDegrees(250);
	oven.waitUntilTemperatureIsReached();
	oven.bake(pizza);
}
```

## Bad Comments

### Redundant and Noise Comments

Comment that does not add any useful information to the code is useless and should not be added. Like describing the content of a variable when its name already does a good job.

``` c#
public class Pizza {
    // The ID of the pizza
    private int id;

    // The list of ingredients
    List<Ingredient> ingredients;

    // Default constructor
    Pizza()
    {
        // ...
    }
```

### Journal Comments

Sometimes people add a comment to record what they have changed. This comments accumulate to create a journal or log.

However there is no need for such comments as your version control system does that for you already.

```c#
/*
  2021-01-25: Add support for HTTPS
  2021-02-03: Retry download three times before failing
  2021-02-05: Add getFileSize()
  2021-03-18: Implement IFileStream
*/
```

### Position Markers

Position Markers ends up just adding noise. Its better to let the proper indentation and code formatting to give the visual structure to your code.

```c#
////////////////////////////////////////////////////////////////////////////////
// Actor class
////////////////////////////////////////////////////////////////////////////////
class Actor
{
	// ...
}
```

### Commented Out Code

There is no need to leave commented code. Control version system are good to keep track of what was there before. If you have committed it you won't lose it.

If you leave commented code the next developer will ask himself why. Are they important? Are they reminders? Or are they just leftovers no one bothered to clean up?
