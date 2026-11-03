"""Search routines and focused checks for the AL04 search contracts."""

from search_support import category_key, id_key


def linear_search(records, target, key=id_key):
	"""Scan in input order and return the first match and its visit trace."""
	trace = []
	for position, record in enumerate(records):
		value = key(record)
		trace.append((position, value))
		if value == target:
			return position, trace
	return None, trace


def binary_search(records, target, key=id_key):
	"""Search an ascending-by-key sequence, tracing each inclusive interval."""
	trace = []
	low, high = 0, len(records) - 1
	while low <= high:
		middle = (low + high) // 2
		value = key(records[middle])
		trace.append((low, high, middle, value))
		if value == target:
			return middle, trace
		if value < target:
			low = middle + 1
		else:
			high = middle - 1
	return None, trace


if __name__ == "__main__":
	import unittest

	# Compact independent records for checking search behavior.
	records = [
		{"id": "T403", "category": "account"},
		{"id": "T401", "category": "network"},
		{"id": "T406", "category": "account"},
		{"id": "T402", "category": "printing"},
		{"id": "T405", "category": "account"},
		{"id": "T404", "category": "network"},
	]
	test_id_key = lambda ticket: ticket["id"]
	test_category_key = lambda ticket: ticket["category"]

	class SearchContractTests(unittest.TestCase):
		def test_linear_found_missing_and_empty(self):
			self.assertEqual(linear_search(records, "T403", test_id_key)[0], 0)
			self.assertIsNone(linear_search(records, "T499", test_id_key)[0])
			self.assertEqual(linear_search([], "T403", test_id_key), (None, []))

		def test_binary_endpoints_and_absent_ranges(self):
			ordered = sorted(records, key=test_id_key)
			for target in ("T401", "T406"):
				position, _ = binary_search(ordered, target, test_id_key)
				self.assertEqual(ordered[position]["id"], target)
			for target in ("T400", "T403.5", "T499"):
				self.assertIsNone(binary_search(ordered, target, test_id_key)[0])
			self.assertEqual(binary_search([], "T401", test_id_key), (None, []))
			self.assertEqual(binary_search([records[0]], "T403", test_id_key)[0], 0)

		def test_duplicate_category_any_match_and_input_unchanged(self):
			original = records.copy()
			category_ordered = sorted(records, key=test_category_key)
			position, _ = binary_search(
				category_ordered, "account", test_category_key
			)
			self.assertEqual(category_ordered[position]["category"], "account")
			self.assertEqual(
				linear_search(records, "account", test_category_key)[0], 0
			)
			self.assertEqual(records, original)

		def test_deliberate_unsorted_binary_miss(self):
			self.assertEqual(linear_search(records, "T401", test_id_key)[0], 1)
			# This selected input misses; not every unsorted input must do so.
			self.assertIsNone(binary_search(records, "T401", test_id_key)[0])

	# Show the same ticket while keeping each position tied to the searched view.
	linear_position, linear_trace = linear_search(records, "T403", test_id_key)
	print("Linear T403:", records[linear_position])
	print("Linear teaching trace (input-order positions):", linear_trace)
	missing_position, _ = linear_search(records, "T499", test_id_key)
	print("Linear T499:", "not found" if missing_position is None else records[missing_position])

	id_ordered = sorted(records, key=test_id_key)
	binary_position, binary_trace = binary_search(id_ordered, "T403", test_id_key)
	print("Binary T403:", id_ordered[binary_position])
	print("Binary teaching trace (ID-ordered view positions):", binary_trace)

	# This is intentionally invalid binary-search input: the records are unsorted.
	print("Unsorted T401 linear position:", linear_search(records, "T401", test_id_key)[0])
	print("Unsorted T401 binary position:", binary_search(records, "T401", test_id_key)[0])
	print("Reason: binary search discards a half based on ordering, which this list lacks.")

	category_ordered = sorted(records, key=test_category_key)
	category_position, _ = binary_search(
		category_ordered, "account", test_category_key
	)
	print("Binary account match:", category_ordered[category_position])
	unittest.main()
