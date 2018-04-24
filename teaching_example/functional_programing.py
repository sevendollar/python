# regular uses
text = type(text) in (tuple, list, set) and ' '.join(text) or text  # covert from tuple or list or set to str
text = type(text) is dict and json.dumps(text) or text  # covert from dict to str
text = [text] * 3

# cool uses
text = [
    {
        tuple: lambda x: ' '.join([str(i) for i in x]),
        list: lambda x: ' '.join([str(i) for i in x]),
        set: lambda x: ' '.join([str(i) for i in x]),
        dict: lambda x: json.dumps(x),
        str: lambda x: x
    }.get(type(text), lambda x: str(x))(text)
] * 3
