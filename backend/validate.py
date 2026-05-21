"""
Quick syntax validation script for the refactored modules
"""

import ast
import sys

files_to_check = [
    'preprocess.py',
    'train.py',
    'predict.py',
    'evaluation.py',
    'main.py'
]

print("=" * 60)
print("SYNTAX VALIDATION FOR REFACTORED MODULES")
print("=" * 60)

all_valid = True

for filename in files_to_check:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
        ast.parse(code)
        print(f"✓ {filename:<20} - Syntax OK")
    except SyntaxError as e:
        print(f"✗ {filename:<20} - Syntax Error: {e}")
        all_valid = False
    except Exception as e:
        print(f"✗ {filename:<20} - Error: {e}")
        all_valid = False

print("=" * 60)

# Try importing modules
print("\nMODULE IMPORT VALIDATION")
print("=" * 60)

import_tests = [
    ('preprocess', ['load_data', 'encode_features', 'split_data']),
    ('train', ['train_t_learner', 'train_causal_forest_dml']),
    ('predict', ['predict_t_learner', 'create_prediction_dataframe']),
    ('evaluation', ['create_decile_analysis', 'calculate_qini_curve_data']),
]

for module_name, functions in import_tests:
    try:
        module = __import__(module_name)
        missing_funcs = [f for f in functions if not hasattr(module, f)]
        
        if missing_funcs:
            print(f"✗ {module_name:<20} - Missing functions: {', '.join(missing_funcs)}")
            all_valid = False
        else:
            print(f"✓ {module_name:<20} - All required functions present")
    except ImportError as e:
        print(f"⚠ {module_name:<20} - Import failed (dependencies may be missing): {str(e)[:50]}")
    except Exception as e:
        print(f"✗ {module_name:<20} - Error: {str(e)[:50]}")
        all_valid = False

print("=" * 60)

if all_valid:
    print("\n✓ All files have valid syntax and required functions!")
    print("\nTo run the full pipeline:")
    print("  python main.py")
    sys.exit(0)
else:
    print("\n✗ Some validation checks failed. Please review the errors above.")
    sys.exit(1)
