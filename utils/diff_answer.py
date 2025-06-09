import difflib

def diff_answers(user_answer: str, correct_answer: str) -> str:
    seqm = difflib.SequenceMatcher(None, user_answer.lower(), correct_answer.lower())
    result = []
    for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
        text = user_answer[a0:a1]
        if opcode == 'equal':
            result.append(text)
        elif opcode == 'replace' or opcode == 'delete':
            result.append(f"*{text}*")
        elif opcode == 'insert':
            inserted = correct_answer[b0:b1]
            result.append(f"[+{inserted}+]")
    return "".join(result)