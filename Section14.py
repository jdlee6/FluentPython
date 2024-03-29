'''
Iterables, iterators, generators

lazily means one item at a time and on demand (iterator pattern)
yield keyword allows the construction of generators which work as iterators

generators fully implement the iterator interface
iterator - retrieves items from a collection, while a generator produce items "out of thin air"

Every collection in Python is iterable and iterators are used internally to support:
    for loops
    collection types construction and extension
    looping over text file lines by line
    list dict and set comprehensions
    tuple unpacking
    unpacking actual parameters with * in function calls 


iter(...) function makes sequences iterable
Sentence take #1: a sequence of words
'''
# # example - take a look at sentence.py - testing iteration on Sentence instance
# from Sec14_examples.sentence import Sentence

# # A sentence is created from a string
# s = Sentence('"The time has come," the Walrus said,')

# # note the output of __repr__ using . . . generated by reprlib.repr
# print(repr(s))
# # Sentence('"The time ha... Walrus said,')

# # Sentence instances iterable (we'll see why in a moment)
# for word in s:
#     print(word)
# # The
# # time
# # has
# # come
# # the
# # Walrus
# # said

# # Being iterable, Sentence objects can be used as input to build lists and other iterable types
# print(list(s))
# # ['The', 'time', 'has', 'come', 'the', 'Walrus', 'said']

# # This example implementation is different from all the others because it is ALSO a sequence due to __getitem__ and __len__ -- and because it is a sequence you can retrieve words by index
# print(s[0])
# # The
# print(s[5])
# # Walrus
# print(s[-1])
# # said

'''
Why sequences are iterable: the iter function

Whenever the interpreter needs to iterate over an object x, it automatically calls iter(x)
the iter built-in function:
    1. checks whether the object implements __iter__ and calls that to obtain an iterator
    2. if __iter__ NOT implemented, but __getitem__ IS implemented, Python creates an iterator that attempts to fetch items in order, starting from index 0 (zero);
    3. if that fails, Python raises a TypeError, saying that "'C' object is not iterable", where C is the class of the target object

*this is why any Python sequence is iterable because they ALL implement __getitem__. 
    -should also implement __iter__ because the special handling of __getitem__ exists for backward compatibility reasons

duck typing: object is considered iterable NOT ONLY with __iter__ but also __getitem__ as long as it accepts int keys starting from 0

goose typing (not as flexible): object is considered iterable if it implements the __iter__ method; no subclassing or registration is required because abc.Iterable implements the __subclasshook__

*most accurate way to check when an object is iterable is to call iter(x) and handle a TypeError exception if it isn't; more accurate than using isinstance(x, abc.Iterable) because iter(x) considers the __getitem__ method while abc.Iterable does NOT (look at the example below)
'''
# example
# class Foo:
#     def __iter__(self):
#         pass

# from collections import abc
# print(issubclass(Foo, abc.Iterable))
# # True

# f = Foo()
# print(isinstance(f, abc.Iterable))
# # True

# # Sentence does NOT pass because it is missing the __iter__ special method even though it is iterable in practice
# print(issubclass(Sentence, abc.Iterable))
# # False

# print(iter(s))
# # <iterator object at 0x7feb98ce0ac8>

# print(list(iter(s)))
# # ['The', 'time', 'has', 'come', 'the', 'Walrus', 'said']


'''
iterables vs. iterators

iterable 
    any object from which the iter built-in function can obtain an iterator. Objects implementing an __iter__ method returning an iterator are iterable. Sequences are ALWAYS iterables; so as are objects implementing a __getitem__ method which takes 0 based indexes

Python obtains iterators FROM iterables 
'''
# # example - string 'ABC' is the ITERABLE (iterator is behind the curtains)
# s = 'ABC'
# for char in s:
#     print(char)
# # A
# # B
# # C

# # example - with a while loop and iter()
# # build an iterator it from the iterable
# it = iter(s)
# while True:
#     try:
#         # repeatedly call next on the iterator to obtain the next item
#         print(next(it))
#     # iterator raises StopIteration when there are NO further items 
#     # StopIteration signals that the iterator is EXHAUSTED
#     except StopIteration:
#         # release the reference to it - the iterator object is discarded
#         del it
#         # break out of the loop
#         break
# # A
# # B
# # C

# # empty list because all the items are printed out
# print(list(it))
# # []

