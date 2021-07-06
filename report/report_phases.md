# Additive Manufacturing & Machine Learning

## Problem
### What is the issue?
- Additive Manufacturing is a field with exploding growth and potential, but its
widespread use in industry limits its ability to produce consistent, high
performing parts.
  - defects include poor surface finish, increased porosity, delamination,
  cracking, and residual stresses, leading to inferior mechanical properties
  and poor geometric conformity
- The current process of producing a part requires trial and error- experimental
science is expensive and simulation does not produce reliable results
### Why do we care?
- AM can produce intricate parts with complex geometries and designs with unique
microstructures and properties
- COVID-19 showed how fragile the global supply chain is, and the ability to
shrink the supply chain, and have flexible, lower cost manufacturing will be
very valuable
  - Decreases material waste, local control of materials, mass customization
- Laser powder bed fusion is a popular and effective method of printing metals
  - Able to achieve extremely detailed parts and complex topolgies
  - applications in aerospace, defense, and biomdeical industries
### How are we going to tackle this issue?
- As outlined below, there are many applications of machine learning in the cycle
of additive manufacturing
  - Machine learning helps to find optimizations of processes that would otherwise
  require intensive DOE, trial and error, or highly complex computational and physical analysis
- We will focus specifically on the section AM Process: Parameter Optimization as outlined
in this [paper](https://www.sciencedirect.com/science/article/pii/S2214860420309106#bib0865)


## Goal
- The goal is to set a standard that will allow the consistent, quality printing of
AM materials, specifically focusing on the process paramter optimization area
- Whatever data we end up finding, we can outline steps to choosing training data
based on a lit review and applying that data to the models to get accurate predictions
and high quality parts
- Within the section below, our focus is on AM Process: Process Parameter Optimization


## Areas for ML Application in AM
### Design for AM
- Material & Topology Design
  - generally, spherical is ideal <-- find citation
  - smaller powders produce higher accuracy for small parameters,
  - pick a compatible printer for that powder
    - given printer and powder, the process parameters will vary
    to determine optimal parameters
    - need data relevant to the powder and machine, can't apply
    other machine data and assume the same <-- find citation
  - ML has been used to develop ideal alloys and to speed up the process
  of topological optimization

### AM Process
- Data
  - NIST has about 100 datapoints for tensile strength, not ideal but
  better than nothing
    - data augementation? 
  - Use FEM to build dataset to determine properties based on parameters?
    - suffers from discrepencies due to simplified assumptions
- Powder Spreading Optimization
  - using CV and ML techniques to automatically identify defects in
  powder spreading
  - re-coater hopping, recoater streaking, debris, super elevation, part
  damage, incomplete spreading
- Process Parameter Optimization
  - ML was mainly used to link their key process parameters to the quality indicators
  at two levels, namely mesoscale level (i.e. porosity or relative density, melt pool
  geometries) and macroscale level (i.e. mechanical properties).
    - Do the mesoscale levels intrinsically determine the macroscale properties, and
    if so to what degree (this is its own research question, could us NN to predict how
    varying levels of porosity/relative density, melt pool geometries affect mech. props.)
      - would it be possible for 
    - If so, we should focus on optimizing the mesoscale with the assumption that the mechanical
    properties will improve
    - It is empircally proven that formability, microstructure, mechanical properties, and residual
    stresses are determined by single tracks governed by molten pool dynamics <-- find citation
  - preset parameters
    - preheating the baseplate, gas enviornment
  - there has been extensive research already and compilation of DOE methods
  to determine which parameters affect certain performance features the most
    - for ex. tensile strength is affected by hatch spacing and powder temp,
    whereas porosity is not affected as much by these factors (see table)
    - build models for each metric of performance, train the data on
    each of these, and then select parameters that optimize each of these metrics
    - would be fantastic if we had vast pools of data to feed into a
    neural networks that would be able to consider every parameter, no matter how small,
    but this isnt the case due to paywalls and limitations/expense of experimental science
      - for ex, you will likely only gather a few parameters rather
      than all $n$ number of possibile parameters
  - when training models, we need to consider that different printers will
  give different results even when keeping parameters consistent
    - therefore, for a specific printer, you need to trian on data consistent
    with that printer
  - dynamic parameters in situ
    - can use deep reinforcement learning as described in [Ogoke](https://arxiv.org/pdf/2102.03355.pdf) to change
    scan speed based on temperature changes, ie real time monitoring and
    control methods
      - how do we model thermal dynamics in several dimensions, including
      base plate, surrounding temp, layer by layer build, different
      depths of build -- Ogoke built a good model of this, but has its
      limitations (could be improved)
- In-Process Defect Monitoring
  - can use ML techniques to discover defects as they unfold live
    
### AM Production
- Manufacturing Planning
  - how do you optimize print times to maximize output and costs
- Quality control
- Data security