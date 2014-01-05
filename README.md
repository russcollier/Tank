PythonTank
==========

A lightweight [inversion of control container](http://en.wikipedia.org/wiki/Inversion_of_control) for Python, inspired by the [Castle project's](http://www.castleproject.org/) [Windsor container](http://docs.castleproject.org/Windsor.MainPage.ashx).

Why?
====

Having spent the majority of my professional software development time doing .NET development these past several years, I've come to know and love using the Castle Windsor IoC container (thanks to a friend and colleague who introduced it to our organization at the time).

When I started doing more Python development, for better or for worse I started trying to apply similar development patterns/techniques I used in .NET to Python, like [Dependency Injection](http://en.wikipedia.org/wiki/Dependency_injection) via constructor arguments.

I did a very brief search for a product similar to Castle Windsor for Python but didn't find anything but a bunch of articles telling me Python doesn't need an IoC container thanks to duck typing. So I decided to start building one myself.

No really, why?!
================

I really like how clean my code feels when using dependency injection. Having my classes be given their collaborators by something "up the chain" and removing the object creation responsibility from my classes just feels good.

Unfortunately as expected, this complicates object creation. In .NET land, Castle Windsor magicks away most of these object creation problems leaving you with very tight and clean "business objects".

While this whole project is probably against the general spirit and philosophy of Python (i.e. it's pretty anti-Pythonic), I still think it's a useful technique, at least for the way I write my Python code.
