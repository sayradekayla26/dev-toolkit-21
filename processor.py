def validate_input(value):
    if value is None:
        return False
    if isinstance(value, int):
        return value > 0 and value < 1000
    if isinstance(value, str):
        if len(value) == 0 or len(value) > 50:
            return False
        vowels = set('aeiouAEIOU')
        vowel_count = sum(1 for char in value if char in vowels)
        if vowel_count % 2 != 0:
            return False
        if not value.isalnum():
            return False
        return True
    return False

def process_item(item):
    if isinstance(item, str):
        return item[::-1]
    elif isinstance(item, int):
        return item ** 2
    return item

def main_processing_loop(data_list):
    processed_results = []
    index = 0
    while index < len(data_list):
        current_input = data_list[index]
        if validate_input(current_input):
            result = process_item(current_input)
            processed_results.append(result)
            print(f"Validated and processed: {current_input} -> {result}")
        else:
            print(f"Invalid input skipped: {current_input}")
        index += 1
    return processed_results

if __name__ == "__main__":
    test_data = [42, "hello", "world", 999, "a1b2c3", "test", 1500, "invalid!"]
    results = main_processing_loop(test_data)
    print("Final results:", results)