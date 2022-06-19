====================
Spherical Kinematics
====================

Here we detail the algorithm for computing the propagation of the position of 
an asteroid given observations. This method uses the laws of kinematic motion
in spherical coordinates.

Definitions
===========

We are using spherical coordinates, namely the coordinates 
:math:`(r, \theta, \phi)` for the radial distance, polar angle, and azimuthal 
angle respectively. In relation to astrometric coordinates RA and DEC, 
:math:`(\alpha, \delta)`:

.. math::

   \alpha = \phi   \qquad   \delta = \frac{\pi}{2} - \theta

Observations taken by the Opihi telescoped and processed by OpihiExarata are
represented as :math:`(\alpha_n, \delta_n, t_n)`. These correspond to the
temporal spherical coordinates :math:`(r=1, \phi_n, \delta_n, t_n)`. For 
:math:`t` is the absolute time of the observation; UNIX time or Julian date 
time works best.

Moreover, in spherical coordinates, the position, velocity, and acceleration 
vectors are given as: (see `Keplerian Ellipses Chapter 2 Reed 2019`_)

.. math::

   \mathbf{r} &= r \mathbf{\hat r} \\
   \mathbf{v} &= \dot{r} \mathbf{\hat r} + r \dot\theta \hat{\boldsymbol\theta } + r \dot\phi \sin\theta \mathbf{\hat{\boldsymbol\phi}} \\
   \mathbf{a} &= \left(\ddot{r} - r\dot\theta^2 - r\dot\phi^2\sin^2\theta \right)\mathbf{\hat r} \\
    &\quad + \left( r\ddot\theta + 2\dot{r}\dot\theta - r\dot\phi^2\sin\theta\cos\theta \right) \hat{\boldsymbol\theta } \\
    &\quad + \left( r\ddot\phi\sin\theta + 2\dot{r}\dot\phi\sin\theta + 2 r\dot\theta\dot\phi\cos\theta \right) \hat{\boldsymbol\phi}

Where the basis vectors of the spherical coordinates are:

.. math::

   \hat{\mathbf r} &= \sin\theta \cos\phi \hat{\mathbf x} + \sin\theta \sin\phi \hat{\mathbf y} + \cos\theta \hat{\mathbf z} \\
   \hat{\boldsymbol\theta} &= \cos\theta \cos\phi \hat{\mathbf x} + \cos\theta \sin\phi \hat{\mathbf y} - \sin\theta \hat{\mathbf z} \\
   \hat{\boldsymbol\phi} &= - \sin\phi \hat{\mathbf x} + \cos\phi \hat{\mathbf y} + 0 \hat{\mathbf z}

However, for the purposes of finding by propagation, we only care about the 
location of the asteroid on the sky as determined by the celestial coordinates. 
The distance from the origin of the coordinate system does not change. Thus:

.. math::

   r = 1 \qquad \dot{r} = \ddot{r} = 0

And thus the kinematic vectors are:

.. math::

   \mathbf{r} &= \mathbf{\hat r} \\
   \mathbf{v} &=  \dot\theta \hat{\boldsymbol\theta } + \dot\phi \sin\theta \mathbf{\hat{\boldsymbol\phi}} \\
   \mathbf{a} &= \left(-\dot\theta^2 - \dot\phi^2\sin^2\theta \right) \mathbf{\hat r} + \left(\ddot\theta - \dot\phi^2\sin\theta\cos\theta \right) \hat{\boldsymbol\theta } + \left(\ddot\phi\sin\theta  + 2 \dot\theta\dot\phi\cos\theta \right) \hat{\boldsymbol\phi}

We can convert these vectors to Cartesian coordinates using the matrix 
transformation. The spherical to Cartesian transformation matrix 
:math:`\mathbf{R}` can be derived from the defining angles of the spherical 
coordinate system :math:`\theta` and :math:`\phi`. Where 
:math:`\mathbf{u}_\text{cart} = \mathbf{R} \mathbf{u}_\text{sph}`.:

.. math::

   \mathbf{R} = \begin{bmatrix}
   \sin\theta\cos\phi & \cos\theta\cos\phi & -\sin\phi \\
   \sin\theta\sin\phi & \cos\theta\sin\phi &  \cos\phi \\
   \cos\theta         & -\sin\theta        & 0
   \end{bmatrix}

