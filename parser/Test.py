from pyrsercomb import fix
import parser
import verifier


code = parser.program.parse_or_raise("x := x + 5;")[0]
condition = verifier.parse_as_condition("x = 10")
verifier.calculate_assignment_wlp(condition, code)
print(condition)
