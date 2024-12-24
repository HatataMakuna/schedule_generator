import csv
from collections import defaultdict

def read_csv(file_path):
    matches_played = defaultdict(list)
    teams = set()

    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            team = row['Team']
            teams.add(team)
            for round_num, opponent in row.items():
                if round_num != 'Team' and opponent:
                    matches_played[team].append(opponent)
                    matches_played[opponent].append(team)
    
    return matches_played, list(teams)

def generate_remaining_schedule(teams, matches_played):
    n = len(teams)
    rounds = []

    for round_num in range(n - 1, n - 1 + 5):
        round_matches = []
        used_teams = set()

        for i in range(n // 2):
            for home in teams:
                if home in used_teams:
                    continue
                for away in teams:
                    if away in used_teams or home == away or away in matches_played[home]:
                        continue
                    round_matches.append((home, away))
                    matches_played[home].append(away)
                    matches_played[away].append(home)
                    used_teams.update([home, away])
                    break

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