'''
standard interface for an iterator has TWO methods:
__next__ 
    returns the next available item, raising StopIteration when there are NO more items
__iter__
    returns self; this allows iterators to be used where an iterable is expected, for example, in a for loop

Iterator ABC implements __iter__ by doing return self which allows an iterator to be used wherever an iterable is required

**Use hasattr to check for both __iter__ and __next__ attributes instead (this is what the __subclasshook__ method does)**
**best way to check if an object x is an iterator is to call isinstance(x, abc.Iterator); Iterator.__subclasshook__ allows this test to work even if the class of x is NOT a real or virtual subclass of iterator
'''
# # example - abc.Iterator class
# # https://hg.python.org/cpython/file/3.4/Lib/_collections_abc.py#l93 
# class Iterator(Iterable):
#     __slots__ = ()

#     @abstractmethod
#     # next(it) --> returns the next item of the iterator
#     def __next__(self):
#         'Return the next item from the iterator. When exhausted, raise StopIteration'
#         raise StopIteration

#     def __iter__(self):
#         return self

#     @classmethod
#     def __subclasshook__(cls, C):
#         if cls is Iterator:
#             if (any("__next__" in B.__dict__ for B in C.__mro__) and
#                 any("__iter__" in B.__dict__ for B in C.__mro__)):
#                 return True
#         return NotImplemented

# example - Sentence class example - see how the iterator is built by iter() and consumed by next()
# from Sec14_examples.sentence import Sentence

# # Create a sentence s3 with 3 words
# s3 = Sentence('Pig and Pepper')

# # obtain an iterator from s3
# it = iter(s3)
# print(it)
# # <iterator object at 0x7f2e2a8cf940>

# # next(it) fetches the next word
# print(next(it))
# # Pig
# print(next(it))
# # and
# print(next(it))
# # Pepper
# # There are no more words so the iterator raises a StopIteration exception
# # print(next(it))
# # # Traceback . . .
# # # StopIteration

# # once exhausted, an iterator becomes useless
# print(list(it))
# # []

# # to go over the sentence again, a new iterator must be built
# print(list(iter(s3)))
# # ['Pig', 'and', 'Pepper']

''''
NO way to check whether there are remaining items, other than call next() and catch StopIteration
NOT possible to reset an iterator; if you need to start over, call iter() on iterable and NOT on the iter() on iterator itself

iterator
    any object that implements the __next__ no-argument method which returns the next item in a series or raises StopIteration when there are NO more items. Iterators also implement the __iter__ method so they are iterable as well


Sentence take #2: a classic iterator (standard)
Makes explict the relationship between the iterable collection and the iterator object

Look at the example below to see the crucial distinction between an iterable and an iterator and HOW they are connected
'''

# example - take a look at sentence_iter.py: Sentence implemented using the Iterator pattern


'''
Making Sentence an iterator: BAD IDEA

iterables: __iter__ NO __next__
iterators: __next__ and __iter__ (iterators' __iter__ should return self)

iterators are also iterable but iterables are NOT iterators

Iterator pattern (can not make the Sentence instance BOTH an iterable and iterator (anti-pattern)):
    -to access an aggregate object's contents without exposing its internal representation
    -to support multiple traversals of aggregate objects
        (Traversing just means to process every character in a string, usually from left end to right end.)
    -to provide a uniform interface for traversing different aggregate structures (that is, to support polymorphic iteration)

*must be possible to obtain multiple independent iterators from the same iterable instance and each iterator must keep its own internal state, so a proper implementation of the pattern requires each call to iter(my_iterable) to create a new, independent, iterator (This is why we NEED SentenceIterator class in our example)


Sentence take #3: Generator Function
Uses a generator function to replace the SentenceIterator class
'''

# example - look at sentence_gen.py: Sentence implemented using a generator function

'''
in the example before this, __iter__ called SentenceIterator constructor to build an iterator and return it; now in this example Sentence is a generator object that is built automatically when the __iter__ method is called because __iter__ is a generator function


How a generator function works

any function that has the "yield" keyword in its body IS a generator function: a function which, when called, returns a generator object
    generator function is a generator factory

*generator function builds a generator object which wraps the body of the function
**generators YIELD or PRODUCE values; calling a generator function RETURNS a generator; RETURN statement in the body of a generator function causes StopIteration to be raised by the generator object
'''
# example - simple function to demonstrate the behavior of generator