Thus, in Cartesian coordinates:

.. math::

   \mathbf{r} &= \mathbf{R} \begin{bmatrix} 1 \\ 0 \\ 0 \end{bmatrix} \\
   \mathbf{v} &= \mathbf{R} \begin{bmatrix} 0 \\ \dot\theta \\ \dot\phi \sin\theta \end{bmatrix} \\
   \mathbf{a} &= \mathbf{R} \begin{bmatrix} -\dot\theta^2 - \dot\phi^2\sin^2\theta \\ \ddot\theta - \dot\phi^2\sin\theta\cos\theta \\ \ddot\phi\sin\theta  + 2 \dot\theta\dot\phi\cos\theta \end{bmatrix}


Generally, as kinematics are defined based on the time derivatives, the general 
equation of motion for constant acceleration can be used to determine the 
movement of the position vector representing the asteroid:

.. math::

   \mathbf{r} \triangleq \mathbf{r} \qquad \mathbf{v} \triangleq \frac{\mathrm{d}\mathbf{r}}{\mathrm{d}t} \qquad \mathbf{a} \triangleq \frac{\mathrm{d}^2\mathbf{r}}{\mathrm{d}t^2} \qquad \mathbf{j} \triangleq \frac{\mathrm{d}^3\mathbf{r}}{\mathrm{d}t^3} = 0

.. math::

   \mathbf{r} = \mathbf{r}_0 + \mathbf{v}_0 \tau + \frac{1}{2} \mathbf{a} \tau^2

Where :math:`\tau` is the time interval between the defining time of 
observation to the current time.

.. _Keplerian Ellipses Chapter 2 Reed 2019: http://www.worldcat.org/oclc/1104053368


Deriving Rates
==============

Multiple observations from Opihi provides multiple sightings of an asteroid at 
many different points in the sky, providing multiple RA and DEC coordinates, 
:math:`\alpha_n` and :math:`\delta_n` at time :math:`t_n`. We have a total of 
:math:`N` RA DEC observations. (The propagation calculation will need to be redone for 
a new observation set :math:`N' = N + 1`.)

We can convert this to spherical coordinates with :math:`\phi_n = \alpha_n` and :math:`\theta_n = \frac{\pi}{2} - \delta_n`.

These multiple observations allows for the determination of the rates of 
change of spherical coordinates for the asteroid, namely: (For the time 
difference :math:`t_\Delta = t_{n+1} - t_n`.)

.. math::

   \dot\theta_p = \frac{\theta_{n+1} - \theta_{n}}{t_{n+1} - t_n}

   \dot\phi_p = \frac{\phi_{n+1} - \phi_{n}}{t_{n+1} - t_n}

   t'_p = \frac{1}{2} \left( t_{n+1} + t_n \right)

...and...

.. math::

   \ddot\theta_q = \frac{\dot\theta_{p+1} - \dot\theta_{p}}{t'_{p+1} - t'_p}

   \ddot\phi_q = \frac{\dot\phi_{p+1} - \dot\phi_{p}}{t'_{p+1} - t'_p}

The first order rates changes over time. As such, it is required that two 
observations be reserved as special observations which the first order rates 
are calculated and to established the spherical coordinate system itself. 
Although it does not need to be the first two observations, it is often 
connivent to use them. As such, using the first two observations 
:math:`n=0` and :math:`n=1`, we have: 

.. math::

   \theta &= \theta_0 \\
   \phi &= \phi_0 \\
   \dot\theta &= \dot\theta_0 = \frac{\theta_1 - \theta_0}{t_1 - t_0} \\
   \dot\phi &= \dot\phi_0 = \frac{\phi_1 - \phi_0}{t_1 - t_0} \\

Because we assume constant acceleration (:math:`\mathbf{j} = 0`), the second
differential values are assumed to be constant and thus an average is more
representational of the value. (A mean or median is valid.)

