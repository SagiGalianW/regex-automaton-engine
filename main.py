import UserInput
from RegexToNDFSM import RegexToNDFSM 
from NDFSMtoDFSMconverter import NDFSMToDFSMConverter
'''
    Usefull regex for testing:
    1) (((((((((((((a)|(b))|(c)))+))+)$(@))$(((((((a)|(b))|(c)))+))+))$(.))$(c))$(o))$(m))
    
    
    
    
    
    
    ? - state for a valid machine
    notice that to build a machine that accept 'a' you need to write ? = (a)
    | -> (?|?)
    $ -> (?$?)
    + -> ((?)+)
    * -> ((?)*)

'''


def welcome_message():
    print("=" * 60)
    print("🧠  Welcome to the REGEX ➜ NFA ➜ DFA Engine".center(60))
    print("-" * 60)
    print("Built by Sagi Galian — a fully parenthesized, operator-strict regex system".center(60))
    print()
    print("✅ Supported operators:")
    print("    • |   → Union")
    print("    • $   → Concatenation")
    print("    • +   → Kleene Plus (one or more repetitions)")
    print("    • *   → Kleene Star (zero or more repetitions)")

    print()
    print("📌 Note:")
    print("    • To use '|': (?|?)")
    print("    • To use '$': (?$?)")
    print("    • To use '+': ((?)+)")
    print("    • To use '*': ((?)*)")
    print("    • ? - state for a valid machine")
    print("    • For atoms e.g., 'a' -> (a) is a valid machine that accept a")
    print("    • Operators must be binary → e.g., ((a)|(b)) NOT ((a)|(b)|(c))")
    print()
    print("🎯 Goal: Convert REGEX ➜ NFA ➜ DFA ➜ Minimized DFA ➜ Check words in L")
    print("🧪 Examples:")
    print("    • (((((((((((((a)|(b))|(c)))+))+)$(@))$(((((((a)|(b))|(c)))+))+))$(.))$(c))$(o))$(m))")
    print("       one @ is included, suffix of .com  (other parts must contain chars from {a, b, c})")
    print("    • (((((a)|(b)))*)$(a))")
    print("       word must ends with an a")

    print("=" * 60)

def main():
    print("[Program is running...]")
    welcome_message()
    operators = {"|", "+", "$", "*"}
    regex = UserInput.get_regex_from_user()
    
    converter = RegexToNDFSM(regex, operators)
    # left, right, op = converter.simplify_regex(regex)
    # print(left, right, op)

    ndfsm = converter.build_DFSM_helper()
    print("\n*** Step 1 - building NDFSM ***")
    print(ndfsm)

    dfsm_converter = NDFSMToDFSMConverter(ndfsm)
    dfsm = dfsm_converter.convert()
    print("\n*** Step 2 - converting NDFSM to DFSM ***")
    print(dfsm)

    print("\n*** Step 3 - minimizing DFSM ***")
    dfsm.minimize()
    print(dfsm)

    print("\n*** Step 4 - checking words ***")
    x = ""
    while x != "stop":
        x = input("Enter word (write 'stop' to quit): ")
        print(dfsm.run(x))

    print("[Program stopped...]")


if __name__ == "__main__":
    main()