# # Any Python function that contains the yield keyword is a generator function
# def gen_123():
#     # Usually the body of a generator function has loop, but not necessarily; here I just repeat yield three times
#     yield 1
#     yield 2
#     yield 3

# # Looking closely, we see gen_123 is a function object
# print(gen_123)
# # <function gen_123 at 0x7f13559491e0>

# # When invoked, gen_123() returns a generator object
# print(gen_123())
# # <generator object gen_123 at 0x7f5a165314f8>

# # Generators are iterators that produce the values of the expressions passed to yield
# for i in gen_123():
#     print(i)
# # 1
# # 2
# # 3

# # for closer inspection, we assign the generator object to g
# g = gen_123()

# # since g is an iterator, calling next(g) fetches the next item produced by yield
# print(next(g))
# # 1
# print(next(g))
# # 2
# print(next(g))
# # 3

# # when the body of the function completes, the generator object raises a StopIteration
# print(next(g))
# # Traceback (most recent call last):
# # ...
# # StopIteration

# example - generator function which prints message when it runs

# # the generator function is defined like any function but uses YIELD
# def gen_AB():
#     print('start')
#     # the first implicit call to next() in the for loop will print 'start' and stop at the first yield, producing the value 'A"
#     yield 'A'
#     print('continue')
#     # the second implicit call to next() in the for loop will print 'continue' and stop at the second yield, producing the value 'B'
#     yield 'B'
#     # the third call to next() will print 'end.' and fall through the end of the function body causing the generator object to raise StopIteration
#     print('end.')

# # to iterate, the for machinery does the equivalent of g = iter(gen_AB()) to get a generator object, and then next(g) at each iteration
# for c in gen_AB():
#     # the loop block prints --> and the value returned by next(g). But this output will be seen only after the output of the print calls inside the generator function
#     print('-->', c)

# # the string 'start' appears as a result of print('start') in the generator function body
# # start

# # yield 'A' in the generator function body produces the value A consumer by the for loop, which gets assigned to the c variable and results in the output --> A
# # --> A

# # Iteration continues with a second call next(g), advancing the generator function body from yield 'A' to yield 'B'. The text continue is output because of the second print in the generator function body
# # continue

# # yield 'B' produces the value B consumed by the for loop, which gets assigned to the c loop variable so the loop prints --> B
# # --> B

# # iteration continues with a third call next(it), advancing to the end of the body of the function. the text end. appears in the ouput because of the third print in the generator function body
# # end.

# # when the generator function body runs to the END, the generator object raises StopIteration. The for loop machinery catches that exception and the loop terminates cleanly.


'''
Sentence take #4: a lazy implementation
*opposite of lazy is eager

Iterator interface is designed to be lazy: next(my_iterator) produces one item at a time
the examples above have NOT been lazy because the __init__ eagerly builds a list of ALL words in the text and binds them to the self.words attribute

re.finditer() is a lazy version of re.findall() and it returns a generator producing re.MatchObject instances on demand
    -saves memory for many matches 

*only produces the next word when it is needed instead of producing all of the words in __init__
'''

# example - take a look at sentence_gen2.py to see how generator expressions can make the code a lot shorter

'''
Sentence take #5: a generator expression
generator functions can be replaced by generator expressions

generator expression is a lazy version of a list comprehension: it doesn't EAGERLY build a list, but returns a generator that will LAZILY produce the items on demand
    -if a list comp is factory of lists; a generator exp. is factory of generators
'''
# # example - the gen_AB generator function is used by a list comp, then by a generator expression

# # this is the same gen_AB function from the previous example
# def gen_AB():
#     print('start')
#     yield 'A'
#     print('continue')
#     yield 'B'
#     print('end.')

# # the list comprehension eagerly iterates over the items yielded by the generator object produced by calling gen_AB(): 'A' and 'B'. Note the output in the next lines: start, continue, end
# res1 = [x*3 for x in gen_AB()]
# # start
# # continue
# # end.

# # this for loop is iterating over the res1 list produced by the list comprehension
# for i in res1:
#     print('-->', i)
# # --> AAA
# # --> BBB

# # the generator expression returns res2. The call to gen_AB() is made, but that call returns a generator which is NOT consumed here
# res2 = (x*3 for x in gen_AB())
# # res2 is a generator object
# print(res2)
# # <generator object <genexpr> at 0x7f0459e19930>

