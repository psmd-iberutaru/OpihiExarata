.. _technical-architecture:

============
Architecture
============

In brief, the OpihiExarata software was created with the following requirements 
in mind to guide the architectural design:

- It must be able to accommodate and provide for the use cases of the Opihi telescope, (see :ref:`user-index`).
- The requirements for the user for interaction must be minimal in complexity but feature complete.
- The software should be robust and allow for components to be interchangeable with each other.
- The software should be easily maintainable, well documented, and use established technologies over custom implementation.

We thus designed the parts of the OpihiExarata software package to follow 
these principles. A visual overview is given in 
:ref:`figure-software-framework-diagram`.

.. _figure-software-framework-diagram:

.. figure:: /assets/images/software-framework-diagram.*

    A comprehensive single image overview of the main components of the 
    OpihiExarata software and all of the parts which make it work. Each of the 
    boxes within OpihiSolution represent an attribute of the overall class 
    while the black arrows detail their interactions. The other interaction 
    lines detail external (primarily GUI and internet service) interaction 
    with the attributes.

To best construct the software with interchangeability and maintainability in 
mind, we often on modularized and abstracted where possible.

The OpihiExarata software handles the analysis of images one at a time. 
All relevant data and results of a given image are stored in a container 
class called OpihiSolution. Historical information are also provided and 
used in the OpihiSolution class.

As described in :ref:`user-system-framework`, there are five main problems 
which this software is to solve for each given image: astrometric plate 
solving, photometric calibration, orbit determination, ephemeris calculation, 
and asteroid on-sky propagation. These five problems are distinct and thus we 
developed five different solution classes to contain the results of each of 
these problems for every image. These solution classes are unimaginatively 
named AstrometricSolution, PhotometricSolution, OrbitalSolution, 
EphemeriticSolution, and PropagativeSolution respectively.

In order for a given solution class to have results to store, we need to 
actually solve the main five problems. We utilize external services and 
other established programs to solve them. In order to use these services to 
obtain the desired results, we use a function to mimic a user using the 
service. We call these functions "vehicle functions". Each service has their 
own vehicle function because each service is different. 

The results derived from vehicle functions are stored in the solution classes
which themselves are ultimately stored in the overarching OpihiSolution class.
More information about the vehicle functions and solution classes can be found
in :ref:`technical-architecture-vehicles-solutions`.

In order for the software to interact with a given service (through its 
corresponding vehicle function) we need to have an API to interact with. 
ALthough many services provide their own API, others do not. Therefore, we 
built custom APIs for each and every supported service. We call our custom 
APIs "engines". Each engine is specifically curtailed for handling Opihi 
data and extracting the needed information from whatever service or program it 
was specifically made for. A list of available engines and other information 
is provided in :ref:`technical-architecture-services-engines`.

All implemented engines solve one of the five main problems. Along with their 
corresponding vehicle functions, there is a standard data input (i.e. to be 
solved) and standard output of results (to be stored in the solution classes), 
as detailed in 
:ref:`technical-architecture-vehicles-solutions`. Because of this 
standardization, all engines (technically engine-vehicle pairs) which all 
solve the same problem are interchangeable with each other. The user can 
select between different implemented engines/services best suited for their 
particular object. This property is also useful if one of the engines/services 
break, Opihi would not become useless.

The user should not need to deal with all of this detail as to keep it simple
in usage. All that is relevant for the user is picking the appropriate 
engine-vehicle pairs based on their applicability to the user's data. They 
should interact with OpihiExarata via the graphical user interface depending 
on the modes of operation (see :ref:`user-automatic-mode` and 
:ref:`user-manual-mode`). More information on how this GUI was built and 
related information can be found in 
:ref:`technical-architecture-graphical-user-interface`.

For ease of maintainability, specific conventions were adopted to both increase 
speed and compatibility between different sections of the code. These 
conventions also assist with making the software easy to maintain. More 
information about these conventions are provided in 
:ref:`technical-conventions`. Moreover, functions which are commonly used 
across the entire software package are collected in a library for reusability 
and consistency; the available functionality provided by the library is 
detailed in :ref:`technical-architecture-library`.

Overall, we created wrapper code around the available services which solve 
one of the five problems to have a more maintainable and replaceable codebase. 
These services (through the "engine" and "vehicle function" wrapper code) take 
a standardized input and provide a standard set of outputs which the software 
uses to generate classes which contain these results and others (as another 
layer of abstraction). We use the results of the five main problems, as 
calculated from a specific Opihi image and other historical observations, to 
determine the needed results (to modify the telescope control or to monitor 
the atmospheric conditions).


.. toctree::
    :maxdepth: 3
    :hidden:
    :caption: Algorithms

    services_engines
    vehicles_solutions
    library
    graphical_user_interface