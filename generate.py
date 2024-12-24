import csv
from collections import defaultdict

def read_csv(file_path):
    matches_played = defaultdict(set)
    teams = set()

    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            team = row['Team']
            teams.add(team)
            for round_num, opponent in row.items():
                if round_num != 'Team' and opponent:
                    matches_played[team].add(opponent)
                    matches_played[opponent].add(team)
    
    return matches_played, list(teams)

def can_play_match(home, away, matches_played, used_teams):
    return away not in used_teams and home != away and away not in matches_played[home]

def backtrack(round_matches, teams, matches_played, used_teams, index):
    if len(round_matches) == len(teams) // 2:
        return True

    if index >= len(teams):
        return False

    home = teams[index]
    if home in used_teams:
        return backtrack(round_matches, teams, matches_played, used_teams, index + 1)

    for away in teams:
        if can_play_match(home, away, matches_played, used_teams):
            round_matches.append((home, away))
            matches_played[home].add(away)
            matches_played[away].add(home)
            used_teams.add(home)
            used_teams.add(away)
            
            if backtrack(round_matches, teams, matches_played, used_teams, index + 1):
                return True
            
            # Backtrack
            round_matches.pop()
            matches_played[home].remove(away)
            matches_played[away].remove(home)
            used_teams.remove(home)
            used_teams.remove(away)

    return False

def generate_remaining_schedule(teams, matches_played):
    n = len(teams)
    rounds = []

    for round_num in range(n - 1, n - 1 + 5):
        round_matches = []
        used_teams = set()

        if not backtrack(round_matches, teams, matches_played, used_teams, 0):
            raise ValueError("Cannot generate a full round without overlaps.")
        
        rounds.append(round_matches)

    return rounds

def print_schedule(schedule, start_round=27):
    for round_num, matches in enumerate(schedule, start_round):
        print(f"Round {round_num}:")
        for match in matches:
            print(f"{match[0]} vs {match[1]}")
        print()

# Example usage
file_path = 'schedule.csv'

# Read teams and their already played opponents from CSV file
matches_played, teams = read_csv(file_path)

# Generate the remaining schedule
remaining_schedule = generate_remaining_schedule(teams, matches_played)

# Print the remaining schedule
print_schedule(remaining_schedule)