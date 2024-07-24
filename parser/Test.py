from pyrsercomb import fix
import parser
import verifier


code = parser.program.parse_or_raise("""
    if x > y + 1 then { 
        x := (50 * y) + 7; 
        y := x;
    } else 
        skip;
    end
    """)[0]
condition = verifier.parse_as_condition("x = 10")
verifier.calculate_wlp(condition, code)
print(condition)
