# OpihiExarata
 An IRTF Opihi telescope software tool used primarily for solving asteroid ephemerides using astrometric solutions.

[![Tests (Windows)](https://github.com/psmd-iberutaru/OpihiExarata/actions/workflows/windows_testing.yml/badge.svg)](https://github.com/psmd-iberutaru/OpihiExarata/actions/workflows/windows_testing.yml) [![Tests (Windows)](https://github.com/psmd-iberutaru/OpihiExarata/actions/workflows/linux_testing.yml/badge.svg)](https://github.com/psmd-iberutaru/OpihiExarata/actions/workflows/linux_testing.yml)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Python Black Linting](https://github.com/psmd-iberutaru/OpihiExarata/actions/workflows/black.yml/badge.svg)](https://github.com/psmd-iberutaru/OpihiExarata/actions/workflows/black.yml)
# Building and Installing

## Python Code and General Software
Run the following commands based on your operating system to build the Python binary wheel (Windows or Linux).
 
```bash
> py -m build
$ python3 -m build
```

Install the wheel package. You will need to modify this command to the proper wheel that you generated from before. Because this project using date-based versioning, your package will likely be that of the date that you build the wheel. (Force reinstall is optional but suggested to ensure you have the most up-to-date version.)
```bash
pip install ./dist/OpihiExarata-YYYY.MM.DD-py3-none-any.whl --force-reinstall
```

# Why the name Exarata?

The IRTF Opihi telescope is named after the opihi, a limpet which lives on rocky shores by sticking to the rocks. In a similar vein, the Opihi telescope sticks hard onto the side of the main IRTF telescope. One of the three opihi species endemic to the Hawaii islands is the Hawaiian blackfoot opihi. The Opihi telescope is similar to this species and for this reason, this software is named after it. (The similarities: the opihi species and the telescope are both black; the Opihi telescope is rather small compared to the IRTF, the blackfoot is a small opihi; and the blackfoot opihi is a high delicacy, similar to this software, it has a rather small audience.)

The binomial taxonomical name of the Hawaiian blackfoot opihi is Cellana exarata. The genus Cellana describes the group of limpets including the opihis, but "exarata" is the identifying part for the Hawaiian blackfoot, thus the name of this software, we decided, is Exarata. A backronym for it, which describes its function: Ephemeris with eXtra Atmospheric Response and Astroid Trajectory Analysis.