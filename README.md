# am-research
Repository for research in [prediciting material performance of additively manufactured materials](https://studentresearch.engineering.columbia.edu/content/data-science-and-predicting-material-performance-additive-manufacturing-carleton-lab).

## Usage
- Requires GNU make to run Makefile installations, inferences, and other file commands from the parent directory.
  - Can also invoke the scripts directly with python (or set up a main.py that invokes the methods from each step)
-  `make install` will install dependencies and set up a virtual environment in directory `env/`
  - Activate the enviornment according to your shell requirements listed [here](https://docs.python.org/3/library/venv.html)
  - Mac/Linux: `source env/bin/activate`
  - Windows: `.\env\Scripts\activate` or `. env/Scripts/activate` when using Git Bash
- `make test` will train and run the models using processed data and selected features
- `make pipeline` runs the process of fetching data from the MS Access databases, processing & splitting the data into test and train files, training and scoring the models
  - Other make commands are fetch, prep, train, infer, vis, ga
- Source files can be edited as necessary, read commentation for guidance in each step of the pipeline

### Installs/Requirements
- Package requirements are provided in requirements.txt
- Make sure Python is up to date- requirement installs may break down with beta versions (3.10) of python or older versions (<3.6)
    - Other packages in requirements.txt were installed as dependencies of these packages (numpy for example- I opted out of using `pip freeze` for the sake of simplicity, so numpy is installed but not on the requirements list)

## Objectives
- Build a standard for AM processing parameters and material features to generate consistent, high performing parts
  - Different materials, printers, and parameters yield varying resulting performance, thus implementation has to be generalized to work with new input data 
  - Raw material feedstock + processing parameters -> ideal melt pool and density
  - Apply DRL techniques to optimize scan path and achieve a consistent melt pool 
- Experimental additive manufacturing data is expensive to gather and often guarded by paywalls or other barriers, so the goal of this research is to provide a structure for others to follow who can access data to print high performing builds
- This structure will stand on the ground of past literature in the field and apply machine learning and analytical methods to achieve the goal of creating high quality builds
- Build ML models using processed data
  - Data will come from open source areas such as the [NIST database](https://ammd.nist.gov/query-ontology/), scraped research papers, other public databases
  - `fetch_data_senvol.py` scrapes data from [Senvol's publically available database](http://senvol.com)
  - `fetch_data_accb.py` fetches data from Microsoft Access database which stores data from published research papers
- Create infrastructure that makes training and testing with new data easy for users
