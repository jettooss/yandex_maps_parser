# Yandex Maps Parser

## Project Description
Yandex Maps Parser is a parser developed to create a dataset for the VTB Hackathon. 

## Project Objective
The objective of the parser was to gather data from Yandex Maps about various locations (places) to create a dataset that could be used for analysis and decision-making during the VTB Hackathon.

## How to Use
1. Install all the necessary dependencies by running `pip install -r requirements.txt`.
2. Run the `parser_1.py` script, passing in all the required parameters (e.g., URL or coordinates) to define the area or objects to parse.
3. The parser will access Yandex Maps pages using the specified parameters and gather information such as coordinates, estimation, categories, review count, address, opening hours, and user comments for each object.
4. The collected data will be saved in JSON  format

## Data Structure
For each parsed object, the following data was collected:
- Coordinates
- Estimation
- Categories
- Review count
- Address
- Opening hours
- Physical entity indicator
- Corporate entity indicator
- User comments
