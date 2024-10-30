from pyrsercomb import fix
import parser
import verifier


code1 = parser.program.parse_or_raise("""
    z := 5;
    y := 5;
    while x > y do{
        z := z + 5;
        y := y + 5;
        x := x - 10;
    }end
    """)

code2 = parser.program.parse_or_raise("""
    if x > y then{
        y := x+1;
    }else
        skip;
    end
""")

t1 = parser.program.parse_or_raise("""
    if y < 0 then{
        f := -1;
        y := 0 - y;
    }else
        f := 1;
    end
""")

t2 = parser.program.parse_or_raise("""
    while y > 0 do{
        a := a + x;
        y := y - 1;
    end
""")

t3 = parser.program.parse_or_raise("""
    if f < 0 then{
        a := 0 - a;
    }else
        skip;
    end
""")

code3 = parser.program.parse_or_raise("""
    x := z;
    y := w;
    a := 0;
    if y < 0 then{
        while y != 0 do{
            a := a - x;
            y := y + 1;
        }end
    }else{
        while y != 0 do{
            a := a + x;
            y := y - 1;
        }end
    }end
""")
t = verifier.parse_as_condition("(a + (y * z)) = w*z")
k = verifier.verify_code(code3, "a = z*w")
print(k)