.. math::

   \ddot\theta = \frac{1}{Q} \sum_q^Q \ddot\theta_q \approx \mathrm{median} (\ddot\theta_q)

   \ddot\phi = \frac{1}{Q} \sum_q^Q \ddot\phi_q \approx \mathrm{median} (\ddot\phi_q)

In the case for :math:`N=2`, then the total number of derived angular first 
order rates is :math:`P=1`. As such the second order rates cannot be 
calculated and :math:`Q=0` (the cardinality of the arrays are zero). By 
default, for this special case:

.. math::

   \#(\ddot\theta_q) = \#(\ddot\phi_q) = 0 \implies Q = 0 \longrightarrow \ddot\theta = 0 \quad \ddot\phi = 0


Spherical Motion
================

With the 0th, 1st, and 2nd order rates calculated from the set of :math:`N` 
observations, the kinematic vectors can be calculated. The special 
observations defining the coordinate system and the velocities also define 
the initial vectors from which kinematics shall be applied to. The 
acceleration vector, being constant means :math:`\mathbf{a}_0 = \mathbf{a}`. 
Namely, these vectors are, in Cartesian coordinates,

.. math::

   \mathbf{r_0} &= \begin{bmatrix}
   \sin\theta\cos\phi & \cos\theta\cos\phi & -\sin\phi \\
   \sin\theta\sin\phi & \cos\theta\sin\phi &  \cos\phi \\
   \cos\theta         & -\sin\theta        & 0
   \end{bmatrix} \begin{bmatrix} 1 \\ 0 \\ 0 \end{bmatrix} \\
   \mathbf{v_0} &= \begin{bmatrix}
   \sin\theta\cos\phi & \cos\theta\cos\phi & -\sin\phi \\
   \sin\theta\sin\phi & \cos\theta\sin\phi &  \cos\phi \\
   \cos\theta         & -\sin\theta        & 0
   \end{bmatrix} \begin{bmatrix} 0 \\ \dot\theta \\ \dot\phi \sin\theta \end{bmatrix} \\
   \mathbf{a} &= \begin{bmatrix}
   \sin\theta\cos\phi & \cos\theta\cos\phi & -\sin\phi \\
   \sin\theta\sin\phi & \cos\theta\sin\phi &  \cos\phi \\
   \cos\theta         & -\sin\theta        & 0
   \end{bmatrix} \begin{bmatrix} -\dot\theta^2 - \dot\phi^2\sin^2\theta \\ \ddot\theta - \dot\phi^2\sin\theta\cos\theta \\ \ddot\phi\sin\theta  + 2 \dot\theta\dot\phi\cos\theta \end{bmatrix}

All three of these vectors are constant in future time. The position at a 
set of future observations at time(s) :math:`t^+_i` can be calculated using 
the kinematic equation; the time intervals :math:`\tau_i` being 
:math:`\tau_i = t^+_i - t_0`:

.. math::

   \mathbf{r}^+_i = \mathbf{r}_0 + \mathbf{v}_0 \left(t^+_i - t_0\right) + \frac{1}{2} \mathbf{a} \left(t^+_i - t_0\right)^2


Celestial Sphere
================

These new future position vectors :math:`\mathbf{r}^+_i` are in Cartesian 
coordinates. The calculations should be done in Cartesian, provided the 
conversion earlier.

Each position vector can be represented as:

.. math::

   \mathbf{r}^+_i = X_i \mathbf{\hat x} + Y_i \mathbf{\hat y} + Z_i \mathbf{\hat z} = \begin{bmatrix} X_i \\ Y_i \\ Z_i \end{bmatrix}

These Cartesian coordinate position vectors, centered on the origin, represents 
where the asteroid is on the celestial sphere in the future at an observation 
time of :math:`t^+_i`. From these Cartesian coordinates, we can extract their 
location in spherical coordinates,

.. math:: 

   r^+_i &= \sqrt{X_i^2 + Y_i^2 + Z_i^2} \\
   \theta^+_i &= \arccos\left(\frac{Z_i}{r^+_i}\right) = \arccos\left(\frac{Z_i}{\sqrt{X_i^2 + Y_i^2 + Z_i^2}}\right) \\
   \phi^+_i &= \arctan\!2(Y_i, X_i) \simeq \arctan\left(\frac{Y_i}{X_i}\right)

