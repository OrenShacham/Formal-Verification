from pyrsercomb import fix
import parser
import verifier


code = parser.program.parse_or_raise("""
    if x >= y  then { 
        y := x + 1 ;
    } else 
        skip;
    end
    """)[0]

scode = parser.program.parse_or_raise("""x := 5;
            y := 5;
""")

k = verifier.verify_code(code, "y != x ")
print(k)
"""
verifier.calculate_wlp(condition, code)
print(condition)
verifier.test_condition(condition)
"""
