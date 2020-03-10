
<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- SPIRE -->
<br />
<p align="center">
  <a href="https://github.com/SpireBadger/USIC">
    <img src="SpireWhite.jpg" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Spire USIC Transfer Script</h3>

  <p align="center">
    This repository contains the python scripts designed to transmit Spire's updated information to its locator company.
    <br />
    <a href="https://github.com/SpireBadger/USIC"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/SpireBadger/USIC">View Demo</a>
    ·
    <a href="https://github.com/SpireBadger/USIC/issues">Report Bug</a>
    ·
    <a href="https://github.com/SpireBadger/USIC/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project




### Built With

* [Python 2.7](https://www.python.org/downloads/release/python-275/)



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

Python 2.7, Arcpy library from ArcGIS 10.3.1 or later, permissions to Oracle SDE, permissions to ProdData server.
The script is set to create any folders that do not exist already in order to function.


### Installation
 
1. Clone the repo
```sh
git clone https://github.com/SpireBadger/USIC.git
```



<!-- USAGE EXAMPLES -->
## Usage

The combined USIC script and the Alabama USIC script will function as is and are pointed toward the production USIC folder. In order to alter the directed path, simply change where the variable setPath is pointing. setpath is first established on line 64.
The log file will be created on the running computer's C: drive at TempUSIC. To alter this path, change the variable sdeTempPath located on line 113. If line 113 is altered, then line 64, setPath, does not need to also be altered. 


<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/SpireBadger/USIC/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

This is a closed project for Spire employees.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- CONTACT -->
## Contact

Project Link: [https://github.com/SpireBadger/USIC](https://github.com/SpireBadger/USIC)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* Brad Craddick
* Robert Domiano
* []()





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=flat-square
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=flat-square
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=flat-square
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=flat-square
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=flat-square
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
