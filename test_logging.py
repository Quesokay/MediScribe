"""
Test if logging to stderr works
"""
import sys
import io

# Set up UTF-8 encoding like the MCP server does
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)

print("="*70)
print("Testing stderr logging...")
print("="*70)

print("Test 1: Regular print", file=sys.stderr)
print("Test 2: With timestamp", file=sys.stderr)
print("Test 3: Processing message", file=sys.stderr)

print("\nIf you see these messages, logging is working!")
print("If not, the terminal might be suppressing stderr output.")