# # ONLY when the for loop iterates over res2, the body of gen_AB actually executes. Each iteration of the for loop implicitly calls next(res2), advancing gen_AB to the next yield. Note the output of gen_AB with the output of the print in the for loop
# for i in res2:
#     print('-->', i)
# # start
# # --> AAA
# # continue
# # --> BBB
# # end.

'''
a generator expression produces a generator and we can use it to further reduce the code in the Sentence class

take a look at sentence_genexp.py
generator expressions are syntactic sugar: they can be replaced by generator functions but sometimes are MORE convenient


Generator expressions: when to use them

Generator functions are much more flexible: you can code complex logic with multiple statements and can use them as coroutines (lets you have many seemingly simultaneous functions in a Python program; implemented as an extension to generators)

If the generator expression spans more than a couple lines, just code a generator function for the sake of readability
    generator functions have a name which means they can be reused


Another example: arithmetic progression generator

classic Iterator pattern focus on traversal (navigating through a data structure)

A standard interface based on a method to fetch the next item in a series is also useful when items are produced on the fly, instead of retrieved from a collection (range built-in)
    *itertools.count function generates a boundless AP

ArithmeticProgression(begin, step[, end])
range(start, stop[, step])

*type of numbers in the result arithmetic progression follows the type of begin or step
'''
# # basically takes the type of 3 and then puts it on the string value of 5 which would turn the string "5" into an integer 5
# result = type(1 + 2)("5")
# print(result)
# # 5

# # example - demonstration of an ArithmeticProgression class
# from Sec14_examples.ArithmeticProgression import ArithmeticProgression

# ap = ArithmeticProgression(0, 1, 3)
# print(list(ap))
# # [0, 1, 2]

# ap = ArithmeticProgression(0, .5, 3)
# print(list(ap))
# # [0.0, 0.5, 1.0, 1.5, 2.0, 2.5]

# ap = ArithmeticProgression(0, 1/3, 1)
# print(list(ap))
# # [0.0, 0.3333333333333333, 0.6666666666666666]

# from fractions import Fraction
# ap = ArithmeticProgression(0, Fraction(1, 3), 1)
# print(list(ap))
# # [Fraction(0, 1), Fraction(1, 3), Fraction(2, 3)]

# from decimal import Decimal
# ap = ArithmeticProgression(0, Decimal('.1'), .3)
# print(list(ap))
# # [Decimal('0'), Decimal('0.1'), Decimal('0.2')]

# take a look at the alternative generator function that does the same job as ArithmeticProgression class


'''
Arithmetic progression with itertools

19 generators inside itertools module
    ie: itertools.count() returns a generator that produces numbers; without arguments it produces a series of integers starting with 0; optional start and step values
'''
# example - itertools.count()
# import itertools

# gen = itertools.count(1, .5)
# print(next(gen))
# # 1
# print(next(gen))
# # 1.5
# print(next(gen))
# # 2.0
# print(next(gen))
# # 2.5

'''
itertools.count() NEVER stops

itertools.takewhile(): produces a generator which consumes another generator and STOPS when a given predicate evaluates to False
'''
# # example - itertools.count() + itertools.takewhile()
# gen = itertools.takewhile(lambda n: n<3, itertools.count(1, .5))
# print(list(gen))
# # [1, 1.5, 2.0, 2.5]

# take a look at aritprog_v3.py

'''
NOT a generator function (has no yield in its body) but still returns a generator SO it operates as a generator factory just like how a generator function does

*The point of aritprog_v3.py is when implementing generators; KNOW what is available in the standard library so you are NOT reinventing the wheel


Generator functions in the standard library
    *general purpose functions that take arbitrary iterables as arguments and return generators that produce selected, computed, or rearranged items
    *take a look at Section14.txt
'''
# # example - Filtering generator functions examples
# def vowel(c):
#     return c.lower() in 'aeiou'

# # filter() method filters the given sequence with the help of a function that tests each element in the sequence to be True or not
# print(list(filter(vowel, 'Aardvark')))
# # ['A', 'a', 'a']

# import itertools
# print(list(itertools.filterfalse(vowel, 'Aardvark')))
# # ['r', 'd', 'v', 'r', 'k']

