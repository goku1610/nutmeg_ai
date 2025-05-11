# Football Data Analysis System Testing

This directory contains tools to test the functionality of the football data analysis system.

## Overview

The testing process involves running a set of predefined queries against the system, capturing the responses, and saving both queries and responses for analysis. The system tests various features including:

1. Player statistics lookup
2. Team performance analysis
3. Competition data retrieval
4. Graph generation
5. Match summary acquisition

## Files

- `test_queries.txt`: Contains the test queries with expected outputs
- `run_test_queries.py`: Script to run the queries and record results
- `test_results/`: Directory where test results are stored
  - `test_results_summary.txt`: Summary of all test runs
  - `query_X_output.txt`: Complete response for query X
  - `chart_data_query_X.json`: JSON data for charts (where applicable)
  - `graphs/`: Directory containing saved graph images

## Running the Tests

1. Make sure the main application is running:
   ```
   python main.py
   ```

2. In a separate terminal, run the test script:
   ```
   python run_test_queries.py
   ```

3. Review the results in the `test_results` directory

## Test Structure

Each test query in the `test_queries.txt` file follows this format:

```
QUERY X: "The query text"
FEATURE: Description of the feature being tested
EXPECTED: Expected behavior of the system
OUTPUT: [To be filled during execution]
```

After running the tests, the `OUTPUT` field will be populated with the actual response from the system.

## Adding New Tests

To add new test cases:

1. Edit `test_queries.txt`
2. Add a new query following the existing format
3. Run the test script to execute the new query

## Interpreting Results

The test summary provides an overview of:
- Query execution time
- Whether a chart was generated
- Location of detailed output files

For more detailed analysis, examine the individual query output files in the `test_results` directory. 