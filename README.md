# schedule_generator
This repository contains a script to generate a round-robin schedule for teams. You can generate schedules where each team plays against every other team once, or you can choose to have teams play against each other twice (home and away). The script reads the existing schedule from a CSV file, generates the remaining matches, and ensures no overlaps with previous rounds.

## Features
- Generate a round-robin schedule for any number of teams.
- Choose between single matches or home-and-away matches.
- Avoids duplicate matches and ensures teams do not play the same opponent more than specified.
- Reads existing schedules from a CSV file to continue scheduling.

## Requirements

- Python 3.6 or later
- `csv` module (comes with Python's standard library)
- `defaultdict` from the `collections` module (comes with Python's standard library)

## Usage

1. Clone the repository:
    ```sh
    git clone https://github.com/HatataMakuna/schedule_generator.git
    cd schedule_generator
    ```

2. Prepare your `schedule.csv` file in the following format:
    ```csv
    Team, R1, R2, ..., RN
    Team 1, Team 2, Team 3, ..., 
    Team 2, Team 1, Team 4, ..., 
    Team 3, Team 5, Team 1, ..., 
    ...
    ```
    - The first column (`Team`) lists all the teams.
    - Each subsequent column (`R1`, `R2`, etc.) lists the opponents that the team has already played against in those rounds.
    - There is a `schedule.xlsx` provided in this repository which acted as a template. You can use this file to edit the teams and opponents. Be sure to save it as `csv` file before running the script.

3. Update the script configuration:
    - Open `generate.py`.
    - Modify the following variables as needed:
      ```python
      file_path = 'schedule.csv'  # Path to your CSV file
      num_rounds_to_generate = 31  # Number of rounds to generate
      starting_round_number = 1  # Starting round number for the new schedule
      match_type = 'twice'  # Set to 'once' or 'twice' based on your requirement
      ```

4. Run the script:
    ```sh
    python generate.py
    ```

5. The script will output the generated schedule.

## Example Output

The script will print the generated schedule in a readable format, for example:
```
Round 1:
Team 1 vs Team 2
Team 3 vs Team 4
...

Round 2:
Team 2 vs Team 1
Team 4 vs Team 3
...
```