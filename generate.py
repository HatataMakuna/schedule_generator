import csv
from collections import defaultdict

def read_csv(file_path):
    matches_played = defaultdict(lambda: {'home': set(), 'away': set()})
    teams = set()

    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            team = row['Team']
            teams.add(team)
            for round_num, opponent in row.items():
                if round_num != 'Team' and opponent:
                    matches_played[team]['home'].add(opponent)
                    matches_played[opponent]['away'].add(team)
    
    return matches_played, list(teams)

def can_play_match(home, away, matches_played, used_teams, match_type):
    if match_type == 'once':
        return away not in used_teams and home != away and away not in matches_played[home]['home'] and away not in matches_played[home]['away']
    elif match_type == 'twice':
        return away not in used_teams and home != away and (away not in matches_played[home]['home'] or away not in matches_played[home]['away'])

def backtrack(round_matches, teams, matches_played, used_teams, index, match_type):
    if len(round_matches) == len(teams) // 2:
        return True

    if index >= len(teams):
        return False

    home = teams[index]
    if home in used_teams:
        return backtrack(round_matches, teams, matches_played, used_teams, index + 1, match_type)

    for away in teams:
        if can_play_match(home, away, matches_played, used_teams, match_type):
            round_matches.append((home, away))
            if match_type == 'once':
                matches_played[home]['home'].add(away)
                matches_played[away]['away'].add(home)
            elif match_type == 'twice':
                if away not in matches_played[home]['home']:
                    matches_played[home]['home'].add(away)
                    matches_played[away]['away'].add(home)
                else:
                    matches_played[home]['away'].add(away)
                    matches_played[away]['home'].add(home)
            used_teams.add(home)
            used_teams.add(away)
            
            if backtrack(round_matches, teams, matches_played, used_teams, index + 1, match_type):
                return True
            
            # Backtrack
            round_matches.pop()
            if match_type == 'once':
                matches_played[home]['home'].remove(away)
                matches_played[away]['away'].remove(home)
            elif match_type == 'twice':
                if away in matches_played[home]['home']:
                    matches_played[home]['home'].remove(away)
                    matches_played[away]['away'].remove(home)
                else:
                    matches_played[home]['away'].remove(away)
                    matches_played[away]['home'].remove(home)
            used_teams.remove(home)
            used_teams.remove(away)

    return False

def generate_remaining_schedule(teams, matches_played, num_rounds, match_type):
    rounds = []

    for _ in range(num_rounds):
        round_matches = []
        used_teams = set()
        if not backtrack(round_matches, teams, matches_played, used_teams, 0, match_type):
            raise ValueError("Cannot generate a full round without overlaps.")
        
        rounds.append(round_matches)

    return rounds

def print_schedule(schedule, start_round=1):
    for round_num, matches in enumerate(schedule, start_round):
        print(f"Round {round_num}:")
        for match in matches:
            print(f"{match[0]} vs {match[1]}")
        print()

# Example usage
file_path = 'schedule.csv'

# Read teams and their already played opponents from CSV file
matches_played, teams = read_csv(file_path)

# Define number of rounds to generate and starting round number
num_rounds_to_generate = 31
starting_round_number = 1

# Choose match type
match_type = 'twice' # Set to 'once' or 'twice'

# Generate the remaining schedule
remaining_schedule = generate_remaining_schedule(teams, matches_played, num_rounds_to_generate, match_type)

# Print the remaining schedule
print_schedule(remaining_schedule, starting_round_number)