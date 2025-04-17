# Indhic-AI_Assignment

This extracts Sanskrit verses from the Astavakragita text and puts them into structured JSON format.

## Installation Steps

### 1. Clone the repository

```
git clone https://github.com/yourname/astavakragita-extractor.git
cd astavakragita-extractor
```

### 2. Create a virtual environment (Optional)

```
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

## Explanation of Text Extraction

1. Fetching from the source using the requests library to download text from the provided URL with error handling

2. Identifies the beginning of the text section using the "# Text" marker, locates the start of verses by searching for "aṣṭāvakragītā" in lowercase and then parses the verse

3. Iterates through lines starting from the identified verse section
   Skips empty lines
   Captures verse content until reaching a marker pattern "// Avg_X.X"

4. Uses r'Avg\_(\d+\.\d+)' to extract verse numbers
   Handles multi-line verses by accumulating lines until reaching a marker

## Usage

```
python text_extraction.py --url URL_TO_TEXT --output OUTPUT_FILE.json
```

#### _Required Arguments:_

--url: The URL where the source text can be found
Example: https://gretil.sub.uni-goettingen.de/gretil/corpustei/transformations/plaintext/sa_aSTAvakragItA.txt

#### _Optional Arguments:_

--output: Filename for the JSON output (defaults to "astavakra_verses.json")
