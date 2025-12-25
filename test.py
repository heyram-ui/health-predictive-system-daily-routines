print('Python is working!')
print('UTF-8 encoding test: ✓')
print('Flash import test starting...')

try:
    import flask
    print('Flask imported successfully!')
except ImportError:
    print('Flask not installed. Installing...')