# skips the truthy elements until False and then yields ALL of the remaining items with no check up
# print(list(itertools.dropwhile(vowel, 'Aardvark')))
# # ['r', 'd', 'v', 'a', 'r', 'k']

# yields items while predicate is declared Truthy and then STOPS as soon as predicate becomes False
# print(list(itertools.takewhile(vowel, 'Aardvark')))
# # ['A', 'a']

# 1 is true; 0 is false --> therefore it takes every parallel iterable item that has a 1 and returns it to the output
# print(list(itertools.compress('Aardvark', (1, 0, 1, 1, 0, 1))))
# # ['A', 'r', 'd', 'a']

# print(list(itertools.islice('Aardvark', 4)))
# # ['A', 'a', 'r', 'd']

# print(list(itertools.islice('Aardvark', 4, 7)))
# # ['v', 'a', 'r']

# print(list(itertools.islice('Aardvark', 1, 7, 2)))
# # ['a', 'd', 'a']

# # example - itertools.accumulate generator function examples
# sample = [5, 4, 2, 8, 7, 6, 3, 0, 9, 1]
# import itertools

# # running sum
# print(list(itertools.accumulate(sample)))
# # [5, 9, 11, 19, 26, 32, 35, 35, 44, 45]

# # running minimum
# print(list(itertools.accumulate(sample, min)))
# # [5, 4, 2, 2, 2, 2, 2, 0, 0, 0]

# # running maximum
# print(list(itertools.accumulate(sample, max)))
# # [5, 5, 5, 8, 8, 8, 8, 8, 9, 9]

# import operator
# # running product
# print(list(itertools.accumulate(sample, operator.mul)))
# # [5, 20, 40, 320, 2240, 13440, 40320, 0, 0, 0]

# # factorials from 1! to 10!
# print(list(itertools.accumulate(range(1, 11), operator.mul)))
# # [1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800]


# example - mapping generator function examples

# # Numbers the letter in the word starting from 1
# print(list(enumerate('albatroz', 1)))
# # [(1, 'a'), (2, 'l'), (3, 'b'), (4, 'a'), (5, 't'), (6, 'r'), (7, 'o'), (8, 'z')]

# # squares of the integers from 0 to 10
# import operator
# print(list(map(operator.mul, range(11), range(11))))
# # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

# # multiplying numbers from two iterables in parallel: results STOP when the shortest iterable ends
# print(list(map(operator.mul, range(11), [2, 4, 8])))
# # [0, 4, 16]

# # this is what the zip built-in function does
# print(list(map(lambda a, b:(a, b), range(11), [2, 4, 8])))
# # [(0, 2), (1, 4), (2, 8)]

# # repeat each letter in the word according to its place in it, starting from 1
# import itertools
# print(list(itertools.starmap(operator.mul, enumerate('albatroz', 1))))
# # ['a', 'll', 'bbb', 'aaaa', 'ttttt', 'rrrrrr', 'ooooooo', 'zzzzzzzz']

# # running average
# sample = [5, 4, 2, 8, 7, 6, 3, 0, 9, 1]
# print(list(itertools.starmap(lambda a, b: b/a, enumerate(itertools.accumulate(sample), 1))))
# # [5.0, 4.5, 3.6666666666666665, 4.75, 5.2, 5.333333333333333, 5.0, 4.375, 4.888888888888889, 4.5]


# example - Merging generator function examples
# import itertools

# # chain is usually called with two or more iterables
# print(list(itertools.chain('ABC', range(2))))
# # ['A', 'B', 'C', 0, 1]

# # chain does nothing useful when called with a single iterable
# print(list(itertools.chain(enumerate('ABC'))))
# # [(0, 'A'), (1, 'B'), (2, 'C')]

# # But chain.from_iterable takes each item from the iterable and chains them in sequence, as long as each item is itself iterable
# print(list(itertools.chain.from_iterable(enumerate('ABC'))))
# # [0, 'A', 1, 'B', 2, 'C']

# # zip is commonly used to merge two iterables into a series of two-tuples
# print(list(zip('ABC', range(5))))
# # [('A', 0), ('B', 1), ('C', 2)]

# # any number of iterables can be consumed by zip in parallel, but the generator stops as soon as the first iterable ends
# print(list(zip('ABC', range(5), [10, 20, 30, 40])))
# # [('A', 0, 10), ('B', 1, 20), ('C', 2, 30)]

