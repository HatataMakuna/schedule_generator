import pandas as pd
from itertools import combinations

def load_schedule(file_path):
    """
    Load the schedule from a CSV or Excel file.
    The schedule should have columns: 'Team', 'R1', 'R2', ..., 'R31'.
    """
    return pd.read_csv(file_path)  # Use pd.read_excel(file_path) for Excel files.

def get_played_matches(schedule, previous_rounds):
    """
    Retrieve all matches already played in the previous rounds (R1-R26).
    """
    played_matches = set()
    for round_col in previous_rounds:
        round_data = schedule[round_col]
        for match in round_data.dropna():  # Ignore NaN (empty) cells.
            played_matches.add(tuple(sorted(match.split('-'))))  # Sort to avoid duplicates.
    return played_matches

def find_missing_matches(schedule, rounds_to_fix):
    """
    Identify teams missing matches in specific rounds (e.g., R27-R31).
    """
    missing_matches = {}
    for round_col in rounds_to_fix:
        round_data = schedule[round_col]
        missing_teams = schedule['Team'][round_data.isna()].tolist()
        missing_matches[round_col] = missing_teams
    return missing_matches

def generate_new_matches(schedule, missing_matches, played_matches, rounds_to_fix):
    """
    Generate new match suggestions for the missing rounds while avoiding overlapping matches.
    """
    teams = schedule['Team'].tolist()
    suggestions = {}  # Store suggested matches for each round.

    for round_col in rounds_to_fix:
        suggestions[round_col] = []
        missing_teams = missing_matches[round_col]

        # Ensure all teams play once in the current round.
        used_teams = set()
        while len(missing_teams) > 1:
            team1 = missing_teams.pop(0)
            for team2 in missing_teams:
                match = tuple(sorted((team1, team2)))
                if match not in played_matches and team1 not in used_teams and team2 not in used_teams:
                    suggestions[round_col].append(f"{team1}-{team2}")
                    played_matches.add(match)
                    used_teams.add(team1)
                    used_teams.add(team2)
                    missing_teams.remove(team2)
                    break

        # Handle any remaining teams (if odd number, one team won't play).
        if missing_teams:
            print(f"Warning: Team(s) {missing_teams} could not be scheduled in {round_col} due to an odd number of teams.")
    
    return suggestions

def main():
    # Path to your schedule file.
    file_path = "schedule.csv"

    # Load the schedule.
    schedule = load_schedule(file_path)

    # Define the columns for previous rounds (R1-R26) and rounds to fix (R27-R31).
    previous_rounds = [f"R{i}" for i in range(1, 27)]
    rounds_to_fix = [f"R{i}" for i in range(27, 32)]

    # Retrieve all matches already played in previous rounds.
    played_matches = get_played_matches(schedule, previous_rounds)

    # Find missing matches in rounds R27-R31.
    missing_matches = find_missing_matches(schedule, rounds_to_fix)

    # Generate new match suggestions for missing rounds while avoiding overlap.
    suggestions = generate_new_matches(schedule, missing_matches, played_matches, rounds_to_fix)

    # Output the suggestions.
    for round_col, matches in suggestions.items():
        print(f"Match suggestions for {round_col}:")
        for match in matches:
            print(f"  {match}")

if __name__ == "__main__":
    main()
