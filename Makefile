PYTHON = python3

# Data paths
RAW_DIR = data/raw
PROCESSED_DIR = data/processed
OUTPUT_DIR = outputs

RAW_GLOBAL = $(RAW_DIR)/reddit_ai_global_2018_2025.csv
CLEAN_DATA = $(PROCESSED_DIR)/reddit_clean.csv

ROLE_DIR = $(PROCESSED_DIR)/role
STUDENT_DIR = $(PROCESSED_DIR)/student
EDUCATOR_DIR = $(PROCESSED_DIR)/educator

# Topic modeling outputs
GLOBAL_OUTPUT = $(OUTPUT_DIR)/global
YEARLY_OUTPUT = $(OUTPUT_DIR)/yearly

ROLE_STUDENT_INPUT = $(ROLE_DIR)/student/reddit_student.csv
ROLE_EDUCATOR_INPUT = $(ROLE_DIR)/educator/reddit_educator.csv

ROLE_STUDENT_OUTPUT = $(OUTPUT_DIR)/role/student
ROLE_EDUCATOR_OUTPUT = $(OUTPUT_DIR)/role/educator

# Topic refinement
STUDENT_TOPICS = $(ROLE_STUDENT_OUTPUT)/topics.csv
EDUCATOR_TOPICS = $(ROLE_EDUCATOR_OUTPUT)/topics.csv
GLOBAL_TOPICS = $(GLOBAL_OUTPUT)/topics.csv

REFINED_STUDENT = $(ROLE_STUDENT_OUTPUT)/refined_topics.csv
REFINED_EDUCATOR = $(ROLE_EDUCATOR_OUTPUT)/refined_topics.csv
REFINED_GLOBAL = $(GLOBAL_OUTPUT)/refined_topics.csv
DTM= outputs/global/dtm_topics_over_time.csv 

# Install dependencies
install:
	pip install -r requirements.txt

# Collect Reddit data
collect:
	$(PYTHON) -m scripts.main_scrape_arctic_shift

# Inspect
inspect:
	$(PYTHON) -m scripts.utils.inspect_csv --input $(CLEAN_DATA)

inspect_year:
	$(PYTHON) -m scripts.utils.inspect_year --input $(CLEAN_DATA) --date_col "created_utc"

inspect_unique:
	$(PYTHON) -m scripts.utils.inspect_unique --input $(CLEAN_DATA) --col "year"
# Merge yearly datasets
merge:
	$(PYTHON) -m scripts.main_merge_yearly \
	--output $(RAW_GLOBAL)

# Preprocess dataset
preprocess:
	$(PYTHON) -m scripts.main_preprocess \
	--input $(RAW_GLOBAL) \
	--output $(CLEAN_DATA)

# Role classification
classify:
	$(PYTHON) -m scripts.main_role_classification \
	--input $(CLEAN_DATA) \
	--output_dir $(ROLE_DIR)

# Global topic modeling
global:
	mkdir -p $(GLOBAL_OUTPUT) 
	$(PYTHON) -m scripts.main_modeling \
	--mode global \
	--input $(CLEAN_DATA) \
	--output $(GLOBAL_OUTPUT)

# Yearly topic modeling
yearly:
	mkdir -p $(YEARLY_OUTPUT)
	$(PYTHON) -m scripts.main_modeling \
	--mode yearly \
	--input $(CLEAN_DATA) \
	--output $(YEARLY_OUTPUT)

# Role topic modeling
role_student:
	mkdir -p $(STUDENT_DIR)
	$(PYTHON) -m scripts.main_modeling \
	--mode role \
	--input $(ROLE_STUDENT_INPUT) \
	--output $(ROLE_STUDENT_OUTPUT)

role_educator:
	mkdir -p $(EDUCATOR_DIR)
	$(PYTHON) -m scripts.main_modeling \
	--mode role \
	--input $(ROLE_EDUCATOR_INPUT) \
	--output $(ROLE_EDUCATOR_OUTPUT)

# DTM
dtm:
	$(PYTHON) -m scripts.main_dtm \
	--model $(GLOBAL_OUTPUT)/model \
	--input $(GLOBAL_OUTPUT)/data_with_topics.csv \
	--output $(GLOBAL_OUTPUT)/dtm

# Topic refinement
refine_global:
	$(PYTHON) -m scripts.main_refine_topics \
	--input $(GLOBAL_TOPICS) \
	--output $(REFINED_GLOBAL) 

refine_student:
	$(PYTHON) -m scripts.main_refine_topics \
	--input $(STUDENT_TOPICS) \
	--output $(REFINED_STUDENT) \
	--corpus_name student

refine_educator:
	$(PYTHON) -m scripts.main_refine_topics \
	--input $(EDUCATOR_TOPICS) \
	--output $(REFINED_EDUCATOR) \
	--corpus_name educator
	
refine_yearly:
	for year in 2018 2019 2020 2021 2022 2023 2024 2025; do \
		$(PYTHON) -m scripts.main_refine_topics \
		--input outputs/yearly/$$year/topics.csv \
		--output outputs/yearly/$$year/refined_topics.csv \
		--corpus_name $$year ; \
	done

categorize:
	$(PYTHON) -m scripts.main_thematic_categorization \
	--input $(GLOBAL_TOPICS) \
	--output outputs/global/topic_with_semantic_categories.csv 


topic_proportion_plot:
	$(PYTHON) -m scripts.main_plot_topic_proportions \
	--input $(GLOBAL_OUTPUT)/semantic_categories_yearly_counts.csv \
	--output $(OUTPUT_DIR)/figures/figures_proportion_stackbar.png

help:
	@echo ""
	@echo "Available commands:"
	@echo "------------------------------------------------------"
	@echo "Setup:"
	@echo "  make install              Install Python dependencies"
	@echo ""
	@echo "Data Pipeline:"
	@echo "  make collect              Collect Reddit data"
	@echo "  make merge                Merge yearly datasets"
	@echo "  make preprocess           Clean and preprocess dataset"
	@echo "  make classify             Run role classification"
	@echo ""
	@echo "Topic Modeling:"
	@echo "  make global               Global topic model"
	@echo "  make yearly               Yearly topic models"
	@echo "  make role_student         Student topic model"
	@echo "  make role_educator        Educator topic model"
	@echo ""
	@echo "Topic Refinement:"
	@echo "  make refine_global        Refine global topics"
	@echo "  make refine_student       Refine student topics"
	@echo "  make refine_educator      Refine educator topics"
	@echo "  make refine_yearly        Refine yearly topics"
	@echo ""
	@echo "Analysis:"
	@echo "  make dtm                  Generate topics-over-time data"
	@echo "  make categorize           Assign semantic topic categories"
	@echo ""
	@echo "Visualization:"
	@echo "  make topic_proportion_plot  Generate stacked bar chart"
	@echo ""