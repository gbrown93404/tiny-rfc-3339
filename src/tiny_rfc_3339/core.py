"""Core validation logic for RFC 3339 date-time strings.

The implementation uses a hand-written state machine rather than regex or
`datetime.strptime`. Doing so lets us enforce RFC 3339's exact grammar
(including optional fractional seconds and the case-insensitive separators)
without importing anything, and without accidentally accepting inputs that
`strptime` would tolerate but the RFC forbids.
"""


def _is_digit(c: str) -> bool:
    return "0" <= c <= "9"


def is_rfc3339(s: str) -> bool:
    """Validate an RFC 3339 date-time string.

    The grammar (from RFC 3339, section 5.6) is:
      date-time = full-date "T" time
      full-date = date-fullyear "-" date-month "-" date-mday
      time      = time-hour ":" time-minute ":" time-second
                    [time-secfrac]
                    time-offset
      time-offset = "Z" / time-numoffset
      time-numoffset = ("+" / "-") time-hour ":" time-minute

    Notes on the decisions made here:
      * The `T` separator and `Z` designator are matched case-insensitively,
        because RFC 3339 section 5.6 explicitly allows a lowercase `t` and
        section 5.6 note 2 permits lowercase `z`.
      * `time-secfrac` is a `.` followed by one or more digits. There is no
        upper bound on digit count in the grammar, so we accept any length.
      * Month/day ranges are syntactically validated (01-12, 01-31) but we do
        NOT validate calendar correctness (e.g. Feb 30). RFC 3339 defines the
        format, not calendar validity, and `datetime` would reject these
        anyway if the caller later parses them.
    """
    if not isinstance(s, str):
        return False

    n = len(s)
    if n < 20:
        # Minimum valid string is 20 chars: YYYY-MM-DDTHH:MM:SSZ
        return False

    i = 0

    # --- full-date: YYYY-MM-DD ---
    if i + 10 > n:
        return False
    for pos in range(i, i + 4):
        if not _is_digit(s[pos]):
            return False
    if s[i + 4] != "-":
        return False
    if not _is_digit(s[i + 5]) or not _is_digit(s[i + 6]):
        return False
    if s[i + 7] != "-":
        return False
    if not _is_digit(s[i + 8]) or not _is_digit(s[i + 9]):
        return False
    # Syntactic month/day range checks.
    if not ("01" <= s[i + 5 : i + 7] <= "12"):
        return False
    if not ("01" <= s[i + 8 : i + 10] <= "31"):
        return False
    i += 10

    # --- "T" separator (case-insensitive per RFC 3339 section 5.6) ---
    if s[i] != "T" and s[i] != "t":
        return False
    i += 1

    # --- time: HH:MM:SS ---
    if i + 8 > n:
        return False
    for pos in range(i, i + 8):
        if pos == i + 2 or pos == i + 5:
            if s[pos] != ":":
                return False
        else:
            if not _is_digit(s[pos]):
                return False
    if not ("00" <= s[i : i + 2] <= "23"):
        return False
    if not ("00" <= s[i + 3 : i + 5] <= "59"):
        return False
    if not ("00" <= s[i + 6 : i + 8] <= "59"):
        return False
    i += 8

    # --- optional time-secfrac: "." 1*DIGIT ---
    if i < n and s[i] == ".":
        i += 1
        # Require at least one digit after the dot.
        start = i
        while i < n and _is_digit(s[i]):
            i += 1
        if i == start:
            return False

    # --- time-offset: "Z" | ("+"|"-") HH ":" MM ---
    if i >= n:
        return False

    if s[i] == "Z" or s[i] == "z":
        i += 1
    else:
        # Numeric offset.
        if i + 6 > n:
            return False
        if s[i] != "+" and s[i] != "-":
            return False
        i += 1
        if not _is_digit(s[i]) or not _is_digit(s[i + 1]):
            return False
        if not ("00" <= s[i : i + 2] <= "23"):
            return False
        i += 2
        if s[i] != ":":
            return False
        i += 1
        if not _is_digit(s[i]) or not _is_digit(s[i + 1]):
            return False
        if not ("00" <= s[i : i + 2] <= "59"):
            return False
        i += 2

    # Trailing characters mean the string is not a valid RFC 3339 timestamp.
    return i == n