# # itertools.zip_longest works like zip, except it consumes all input iterables to the end, padding output tuples with None as needed
# print(list(itertools.zip_longest('ABC', range(5))))
# # [('A', 0), ('B', 1), ('C', 2), (None, 3), (None, 4)]

# # The fillvalue keyword argument specifies a custom padding value
# print(list(itertools.zip_longest('ABC', range(5), fillvalue='?')))
# # [('A', 0), ('B', 1), ('C', 2), ('?', 3), ('?', 4)]


# example - itertools.product generator function examples
# import itertools

# # the cartesian product of a str with three characters and a range with two integers yields six tuples (because 3 * 2 is 6)
# print(list(itertools.product('ABC', range(2))))
# # [('A', 0), ('A', 1), ('B', 0), ('B', 1), ('C', 0), ('C', 1)]

# # the product of two card ranks (AK) and four suits is a series of eight tuples
# suits = 'spades hearts diamonds clubs'.split()
# print(list(itertools.product('AK', suits)))
# # [('A', 'spades'), ('A', 'hearts'), ('A', 'diamonds'), ('A', 'clubs'), ('K', 'spades'), ('K', 'hearts'), ('K', 'diamonds'), ('K', 'clubs')]

# # given a single iterable, product yields a series of one-tuples [NOT very useful]
# print(list(itertools.product('ABC')))
# # [('A',), ('B',), ('C',)]

# # The repeat=N keyword argument tells product to consume each input iterable N times
# print(list(itertools.product('ABC', repeat=2)))
# # [('A', 'A'), ('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'B'), ('B', 'C'), ('C', 'A'), ('C', 'B'), ('C', 'C')]

# print(list(itertools.product(range(2), repeat=3)))
# # [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]

# rows = itertools.product('AB', range(2), repeat=2)
# for row in rows:
#     print(row)
# # ('A', 0, 'A', 0)
# # ('A', 0, 'A', 1)
# # ('A', 0, 'B', 0)
# # ('A', 0, 'B', 1)
# # ('A', 1, 'A', 0)
# # ('A', 1, 'A', 1)
# # ('A', 1, 'B', 0)
# # ('A', 1, 'B', 1)
# # ('B', 0, 'A', 0)
# # ('B', 0, 'A', 1)
# # ('B', 0, 'B', 0)
# # ('B', 0, 'B', 1)
# # ('B', 1, 'A', 0)
# # ('B', 1, 'A', 1)
# # ('B', 1, 'B', 0)
# # ('B', 1, 'B', 1)


# example - count and repeat
# import itertools, operator

# # build a count generator ct
# ct = itertools.count()
# # retrieve the first item from ct
# print(next(ct))
# # 0

# # I can't build a list from ct, because ct never stops, so I fetch the next three items
# print((next(ct), next(ct), next(ct)))
# # (1, 2, 3)

# # I can build a list from a count generator if it is LIMITED by the islice or takewhile
# print(list(itertools.islice(itertools.count(1, .3), 3)))
# # [1, 1.3, 1.6]

# # Build a cycle generator from 'ABC' and fetch its first item, 'A'
# cy = itertools.cycle('ABC')
# print(next(cy))
# # A

# print(next(cy), next(cy), next(cy), next(cy))
# # A B C A

# # A list can only be built if limited by islice; the next seven items are retrieved here
# print(list(itertools.islice(cy, 7)))
# # ['B', 'C', 'A', 'B', 'C', 'A', 'B']

# # build a repeat generator that will yield the number 7 forever
# rp = itertools.repeat(7)
# print((next(rp), next(rp)))
# # (7, 7)

# # A repeat generator can be limited by passing the times argument: here the number 8 will be produced 4 times
# print(list(itertools.repeat(8, 4)))
# # [8, 8, 8, 8]

# # A common use of repeat: providing a fixed argument in map; here it provides the 5 multiplier
# print(list(map(operator.mul, range(11), itertools.repeat(5))))
# # [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]

'''
****
the combinations, combinations_with_replacement and permutations generator functions - together with product - are called combinatoric generators
*close relationship between itertools.produce and the remaining combinatoric functions as well
****
'''

# example - combinatoric generator functioins yield multiple values per input item
# import itertools

