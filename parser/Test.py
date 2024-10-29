from pyrsercomb import fix
import parser
import verifier


wcode = parser.program.parse_or_raise("""
    z := 5;
    y := 5;
    while x > y do{
        z := z + 5;
        y := y + 5;
        x := x - 10;
    }end
    """)
k = verifier.verify_code(wcode, "z = y")
print(k)
