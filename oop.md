# Python OOP — Practical Reference
### For humans coming from Lua / JS

---

## The Basics — Class & Instance

```python
class Duck:
    def __init__(self, name, color):   # constructor — runs on Duck(...)
        self.name = name               # instance attribute
        self.color = color

    def quack(self):                   # instance method — self = the instance
        print(f"{self.name} says quack!")

duck_a = Duck("Gerald", "yellow")
duck_b = Duck("Beatrice", "white")
duck_a.quack()   # "Gerald says quack!"
```

> `self` is like Lua's `:` method syntax — Python just makes it explicit as the first parameter.

---

## Class vs Instance Attributes

```python
class Duck:
    species = "Anatidae"    # class attribute — SHARED by all instances

    def __init__(self, name):
        self.name = name    # instance attribute — unique per instance
```

**Watch out — mutable class attributes are a trap:**
```python
class Duck:
    friends = []   # ⚠️ shared across ALL instances

# Better:
class Duck:
    def __init__(self):
        self.friends = []   # ✅ each instance gets its own list
```

---

## The Four Method Types

```python
class Duck:
    def quack(self):            # regular — access to instance via self
        print(self.name)

    @classmethod
    def from_dict(cls, data):   # class method — receives class as cls
        return cls(data["name"])

    @staticmethod
    def sound():                # static — no self, no cls, just a namespaced function
        return "Quack!"

    @property
    def label(self):            # property — looks like attribute, runs like method
        return f"Duck: {self.name}"

duck.label    # "Duck: Gerald" — no () needed
```

| Decorator | First Arg | Access Instance? | Access Class? | Common Use |
|---|---|---|---|---|
| *(none)* | `self` | ✅ | ✅ | normal behaviour |
| `@classmethod` | `cls` | ❌ | ✅ | alternative constructors |
| `@staticmethod` | *(none)* | ❌ | ❌ | utility/helper functions |
| `@property` | `self` | ✅ | ✅ | computed read-only attributes |

---

## Inheritance

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "..."

class Duck(Animal):
    def speak(self):                        # override
        return "Quack!"

class MuteDuck(Duck):
    def speak(self):
        return super().speak() + " (quietly)"  # super() calls parent
```

---

## Dunder Methods — The Metamethods

| Dunder | Lua equivalent | Triggered by |
|---|---|---|
| `__init__` | constructor `new()` | `Duck(...)` |
| `__str__` | `__tostring` | `str(x)`, `print(x)` |
| `__eq__` | `__eq` | `a == b` |
| `__lt__` | `__lt` | `a < b` |
| `__add__` | `__add` | `a + b` |
| `__len__` | `__len` | `len(x)` |
| `__getitem__` | `__index` | `x[key]` |
| `__setitem__` | `__newindex` | `x[key] = val` |
| `__call__` | `__call` | `x()` |

---

## Encapsulation — Visibility Conventions

Python has **no true private** — it uses naming conventions:

```python
self.name      # public — access freely
self._mood     # _single = "internal, please don't touch" (convention only)
self.__secret  # __double = name-mangled, actively hard to access from outside
```

---

## Dataclasses — Less Boilerplate

When a class is mostly storing data, `@dataclass` auto-generates `__init__`, `__repr__`, and `__eq__`:

```python
from dataclasses import dataclass

@dataclass
class Duck:
    name: str
    color: str
    age: int = 0     # default value

duck = Duck("Gerald", "yellow")
print(duck)          # Duck(name='Gerald', color='yellow', age=0)
```

---

## Composition over Inheritance

```python
# Inheritance = "is a"
class RubberDuck(Duck): ...

# Composition = "has a" — generally more flexible
class Pond:
    def __init__(self):
        self.ducks = []

    def add_duck(self, duck: Duck):
        self.ducks.append(duck)
```

> Use inheritance when the relationship is truly "is a". Use composition when it's "has a" or "uses a".

---
 
## Quick Reference

| Concept | Syntax |
|---|---|
| Define class | `class MyClass:` |
| Constructor | `def __init__(self, ...)` |
| Instance method | `def method(self, ...)` |
| Class method | `@classmethod` + `def method(cls, ...)` |
| Static method | `@staticmethod` + `def method(...)` |
| Computed attribute | `@property` + `def attr(self)` |
| Inherit | `class Child(Parent):` |
| Call parent | `super().method()` |
| Internal convention | `self._name` |
| Data-only class | `@dataclass` |
