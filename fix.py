
import sys
import os

def fix_encoding(filename):
    print(f'Fixing {filename}...')
    
    # Read file with different encodings
    encodings = ['utf-16', 'utf-16-le', 'utf-16-be', 'utf-8-sig', 'latin-1', 'cp1252']
    
    for enc in encodings:
        try:
            with open(filename, 'r', encoding=enc) as f:
                content = f.read()
            print(f'  Successfully read as {enc}')
            
            # Write as UTF-8
            with open(filename, 'w', encoding='utf-8') as f:
                f.write('# -*- coding: utf-8 -*-\n' + content)
            print(f'  Converted to UTF-8')
            return True
        except UnicodeDecodeError:
            continue
    
    # Try binary reading
    try:
        with open(filename, 'rb') as f:
            data = f.read()
        
        # Remove UTF-16 BOM if present
        if data.startswith(b'\xff\xfe'):
            content = data[2:].decode('utf-16')
        elif data.startswith(b'\xfe\xff'):
            content = data[2:].decode('utf-16be')
        else:
            content = data.decode('utf-8', errors='ignore')
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('# -*- coding: utf-8 -*-\n' + content)
        
        print('  Converted using binary method')
        return True
    except Exception as e:
        print(f'  Error: {e}')
        return False

if __name__ == '__main__':
    if fix_encoding('app.py'):
        print('✅ Encoding fixed successfully!')
    else:
        print('❌ Could not fix encoding')
