def get_matches(pattern, text):
    m = len(pattern)
    n = len(text)

    no_states = (1 << m) - 1

    transitions = [no_states for _ in range(128)]
    for i in range(m):
        transitions[ord(pattern[i])] &= ~(1 << i)

    matches = []
    states = no_states
    for j in range(n):
        states = ((states << 1) & no_states) | transitions[ord(text[j])]
        if states >> m - 1 == 0:
            matches.append(j - m + 1)

    return matches