.. note::
   In order to properly handle the quadrant issue, the 2-argument arctangent is 
   required. Moreover, if the 2-argument arctangent function returns in a range 
   :math:`-\pi \leq \angle \leq \pi`, it can be converted to the usual range of 
   :math:`0 \leq \phi \leq 2\pi` with: :math:`\phi = \angle \mod 2\pi` 
   or :math:`\phi = \angle \mod 360^\circ`

These spherical coordinate locations can then be converted into future RA and 
DEC temporal coordinates :math:`(\alpha^+_i, \delta^+_i, t^+_i)`:

.. math::

   \alpha^+_i &= \phi^+_i \\
   \delta^+_i &= \frac{\pi}{2} - \theta^+_i \\
   t^+_i &= t^+_i


Lemmas
======

Derivation of Vector Equation of Motion
---------------------------------------

Newton's second law and constant acceleration stipulates:

.. math::

   \mathbf{F} = m \mathbf{a} = m \ddot{\mathbf{r}} \qquad \dot{\mathbf{F}} = 0

This thus provides the differential equation of motion (For constant :math:`\mathbf{F}`.)

.. math::

   \ddot{\mathbf{r}} = \frac{\mathrm{d}^2\mathbf{r}}{\mathrm{d}t^2} = \frac{\mathbf{F}}{m}

We define based on the laws of integrations (and in essence the fundamental 
theorem of calculus):

.. math::

   \dot{\mathbf{f}} \triangleq \frac{\mathrm{d}\mathbf{f}}{\mathrm{d}t} \Longleftrightarrow \int \dot{\mathbf{f}} \mathrm{d} t = \mathbf{f} + \mathbf{C} 

.. math::

   \int \frac{\mathrm{d}\mathbf{f}}{\mathrm{d}t} \mathrm{d} t = \mathbf{f}

We can solve the differential equation of motion:

.. math::

   \ddot{\mathbf{r}} &= \frac{\mathbf{F}}{m} \\
   \frac{\mathrm{d}}{\mathrm{d}t} \left( \frac{\mathrm{d}\mathbf{r}}{\mathrm{d}t} \right) &= \frac{\mathbf{F}}{m} \\
   \int \frac{\mathrm{d}}{\mathrm{d}t} \left( \frac{\mathrm{d}\mathbf{r}}{\mathrm{d}t} \right) \mathrm{d}t &= \int \frac{\mathbf{F}}{m} \mathrm{d}t = \frac{\mathbf{F}}{m} \int 1 \mathrm{d}t = \frac{\mathbf{F}}{m} t + \mathbf{C_1} \\
   \frac{\mathrm{d}\mathbf{r}}{\mathrm{d}t} &= \frac{\mathbf{F}}{m} t + \mathbf{C_1} \\
   \int \frac{\mathrm{d}\mathbf{r}}{\mathrm{d}t} \mathrm{d}t &= \int \frac{\mathbf{F}}{m} t + \mathbf{C_1} \mathrm{d}t = \frac{\mathbf{F}}{m} \int t \mathrm{d}t + \int \mathbf{C_1} \mathrm{d}t = \frac{\mathbf{F}}{m} \frac{1}{2} t^2 + \mathbf{C_1} t + \mathbf{C_2} \\
   \mathbf{r} &= \frac{\mathbf{F}}{m} \frac{1}{2} t^2 + \mathbf{C_1} t + \mathbf{C_2}

For the initial conditions:

.. math::

   t = 0 &\implies \mathbf{r} = \mathbf{C_2} = \mathbf{r_0} \\ 
   t = 0 &\implies \frac{\mathrm{d}\mathbf{r}}{\mathrm{d}t} = \mathbf{C_1} = \mathbf{v_0} \\
   \dot{\mathbf{F}} = 0 &\implies \frac{\mathrm{d}^2\mathbf{r}}{\mathrm{d}t^2} = \frac{\mathbf{F}}{m} = \mathbf{a_0} = \mathbf{a}

Thus, the total valid solution is:

.. math::

   \mathbf{r} = \mathbf{r_0} + \mathbf{v_0} t + \frac{1}{2} \mathbf{a} t^2