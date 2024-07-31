response = (
    client.query.get("JeopardyQuestion", ["question"])
    .with_limit(1)
    .do()
)

print(response)