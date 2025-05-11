import base64
from google import genai
from google.genai import types
import dotenv
import datetime as dt
import os

dotenv.load_dotenv()
class LLMCalls:
    def __init__(self):
        self.client = genai.Client(
            vertexai=False,
            project="",
            location=""
        )


    def query_resolver(self,query):
        files=[]
        files.append(self.client.files.upload(file="conversation.txt"))

        
        prompt = f"""
The current date is {str(dt.datetime.now())}.
You are an agent that has to describe which pages to get data from depending on the user query. The following are the 4 types of pages available:
Type 1: Player stats: This includes complete details for a player such as team played for, matches, goals, assists etc for each competition. It also includes shooting stats, passing stats, posession, playing time, etc.
Type 2: Team overall: This includes results for any competitions the team played in. This only has competition wise wins/losses count and final position and points for the team. It has no other data.
Type 3: Team season: This includes details for a team for a specific season. This has further details like stats per player, all fixtures and results of the season. It also includes goalkeeping, shooting, passing, possession, defensive, and playing time stats.
Type 4: Competition season: This includes details for a competition for a specific season. This includes the league table, stats per team, as well as various leaderboards (including but not limited to most goals, most assists, most shots, most fouls etc)
Type 5: Graph_to_be_drawn: This signifies if the latest user query wants a graph to be drawn or not. If yes then this will be set to true.
Type 6: General_query: This is a general query that does not require any specific page to be accessed. It can be answered with basic web search results. This is a list which is either empty if not required or contains the queries which are required to be searched for the given user query which may return the best results.

Give the output in the format of a dictionary as follows:
{{"Players":["Player1", "Player2", "Player3"],"Team_overall":["Team1", "Team2", "Team3"],"Team_season":["Team1 season", "Team2 season", "Team3 season"],"Competition_season":["Competition1 season", "Competition2 season", "Competition3 season"],"Graph_to_be_drawn":[True/False],"General_query":["query1", "query2", "query3"]}}
It is up to you to decide which pages need to be accessed. Try to minimize the total number of pages needed to be accessed since this increases the computation time. However make sure that the pages do answer the query.
Here are some examples for you:
Query: "How many goals have Messi and ronaldo scored in their careers?"
Output: {{"Players":["Lionel Messi", "Cristiano Ronaldo"],"Team_overall":[],"Team_season":[],"Competition_season":[],"Graph_to_be_drawn":[False],"General_query":[]}}
Reason: the data is only available in the player stats page. 

Query "How many goals has Real Madrid scored in La Liga 2024-25?"
Output: {{"Players": [],"Team_overall": ["Real Madrid"],"Team_season": [],"Competition_season": [],"Graph_to_be_drawn":[False],"General_query":[]}}
Reason: the data is available in the team overall page. 

Query: "did madrid perform better with or without Mbappe?"
Output: {{"Players": ["Kylian Mbappe"],"Team_overall": ["Real Madrid"],"Team_season": [],"Competition_season": [],"Graph_to_be_drawn":[False],"General_query":[]}}
Reason: You need to know which seasons mbappe played for madrid from the players page. then you need the team overall page for madrid's performance.

Query: "How many goals did barcelona score in the last 4 UCL seasons? Give a graphical representation of the data."
Output: {{"Players":[],"Team_overall":[],"Team_season":["Barcelona 2021-22", "Barcelona 2022-23", "Barcelona 2023-24", "Barcelona 2024-25"],"Competition_season":[],"Graph_to_be_drawn":[True],"General_query":[]}}
Reason: The data is available in the team season page. You need to know which seasons barcelona played in the UCL. The graph_to_be_drawn is set to true since the user asked for a graphical representation.

Query: "Against which team did barcelona win the most matches in the last 4 UCL seasons?"
Output: {{"Players":[],"Team_overall":[],"Team_season":["Barcelona 2021-22", "Barcelona 2022-23", "Barcelona 2023-24", "Barcelona 2024-25"],"Competition_season":[],"Graph_to_be_drawn":[False],"General_query":[]}}
Reason: Matchwise data is available in the season wise pages, so you need all 4 season pages for barcelona.

Query: "Who is the most decorated player in football history?"
Output: {{"Players":[],"Team_overall":[],"Team_season":[],"Competition_season":[],"Graph_to_be_drawn":[False],"General_query":["Who is the most decorated player in football history?"]}}
Reason: This is a general query that does not require any specific page to be accessed. It can be answered with basic web search results."

The current conversation history till now has also been provided in conversation.txt. Decide accordingly if any specific pages are required with specific focus on the latest user query.
Give the reasoning first, and end your answer with the dictionary.
The query you need to respond to is: {query}
"""
        model = "gemini-2.5-flash-preview-04-17"
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_uri(
                        file_uri=files[0].uri,
                        mime_type=files[0].mime_type,
                        ) ,
                    types.Part.from_text(text=prompt),
                ],
            ),
        ]
        generate_content_config = types.GenerateContentConfig(
            response_mime_type="text/plain",
        )


        output=self.client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
        ).text
        # print(output)
        
        try:
            return eval('{"'+output.split('{"')[1].split(']}')[0]+']}')
        except Exception as e:
            print(f"Error parsing LLM output: {e}")
            print("Retrying query_resolver from the beginning...")
            return self.query_resolver(query)

    def generate_output(self, query):
        prompt = f"""
The current date is {str(dt.datetime.now())}.
You are an football analyst that has to answer the user query based on the data available in the files.
The conversation history till now has also been provided in conversation.txt.
Do not reveal any information about your data source/website.
Do not use phrases such as "Based on the data I have" or "Based on the given information" or "Looking at the available statistics". The end user should not know that you are looking at the given webpage.
Give detailed answers whenever possible/required.
The user query is: {query}
"""
        output_dir = "outputs"
        model = "gemini-2.5-flash-preview-04-17"
        files = []
        for filename in os.listdir(output_dir):
            file_path = os.path.join(output_dir, filename)
            if os.path.isfile(file_path):
                files.append(self.client.files.upload(file=file_path))
        files.append(self.client.files.upload(file="conversation.txt"))
        contents = [
            types.Content(
                role="user",
                parts=[
                    *[
                        types.Part.from_uri(
                            file_uri=f.uri,
                            mime_type=f.mime_type,
                        ) for f in files
                    ],
                    types.Part.from_text(text=prompt),
                ],
            ),
        ]
        generate_content_config = types.GenerateContentConfig(
            temperature=1,
            response_mime_type="text/plain",
        )
        output=self.client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
        ).text
        return output
    
    def summaries_required(self, query, current_summaries):
        prompt = f"""
The current date is {str(dt.datetime.now())}.
You have these files available with you. You need to answer this query:{query}. 
Summary of a match is defined as textual details about the events of the match, and not simply its scoreline.
If you require more detailed information regarding the matches such as its summary or for more detailed reviews, you can request it by outputting a list in the following format:
Here by summary we want a detailed analysis of the whole match and what all factors contributed to them as well which cannot be inferred from stats.
['team1 vs team2 dd mmm, yyyy', 'team1 vs team3 dd mmm, yyyy']
The current conversation history till now has also been provided in conversation.txt. Decide accordingly if any specific match summaries are required.
The summaries that are currently available are: {current_summaries}
You can ask for summaries of matches that are not in the above list.
Never give more than 10 summaries at a time.
If no extra information is required, output an empty list.
Do not repeat any information/code already given to you. simply give reasoning and then the list.
Here are a few examples:
Example 1:
Query: "How did Arsenal manage to defeat Manchester City despite having lower possession and fewer shots on goal?"

Reasoning:
The query asks how Arsenal defeated Manchester City despite inferior stats. This cannot be answered from basic match statistics alone and requires tactical and contextual analysis — i.e., the summary. The match summary will reveal whether the win was due to defensive organization, a counter-attacking strategy, a red card incident, or any other factor not evident from stats.

Output_format:
*****['Arsenal vs Manchester City 02 Feb, 2025']*****

Example 2:
Query: "Compare Real Madrid's performances in El Clasico this season."

Reasoning:
A statistical comparison would be incomplete without understanding the tactical evolution, key absences, coaching changes, and match context in each El Clasico. These details come from match summaries. We need summaries for all El Clasico matches in the last two seasons (max 10).

Output_format:
*****[Real Madrid vs Barcelona 26 Oct, 2024', 'Real Madrid vs Barcelona 12 Jan, 2025', 'Real Madrid vs Barcelona 26 Apr, 2025']*****

Example 3:
Query: "How many goals has messi scored in his career?"

Reasoning:
The query is straightforward and can be answered with basic statistics. No match summaries are needed.

Output_format:
*****[]*****


Note: Strictly follow the output format. You are an expert you must not fail at any cost in maintaining the output format. Do not miss the ***** both before and after the output otherwise it will crash the whole program. Do not use backticks or any other formatting. Only return as shown in the example for the data. Ensure the JSON is properly formatted with no syntax errors.
"""
        output_dir = "outputs"
        model = "gemini-2.5-flash-preview-04-17"
        files = []
        for filename in os.listdir(output_dir):
            file_path = os.path.join(output_dir, filename)
            if os.path.isfile(file_path):
                files.append(self.client.files.upload(file=file_path))
        files.append(self.client.files.upload(file="conversation.txt"))
        contents = [
            types.Content(
                role="user",
                parts=[
                    *[
                        types.Part.from_uri(
                            file_uri=f.uri,
                            mime_type=f.mime_type,
                        ) for f in files
                    ],
                    types.Part.from_text(text=prompt),
                ],
            ),
        ]
        generate_content_config = types.GenerateContentConfig(
            temperature=0.4,
            response_mime_type="text/plain",
        )
        output=self.client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
        ).text
        print(output)
        try:
            return eval(output.split("*****")[1])
        except Exception as e:
            print(f"Error parsing LLM output in summaries_required: {e}")
            print("Retrying summaries_required from the beginning...")
            return self.summaries_required(query, current_summaries)

    
    def generate_graph_content(self, query):
        prompt = f"""
    The current date is {str(dt.datetime.now())}.
    You are a football analyst that has to answer the user query based on the data available in the files.
    The conversation history till now has also been provided in conversation.txt.
    Do not reveal any information about your data source/website.
    Do not use phrases such as "Based on the data I have" or "Based on the given information" or "Looking at the available statistics". The end user should not know that you are looking at the given webpage.
    Give detailed answers whenever possible/required.
    The user query is: {query}

    First, provide a detailed explanation and analysis in response to the query.
    
    Then, enclosed in ***** markers, return the chart data in a JSON format that can be used with Chart.js or Plotly.js.
    Structure the data appropriately for the frontend visualization library with proper labels, datasets, and options.
    
    IMPORTANT: You must include a text explanation BEFORE the chart data. The chart cannot stand alone.
    Your output must follow this format exactly:

    [Your text explanation here]

    *****
    {{
      "type": "bar",
      "data": {{
          "labels": ["2025-04-20", "2024-10-27", "2024-01-14", "2023-04-05"],
          "datasets": [
          {{
              "label": "Real Madrid",
              "data": [2, 1, 4, 4],
              "backgroundColor": "#00529F"
          }},
          {{
              "label": "Barcelona",
              "data": [1, 0, 1, 0],
              "backgroundColor": "#C6001E"
          }}
          ]
      }},
      "options": {{
          "responsive": true,
          "plugins": {{
          "title": {{
              "display": true,
              "text": "Goals Scored in Last 4 Real Madrid vs Barcelona Matches"
          }}
          }},
          "scales": {{
          "y": {{
              "title": {{
              "display": true,
              "text": "Goals Scored"
              }}
          }}
          }}
      }}
    }}
    *****

    Do not use backticks or any other formatting. Only return as shown in the example for the data. Ensure the JSON is properly formatted with no syntax errors.
    Do not use any ```JSON or anything over here. Just return the JSON data as shown in the example. Follow the format strictly.
    """
        output_dir = "outputs"
        model = "gemini-2.5-flash-preview-04-17"
        files = []
        for filename in os.listdir(output_dir):
            file_path = os.path.join(output_dir, filename)
            if os.path.isfile(file_path):
                files.append(self.client.files.upload(file=file_path))
        files.append(self.client.files.upload(file="conversation.txt"))
        contents = [
            types.Content(
                role="user",
                parts=[
                    *[
                        types.Part.from_uri(
                            file_uri=f.uri,
                            mime_type=f.mime_type,
                        ) for f in files
                    ],
                    types.Part.from_text(text=prompt),
                ],
            ),
        ]
        generate_content_config = types.GenerateContentConfig(
            temperature=1,
            response_mime_type="text/plain",
        )
        output=self.client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
        ).text
        print(output)
        return output

if __name__ == "__main__":
    llm = LLMCalls()
    source=llm.generate_graph_content("give summaries of real madrid's matches against barca with a graph for the last 4 matches")
    print(source)   