from app.agents.parser_agent import ParserAgent

parser = ParserAgent()

route = parser.parse(
    "I want to travel from Hyderabad to Suryapet covering Kodad."
)

print(type(route))
print(route)