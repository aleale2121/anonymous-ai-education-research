# Anonymous Research Repository

This repository contains the topic modelling output and the code used to collect, preprocess, and analyze Reddit discussions about Artificial Intelligence in education.

The pipeline includes data collection, preprocessing, role classification, topic modeling using BERTopic, topic refinement, and thematic analysis.


---

# Repository Structure

```
.
├── data
│   ├── raw
│   ├── processed
│   └── external
│
├── outputs
│   ├── global
│   ├── yearly
│   └── role
│
├── scripts
│
├── src
│   ├── data_collection
│   ├── role_classification
│   ├── thematic_categorization
│   ├── topic_modeling
│   ├── topic_refinement
│   └── visualization
|
├── requirements.txt
├── Makefile
└── README.md
```

---

### Outputs

**outputs/global**

Results from the global topic model.

**outputs/yearly**

Topic models generated independently for each year.

**outputs/role**

Topic models generated separately for student and educator subsets.

---

# Installation

Create a Python environment and install dependencies:

```
make install
```

or

```
pip install -r requirements.txt
```

---

# Pipeline Overview

The workflow consists of the following stages:

1. Data collection
2. Dataset merging
3. Data preprocessing
4. Role classification
5. Topic modeling
6. Topic refinement
7. Thematic categorization
8. Visualization

---

# Running the Pipeline

### Collect Reddit data

```
make collect
```

### Merge yearly datasets

```
make merge
```

### Preprocess dataset

```
make preprocess
```

### Role classification

```
make classify
```

---

# Topic Modeling

### Global topic model

```
make global
```

### Yearly topic models

```
make yearly
```

### Role-based topic models

Student topics:

```
make role_student
```

Educator topics:

```
make role_educator
```

---

# Topic Refinement

Refine topic labels using the LLM-assisted refinement pipeline.

```
make refine_global
make refine_student
make refine_educator
make refine_yearly
```

---

# Thematic Categorization

Group topics into higher-level semantic categories.

```
make categorize
```

---

# Visualization

Generate the stacked bar chart used in the analysis.

```
make topic_proportion_plot
```

Output:

```
outputs/figures/figures_proportion_stackbar.png
```

---

# Requirements

Python 3.9+

Dependencies are listed in:

```
requirements.txt
```

Key libraries include:

* BERTopic
* pandas
* scikit-learn
* transformers
* matplotlib
* seaborn

---

# Notes for Reviewers

This repository is provided for anonymous review. Identifying information has been removed to preserve double-blind evaluation.

The code implements the experimental pipeline described in the submitted manuscript.
