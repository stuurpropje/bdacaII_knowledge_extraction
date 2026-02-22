# Knowledge Extraction

## Table of contents

- [Introduction](#introduction)
- [Project Overview](#project-overview)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Contact](#contact)

## Introduction

This project is part of an assignment of the course Big Data II of the University of Amsterdam.
It aims to examine the gender representation among current state leaders. It does this through construction of a [Resource Description Framework (RDF)](https://en.wikipedia.org/wiki/Resource_Description_Framework), which allows for visualisations such as the distribution of characteristics.

The RDF can be found in the [data](data/) folder. The results and insights in this project showcases the inequality of specific cultural dominances. Additionally, this project can be used as a baseline for further knowledge graph construction and Wikipedia information scraping.

## Project overview

Data stems from the [World Leaders](https://en.wikipedia.org/wiki/List_of_current_heads_of_state_and_government) Wikipedia page. This results in the analysis of 196 world leaders as characterised by the web page. The following Research Questions were asked:

1. What is the gender distribution of current state leaders globally?
2. Are there differences in Wikipedia visibility between male and female leaders (e.g., page length, references, cross-language presence)?

The following steps were taken to construct the RDF:

1. Collection of data from the [World Leaders](https://en.wikipedia.org/wiki/List_of_current_heads_of_state_and_government) page.
2. Collection of data from each respective world leader page.
3. Cleaning and normalisation of data.
4. Extraction of subjects, predicates and objects.
5. Construction of knowledge graph.

## Installation

Clone the repository.

```cmd
git clone https://github.com/11907223/lesroosters
```

Navigate to the directory.

### Using a Conda environment
Install the required dependencies:

```cmd
conda env create -f environment.yml
```

### Using an uv environment

Windows:
```cmd
irm https://astral.sh/uv/install.ps1 | iex
```

macOS:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

In VS Code’s take the following steps:
1. Run Task
2. Setup Python env (uv)
3. Continue without scanning the task output
4. Wait
5. A folder named .venv will appear, which should indicate a succesfull installation.

## Project Structure

- [notebooks:](notebooks/) Contains all Jupyter notebooks used to create the RDF.
- [data:](data/) Contains the raw data in csv files and a relational file in a RDF Turtle file.
- [output:](output/) Contains image files of results and UML.
- [environment.yml](/environment.yml) File specifying installation of Python environment through Conda.
- [uv.lock](/uv.lock) File specifying installation of Python environment through uv.

## Contact

Inquiries about this project can be emailed to elean.huang@student.uva.nl