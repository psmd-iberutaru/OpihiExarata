====================
Spherical Kinematics
====================

Here we detail the algorithm for computing the propagation of the position of 
an asteroid given observations. This method uses the laws of kinematic motion
in spherical coordinates.

Definitions
===========

We are using spherical coordinates, namely the coordinates :math:`(r, \theta, \phi)`
for the radial distance, polar angle, and azimuthal angle respectively. In relation to
astrometric coordinates RA and DEC, :math:`(\alpha, \delta)`:

.. math::

   \alpha = \phi

   \delta = \pi - \theta

Observations taken by the Opihi telescoped and processed by OpihiExarata are
represented as :math:`(\alpha_i, \delta_i, t_i)`. These correspond to the
temporal spherical coordinates :math:`(r=1, \phi_i, \delta_i, t_i)`.

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

   \mathbf{\hat r} &= \sin\theta \cos\phi \mathbf{\hat x} + \sin\theta \sin\theta \mathbf{\hat y} + \cos\theta \mathbf{\hat z} \\
   \hat{\boldsymbol\theta} &= \cos\theta \mathbf{\hat x} + \cos\theta \sin\phi \mathbf{\hat y} - \sin\theta \mathbf{\hat z} \\
   \hat{\boldsymbol\phi} &= -\sin\phi \mathbf{\hat x} + \cos\phi \mathbf{\hat y} + 0 \mathbf{\hat z}

However, for the purposes of finding by propagation, we only care about the location 
of the asteroid on the sky as determined by the celestial coordinates. The distance 
from the origin of the coordinate system does not change. Thus:

.. math::

   r = 1 \qquad \dot{r} = \ddot{r} = 0

And thus the kinematic vectors are:

.. math::

   \mathbf{r} &= \mathbf{\hat r} \\
   \mathbf{v} &=  \dot\theta \hat{\boldsymbol\theta } + \dot\phi \sin\theta \mathbf{\hat{\boldsymbol\phi}} \\
   \mathbf{a} &= \left(-\dot\theta^2 - \dot\phi^2\sin^2\theta \right) \mathbf{\hat r} + \left(\ddot\theta - \dot\phi^2\sin\theta\cos\theta \right) \hat{\boldsymbol\theta } + \left(\ddot\phi\sin\theta  + 2 \dot\theta\dot\phi\cos\theta \right) \hat{\boldsymbol\phi}

Generally, as kinematics are defined based on the time derivatives, the general 
equation of motion for constant acceleration can be used to determine the 
movement of the position vector representing the asteroid:

.. math::

   \mathbf{r} \triangleq \mathbf{r} \qquad \mathbf{v} \triangleq \frac{\mathrm{d}\mathbf{r}}{\mathrm{d}t} \qquad \mathbf{a} \triangleq \frac{\mathrm{d}^2\mathbf{r}}{\mathrm{d}t^2} \qquad \mathbf{j} \triangleq \frac{\mathrm{d}^3\mathbf{r}}{\mathrm{d}t^3} = 0

.. math::

   \mathbf{r} = \mathbf{r}_0 + \mathbf{v}_0 t + \frac{1}{2} \mathbf{a} t^2

.. _Keplerian Ellipses Chapter 2 Reed 2019: http://www.worldcat.org/oclc/1104053368

