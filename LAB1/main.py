#D1 Deszczowa Goraco Wysoka Slaby Tak
#D2 Pochmurna Lagodnie Wysoka Slaby Tak
#D3 Sloneczna Chlodno Wysoka Mocny Tak
#D4 Sloneczna Goraco Wysoka Mocny Tak
#D5 Pochmurna Goraco Normalna Mocny Tak
#D6 Sloneczna Chlodno Wysoka Slaby Tak
#D7 Deszczowa Goraco Wysoka Mocny Tak
#D8 Deszczowa Chlodno Wysoka Mocny Tak
#D9 Deszczowa Lagodnie Normalna Mocny Tak
#D10 Deszczowa Lagodnie Wysoka Mocny Nie
#D11 Sloneczna Chlodno Normalna Mocny Nie
#D12 Deszczowa Lagodnie Normalna Slaby Nie
#D13 Pochmurna Goraco Wysoka Slaby Nie
#D14 Sloneczna Goraco Normalna Mocny Nie

#1 1 1 1 3 1 1
#1 1 1 1 3 2 1
#1 1 1 3 2 1 0
#1 1 1 3 3 2 1
#1 1 2 1 2 1 0
#1 1 2 1 2 2 1
#1 1 2 2 3 1 0
#1 1 2 2 4 1 1

#values.txt

with open("dane/values.txt", "r") as f:
    data = [list(map(int, line.split())) for line in f]

kolumny = ["a1", "a2", "a3", "a4", "a5", "a6", "d"]
wiersze = [f"o{i + 1}" for i in range(len(data))]

atrybuty = len(kolumny) - 1
obiekty = len(wiersze)

print("Liczba atrybutów:", atrybuty)
print("Liczba obiektów:", obiekty)

for i in range(obiekty):
    print("\nObiekt:", wiersze[i], data[i])

    for j in range(atrybuty):
        print(f"[{wiersze[i]}, {kolumny[j]}] = {data[i][j]} -> decyzja {data[i][-1]}")

        if data[i][-1] == 0 and data[i][j] == data[i][0]:
            print(f"Break na [{wiersze[i]}, {kolumny[j]}] = {data[i][j]}")
            break

#SystemDecyzyjny.txt

with open("dane/SystemDecyzyjny.txt", "r", encoding="utf-8") as f:
    data = [line.strip().split() for line in f]

kolumny = ["Pogoda", "Temperatura", "Wilgotnosc", "Wiatr", "Decyzja"]
wiersze = [f"D{i + 1}" for i in range(len(data))]

atrybuty = len(kolumny) - 1
obiekty = len(wiersze)

print("Liczba atrybutów:", atrybuty)
print("Liczba obiektów:", obiekty)

for i in range(obiekty):
    print("\nObiekt:", wiersze[i], data[i])

    for j in range(atrybuty):
        print(f"[{wiersze[i]}, {kolumny[j]}] = {data[i][j]} -> decyzja {data[i][-1]}")

        if data[i][-1] == "Nie" and data[i][j] == data[i][0]:
            print(f"Break na [{wiersze[i]}, {kolumny[j]}] = {data[i][j]}")
            break


def load_data(filename):
    """Load data from file"""
    data = []
    with open(filename, 'r') as file:
        for line in file:
            data.append([int(val) for val in line.strip().split()])
    return data


def check_rule_consistency(rule, data, decision_class):
    """Check if rule is consistent - all objects matching the rule have the same decision"""
    for obj in data:
        # Check if object matches the rule
        matches_rule = True
        for attr_idx, value in rule:
            if obj[attr_idx] != value:
                matches_rule = False
                break

        # If object matches but has different decision, rule is inconsistent
        if matches_rule and obj[-1] != decision_class:
            return False

    return True


def find_objects_covered_by_rule(rule, data):
    """Find all objects covered by a rule"""
    covered_indices = []
    for idx, obj in enumerate(data):
        matches = True
        for attr_idx, value in rule:
            if obj[attr_idx] != value:
                matches = False
                break
        if matches:
            covered_indices.append(idx)
    return covered_indices


def covering_algorithm(data):
    """Step-by-step covering algorithm implementation"""
    print("\nStarting covering algorithm...")

    # Store rules as (rule, decision_class, covered_objects)
    rules = []

    # Keep track of uncovered objects
    uncovered = list(range(len(data)))

    # Maximum rule length is number of attributes (excluding decision)
    max_rule_length = len(data[0]) - 1

    while uncovered:
        print(f"\nUncovered objects: {[i + 1 for i in uncovered]}")  # Use 1-based indexing in output
        found_rule = False

        # Try rules of increasing length (order)
        for rule_length in range(1, max_rule_length + 1):
            print(f"\nTrying rules of order {rule_length}:")

            # Check each uncovered object
            for obj_idx in uncovered:
                obj = data[obj_idx]
                decision_class = obj[-1]

                print(f"  Examining object {obj_idx + 1} (decision class: {decision_class}):")

                # Try all combinations of attributes of the current length
                import itertools
                for attr_combination in itertools.combinations(range(max_rule_length), rule_length):
                    # Create rule from this object's values
                    rule = [(attr_idx, obj[attr_idx]) for attr_idx in attr_combination]

                    # Format the rule for display
                    rule_str = " ∧ ".join([f"(a{attr_idx + 1} = {value})" for attr_idx, value in rule])

                    # Check if rule is consistent
                    if check_rule_consistency(rule, data, decision_class):
                        # Find objects covered by this rule
                        covered = find_objects_covered_by_rule(rule, data)

                        # Is the rule covering any uncovered objects?
                        covering_uncovered = [idx for idx in covered if idx in uncovered]

                        if covering_uncovered:
                            print(f"    Found consistent rule: {rule_str} => (d = {decision_class})")
                            print(f"    This rule covers objects: {[i + 1 for i in covered]}")

                            # Add rule to our list
                            rules.append((rule, decision_class, covered))

                            # Remove newly covered objects from uncovered list
                            for idx in covering_uncovered:
                                if idx in uncovered:
                                    uncovered.remove(idx)

                            found_rule = True
                            break
                    else:
                        print(f"    Rule {rule_str} is inconsistent for decision {decision_class}")

                if found_rule:
                    break

            if found_rule:
                break

        # If we couldn't find any rule in this iteration, we're done
        if not found_rule:
            print(f"\nCould not find consistent rules for objects: {[i + 1 for i in uncovered]}")
            break

    return rules


def print_final_rules(rules, data):
    """Print final rules in a readable format"""
    print("\n=== FINAL RULES ===")
    for i, (rule, decision_class, covered) in enumerate(rules, 1):
        rule_str = " ∧ ".join([f"(a{attr_idx + 1} = {value})" for attr_idx, value in rule])
        print(f"Rule {i}: {rule_str} => (d = {decision_class})")
        print(f"  Covers objects: {[i + 1 for i in covered]}")  # Use 1-based indexing in output
        print(f"  Support: {len(covered)}")


def main():
    data = load_data("dane/values.txt")

    print("Loaded data:")
    for i, row in enumerate(data, 1):
        attr_values = ', '.join([f"a{j + 1}={val}" for j, val in enumerate(row[:-1])])
        print(f"Object {i}: {attr_values}, d={row[-1]}")

    rules = covering_algorithm(data)
    print_final_rules(rules, data)


if __name__ == "__main__":
    main()