# # all combinations of len() == 2 from the items in 'ABC'; item ordering in the generated tuples is irrelevant (they could be sets)
# print(list(itertools.combinations('ABC', 2)))
# # [('A', 'B'), ('A', 'C'), ('B', 'C')]

# # all combinations of len() == 2 from the items in 'ABC', including combinations with repeated items
# print(list(itertools.combinations_with_replacement('ABC', 2)))
# # [('A', 'A'), ('A', 'B'), ('A', 'C'), ('B', 'B'), ('B', 'C'), ('C', 'C')]

# # all permutations of len() == 2 from the items in 'ABC'; item ordering in the generated tuples is relevant
# # returns successive 2nd argument length permutations of elements in the iterable
# print(list(itertools.permutations('ABC', 2)))
# # [('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('C', 'A'), ('C', 'B')]

# # cartesian product from 'ABC' and 'ABC' (that's the effect of repeat=2)
# print(list(itertools.product('ABC', repeat=2)))
# # [('A', 'A'), ('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'B'), ('B', 'C'), ('C', 'A'), ('C', 'B'), ('C', 'C')]


'''
itertools.groupby ASSUME that the input iterable is sorted by the grouping criterion, or at least that the items are clustered by that criterion -- even if not sorted
'''

# example - itertools.groupby
# import itertools

# # groupby yields tuples of (key, group_generator)
# print(list(itertools.groupby('LLLLAAGGG')))
# # [('L', <itertools._grouper object at 0x7f777d2b8780>), ('A', <itertools._grouper object at 0x7f777beb9400>), ('G', <itertools._grouper object at 0x7f777beb9358>)]

# # handling groupby generators involves nested iteration: in this case the outer for loop and the inner list constructor
# for char, group in itertools.groupby('LLLLAAAGG'):
#     print(char, '->', list(group))
# # L -> ['L', 'L', 'L', 'L']
# # A -> ['A', 'A', 'A']
# # G -> ['G', 'G']

# # to use groupby the input should be sorted; here the words are sorted by length
# animals = ['duck', 'eagle', 'rat', 'giraffe', 'bear', 'bat', 'dolphin', 'shark', 'lion']
# animals.sort(key=len)
# print(animals)
# # ['rat', 'bat', 'duck', 'bear', 'lion', 'eagle', 'shark', 'giraffe', 'dolphin']

# # Again, the for loop over the key and group pair, to display the key and expand the group into a list
# for length, group in itertools.groupby(animals, len):
#     print(length, '->', list(group))
# # 3 -> ['rat', 'bat']
# # 4 -> ['duck', 'bear', 'lion']
# # 5 -> ['eagle', 'shark']
# # 7 -> ['giraffe', 'dolphin']

# # here the reverse generator is used to iterator over the animals from right to left
# for length, group in itertools.groupby(reversed(animals), len):
#     print(length, '->', list(group))
# # 7 -> ['dolphin', 'giraffe']
# # 5 -> ['shark', 'eagle']
# # 4 -> ['lion', 'bear', 'duck']
# # 3 -> ['bat', 'rat']


# # example - itertools.tee yields multiple generators, each yielding every item of the input generator
# import itertools

# print(list(itertools.tee('ABC')))
# # [<itertools._tee object at 0x7f7cf30ae108>, <itertools._tee object at 0x7f7cf30ae148>]

# g1, g2 = itertools.tee('ABC')
# print(next(g1))
# # A

# print(next(g2))
# # A

# print(list(g1))
# # ['B', 'C']

# print(list(g2))
# # ['B', 'C']

# print(list(zip(*itertools.tee('ABC'))))
# # [('A', 'A'), ('B', 'B'), ('C', 'C')]

'''
note that some examples used combinations of generator functions - this is a GREAT feature of these functions: since they all take generators as arguments and return generators, they can be COMBINED in many ways


New syntax in Python3.3+: yield from
*nested for loops are the traditional solution when a generator function needs to yield values produced from another generator
'''
# example - homemade implementation of a chaining generator
# def chain(*iterables):
#     for it in iterables:
#         for i in it:
#             yield i

# s = 'ABC'
# t = tuple(range(3))
# print(list(chain(s, t)))
# # ['A', 'B', 'C', 0, 1, 2]

