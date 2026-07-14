# Study

This directory includes all code in the base pipeline, data for the project, figure creation scripts.

## Overall Organization

Each directory is a different step of the FapC virtual screen pipeline. It is organized by subsections (initial letter in directory name), then in order of the pipeline by number.

## Subsection Overview
- 0 = template section / testing section. Not involved in actual pipeline
- a = where data from previous work / projects is held.
- b = docking of initial diversity set of molecules to FapC
- c = pharmacophore search of the top hits of the diversity set
- d = docking molecules from the diversity pharmacophore search (c) to FapC
- e = pharmacophore search of experimentally tested compounds
- f = docking molecules from the experimental pharmacophore search (e) to FapC
- g = final results
- z = archived sections. No longer part of pipeline.

## Subdirectory Organization
- README: holds in detail information about (1) what the subsection does (2) how to use code present (3) what each script does (4) all data that should be output by it
- Analysis: holds all scripts (python, bash, batch jobs) for each section of the pipeline. Temporary files required for running of that section may be stored as well.
  - Example: script that creates batch job to run pharmit, script that analyses GNINA outputs
- Data: holds all outputs of subsection.
  - Example: results of pharmacophore search, reformatting SDFs prepped for docking
- Figures: holds scripts to create figures used in presentations or papers. Generally connected to that section.
- Visualization: holds PyMol saves / scripts that set up visualizations important in the pipeline
