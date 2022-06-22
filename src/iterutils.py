def pieces(collection: iter, portions: int) -> iter:
	for s,e in zip(
			range(0, len(collection), portions),
			range(portions, len(collection) + portions,
			portions)
		):
		e = len(collection) if e > len(collection) else e
		yield (s,e), collection[s:e]