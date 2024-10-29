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

wcode = parser.program.parse_or_raise("""
    z := 5;
    y := 5;
    x := 40;
    while x > y do{
        z := z + 5;
        y := y + 5;
        x := x - 10;
    }end
    """)
# post_condition = verifier.parse_as_condition("(1>1) && (((1>1 && 2>2) && c>c) && ((1>1 && 2>2) && 3>3))")
k = verifier.verify_code(wcode, "z = y")
print(k)
"""
verifier.calculate_wlp(condition, code)
print(condition)
verifier.test_condition(condition)
"""
