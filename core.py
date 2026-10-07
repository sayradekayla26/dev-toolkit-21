import sys

def validate_input(data):
    try:
        return int(data)
    except (ValueError, TypeError):
        raise ValueError(f'Invalid signal detected: {data}')

def processor_loop():
    print('Dev-toolkit-21 operational. Awaiting inputs...')
    while True:
        user_input = sys.stdin.readline().strip()
        if user_input.lower() in ('exit', 'quit'):
            break
        
        try:
            validated = validate_input(user_input)
            result = validated * 42
            sys.stdout.write(f'Processed: {result}\n')
        except ValueError as e:
            sys.stderr.write(f'Skipped: {e}\n')

if __name__ == '__main__':
    try:
        processor_loop()
    except KeyboardInterrupt:
        sys.exit(0)