import os
import re
import time
import json
import requests
import shutil
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:5000/chat_api"
OUTPUT_DIR = "test_results"
QUERY_FILE = "test_queries.txt"
RESULTS_FILE = "test_results_summary.txt"
GRAPHS_DIR = os.path.join(OUTPUT_DIR, "graphs")

def setup_directories():
    """Create output directories if they don't exist"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(GRAPHS_DIR, exist_ok=True)
    
    # Clear previous outputs directory for each test run
    outputs_folder = "outputs"
    if os.path.exists(outputs_folder):
        for filename in os.listdir(outputs_folder):
            file_path = os.path.join(outputs_folder, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
    
    # Clear conversation.txt if it exists
    if os.path.exists("conversation.txt"):
        os.remove("conversation.txt")
        
    # Remove previous graph image if it exists
    graph_file = os.path.join("static", "graph.png")
    if os.path.exists(graph_file):
        try:
            os.remove(graph_file)
            print(f"Removed previous graph image: {graph_file}")
        except Exception as e:
            print(f"Error deleting graph image {graph_file}: {e}")

def parse_queries(file_path):
    """Parse the test queries file and extract queries"""
    with open(file_path, "r") as f:
        content = f.read()
    
    # Extract query blocks using regex
    pattern = r'QUERY\s+(\d+):\s+"([^"]+)"'
    return re.findall(pattern, content)

def run_query(query):
    """Send query to the API and return response"""
    data = {"message": query}
    response = requests.post(BASE_URL, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Request failed with status code {response.status_code}"}

def update_query_file(query_file, query_num, output):
    """Update the query file with the output"""
    with open(query_file, "r") as f:
        content = f.read()
    
    # Replace the [To be filled during execution] placeholder with actual output
    pattern = f'QUERY {query_num}:.+?OUTPUT: \\[To be filled during execution\\]'
    replacement = f'QUERY {query_num}:.+?OUTPUT: {output.replace("$", "\\$")}'
    
    updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open(query_file, "w") as f:
        f.write(updated_content)

def save_graph_if_exists():
    """Check if a graph was generated and save it to the results directory"""
    graph_file = os.path.join("static", "graph.png")
    if os.path.exists(graph_file):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        destination = os.path.join(GRAPHS_DIR, f"graph_{timestamp}.png")
        shutil.copy2(graph_file, destination)
        return destination
    return None

def run_all_queries():
    """Run all test queries and compile results"""

    
    # Parse queries from file
    queries = parse_queries(QUERY_FILE)
    
    results = []
    for query_num, query_text in queries:
        print(f"\nRunning Query {query_num}: {query_text}")
        setup_directories()
        # Run query
        start_time = time.time()
        response = run_query(query_text)
        end_time = time.time()
        
        # Process response
        if "error" in response:
            output = f"ERROR: {response['error']}"
        else:
            output = response.get("response", "No response")
            
            # Check if there's chart data
            if "chart_data" in response:
                # Save chart data as JSON
                chart_file = os.path.join(OUTPUT_DIR, f"chart_data_query_{query_num}.json")
                with open(chart_file, "w") as f:
                    json.dump(response["chart_data"], f, indent=2)
                output += f"\n\n[Chart data saved to {chart_file}]"
        
        # Check if a graph image was generated
        graph_file = save_graph_if_exists()
        if graph_file:
            output += f"\n\n[Graph image saved to {graph_file}]"
        
        # Truncate output if it's too long
        if len(output) > 500:
            display_output = output[:500] + "... [truncated]"
        else:
            display_output = output
            
        print(f"Response: {display_output}")
        print(f"Time taken: {end_time - start_time:.2f} seconds")
        
        # Save full output to file
        query_output_file = os.path.join(OUTPUT_DIR, f"query_{query_num}_output.txt")
        with open(query_output_file, "w") as f:
            f.write(f"QUERY: {query_text}\n\n")
            f.write(f"RESPONSE:\n{output}\n\n")
            f.write(f"TIME TAKEN: {end_time - start_time:.2f} seconds")
        
        # Log result
        results.append({
            "query_num": query_num,
            "query": query_text,
            "output_file": query_output_file,
            "time_taken": end_time - start_time,
            "chart_generated": "chart_data" in response or graph_file is not None
        })
        
        # Wait to avoid overloading the server
        time.sleep(1)
    
    # Generate summary
    with open(os.path.join(OUTPUT_DIR, RESULTS_FILE), "w") as f:
        f.write("# Test Queries Results Summary\n")
        f.write(f"Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for result in results:
            f.write(f"## Query {result['query_num']}\n")
            f.write(f"- Query: \"{result['query']}\"\n")
            f.write(f"- Time taken: {result['time_taken']:.2f} seconds\n")
            f.write(f"- Chart generated: {'Yes' if result['chart_generated'] else 'No'}\n")
            f.write(f"- Output file: {result['output_file']}\n\n")
    
    print(f"\nAll queries completed. Results saved to {OUTPUT_DIR}/{RESULTS_FILE}")

if __name__ == "__main__":
    # Check if the server is running first
    try:
        response = requests.get("http://127.0.0.1:5000/")
        if response.status_code == 200:
            run_all_queries()
        else:
            print("Server doesn't seem to be running properly. Please start the Flask server first.")
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to the server. Please start the Flask server first by running 'python main.py'") 