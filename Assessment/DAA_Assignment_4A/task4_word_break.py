"""
Task 4 - Pseudocode Forensics: WordBreak
Includes both the faulty version (for demonstrating the defect) and the
corrected version (which checks DP[j] before accepting a dictionary match).
"""


def word_break_faulty(text, dictionary):
    """Reproduces the ORIGINAL defect: never checks DP[j]."""
    n = len(text)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        dp[i] = False
        for j in range(0, i):
            if text[j:i] in dictionary:          # BUG: missing 'dp[j] and'
                dp[i] = True
                break
    return dp[n], dp


def word_break_corrected(text, dictionary):
    """CORRECTED: requires dp[j] to be True before accepting the match."""
    n = len(text)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        dp[i] = False
        for j in range(0, i):
            if dp[j] and text[j:i] in dictionary:   # fix
                dp[i] = True
                break
    return dp[n], dp


if __name__ == "__main__":
    # Task 4.2: failing input for the faulty algorithm
    text, dictionary = "xcat", {"cat"}
    faulty_result, faulty_dp = word_break_faulty(text, dictionary)
    fixed_result, fixed_dp = word_break_corrected(text, dictionary)
    print(f"Text={text!r}  Dictionary={dictionary}")
    print(f"  Faulty algorithm    -> {faulty_result}  (DP = {faulty_dp})")
    print(f"  Corrected algorithm -> {fixed_result}  (DP = {fixed_dp})")
    print("  Expected answer: False (the prefix 'x' is not a dictionary word)")

    # Task 4.4: regression check - a case the faulty version already got right
    print()
    text2, dictionary2 = "icecream", {"ice", "cream"}
    faulty_result2, _ = word_break_faulty(text2, dictionary2)
    fixed_result2, _ = word_break_corrected(text2, dictionary2)
    print(f"Text={text2!r}  Dictionary={dictionary2}")
    print(f"  Faulty algorithm    -> {faulty_result2}")
    print(f"  Corrected algorithm -> {fixed_result2}")
    print("  Expected answer: True  ('ice' + 'cream')")