'''
the chain generator function is delegating to each eceived iterable in turn. 

syntax to make it shorter is shown below

yield from i replaces the inner for loop completely. yield from: creates a channel connecting the inner generator directly to the client of the outer generator (channel is important when generators are used as coroutines and NOT only produce but also consume the values from the client code)
'''
# def chain(*iterables):
#     for i in iterables:
#         yield from i

# print(list(chain(s, t)))
# # ['A', 'B', 'C', 0, 1, 2]


'''
Iterable reducing functions

"reducing", "folding", or "accumulating" functions take an iterable and return a single result
every built in listed below can be implemented with functools.reduce()

*special cases with "all" and "any" is that there is an important optimization that can't be done with reduce: these functions short-circuit, that is they stop consuming the iterator as soon as the result is determined

**sorted builds and reutnrs an actual list (consumes arbitrary iterable)
    only work with iterables that eventually stop; if NOT then it would just never return anything
take a look at Section14.txt
'''

# # example - results of all and any for some sequences

# print(all([1, 2, 3]))
# # True
# print(all([1, 0, 3]))
# # False
# print(all([]))
# # True
# print(any([1, 2, 3]))
# # True
# print(any([1, 0, 3]))
# # True
# print(any([0, 0.0]))
# # False
# print(any([]))
# # False
# g = (n for n in [0, 0.0, 7, 8])
# print(any(g))
# # True
# print(next(g))
# # 8


'''
A closer look at the iter function

iter(x) is called when it needs to iterate over an object x

**another trick: it can be called with two arguments to create an iterator from a regular function or any callable object
    1st arg: must be a callable to be invoked repeatedly (with NO arguments) to yield values
    2nd arg: sentinel (marker value which, when returned by the callable, causes the iterator to raise StopIteration instead of yielding the sentinel)
'''
# example - how to use iter to roll a 6 sided die until a 1 is rolled
from random import randint

def d6():
    return randint(1, 6)

d6_iter = iter(d6, 1)
print(d6_iter)
# <callable_iterator object at 0x7ff95d44c5f8>

for roll in d6_iter:
    print(roll)
# 6
# 2
# 6
# 5
# 3

'''
Note that the iter function here RETURNS a callable_iterator.

*For loop will NEVER display 1 because that is the SENTINEL value (special value in the context of an algorithm which uses its presence as a condition of TERMINATION, typically in a loop (sourced @ wiki))
    if value returned is EQUAL to sentinel, StopIteration will be raised, otherwise the value will be returned (source from docs)

**the iterator becomes useless after exhaustion so to rebuild you would have to invoke iter(...) again
'''
# another example - from docs
# https://docs.python.org/3/library/functions.html#iter


'''
Case Study: Generators in a database conversion utility
https://github.com/fluentpython/isis2json

Problem: isis2json.py needed to support the binary .mst files and be able to read files in ISO-2709 format but the libraries used to read ISO-2709 and .mst files had different interfaces

Solution: isolate the reading logic into a pair of generator functions: one for each supported input format --> main script was eventually split down into 4 functions
    1. main
    2. iter_iso_records (generator function that reads .iso files)
    3. iter_mst_records (generator functions that reads .mst files)
    4. write_json (function performing the actual writing of the JSON records)

*Leveraging generator functions allowed him to decouple the reading logic from the writing logic 
**Real example of how generators provided a flexible solution to processing HUGE databases and keeping memory usage LOW


Generators as coroutines

Coroutine implementation added extra methods and functionality to generator objects; most notable the .send() method

.send() allows two-way data exchange between the client code and the generator
in contrast with .__next__() which ONLY lets the client receive data from the generator

1. Generators produce data for iteration
2. Coroutines are CONSUMERS of data
3. Coroutines are NOT related to iteration
    *there is a use of having yield produce a value in a coroutine BUT it's NOT tied to iteration

Chapter 16 will be dedicated to Coroutines 


Semantics of generator vs. iterator
    1. interface viewpoint 
        iterator: __next__ & __iter__
        generator implements both __next__ and __iter__ so from this perspective every generator is an iterator
                ex. enumerate()

    2. implementation viewpoint
        generator can be coded in two ways:
            1. function with the yield keyword
            2. generator expression
            generator type instances implement the iterator interface

    3. conceptual viewpoint
        iterator traverses a collection and yields items from it (reads values from an existing data source)
        generator may produce values without necessarily traversing a collection, like range()
            *can use a generator to perform the basic duties of an iterator: traversing through a collection AND yielding items from it
'''