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

code3 = parser.program.parse_or_raise("""
    x := 5;
    z := 0;
    while x != 0 do{
    x := x-1;
    z := z+5;
    }end
""")

code4 = parser.program.parse_or_raise("""
    x := 7;
    y := 13;
    z := 21;
    a := 0;
    if x > y then{
        if y > z then{
            a := 6;
        }else{
            if z > y then{
                a := 7;
            }else{
                a := 8;
            }end
        }end
    }else{
        if x > z then{
            a := 9;
        }else{
            if y > z then{
                a := 10;
            }else{
                a := 11;
            }end
        }end
    }end
""")


k = verifier.verify_code(code4, "a=11")
print(k)
