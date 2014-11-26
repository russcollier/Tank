Tank
==========

Tank is a lightweight [inversion of control](http://en.wikipedia.org/wiki/Inversion_of_control) (IoC) container for Python, inspired by the [Castle project's](http://www.castleproject.org/) [Windsor container](http://docs.castleproject.org/Windsor.MainPage.ashx).

If you follow some established software development best practices like single responsibility principle, coding to interfaces/abstractions, dependency injection, etc. you can become forced to build smaller, more focused components. However, the trade off is typically increased complexity, especially around object creation. In order to create one component, you may need to create several other components, which require other components, and so on and so forth.

Using an IoC container like Tank, you can reduce some of this object creation complexity in your own code by making that complexity the container's problem. This keeps object creation concerns out of your code, so you don't have to couple yourself to implementations and clutter your own logic with object creation boilerplate.

Overview
========
To hopefully keep things consistent and a bit easier to understand, Tank uses terminology similar to Castle Windsor:

* Service - an abstract contract describing some cohesive unit of functionality. Typically we define a service as an [abstract base class](https://docs.python.org/2/library/abc.html) (like a .NET interface - just a contract, no implementation)
* Component - a concrete implementation of a service. Basically the class that extends/implements the abstract base class that defines the service
* Dependency - components depend on services of other components. This allows for nicely decoupled code since it gets you to depend on/code to abstractions instead of implementations

By design Tank only supports injecting dependencies that are declared as constructor (i.e. the class' \_\_init\_\_ method). This is to help encourage you to build immutable components as opposed to injecting dependencies via properties, setters, etc.

Much like a Castle Windsor container, to effectively use a Tank container, "we're dealing with small components, exposing small, well defined, abstract services, depending on services provided by other components, and on some configuration values to fulfil contracts of their services."

<blockquote>
You will end up having many small, decoupled components, which will allow you to rapidly change and evolve your application limiting the scope of changes, but the downside of that is you'll end up having plenty small classes with multiple dependencies that someone will have to manage.

That is the job of a container.
</blockquote>

<sub>Quotes from the Castle Windsor docs: http://docs.castleproject.org/Windsor.Services-and-Components.ashx</sub>

## How Services Are Registered

Once you have a container created, the basic way to register your services with it is by calling the container's <code>register()</code> method.

This method typically takes two arguments:
- The fully qualified class name of your service as a string
- The fully qualified class name of the component that implements that service as a string __-OR-__
- A function/method to call (a.k.a. a "factory method") which will return an instance of your service class.

Alternatively, you can just registered the fully qualified class name of the component on its own. This is useful in situations when you want to register a third party component with the container without having to build your own adapter/wrapper class just to fit it into the container.

The last service registration wins. Basically the container is internally tracking all of the registrations it is given, so if you try to register the same component twice, the last registration will supercede all previous registrations (this may change).

## How Components Are Created

The container only creates components when it is asked to "resolve" them, either explicitly, or while resolving the dependencies of another component. So even if you registered 100 services, but only tried to resolve one of them (whose component didn't have any dependencies), the container would only ever create that one service's component object/instance.

The container internally keeps track of each instance it creates. So basically each component is treated as a [Singleton](http://en.wikipedia.org/wiki/Singleton_pattern) where only one instance is created for the life time of the application. That is of course, assuming you leave the creation of that component class entirely up to the container!

Also it's worth noting that when we refer to components, we're referring to classes that implement interfaces. Not all of your classes will fit into this definition (and thus shouldn't be controlled by the container), particularly things like domain model classes, DTOs, etc.

## How Dependencies Are Configured

For better or for worse, Python doesn't have a clear cut form of type hinting that Tank can use to figure out which service it should resolve for a particular component dependency (or if there is one and I'm just missing it, please let me know!).

To workaround this, Tank relies on special markup in a component class' docstring. In the class docstring, you list your dependencies' (i.e. \_\_init\_\_ arguments) fully qualified class names each on their own line and preceded with an @ character.

For example, if I had a constructor that expected the first argument to be some object that implements the abstract base class lib.moduleA.IFoo, and the second argument to be another object that implements the abstract base class lib.moduleB.IBar, then my component class would look something like:

```python
class MyComponent:
    """
    @lib.moduleA.IFoo
    @lib.moduleB.IBar
    """
    def __init__(self, foo_component, bar_component):
        ...
```

So when the container tries to resolve the component named MyComponent, it will fetch (or create) its IFoo component, its IBar component, and pass them to the MyComponent constructor in that order.

It ain't pretty, but it works for now.

## Basic Example

```python
class Car:
    """
    @tests.cars.IEngine
    """
    def __init__(self, engine):
        self.__engine = engine

    @property
    def engine(self):
        return self.__engine

container = Container()
container.register('tests.cars.IEngine', 'tests.cars.FourCylinder')
container.register('Car')

car = container.resolve('Car')
assert isinstance(car.engine, IEngine)
```

Slightly More Advanced Topics
=============================

## Factory Methods
Sometimes for a variety of reasons, you don't want to (or can't) give the container total control over object creation. In these situations, you can still leverage the container for resolving your services by using factory methods for component registrations.

You do this using the container's <code>register()</code> method's <code>factory_method</code> argument, giving it either the name of the function or method to call, or just a lambda to execute (with no parameters).

### Factory Method Exapmle

```python
container = Container()
container.register('tests.cars.IEngine', factory_method=lambda: SixCylinder())
container.register('Car')

car = container.resolve('Car')
assert isinstance(car.engine, IEngine)
```

## Installers

Installers give developers a way to group together related sets of service registrations into more reusable chunks.

To make an installer, you simply create a class that implements the tank.installer.IInstaller "interface", which is basically just one method where you are given the container. Then you perform your registrations on the container inside your installer.

To use your installer, you simply create an instance of it and give it to the container via the container's <code>install()</code> method.

Then you can do things like define an installer for each of your modules or submodules to have a more convenient way to install your module's services into the container.

### Installers Example

```python
class InstallerForProd(IInstaller):
    def install(self, container):
        container.register('tests.installers.ICreateTheMessage', 'tests.installers.TheMessageProvider')
        container.register('tests.installers.ISendTheMessage', 'tests.installers.RealMessageSender')

container = Container()
container.install(InstallerForProd())

sender = container.resolve('tests.installers.ISendTheMessage')
assert isinstance(sender, ISendTheMessage)
```

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
